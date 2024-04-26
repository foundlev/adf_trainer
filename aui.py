import copy
import tkinter
from tkinter.ttk import Label
from PIL import Image, ImageTk, ImageFont, ImageDraw
import sys
import threading
import time
import random
import os

import config
import aobjects
from aobjects import StorageCell
import afuncs
import amodels


#########################

# ЯП: Python 3.10.5
# Дата начала разработки: 15.10.2022
# Дата окончания разработки: \
#   - Основная: 18.12.2022
#   - Исправления и оптимизация: XX.XX.XXXX

#########################


class App:
    def __init__(self):
        self.pics = {}
        self.fonts = {}
        self.values = {}

        self.root = tkinter.Tk()
        self.display = aobjects.ObjectSize(
            x=self.root.winfo_screenwidth(),
            y=self.root.winfo_screenheight()
        )
        self.panel = None

        # Boeing.
        self.boeing_adf_1_default = float(random.randint(config.ADF_RANGE[0], config.ADF_RANGE[1]))
        self.boeing_adf_2_default = float(random.randint(config.ADF_RANGE[0], config.ADF_RANGE[1]))

        self.boeing_vor_act_1_default = str(
            round(random.randint(int(config.VOR_RANGE[0] * 10), int(config.VOR_RANGE[1] * 10)) / 10, 2)) + "0"
        self.boeing_vor_stby_1_default = str(
            round(random.randint(int(config.VOR_RANGE[0] * 10), int(config.VOR_RANGE[1] * 10)) / 10, 2)) + "0"
        self.boeing_vor_act_2_default = str(
            round(random.randint(int(config.VOR_RANGE[0] * 10), int(config.VOR_RANGE[1] * 10)) / 10, 2)) + "0"
        self.boeing_vor_stby_2_default = str(
            round(random.randint(int(config.VOR_RANGE[0] * 10), int(config.VOR_RANGE[1] * 10)) / 10, 2)) + "0"

        self.boeing_ddb_arrow = amodels.Pointer()
        self.boeing_dsg_arrow = amodels.Pointer()
        self.boeing_bdb_arrow = amodels.Pointer()
        self.boeing_bsg_arrow = amodels.Pointer()

        # Airbus.
        self.airbus_adf_1_act_default = float(random.randint(config.ADF_RANGE[0], config.ADF_RANGE[1]))
        self.airbus_adf_1_stby_default = float(random.randint(config.ADF_RANGE[0], config.ADF_RANGE[1]))
        self.airbus_adf_2_act_default = float(random.randint(config.ADF_RANGE[0], config.ADF_RANGE[1]))
        self.airbus_adf_2_stby_default = float(random.randint(config.ADF_RANGE[0], config.ADF_RANGE[1]))

        self.airbus_vor_1_act_default = str(
            round(random.randint(int(config.VOR_RANGE[0] * 10), int(config.VOR_RANGE[1] * 10)) / 10, 2)) + "0"
        self.airbus_vor_1_stby_default = str(
            round(random.randint(int(config.VOR_RANGE[0] * 10), int(config.VOR_RANGE[1] * 10)) / 10, 2)) + "0"
        self.airbus_vor_2_act_default = str(
            round(random.randint(int(config.VOR_RANGE[0] * 10), int(config.VOR_RANGE[1] * 10)) / 10, 2)) + "0"
        self.airbus_vor_2_stby_default = str(
            round(random.randint(int(config.VOR_RANGE[0] * 10), int(config.VOR_RANGE[1] * 10)) / 10, 2)) + "0"

        self.airbus_ddb_arrow = amodels.Pointer()
        self.airbus_dsg_arrow = amodels.Pointer()
        self.airbus_bdb_arrow = amodels.Pointer()
        self.airbus_bsg_arrow = amodels.Pointer()

        self.aircraft = amodels.Aircraft()

        self._load_pics()
        self._load_fonts()

    def _open_img(self, img_path: str, size: tuple[int, int]):
        abs_path = afuncs.rsc_path(img_path)
        new_size = self.rsz(size)

        return Image.open(abs_path).convert("RGBA").resize(new_size)

    def _open_font(self, font_path: str, size: int):
        abs_path = afuncs.rsc_path(font_path)
        new_size = int(self.rsz((size, 0)).x)

        return ImageFont.truetype(abs_path, size=new_size)

    def _load_pics(self):
        self.pics["bg"] = self._open_img("data\\img\\bg.png", (1916, 1076))
        self.pics["bgUpper"] = self._open_img("data\\img\\bg_upper.png", (1916, 1076))
        self.pics["expandIcon"] = self._open_img("data\\img\\expand.png", (50, 50))
        self.pics["aircraft"] = self._open_img("data\\img\\aircraft.png", (90, 90))

        # Карта развернута.
        self.pics["map"] = self._open_img("data\\img\\map.png", (1916, 1076))
        self.pics["mapCleared"] = self._open_img("data\\img\\map_cleared.png", (1916, 1076))
        self.pics["minimizeIcon"] = self._open_img("data\\img\\minimize.png", (75, 75))
        self.pics["tpHere"] = self._open_img("data\\img\\tp_here.png", config.TPHERE_BANNER_SIZE)
        self.pics["point"] = self._open_img("data\\img\\point.png", (6, 6))
        self.pics["markerInfoBanner"] = self._open_img("data\\img\\marker_info.png", config.MARKER_BANNER_SIZE)
        self.pics["markers"] = {
            "VOR": self._open_img("data\\img\\icon_vor.png", (60, 46)),
            "VORDME": self._open_img("data\\img\\icon_vordme.png", (60, 46)),
            "DME": self._open_img("data\\img\\icon_dme.png", (60, 46)),
            "NDB": self._open_img("data\\img\\icon_ndb.png", (60, 46)),
            "NDBDME": self._open_img("data\\img\\icon_ndbdme.png", (60, 46))
        }

        # Метки маяков.
        self.pics["points"] = {
            "red": self._open_img("data\\img\\point_red.png", config.MARKER_SIZE),
            "purple": self._open_img("data\\img\\point_purple.png", config.MARKER_SIZE),
            "orange": self._open_img("data\\img\\point_orange.png", config.MARKER_SIZE),
            "blue": self._open_img("data\\img\\point_blue.png", config.MARKER_SIZE),
        }

        # Переключатели.
        self.pics["switchers"] = {
            "big": {
                "green": self._open_img("data\\img\\switcher_green.png", (80, 80)),
                "orange": self._open_img("data\\img\\switcher_orange.png", (80, 80))
            },
            "small": {
                "double": self._open_img("data\\img\\switcher_small_double.png", (80, 80)),
                "single": self._open_img("data\\img\\switcher_small_single.png", (80, 80)),
                "normal": self._open_img("data\\img\\switcher_small.png", (60, 60))
            },
            "level": {
                "normal": self._open_img("data\\img\\level.png", (80, 80)),
                "middle": {
                    "small": self._open_img("data\\img\\level_middle.png", (80, 80)),
                    "big": self._open_img("data\\img\\level_round.png", (26, 26))
                }
            }
        }
        self.pics["headings"] = (
            self._open_img("data\\img\\heading1.png", (160, 160)),
            self._open_img("data\\img\\heading2.png", (406, 406))
        )
        self.pics["simultaneousSwitcher"] = {
            "green": self._open_img("data\\img\\synhr_green.png", (108, 62)),
            "red": self._open_img("data\\img\\synhr_red.png", (108, 62)),
            "button": self._open_img("data\\img\\synhr_button.png", (65, 65))
        }

        self.pics["panel"] = {
            "indicator": self._open_img("data\\img\\green_indicator.png", (17, 17)),
            "boeing": {
                "1": self._open_img("data\\img\\boeing_panel_1.png", (629, 410)),
                "2": self._open_img("data\\img\\boeing_panel_2.png", (629, 410)),
                "3": self._open_img("data\\img\\boeing_panel_3.png", (629, 410))
            },
            "airbus": {
                "1": self._open_img("data\\img\\airbus_panel_1.png", (629, 410)),
                "2": self._open_img("data\\img\\airbus_panel_2.png", (629, 410))
            }
        }

        self.pics["rotate"] = {
            "big": self._open_img("data\\img\\rotate_big.png", (160, 160)),
            "miniBig": self._open_img("data\\img\\rotate_big.png", (140, 140)),
            "medium": self._open_img("data\\img\\rotate_medium.png", (160, 160)),
            "miniMedium": self._open_img("data\\img\\rotate_medium.png", (140, 140)),
            "small": self._open_img("data\\img\\rotate_small.png", (160, 160))
        }

        self.pics["arrows"] = {
            "single": {
                "green": self._open_img("data\\img\\arrows_single_green.png", (410, 410)),
                "blue": self._open_img("data\\img\\arrows_single_blue.png", (410, 410))
            },
            "double": {
                "green": self._open_img("data\\img\\arrows_double_green.png", (410, 410)),
                "blue": self._open_img("data\\img\\arrows_double_blue.png", (410, 410))
            }
        }

        self.pics["arrow"] = {
            "single": self._open_img("data\\img\\arrow_single.png", (140, 140)),
            "double": self._open_img("data\\img\\arrow_double.png", (140, 140))
        }

    def _load_fonts(self):
        self.fonts["roboto"] = {
            "bold": self._open_font("data\\fonts\\Roboto-Bold.ttf", 16),
            "medium": {
                26: self._open_font("data\\fonts\\Roboto-Medium.ttf", 26),
                22: self._open_font("data\\fonts\\Roboto-Medium.ttf", 22)
            },
            "regular": self._open_font("data\\fonts\\Roboto-Regular.ttf", 20)
        }
        self.fonts["timer"] = {
            44: self._open_font("data\\fonts\\CursedTimerUlil.ttf", 44),
            38: self._open_font("data\\fonts\\CursedTimerUlil.ttf", 38),
            26: self._open_font("data\\fonts\\CursedTimerUlil.ttf", 26)
        }
        self.fonts["calculator"] = {
            30: self._open_font("data\\fonts\\Calculatrix7Regular.ttf", 30)
        }
        self.fonts["helvetica"] = {
            20: self._open_font("data\\fonts\\HelveticaLT57Condensed.ttf", 24)
        }

    def _click(self, event):
        self._catch_event(event)

    def _mouse_scroll(self, event):
        self._catch_event(event)

    def _change_angle(self, name, dev_angle):
        now_angle = self.value(name, default_value=0)
        self.value(name, now_angle + dev_angle)

    def _add_vor_value(self, name, dev_value, default_value):
        if name is None:
            return
        now_value = str(self.value(name, default_value=default_value)).replace(".", "")
        if len(now_value) < 5:
            now_value += str(dev_value)
            self.value(name, now_value)

    def _backspace_vor_value(self, name, default_value):
        if name is None:
            return
        now_value = str(self.value(name, default_value=default_value)).replace(".", "")
        if len(now_value) > 1:
            now_value = now_value[:-1]
            self.value(name, now_value)

    def get_vor_value(self, name, default_value) -> float:
        if name is None:
            return 0.0

        now_value = str(self.value(name, default_value=default_value)).replace(".", "")
        if len(now_value) == 5 and now_value.isdigit():
            frq = round(int(now_value) / 100, 2)
            return frq
        return 0.0

    def _change_value(self, name, dev_value, default_value, min_value, max_value):
        now_value = float(self.value(name, default_value=default_value))
        now_value += dev_value

        if now_value < min_value:
            now_value = min_value
        elif now_value > max_value:
            now_value = max_value

        self.value(name, round(now_value, 2))

    def _catch_event(self, event):
        def touch_marker(ev, display) -> bool:
            for marker, values in config.MARKERS.items():
                for frq, coords in values["points"].items():

                    zn_x = 10
                    zn_y = 20
                    coords_map = (
                        (coords[0] - zn_x, coords[1] - zn_y),
                        (coords[0] + zn_x, coords[1] + zn_y)
                    )

                    if afuncs.in_zone(ev, coords_map[0], coords_map[1], display):
                        self.value("actMarkerType", marker)
                        self.value("actMarkerFrq", frq)
                        self.value("actMarkerCoords", coords)

                        return True

        rsz_event = afuncs.fast_convert(event)
        print(f"Event: {event} | For code: {rsz_event}")

        # Нажатие ЛКМ.
        if event.num == 1:

            if self.value("mapExpanded"):
                # Кнопка свернуть карту.
                if afuncs.in_zone(event, (1833, 15), (1902, 86), self.display):
                    self.value("mapExpanded", False)

                # Отмена нажатия на маяк.
                elif (self.value("actMarkerCoords") and
                      afuncs.in_zone(
                          event,
                          (self.value("actMarkerCoords")[0] - 125, self.value("actMarkerCoords")[1] - 110),
                          (self.value("actMarkerCoords")[0] + 125, self.value("actMarkerCoords")[1] - 50),
                          self.display
                      )):
                    self.value("actMarkerType", False)
                    self.value("actMarkerFrq", False)
                    self.value("actMarkerCoords", False)

                # Нажатие на маяк.
                elif touch_marker(event, self.display):
                    pass

                # Отмена постановки точки перемещения самолета.
                elif (self.value("tpHerePoint") and
                      afuncs.in_zone(
                          event,
                          (self.value("tpHerePoint")[0] + self.rsz_single(107), self.value("tpHerePoint")[1] - self.rsz_single(106)),
                          (self.value("tpHerePoint")[0] + self.rsz_single(124), self.value("tpHerePoint")[1] - self.rsz_single(90)),
                          None
                      )):
                    self.value("tpHerePoint", False)

                # Перенос самолета на выбранную точку.
                elif (self.value("tpHerePoint") and
                      afuncs.in_zone(
                          event,
                          (self.value("tpHerePoint")[0] - self.rsz_single(121), self.value("tpHerePoint")[1] - self.rsz_single(95)),
                          (self.value("tpHerePoint")[0] + self.rsz_single(120), self.value("tpHerePoint")[1] - self.rsz_single(65)),
                          None
                      )):
                    new_aircraft_coords = afuncs.calc_resize(self.value("tpHerePoint"), self.display, rev=True)
                    self.value("tpHerePoint", False)
                    self.aircraft.x, self.aircraft.y = new_aircraft_coords

                # Постановка точки перемещения самолета.
                elif afuncs.in_zone(event, config.MAPS_WALLS[0], config.MAPS_WALLS[1], self.display):
                    self.value("tpHerePoint", (event.x, event.y))

            else:
                boeing_panel_number = self.value(StorageCell.boeing_panel, default_value=1)
                if boeing_panel_number == 2:
                    keyboard_insert_in = StorageCell.boeing_vor_sfrq_1
                    vor_act_name = StorageCell.boeing_vor_afrq_1
                    stby_default_frq = self.boeing_vor_stby_1_default
                    act_default_frq = self.boeing_vor_act_1_default
                elif boeing_panel_number == 3:
                    keyboard_insert_in = StorageCell.boeing_vor_sfrq_2
                    vor_act_name = StorageCell.boeing_vor_afrq_2
                    stby_default_frq = self.boeing_vor_stby_2_default
                    act_default_frq = self.boeing_vor_act_2_default
                else:
                    keyboard_insert_in = None
                    stby_default_frq = None
                    vor_act_name = None
                    act_default_frq = None

                # Кнопка выход.
                if afuncs.in_zone(event, (968, 970), (1238, 1049), self.display):
                    self.exit()

                # Кнопка информация.
                elif afuncs.in_zone(event, (681, 972), (952, 1047), self.display):
                    os.startfile(afuncs.rsc_path("data\\img\\info.png"))

                # Кнопка разворачивания карты.
                elif afuncs.in_zone(event, (891, 699), (937, 743), self.display):
                    self.value("mapExpanded", True)

                # Кнопки переключения панелей.
                elif afuncs.in_zone(event, (20, 656), (150, 694), self.display):
                    self.value(StorageCell.boeing_panel, 1)

                elif afuncs.in_zone(event, (150, 656), (283, 694), self.display):
                    self.value(StorageCell.boeing_panel, 2)

                elif afuncs.in_zone(event, (283, 656), (415, 694), self.display):
                    self.value(StorageCell.boeing_panel, 3)

                elif afuncs.in_zone(event, (1281, 656), (1411, 693), self.display):
                    self.value(StorageCell.airbus_panel, 1)

                elif afuncs.in_zone(event, (1411, 656), (1544, 694), self.display):
                    self.value(StorageCell.airbus_panel, 2)

                # Панель Boeing.
                elif afuncs.in_zone(event, (688, 135), (774, 186), self.display):
                    self.value(StorageCell.boeing_digital_level_1, "vor")

                elif afuncs.in_zone(event, (693, 222), (775, 273), self.display):
                    self.value(StorageCell.boeing_digital_level_1, "adf")

                elif afuncs.in_zone(event, (648, 179), (766, 225), self.display):
                    self.value(StorageCell.boeing_digital_level_1, False)

                elif afuncs.in_zone(event, (808, 135), (931, 178), self.display):
                    self.value(StorageCell.boeing_digital_level_2, "vor")

                elif afuncs.in_zone(event, (816, 216), (906, 268), self.display):
                    self.value(StorageCell.boeing_digital_level_2, "adf")

                elif afuncs.in_zone(event, (820, 182), (944, 227), self.display):
                    self.value(StorageCell.boeing_digital_level_2, False)

                # Набор на клавиатуре.
                # 1.
                elif afuncs.in_circle(event, (407, 782), 24, self.display):
                    self._add_vor_value(keyboard_insert_in, "1", default_value=stby_default_frq)
                # 2.
                elif afuncs.in_circle(event, (485, 782), 24, self.display):
                    self._add_vor_value(keyboard_insert_in, "2", default_value=stby_default_frq)
                # 3.
                elif afuncs.in_circle(event, (565, 782), 24, self.display):
                    self._add_vor_value(keyboard_insert_in, "3", default_value=stby_default_frq)
                # 4.
                elif afuncs.in_circle(event, (407, 851), 24, self.display):
                    self._add_vor_value(keyboard_insert_in, "4", default_value=stby_default_frq)
                # 5.
                elif afuncs.in_circle(event, (485, 851), 24, self.display):
                    self._add_vor_value(keyboard_insert_in, "5", default_value=stby_default_frq)
                # 6.
                elif afuncs.in_circle(event, (565, 851), 24, self.display):
                    self._add_vor_value(keyboard_insert_in, "6", default_value=stby_default_frq)
                # 7.
                elif afuncs.in_circle(event, (407, 923), 24, self.display):
                    self._add_vor_value(keyboard_insert_in, "7", default_value=stby_default_frq)
                # 8.
                elif afuncs.in_circle(event, (485, 923), 24, self.display):
                    self._add_vor_value(keyboard_insert_in, "8", default_value=stby_default_frq)
                # 9.
                elif afuncs.in_circle(event, (565, 923), 24, self.display):
                    self._add_vor_value(keyboard_insert_in, "9", default_value=stby_default_frq)
                # 0.
                elif afuncs.in_circle(event, (485, 991), 24, self.display):
                    self._add_vor_value(keyboard_insert_in, "0", default_value=stby_default_frq)
                # CLR.
                elif afuncs.in_circle(event, (565, 991), 24, self.display):
                    self._backspace_vor_value(keyboard_insert_in, default_value=stby_default_frq)

                # Кнопка Transfer.
                elif afuncs.in_zone(event, (39, 832), (73, 878), self.display):
                    if self.get_vor_value(keyboard_insert_in, default_value=stby_default_frq):
                        act_frq = self.value(vor_act_name, default_value=act_default_frq)
                        stby_frq = self.value(keyboard_insert_in, default_value=stby_default_frq)
                        if stby_frq:
                            vor_stby_value = afuncs.fill_number_dot(str(stby_frq))
                            self.value(vor_act_name, vor_stby_value)
                            self.value(keyboard_insert_in, str(act_frq).replace(".", ""))

                # Переключение переключателей ADF - VOR.
                elif afuncs.in_zone(event, (679, 511), (775, 600), self.display):
                    now_pos = self.value(StorageCell.boeing_sw_1, default_value=0)
                    self.value(StorageCell.boeing_sw_1, int(not bool(now_pos)))

                elif afuncs.in_zone(event, (837, 511), (922, 600), self.display):
                    now_pos = self.value(StorageCell.boeing_sw_2, default_value=0)
                    self.value(StorageCell.boeing_sw_2, int(not bool(now_pos)))

                # Панель Airbus.
                elif afuncs.in_zone(event, (980, 161), (1023, 252), self.display):
                    self.value(StorageCell.airbus_digital_level_1, "adf")

                elif afuncs.in_zone(event, (1071, 159), (1123, 246), self.display):
                    self.value(StorageCell.airbus_digital_level_1, "vor")

                elif afuncs.in_zone(event, (1019, 152), (1080, 257), self.display):
                    self.value(StorageCell.airbus_digital_level_1, False)

                elif afuncs.in_zone(event, (1131, 161), (1175, 252), self.display):
                    self.value(StorageCell.airbus_digital_level_2, "adf")

                elif afuncs.in_zone(event, (1220, 159), (1273, 246), self.display):
                    self.value(StorageCell.airbus_digital_level_2, "vor")

                elif afuncs.in_zone(event, (1173, 152), (1229, 257), self.display):
                    self.value(StorageCell.airbus_digital_level_2, False)

                elif afuncs.in_zone(event, (1809, 964), (1859, 1049), self.display):
                    if self.value(StorageCell.airbus_panel, default_value=1) == 1:
                        level_number = StorageCell.airbus_panel_1_level
                    else:
                        level_number = StorageCell.airbus_panel_2_level
                    now_value = self.value(level_number, default_value=False)
                    self.value(level_number, not now_value)

                elif afuncs.in_zone(event, (1403, 1008), (1460, 1044), self.display):
                    if self.value(StorageCell.airbus_panel, default_value=1) == 1:
                        vor_number = StorageCell.airbus_panel_1_vor
                        level_number = StorageCell.airbus_panel_1_level
                    else:
                        vor_number = StorageCell.airbus_panel_2_vor
                        level_number = StorageCell.airbus_panel_2_level
                    if self.value(level_number, default_value=False):
                        self.value(vor_number, True)

                elif afuncs.in_zone(event, (1647, 1006), (1706, 1044), self.display):
                    if self.value(StorageCell.airbus_panel, default_value=1) == 1:
                        vor_number = StorageCell.airbus_panel_1_vor
                        level_number = StorageCell.airbus_panel_1_level
                    else:
                        vor_number = StorageCell.airbus_panel_2_vor
                        level_number = StorageCell.airbus_panel_2_level
                    if self.value(level_number, default_value=False):
                        self.value(vor_number, False)

                elif afuncs.in_zone(event, (1560, 743), (1615, 779), self.display):
                    if self.value(StorageCell.airbus_panel, default_value=1) == 1:
                        level_number = StorageCell.airbus_panel_1_level
                        vor_number = StorageCell.airbus_panel_1_vor

                        if self.value(vor_number, default_value=True):
                            afrq_name = StorageCell.airbus_vor_afrq_1
                            afrq_default = self.airbus_vor_1_act_default
                            sfrq_name = StorageCell.airbus_vor_sfrq_1
                            sfrq_default = self.airbus_vor_1_stby_default
                        else:
                            afrq_name = StorageCell.airbus_adf_afrq_1
                            afrq_default = self.airbus_adf_1_act_default
                            sfrq_name = StorageCell.airbus_adf_sfrq_1
                            sfrq_default = self.airbus_adf_1_stby_default
                    else:
                        level_number = StorageCell.airbus_panel_2_level
                        vor_number = StorageCell.airbus_panel_2_vor

                        if self.value(vor_number, default_value=True):
                            afrq_name = StorageCell.airbus_vor_afrq_2
                            afrq_default = self.airbus_vor_2_act_default
                            sfrq_name = StorageCell.airbus_vor_sfrq_2
                            sfrq_default = self.airbus_vor_2_stby_default
                        else:
                            afrq_name = StorageCell.airbus_adf_afrq_2
                            afrq_default = self.airbus_adf_2_act_default
                            sfrq_name = StorageCell.airbus_adf_sfrq_2
                            sfrq_default = self.airbus_adf_2_stby_default

                    if self.value(level_number, default_value=False):
                        afrq = self.value(afrq_name, default_value=afrq_default)
                        sfrq = self.value(sfrq_name, default_value=sfrq_default)

                        self.value(afrq_name, sfrq)
                        self.value(sfrq_name, afrq)

                # Кнопка разворот ВС влево.
                elif afuncs.in_zone(event, (1022, 687), (1098, 720), self.display):
                    self.aircraft.change_hdg(-5)

                # Кнопка разворот ВС вправо.
                elif afuncs.in_zone(event, (1118, 677), (1190, 727), self.display):
                    self.aircraft.change_hdg(5)

                # Кнопка ускорения времени.
                elif afuncs.in_zone(event, (1101, 835), (1172, 880), self.display):
                    self.aircraft.change_boost(aobjects.ChangeBoostType.up)

                # Кнопка замедления времени.
                elif afuncs.in_zone(event, (1179, 835), (1245, 880), self.display):
                    self.aircraft.change_boost(aobjects.ChangeBoostType.down)

                # Переключение переключателей ADF - VOR.
                elif afuncs.in_zone(event, (1000, 522), (1088, 620), self.display):
                    now_pos = self.value(StorageCell.airbus_sw_1, default_value=0)
                    self.value(StorageCell.airbus_sw_1, int(not bool(now_pos)))

                elif afuncs.in_zone(event, (1167, 522), (1234, 620), self.display):
                    now_pos = self.value(StorageCell.airbus_sw_2, default_value=0)
                    self.value(StorageCell.airbus_sw_2, int(not bool(now_pos)))

        # Вращение колесика мыши.
        elif event.delta:
            scroll_speed = -afuncs.calc_scrool_speed(event.delta)
            # scroll_speed = 1 if scroll_speed > 0 else -1
            rotation_rate = 5
            rotation_angle = scroll_speed * rotation_rate

            boeing_panel_number = self.value(StorageCell.boeing_panel, default_value=1)
            airbus_panel_number = self.value(StorageCell.airbus_panel, default_value=1)

            if boeing_panel_number == 1:

                if afuncs.in_circle(event, (180, 920), 40, self.display):
                    self._change_angle(StorageCell.boeing_rotate_1_small, rotation_angle)
                    self._change_value(StorageCell.boeing_adf_frq_1, round(scroll_speed * 0.5, 1),
                                       self.boeing_adf_1_default, config.ADF_RANGE[0], config.ADF_RANGE[1])

                elif afuncs.in_circle(event, (180, 920), 60, self.display):
                    self._change_angle(StorageCell.boeing_rotate_1_medium, rotation_angle)
                    self._change_value(StorageCell.boeing_adf_frq_1, int(scroll_speed * 10),
                                       self.boeing_adf_1_default, config.ADF_RANGE[0], config.ADF_RANGE[1])

                elif afuncs.in_circle(event, (180, 920), 120, self.display):
                    self._change_angle(StorageCell.boeing_rotate_1_big, rotation_angle)
                    self._change_value(StorageCell.boeing_adf_frq_1, int(scroll_speed * 100),
                                       self.boeing_adf_1_default, config.ADF_RANGE[0], config.ADF_RANGE[1])

                elif afuncs.in_circle(event, (470, 920), 40, self.display):
                    self._change_angle(StorageCell.boeing_rotate_2_small, rotation_angle)
                    self._change_value(StorageCell.boeing_adf_frq_2, round(scroll_speed * 0.5, 2),
                                       self.boeing_adf_2_default, config.ADF_RANGE[0], config.ADF_RANGE[1])

                elif afuncs.in_circle(event, (470, 920), 60, self.display):
                    self._change_angle(StorageCell.boeing_rotate_2_medium, rotation_angle)
                    self._change_value(StorageCell.boeing_adf_frq_2, int(scroll_speed * 10),
                                       self.boeing_adf_2_default, config.ADF_RANGE[0], config.ADF_RANGE[1])

                elif afuncs.in_circle(event, (470, 920), 120, self.display):
                    self._change_angle(StorageCell.boeing_rotate_2_big, rotation_angle)
                    self._change_value(StorageCell.boeing_adf_frq_2, int(scroll_speed * 100),
                                       self.boeing_adf_2_default, config.ADF_RANGE[0], config.ADF_RANGE[1])

            if airbus_panel_number == 1:
                level_number = StorageCell.airbus_panel_1_level
                level_value = self.value(level_number, default_value=False)

                vor_number = StorageCell.airbus_panel_1_vor
                vor_able = self.value(vor_number, default_value=True)

                adf_frq = StorageCell.airbus_adf_sfrq_1
                vor_frq = StorageCell.airbus_vor_sfrq_1

                rotate_big = StorageCell.airbus_rotate_1_big
                rotate_medium = StorageCell.airbus_rotate_1_medium

                if vor_able:
                    frq_act_default = self.airbus_vor_1_act_default
                    frq_stby_default = self.airbus_vor_1_stby_default
                    frq_name = vor_frq
                else:
                    frq_act_default = self.airbus_adf_1_act_default
                    frq_stby_default = self.airbus_adf_1_stby_default
                    frq_name = adf_frq

            else:
                level_number = StorageCell.airbus_panel_2_level
                level_value = self.value(level_number, default_value=False)

                vor_number = StorageCell.airbus_panel_2_vor
                vor_able = self.value(vor_number, default_value=True)

                adf_frq = StorageCell.airbus_adf_sfrq_2
                vor_frq = StorageCell.airbus_vor_sfrq_2

                rotate_big = StorageCell.airbus_rotate_2_big
                rotate_medium = StorageCell.airbus_rotate_2_medium

                if vor_able:
                    frq_act_default = self.airbus_vor_2_act_default
                    frq_stby_default = self.airbus_vor_2_stby_default
                    frq_name = vor_frq
                else:
                    frq_act_default = self.airbus_adf_2_act_default
                    frq_stby_default = self.airbus_adf_2_stby_default
                    frq_name = adf_frq

            if vor_able:
                dev_step_big = 1
                dev_step_medium = 0.05

                frq_min = config.VOR_RANGE[0]
                frq_max = config.VOR_RANGE[1]
            else:
                dev_step_big = 10
                dev_step_medium = 0.5

                frq_min = config.ADF_RANGE[0]
                frq_max = config.ADF_RANGE[1]

            if afuncs.in_circle(event, (1700, 896), 50, self.display) and level_value:
                self._change_angle(rotate_medium, rotation_angle)
                self._change_value(frq_name, float(scroll_speed * dev_step_medium),
                                   frq_stby_default, frq_min, frq_max)

            elif afuncs.in_circle(event, (1700, 896), 100, self.display) and level_value:
                self._change_angle(rotate_big, rotation_angle)
                self._change_value(frq_name, int(scroll_speed * dev_step_big),
                                   frq_stby_default, frq_min, frq_max)

    def rsz(self, values: tuple[int, int] | tuple[float, float]) -> aobjects.ObjectSize:
        return afuncs.calc_resize(values, self.display)

    def rsz_single(self, value: int | float) -> int:
        return self.rsz((value, value)).x

    def value(self, key: str, new_value: any = None, default_value: any = None):
        if new_value is None:

            now_value = self.values.get(key, default_value)
            if isinstance(now_value, (list, dict, tuple, set)):
                now_value = copy.deepcopy(now_value)

            return now_value

        else:
            if isinstance(new_value, (list, dict, tuple, set)):
                new_value = copy.deepcopy(new_value)
            self.values[key] = new_value

    @staticmethod
    def exit():
        sys.exit()

    def load(self):
        self.root.title(config.APP_TITLE)
        self.root.wm_attributes('-fullscreen', True)
        self.root.configure(background='black')

        frame_main = tkinter.Frame(self.root)
        frame_main.pack(side=tkinter.TOP, fill='x')

        bg = copy.deepcopy(self.pics["bg"])
        bg_photo = ImageTk.PhotoImage(bg)

        self.panel = Label(frame_main, image=bg_photo)
        self.panel.pack(side=tkinter.BOTTOM)

        # Реакция на ЛКМ.
        self.root.bind("<1>", self._click)
        # Реакция на вращение колесика мыши.
        self.root.bind("<MouseWheel>", self._mouse_scroll)

        t = threading.Thread(target=self._update_screen, daemon=True)
        t.start()

        f = threading.Thread(target=self._update_process, daemon=True)
        f.start()

        self.root.mainloop()

    def _update_process(self):
        while True:
            time.sleep(0.05)

            updated = float(self.value("aircraftUpdated", default_value=0.0))
            t = time.time()

            if updated:
                seconds = t - updated
                self.aircraft.fly(seconds_passed=seconds)

            self.value("aircraftUpdated", t)

            if config.SHOW_TRACK:
                updated_track = float(self.value("trackUpdated", default_value=0.0))

                if t - updated_track >= 0.1:
                    self.value("trackUpdated", t)

                    points = self.value("trackPoints")
                    if not points:
                        points = []
                    points.append((self.aircraft.x, self.aircraft.y))
                    self.value("trackPoints", points)

            # Обновляем все стрелки.
            # (Объект стрелки, ячейка с частотой, ячейка с переключателем, частота по умолчанию, треб. знач. переключ., цвет стрелки, м. исчез.).
            pointers = (
                # Цифровые стрелки Boeing.
                (self.boeing_dsg_arrow, StorageCell.boeing_adf_frq_1, self.boeing_adf_1_default, StorageCell.boeing_digital_level_1, "adf", "blue", True),
                (self.boeing_dsg_arrow, StorageCell.boeing_vor_afrq_1, self.boeing_vor_act_1_default, StorageCell.boeing_digital_level_1, "vor", "green", True),
                (self.boeing_ddb_arrow, StorageCell.boeing_adf_frq_2, self.boeing_adf_2_default, StorageCell.boeing_digital_level_2, "adf", "blue", True),
                (self.boeing_ddb_arrow, StorageCell.boeing_vor_afrq_2, self.boeing_vor_act_2_default, StorageCell.boeing_digital_level_2, "vor", "green", True),
                # Физ. стрелки Boeing. 0 - VOR, 1 - ADF.
                (self.boeing_bsg_arrow, StorageCell.boeing_adf_frq_1, self.boeing_adf_1_default, StorageCell.boeing_sw_1, 1, "backup", False),
                (self.boeing_bsg_arrow, StorageCell.boeing_vor_afrq_1, self.boeing_vor_act_1_default, StorageCell.boeing_sw_1, 0, "backup", False),
                (self.boeing_bdb_arrow, StorageCell.boeing_adf_frq_2, self.boeing_adf_2_default, StorageCell.boeing_sw_2, 1, "backup", False),
                (self.boeing_bdb_arrow, StorageCell.boeing_vor_afrq_2, self.boeing_vor_act_2_default, StorageCell.boeing_sw_2, 0, "backup", False),
                # Цифровые стрелки Airbus.
                (self.airbus_dsg_arrow, StorageCell.airbus_adf_afrq_1, self.airbus_adf_1_act_default, StorageCell.airbus_digital_level_1, "adf", "blue", True),
                (self.airbus_dsg_arrow, StorageCell.airbus_vor_afrq_1, self.airbus_vor_1_act_default, StorageCell.airbus_digital_level_1, "vor", "green", True),
                (self.airbus_ddb_arrow, StorageCell.airbus_adf_afrq_2, self.airbus_adf_2_act_default, StorageCell.airbus_digital_level_2, "adf", "blue", True),
                (self.airbus_ddb_arrow, StorageCell.airbus_vor_afrq_2, self.airbus_vor_2_act_default, StorageCell.airbus_digital_level_2, "vor", "green", True),
                # Физ. стрелки Airbus. 0 - VOR, 1 - ADF.
                (self.airbus_bsg_arrow, StorageCell.airbus_adf_afrq_1, self.airbus_adf_1_act_default, StorageCell.airbus_sw_1, 1, "backup", False),
                (self.airbus_bsg_arrow, StorageCell.airbus_vor_afrq_1, self.airbus_vor_1_act_default, StorageCell.airbus_sw_1, 0, "backup", False),
                (self.airbus_bdb_arrow, StorageCell.airbus_adf_afrq_2, self.airbus_adf_2_act_default, StorageCell.airbus_sw_2, 1, "backup", False),
                (self.airbus_bdb_arrow, StorageCell.airbus_vor_afrq_2, self.airbus_vor_2_act_default, StorageCell.airbus_sw_2, 0, "backup", False)
            )

            for pointer in pointers:
                # Получаем частоту.
                frq = self.value(pointer[1], default_value=pointer[2])
                # Получаем угол на навигационную точку.
                naviad_angle = self.aircraft.angle_to_navaid(frq)

                pointer_obj = pointer[0]

                switcher_name = pointer[3]
                switcher_must_value = pointer[4]
                color = pointer[5]
                can_disapper = pointer[6]

                switcher_value = self.value(switcher_name, default_value=0)

                if not (naviad_angle is None) and switcher_value == switcher_must_value:
                    pointer_obj.color = color
                    pointer_obj.active = True
                    pointer_obj.to(angle=naviad_angle)
                    pointer_obj.rotate()
                    pointer_obj.frq = frq
                else:
                    if not pointer_obj.is_active() or (pointer_obj.is_active() and pointer_obj.color == color):
                        pointer_obj.reset(can_disapper, color)

    def _update_screen(self):
        while True:
            if self.value("mapExpanded"):
                bg = copy.deepcopy(self.pics["map"])

                # Кнопка свернуть карту.
                minimize_icon = copy.deepcopy(self.pics["minimizeIcon"])
                bg.alpha_composite(minimize_icon, self.rsz((1830, 12)))

                if config.SHOW_TRACK:
                    # Отобраем точки траектории.
                    points = self.value("trackPoints")
                    if points:
                        point_icon = copy.deepcopy(self.pics["point"])
                        for point in points:
                            bg.alpha_composite(point_icon, self.rsz((point[0], point[1])))

                # Отображаем точку для переноса самолета.
                tp_here_coords = self.value("tpHerePoint")
                if tp_here_coords:
                    tp_here_icon = copy.deepcopy(self.pics["tpHere"])
                    tp_here_size = self.rsz(config.TPHERE_BANNER_SIZE)

                    new_coords = (
                        int(tp_here_coords[0] - tp_here_size[0] / 2),
                        int(tp_here_coords[1] - tp_here_size[1])
                    )

                    bg.alpha_composite(tp_here_icon, new_coords)

                # Отображаем маяки.
                for marker in config.MARKERS.keys():
                    marker_icon = copy.deepcopy(self.pics["points"][config.MARKERS[marker]["color"]])

                    for marker_pos in config.MARKERS[marker]["points"].values():
                        bg.alpha_composite(marker_icon, self.rsz(
                            (marker_pos[0] - config.MARKER_SIZE[0] / 2, marker_pos[1] - config.MARKER_SIZE[1])))

                # Иконка самолета на карте.
                aircraft_icon = copy.deepcopy(self.pics["aircraft"]).rotate(self.aircraft.hdg())
                bg.alpha_composite(aircraft_icon, self.rsz(self.aircraft.position()))

                # Отображаем информацию о маяке.
                m_banner_coords = self.value("actMarkerCoords")
                if m_banner_coords:
                    m_banner_icon = copy.deepcopy(self.pics["markerInfoBanner"])
                    m_banner_size = config.MARKER_BANNER_SIZE

                    m_type = self.value("actMarkerType")
                    m_frq = self.value("actMarkerFrq")

                    new_coords = (
                        m_banner_coords[0] - m_banner_size[0] / 2,
                        m_banner_coords[1] - m_banner_size[1]
                    )

                    bg.alpha_composite(m_banner_icon, self.rsz(new_coords))

                    m_type_coords = (new_coords[0] + 10, new_coords[1] + 10)
                    m_type_icon = copy.deepcopy(self.pics["markers"][m_type])

                    bg.alpha_composite(m_type_icon, self.rsz(m_type_coords))

                    frq_measuring = {
                        "VOR": "МГц",
                        "DME": "МГц",
                        "VORDME": "МГц",
                        "DVORDME": "МГц",
                        "NDB": "кГц"
                    }

                    if m_type == "NDBDME":
                        m_desription = f"NDB: 995 КГц\nDME: 108.1 МГц"
                    else:
                        # if m_frq in ("108.4", "108.8"):
                        #     m_type = "DVORDME"

                        if m_type == "VORDME":
                            m_type_show = "VOR/DME"
                        elif m_type == "DVORDME":
                            m_type_show = "DVOR/DME"
                        else:
                            m_type_show = m_type

                        m_desription = f"{m_type_show}\n{m_frq} {frq_measuring[m_type]}"

                    m_text_coords = (new_coords[0] + 80, new_coords[1] + 10)
                    m_text = ImageDraw.Draw(bg)
                    m_text.text(self.rsz(m_text_coords), m_desription,
                                font=self.fonts["roboto"]["regular"], fill=(0, 0, 0))

            else:
                bg = copy.deepcopy(self.pics["bg"])

                # Мини карта.
                pos = aobjects.ObjectSize(x=self.aircraft.x, y=self.aircraft.y)
                crop_size = self.rsz((pos.x - 128, pos.y - 128)), self.rsz((pos.x + 128, pos.y + 128))

                map_ulsk = copy.deepcopy(self.pics["mapCleared"])
                map_height = self.pics["map"].height

                # Отображаем маяки.
                for marker in config.MARKERS.keys():
                    marker_icon = copy.deepcopy(self.pics["points"][config.MARKERS[marker]["color"]])

                    for marker_pos in config.MARKERS[marker]["points"].values():
                        map_ulsk.alpha_composite(marker_icon, self.rsz(
                            (marker_pos[0] - config.MARKER_SIZE[0] / 2, marker_pos[1] - config.MARKER_SIZE[1])))

                map_ulsk = map_ulsk.crop(
                    (crop_size[0][0], crop_size[0][1], crop_size[1][0], crop_size[1][1])
                )
                bg.alpha_composite(map_ulsk.resize(self.rsz((256, 256))), self.rsz((688, 689)))

                # Иконка самолета на мини-карте.
                aircraft_icon = copy.deepcopy(self.pics["aircraft"]).rotate(self.aircraft.hdg())
                bg.alpha_composite(aircraft_icon, self.rsz((771, 772)))

                # Надписи.
                boost_caption = ImageDraw.Draw(bg)
                boost_caption.text(self.rsz((1044, 841)), f"x{self.aircraft.boost}",
                                   font=self.fonts["roboto"]["medium"][26])

                # Кнопка развернуть карту.
                expend_icon = copy.deepcopy(self.pics["expandIcon"])
                bg.alpha_composite(expend_icon, self.rsz((890, 694)))

                # Указатели курса.
                hdg_icon_rotate = self.aircraft.get_heading()

                hdg_small_icon = copy.deepcopy(self.pics["headings"][0])

                bg.alpha_composite(hdg_small_icon.rotate(hdg_icon_rotate), self.rsz((722, 409)))
                bg.alpha_composite(hdg_small_icon.rotate(hdg_icon_rotate), self.rsz((1041, 436)))

                hdg_large_icon = copy.deepcopy(self.pics["headings"][1])
                bg.alpha_composite(hdg_large_icon.rotate(hdg_icon_rotate), self.rsz((127, 119)))
                bg.alpha_composite(hdg_large_icon.rotate(hdg_icon_rotate), self.rsz((1385, 119)))

                # Отображения панелей.
                boeing_panel_number = self.value(StorageCell.boeing_panel, default_value=1)
                if boeing_panel_number:
                    panel_icon = copy.deepcopy(self.pics["panel"]["boeing"][str(boeing_panel_number)])
                    bg.alpha_composite(panel_icon, self.rsz((11, 653)))

                airbus_panel_number = self.value(StorageCell.airbus_panel, default_value=1)
                if airbus_panel_number:
                    panel_icon = copy.deepcopy(self.pics["panel"]["airbus"][str(airbus_panel_number)])
                    bg.alpha_composite(panel_icon, self.rsz((1271.5, 652.5)))

                lvl_icon = copy.deepcopy(self.pics["switchers"]["level"]["normal"])
                lvl_icon_m = copy.deepcopy(self.pics["switchers"]["level"]["middle"]["small"])
                lvl_icon_mb = copy.deepcopy(self.pics["switchers"]["level"]["middle"]["big"])

                earrow_sg = copy.deepcopy(self.pics["arrows"]["single"]["green"])
                earrow_dg = copy.deepcopy(self.pics["arrows"]["double"]["green"])

                earrow_sb = copy.deepcopy(self.pics["arrows"]["single"]["blue"])
                earrow_db = copy.deepcopy(self.pics["arrows"]["double"]["blue"])

                barrow_s = copy.deepcopy(self.pics["arrow"]["single"])
                barrow_d = copy.deepcopy(self.pics["arrow"]["double"])

                # Панель Boeing.
                digital_lvl_value_1 = self.value(StorageCell.boeing_digital_level_1, default_value=False)
                digital_lvl_value_2 = self.value(StorageCell.boeing_digital_level_2, default_value=False)

                lvl_coords_1 = {
                    "adf": (720, 207),
                    "vor": (720, 176),
                    False: (720, 192)
                }
                lvl_coords_2 = {
                    "adf": (847, 207),
                    "vor": (847, 176),
                    False: (847, 192)
                }

                bg.alpha_composite(lvl_icon_mb, self.rsz(lvl_coords_1[digital_lvl_value_1]))
                bg.alpha_composite(lvl_icon_mb, self.rsz(lvl_coords_2[digital_lvl_value_2]))

                rb_big = copy.deepcopy(self.pics["rotate"]["big"])
                rb_medium = copy.deepcopy(self.pics["rotate"]["medium"])
                rb_small = copy.deepcopy(self.pics["rotate"]["small"])

                if boeing_panel_number == 1:
                    bg.alpha_composite(rb_big.rotate(self.value(StorageCell.boeing_rotate_1_big, default_value=0)),
                                       self.rsz((100, 840)))
                    bg.alpha_composite(
                        rb_medium.rotate(self.value(StorageCell.boeing_rotate_1_medium, default_value=0)),
                        self.rsz((100, 840)))
                    bg.alpha_composite(rb_small.rotate(self.value(StorageCell.boeing_rotate_1_small, default_value=0)),
                                       self.rsz((100, 840)))

                    bg.alpha_composite(rb_big.rotate(self.value(StorageCell.boeing_rotate_2_big, default_value=0)),
                                       self.rsz((570 - 180, 840)))
                    bg.alpha_composite(
                        rb_medium.rotate(self.value(StorageCell.boeing_rotate_2_medium, default_value=0)),
                        self.rsz((570 - 180, 840)))
                    bg.alpha_composite(rb_small.rotate(self.value(StorageCell.boeing_rotate_2_small, default_value=0)),
                                       self.rsz((570 - 180, 840)))

                    adf_1_frq = ImageDraw.Draw(bg)
                    adf_1_value = afuncs.fill_number_left_space(str(
                        round(self.value(StorageCell.boeing_adf_frq_1, default_value=self.boeing_adf_1_default), 1)
                    ))
                    adf_1_frq.text(self.rsz((112, 742)),
                                   adf_1_value,
                                   font=self.fonts["timer"][44], fill="#FFC92F")

                    adf_2_frq = ImageDraw.Draw(bg)
                    adf_2_value = afuncs.fill_number_left_space(str(
                        round(self.value(StorageCell.boeing_adf_frq_2, default_value=self.boeing_adf_2_default), 1)
                    ))
                    adf_2_frq.text(self.rsz((400, 742)),
                                   adf_2_value,
                                   font=self.fonts["timer"][44], fill="#FFC92F")

                else:
                    if boeing_panel_number == 2:
                        vor_act_name = StorageCell.boeing_vor_afrq_1
                        vor_stby_name = StorageCell.boeing_vor_sfrq_1

                        vor_act_default = self.boeing_vor_act_1_default
                        vor_stby_default = self.boeing_vor_stby_1_default
                    else:
                        vor_act_name = StorageCell.boeing_vor_afrq_2
                        vor_stby_name = StorageCell.boeing_vor_sfrq_2

                        vor_act_default = self.boeing_vor_act_2_default
                        vor_stby_default = self.boeing_vor_stby_2_default

                    vor_act_frq = ImageDraw.Draw(bg)
                    vor_act_value = afuncs.fill_number_dot(str(self.value(vor_act_name, default_value=vor_act_default)))
                    vor_act_frq.text(self.rsz((196, 808)), vor_act_value,
                                     font=self.fonts["timer"][38], fill="#FFC92F")

                    vor_stby_frq = ImageDraw.Draw(bg)
                    vor_stby_value = afuncs.fill_number_dot(
                        afuncs.fill_number_left_underline(
                            str(self.value(vor_stby_name, default_value=vor_stby_default))
                        ))
                    vor_stby_frq.text(self.rsz((196, 865)), vor_stby_value,
                                      font=self.fonts["timer"][38], fill="#FFC92F")

                # Переключатели ADF - VOR.
                sw_sg_icon = copy.deepcopy(self.pics["switchers"]["small"]["single"])
                sw_db_icon = copy.deepcopy(self.pics["switchers"]["small"]["double"])

                # Положения переключателей ADF - VOR.
                # 0 - VOR, 1 - ADF
                sw_1_pos = self.value(StorageCell.boeing_sw_1, default_value=0)
                sw_2_pos = self.value(StorageCell.boeing_sw_2, default_value=0)

                bg.alpha_composite(sw_sg_icon.rotate(-90 if sw_1_pos else 0), self.rsz((668, 540)))
                bg.alpha_composite(sw_db_icon.rotate(90 if sw_2_pos else 0), self.rsz((856, 540)))

                # Стрелки PFD и резервные.
                # Объект стрелки, картинка стрелки (зеленая - VOR, синяя - ADF)
                pointers = (
                    (self.boeing_dsg_arrow, (earrow_sg, earrow_sb), (124, 115), (40 + 50, 520), "1"),
                    (self.boeing_ddb_arrow, (earrow_dg, earrow_db), (124, 115), (620 - 114, 520), "2"),
                    (self.boeing_bsg_arrow, (barrow_s,), (732, 418), None),
                    (self.boeing_bdb_arrow, (barrow_d,), (732, 418), None)
                )
                for pointer in pointers:
                    pointer_obj = pointer[0]
                    if pointer_obj.is_active():
                        pointer_coords = pointer[2]
                        if pointer_obj.color == "blue":
                            pointer_icon = pointer[1][1].rotate(pointer_obj.get_angle())
                        elif pointer_obj.color in ("green", "backup"):
                            pointer_icon = pointer[1][0].rotate(pointer_obj.get_angle())
                        else:
                            continue

                        bg.alpha_composite(pointer_icon, self.rsz(pointer_coords))

                        if pointer_obj.color in ("blue", "green"):
                            arr_act_t = ImageDraw.Draw(bg)

                            if pointer_obj.color == "green":
                                # VOR - зеленый.
                                arr_dist = self.aircraft.distance_to_navaid(pointer_obj.frq, self.display, map_height)
                                arr_dist = arr_dist if arr_dist <= config.DME_MAX_DIST else None

                                arr_act_tv = f"VOR {pointer[4]}\n{pointer_obj.frq}"
                                if arr_dist:
                                    arr_act_tv += f"\nDME {arr_dist}"
                                clr_code = "#00FF00"
                            else:
                                # ADF - синий
                                arr_act_tv = f"ADF {pointer[4]}\n{pointer_obj.frq}"
                                clr_code = "#00FFFF"
                            arr_act_t.text(self.rsz(pointer[3]), arr_act_tv, font=self.fonts["roboto"]["medium"][22], fill=clr_code)

                # Панель Airbus.
                digital_lvl_value_1 = self.value(StorageCell.airbus_digital_level_1, default_value=False)
                digital_lvl_value_2 = self.value(StorageCell.airbus_digital_level_2, default_value=False)

                if digital_lvl_value_1 == "adf":
                    lvl_icon_1 = lvl_icon.rotate(90)
                elif digital_lvl_value_1 == "vor":
                    lvl_icon_1 = lvl_icon.rotate(-90)
                else:
                    lvl_icon_1 = lvl_icon_m

                bg.alpha_composite(lvl_icon_1, self.rsz((1010, 165)))

                if digital_lvl_value_2 == "adf":
                    lvl_icon_2 = lvl_icon.rotate(90)
                elif digital_lvl_value_2 == "vor":
                    lvl_icon_2 = lvl_icon.rotate(-90)
                else:
                    lvl_icon_2 = lvl_icon_m

                bg.alpha_composite(lvl_icon_2, self.rsz((1156, 165)))

                if airbus_panel_number == 1:
                    level_number = StorageCell.airbus_panel_1_level
                    vor_number = StorageCell.airbus_panel_1_vor
                    vor_able = self.value(vor_number, default_value=True)

                    rotate_angle_big = self.value(StorageCell.airbus_rotate_1_big, default_value=0)
                    rotate_angle_medium = self.value(StorageCell.airbus_rotate_1_medium, default_value=0)

                    vor_act_name = StorageCell.airbus_vor_afrq_1
                    vor_stby_name = StorageCell.airbus_vor_sfrq_1
                    adf_act_name = StorageCell.airbus_adf_afrq_1
                    adf_stby_name = StorageCell.airbus_adf_sfrq_1

                    vor_act_default = self.airbus_vor_1_act_default
                    vor_stby_default = self.airbus_vor_1_stby_default
                    adf_act_default = self.airbus_adf_1_act_default
                    adf_stby_default = self.airbus_adf_1_stby_default

                    if vor_able:
                        frq_act_name = vor_act_name
                        frq_stby_name = vor_stby_name

                        frq_act_default = vor_act_default
                        frq_stby_default = vor_stby_default
                    else:
                        frq_act_name = adf_act_name
                        frq_stby_name = adf_stby_name

                        frq_act_default = adf_act_default
                        frq_stby_default = adf_stby_default
                else:
                    level_number = StorageCell.airbus_panel_2_level
                    vor_number = StorageCell.airbus_panel_2_vor
                    vor_able = self.value(vor_number, default_value=True)

                    rotate_angle_big = self.value(StorageCell.airbus_rotate_2_big, default_value=0)
                    rotate_angle_medium = self.value(StorageCell.airbus_rotate_2_medium, default_value=0)

                    vor_act_name = StorageCell.airbus_vor_afrq_2
                    vor_stby_name = StorageCell.airbus_vor_sfrq_2
                    adf_act_name = StorageCell.airbus_adf_afrq_2
                    adf_stby_name = StorageCell.airbus_adf_sfrq_2

                    vor_act_default = self.airbus_vor_2_act_default
                    vor_stby_default = self.airbus_vor_2_stby_default
                    adf_act_default = self.airbus_adf_2_act_default
                    adf_stby_default = self.airbus_adf_2_stby_default

                    if vor_able:
                        frq_act_name = vor_act_name
                        frq_stby_name = vor_stby_name

                        frq_act_default = vor_act_default
                        frq_stby_default = vor_stby_default
                    else:
                        frq_act_name = adf_act_name
                        frq_stby_name = adf_stby_name

                        frq_act_default = adf_act_default
                        frq_stby_default = adf_stby_default

                level_value = self.value(level_number, default_value=False)

                lvl_icon_1 = lvl_icon.rotate(0 if level_value else 180)
                bg.alpha_composite(lvl_icon_1, self.rsz((1792, 964)))

                green_ind_icon = copy.deepcopy(self.pics["panel"]["indicator"])
                if level_value:
                    bg.alpha_composite(green_ind_icon, self.rsz((1296, 1028)))

                    if vor_able:
                        bg.alpha_composite(green_ind_icon, self.rsz((1405, 983)))
                    else:
                        bg.alpha_composite(green_ind_icon, self.rsz((1628, 1013)))

                rb_big_mini = copy.deepcopy(self.pics["rotate"]["miniBig"])
                rb_medium_mini = copy.deepcopy(self.pics["rotate"]["miniMedium"])

                bg.alpha_composite(rb_big_mini.rotate(rotate_angle_big), self.rsz((1630, 826)))
                bg.alpha_composite(rb_medium_mini.rotate(rotate_angle_medium), self.rsz((1630, 826)))

                if level_value:
                    act_frq = ImageDraw.Draw(bg)
                    frq_act_value = afuncs.fill_number_left_space(afuncs.fill_number_right_zero(
                        str(self.value(frq_act_name, default_value=frq_act_default)),
                        length=2 if vor_able else 1
                    ))
                    act_frq.text(self.rsz((1365, 744)), frq_act_value,
                                 font=self.fonts["timer"][44], fill="#FFC92F")

                    stby_frq = ImageDraw.Draw(bg)
                    frq_stby_value = afuncs.fill_number_left_space(afuncs.fill_number_right_zero(
                        str(self.value(frq_stby_name, default_value=frq_stby_default)),
                        length=2 if vor_able else 1
                    ))
                    stby_frq.text(self.rsz((1652, 744)), frq_stby_value,
                                  font=self.fonts["timer"][44], fill="#FFC92F")

                # Установленные частоты.
                vor_frq_1 = self.value(StorageCell.airbus_vor_afrq_1)
                vor_frq_2 = self.value(StorageCell.airbus_vor_afrq_2)
                adf_frq_1 = self.value(StorageCell.airbus_adf_afrq_1)
                adf_frq_2 = self.value(StorageCell.airbus_adf_afrq_2)

                if self.value(StorageCell.airbus_sw_1, default_value=0) == 0:
                    dme_dist_1 = self.aircraft.distance_to_navaid(vor_frq_1, self.display, map_height)
                    dme_dist_1 = dme_dist_1 if dme_dist_1 <= config.DME_MAX_DIST else None
                else:
                    dme_dist_1 = None

                if self.value(StorageCell.airbus_sw_2, default_value=0) == 0:
                    dme_dist_2 = self.aircraft.distance_to_navaid(vor_frq_2, self.display, map_height)
                    dme_dist_2 = dme_dist_2 if dme_dist_2 <= config.DME_MAX_DIST else None
                else:
                    dme_dist_2 = None

                # Стрелки PFD и резервные.
                # Объект стрелки, картинка стрелки (зеленная - VOR, синяя - ADF)
                pointers = (
                    (self.airbus_dsg_arrow, (earrow_sg, earrow_sb), (1382, 115), (1302 + 50, 520), "1"),
                    (self.airbus_ddb_arrow, (earrow_dg, earrow_db), (1382, 115), (1875 - 114, 520), "2"),
                    (self.airbus_bsg_arrow, (barrow_s,), (1052, 444)),
                    (self.airbus_bdb_arrow, (barrow_d,), (1052, 444))
                )
                for pointer in pointers:
                    pointer_obj = pointer[0]
                    if pointer_obj.is_active():
                        pointer_coords = pointer[2]
                        if pointer_obj.color == "blue":
                            pointer_icon = pointer[1][1].rotate(pointer_obj.get_angle())
                        elif pointer_obj.color in ("green", "backup"):
                            pointer_icon = pointer[1][0].rotate(pointer_obj.get_angle())
                        else:
                            continue

                        bg.alpha_composite(pointer_icon, self.rsz(pointer_coords))

                        if pointer_obj.color in ("blue", "green"):
                            arr_act_t = ImageDraw.Draw(bg)

                            if pointer_obj.color == "green":
                                # VOR - зеленый.
                                arr_dist = self.aircraft.distance_to_navaid(pointer_obj.frq, self.display, map_height)
                                arr_dist = arr_dist if arr_dist <= config.DME_MAX_DIST else None

                                arr_act_tv = f"VOR {pointer[4]}\n{pointer_obj.frq}"
                                if arr_dist:
                                    arr_act_tv += f"\nDME {arr_dist}"
                                clr_code = "#00FF00"
                            else:
                                # ADF - синий
                                arr_act_tv = f"ADF {pointer[4]}\n{pointer_obj.frq}"
                                clr_code = "#00FFFF"
                            arr_act_t.text(self.rsz(pointer[3]), arr_act_tv, font=self.fonts["roboto"]["medium"][22], fill=clr_code)

                # Дистанция DME.
                distance_1 = ImageDraw.Draw(bg)
                dme_distance_1 = str(dme_dist_1) if dme_dist_1 else "---.-"
                distance_1.text(self.rsz((1024, 380)),
                                text=afuncs.fill_number_left_space(dme_distance_1, length=4),
                                font=self.fonts["timer"][26])

                distance_2 = ImageDraw.Draw(bg)
                dme_distance_2 = str(dme_dist_2) if dme_dist_2 else "---.-"
                distance_2.text(self.rsz((1139, 380)),
                                text=afuncs.fill_number_left_space(dme_distance_2, length=4),
                                font=self.fonts["timer"][26])

                # Переключатели ADF - VOR.
                sw_n_icon = copy.deepcopy(self.pics["switchers"]["small"]["normal"])

                # Положения переключателей ADF - VOR.
                # 0 - VOR, 1 - ADF
                sw_1_pos = self.value(StorageCell.airbus_sw_1, default_value=0)
                sw_2_pos = self.value(StorageCell.airbus_sw_2, default_value=0)

                bg.alpha_composite(sw_n_icon.rotate(-90 if sw_1_pos else 0), self.rsz((990, 564)))
                bg.alpha_composite(sw_n_icon.rotate(90 if sw_2_pos else 0), self.rsz((1186, 564)))

                # Отображаем верхний слой статичных объектов.
                bg_upper = copy.deepcopy(self.pics["bgUpper"])

                boeing_hdg_caption = ImageDraw.Draw(bg_upper)
                hdg_formated = afuncs.fill_number_left_zero(
                    str(afuncs.format_degrees(round(self.aircraft.get_heading()))))
                boeing_hdg_caption.text(self.rsz((310, 110)),
                                        text=hdg_formated,
                                        font=self.fonts["roboto"]["medium"][22])

                bg.alpha_composite(bg_upper, (0, 0))

            bg_photo = ImageTk.PhotoImage(bg)
            self.panel.configure(image=bg_photo)
            self.panel.image = bg_photo

            time.sleep(0.05)
