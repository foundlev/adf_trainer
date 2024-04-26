import random
import math
import time

import config
import aobjects
import afuncs


class Pointer:
    def __init__(self):
        self.angle = random.randint(0, 359)
        self.frq = None
        self.to_angle = None
        self.color = None
        self.active = False
        self.updated = time.time()

    def is_active(self) -> bool:
        return bool(self.active and self.color)

    def reset(self, can_disapper: bool, color: str):
        self.to_angle = None
        if can_disapper:
            self.frq = None
            self.active = False
        else:
            self.frq = None
            self.color = color
            self.active = True

    def get_angle(self) -> int:
        return -int(self.angle)

    def to(self, angle: int):
        self.to_angle = angle

    def _clear_angles(self):
        if self.angle < 0:
            self.angle += 360
        elif self.angle >= 360:
            self.angle -= 360

        if self.to_angle < 0:
            self.to_angle += 360
        elif self.to_angle >= 360:
            self.to_angle -= 360

    def rotate(self):
        if self.to_angle is None:
            return

        tick_time = 0.1
        step = 10

        t = time.time()
        if t - self.updated < tick_time:
            return
        self.updated = t

        self._clear_angles()

        dev = self.to_angle - self.angle

        if abs(dev) <= step:
            self.angle = self.to_angle
            self.to_angle = None
            return

        if 180 >= dev >= 0:
            moving = 1
        elif dev > 180:
            moving = -1
        elif 0 >= dev >= -180:
            moving = -1
        elif -180 >= dev >= -360:
            moving = 1
        else:
            return

        self.angle += (step * moving)


class Aircraft:
    def __init__(self):
        self.x = None
        self.y = None
        self.heading = None
        # Скорость: пикселей в секунду
        self.speed = 0.85
        self.boost = config.BOOST_MODE_DEFAULT
        # Размер самолета.
        self.dimensions = aobjects.ObjectSize(90, 90)

        # HDG для занятия.
        self.final_hdg = None

        self._respawn()

    def __str__(self) -> str:
        return f"Aircraft | X: {self.x} | Y: {self.y} | BOOST: {self.boost}"

    def _correct_hdg(self):
        if self.heading < 0:
            self.heading += 360
        elif self.heading >= 360:
            self.heading -= 360

    def _respawn(self):
        period_x = config.MAPS_WALLS[1][0] - config.MAPS_WALLS[0][0]
        period_y = config.MAPS_WALLS[1][1] - config.MAPS_WALLS[0][1]

        addition_x = random.uniform(0, period_x * 0.8)
        addition_y = random.uniform(0, period_y * 0.8)

        self.x = config.MAPS_WALLS[0][0] + period_x * 0.1 + addition_x
        self.y = config.MAPS_WALLS[0][1] + period_y * 0.1 + addition_y

        self.heading = random.uniform(0, 360)

    def distance_to_navaid(self, frq: float | str, screen_size: tuple[int, int] | aobjects.ObjectSize,
                           map_height_pixels: int) -> float:
        navaid_coords = afuncs.get_navaid_coords(frq, navaid_type=aobjects.NavaidTypes.vordme_dme)
        if navaid_coords and not (str(frq) in ("995", "995.0")):
            aircraft_coords = afuncs.calc_resize(self.position(), screen_size)
            el_coords = afuncs.calc_resize(navaid_coords, screen_size)
            return afuncs.get_distance(aircraft_coords, el_coords, map_height_pixels)
        return 0.0

    def angle_to_navaid(self, frq: float | str) -> int | None:
        navaid_coords = afuncs.get_navaid_coords(frq, navaid_type=aobjects.NavaidTypes.vordme_ndb_ndbdme, exl=["DME"])
        if navaid_coords:
            return int(afuncs.get_angle(self.position(), navaid_coords, magnetic=False) - self.heading)

    def change_hdg(self, changing_value: int | float):
        self.heading += changing_value
        self._correct_hdg()

    def change_boost(self, mode: aobjects.ChangeBoostType):
        idx = config.BOOST_MODES.index(self.boost)

        if mode == aobjects.ChangeBoostType.up:
            if idx < len(config.BOOST_MODES) - 1:
                self.boost = config.BOOST_MODES[idx + 1]
        elif mode == aobjects.ChangeBoostType.down:
            if idx > 0:
                self.boost = config.BOOST_MODES[idx - 1]

    def position(self) -> aobjects.ObjectSize:
        return aobjects.ObjectSize(self.x - self.dimensions.x / 2, self.y - self.dimensions.y / 2)

    def get_heading(self) -> float:
        return self.heading - 12

    def hdg(self) -> int:
        return int(-self.heading)

    def fly(self, seconds_passed: float):
        distance = self.speed * self.boost * seconds_passed
        heading_rad = self.heading * math.pi / 180

        distance_x = math.sin(heading_rad) * distance
        distance_y = -math.cos(heading_rad) * distance

        self.x += distance_x
        self.y += distance_y

        # Разворачиваем самолет, если он за границами карты.
        position = self.position()
        if self.final_hdg is None and not afuncs.in_zone(position, config.MAPS_WALLS[0], config.MAPS_WALLS[1], None):
            self.final_hdg = int(afuncs.get_angle(position, config.DIVERT_POINT, magnetic=False))

        if not (self.final_hdg is None):
            hdg_deviation = afuncs.calc_deviation(self.heading, self.final_hdg)
            print(f"TO ULSK: {self.final_hdg} | PLANE: {self.heading} | DEV: {hdg_deviation}")
            # Если курс не совпадает с нужным.
            if abs(hdg_deviation) <= 5:
                self.heading = self.final_hdg
                self.final_hdg = None
            else:
                hdg_changing_direction = 1 if hdg_deviation < 200 else -1
                # Исправляем его.
                self.change_hdg((hdg_changing_direction * seconds_passed * self.boost * 2))
