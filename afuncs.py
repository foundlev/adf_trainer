import os
import math

import aobjects
import config


def calc_resize(obj_size: tuple[int, int], screen_size: tuple[int, int] | aobjects.ObjectSize,
                rev: bool = False) -> aobjects.ObjectSize:
    x, y = obj_size

    if isinstance(screen_size, aobjects.ObjectSize):
        w = screen_size.x
        h = screen_size.y
    elif screen_size is None:
        return aobjects.ObjectSize(
            x=x, y=y
        )
    else:
        w, h = screen_size

    multiplier_w = w / config.STANDART_RESOLUTION[0]
    multiplier_h = h / config.STANDART_RESOLUTION[1]

    if multiplier_w > multiplier_h:
        multiplier = multiplier_h
    else:
        multiplier = multiplier_w

    if rev:
        return aobjects.ObjectSize(
            x=int(x / multiplier),
            y=int(y / multiplier)
        )
    else:
        return aobjects.ObjectSize(
            x=int(x * multiplier),
            y=int(y * multiplier)
        )


def calc_gaps(obj_size: tuple[int, int], screen_size: tuple[int, int] | aobjects.ObjectSize) -> aobjects.ObjectSize:
    resized_obj = calc_resize(obj_size, screen_size)

    return aobjects.ObjectSize(
        x=int((screen_size[0] - resized_obj.x) / 2),
        y=int((screen_size[1] - resized_obj.y) / 2)
    )


def rsc_path(relative_path: str) -> str:
    base_path = os.path.abspath(".")

    if relative_path[0] == "\\":
        result = base_path + relative_path
    else:
        result = base_path + "\\" + relative_path
    return result


def in_zone(event, p_1: tuple, p_2: tuple, screen_size: None | tuple[int, int] | aobjects.ObjectSize) -> bool:
    new_p_1 = calc_resize(p_1, screen_size)
    new_p_2 = calc_resize(p_2, screen_size)

    return new_p_1.x <= event.x <= new_p_2.x and new_p_1.y <= event.y <= new_p_2.y


def in_circle(event, center: tuple, radius: int, screen_size: tuple[int, int] | aobjects.ObjectSize) -> bool:
    new_center = calc_resize(center, screen_size)
    new_radius = calc_resize((radius, 0), screen_size).x

    hypotenuse = math.sqrt((event.x - new_center.x) ** 2 + (event.y - new_center.y) ** 2)
    return hypotenuse <= new_radius


def calc_scrool_speed(delta: int) -> float:
    return delta / 120


def fast_convert(a) -> tuple[int, int]:
    return int(round(a.x / 1.5618)), int(round(a.y / 1.5618))


def rad_to_degrees(rad: float) -> float:
    return rad * 180 / math.pi


def degrees_to_rad(degrees: float) -> float:
    return degrees / 180 * math.pi


def calc_deviation(hgd: float, to_maintain: float) -> float:
    while hgd < 360 or to_maintain < 360:
        hgd += 360
        to_maintain += 360

    dev = to_maintain - hgd
    while dev >= 360:
        dev -= 360

    while dev < 0:
        dev += 360

    return dev


def format_degrees(number: int) -> int:
    if number < 0:
        number += 360
    elif number > 359:
        number -= 360
    return int(number)


def fill_number_dot(number: str) -> str:
    number = number.replace(".", "")
    while len(number) < 5:
        number = str(number) + " "
    return number[:3] + "." + number[3:]


def fill_number_left_underline(number: str) -> str:
    while len(number) < 5:
        number += "_"
    return number


def fill_number_left_space(number: str, length=6) -> str:
    while len(number) < length:
        number = " " + str(number)
    return number


def fill_number_right_zero(number: str, length=2) -> str:
    while len(number.split(".")[1]) < length:
        number = number + "0"
    return number


def fill_number_left_zero(number: str) -> str:
    while len(number) < 3:
        number = "0" + str(number)
    return number


def convert_to_objectsize(value: tuple | aobjects.ObjectSize) -> aobjects.ObjectSize:
    if isinstance(value, tuple):
        return aobjects.ObjectSize(*value)
    return value


def get_distance(point_1: tuple[int, int] | aobjects.ObjectSize, point_2: tuple[int, int] | aobjects.ObjectSize,
                 map_height_pixels: int) -> float:
    map_height_km = 282.96985
    km_in_pixel = map_height_km / map_height_pixels

    point_1 = convert_to_objectsize(point_1)
    point_2 = convert_to_objectsize(point_2)

    pixels = math.sqrt((point_2.x - point_1.x) ** 2 + (point_2.y - point_1.y) ** 2)

    return round(pixels * km_in_pixel, 1)


def get_angle(center: tuple[int, int] | aobjects.ObjectSize, point: tuple[int, int] | aobjects.ObjectSize,
              magnetic: bool) -> float:
    center = convert_to_objectsize(center)

    point = convert_to_objectsize(point)

    if center.x == point.x and center.y == point.y:
        result_angle = (-12.0 if magnetic else 0.0)
    else:
        vector_1 = (0, -500 - center.y)
        vector_2 = (point.x - center.x, point.y - center.y)

        angle = math.acos(
            (vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1]) / (
                    math.sqrt(vector_1[0] ** 2 + vector_1[1] ** 2) * math.sqrt(vector_2[0] ** 2 + vector_2[1] ** 2)
            )
        )
        result_angle = abs(rad_to_degrees(angle) + (-360 if point.x < center.x else 0)) + (-12 if magnetic else 0)

        if result_angle < 0:
            result_angle += 360
    return result_angle


def convert_float(number: str) -> float | None:
    try:
        return float(number)
    except:
        return


def get_navaid_coords(frq: float | str, navaid_type, exl: list | None = None) -> tuple[int, int] | None:
    frq = str(frq)
    if not exl:
        exl = []
    for k in navaid_type:
        if not (k in exl):
            for el_frq, el_coords in config.MARKERS[k]["points"].items():
                if el_frq == frq or el_frq == str(convert_float(frq)):
                    return el_coords


if __name__ == "__main__":
    print(fast_convert(aobjects.ObjectSize(x=190 + 382, y=150 + 60)))
