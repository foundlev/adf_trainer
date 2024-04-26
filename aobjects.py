from typing import NamedTuple


class StorageCell:
    airbus_panel = "airbusPanel"
    boeing_panel = "boeingPanel"
    # Панель Boeing.
    boeing_digital_level_1 = "boeingDigitalLevel1"
    boeing_digital_level_2 = "boeingDigitalLevel2"
    # Вращение селекторов.
    boeing_rotate_1_big = "boeingRotate1Big"
    boeing_rotate_1_medium = "boeingRotate1Medium"
    boeing_rotate_1_small = "boeingRotate1Small"
    boeing_rotate_2_big = "boeingRotate2Big"
    boeing_rotate_2_medium = "boeingRotate2Medium"
    boeing_rotate_2_small = "boeingRotate2Small"
    # Переключатели.
    boeing_sw_1 = "boeingSwitcher1"
    boeing_sw_2 = "boeingSwitcher2"
    # Частоты.
    boeing_adf_frq_1 = "boeingAdfFrq1"
    boeing_adf_frq_2 = "boeingAdfFrq2"
    boeing_vor_afrq_1 = "boeingVorAfrq1"
    boeing_vor_afrq_2 = "boeingVorAfrq2"
    boeing_vor_sfrq_1 = "boeingVorSfrq1"
    boeing_vor_sfrq_2 = "boeingVorSfrq2"
    # Панель Airbus.
    airbus_digital_level_1 = "airbusDigitalLevel1"
    airbus_digital_level_2 = "airbusDigitalLevel2"
    airbus_backup_level_1 = "airbusBackupLevel1"
    airbus_backup_level_2 = "airbusBackupLevel2"
    airbus_panel_1_level = "airbusPanel1Level"
    airbus_panel_2_level = "airbusPanel2Level"
    airbus_panel_1_vor = "airbusPanel1Vor"
    airbus_panel_2_vor = "airbusPanel2Vor"
    # Вращение селекторов.
    airbus_rotate_1_big = "airbusRotate1Big"
    airbus_rotate_1_medium = "airbusRotate1Medium"
    airbus_rotate_2_big = "airbusRotate2Big"
    airbus_rotate_2_medium = "airbusRotate2Medium"
    # Переключатели.
    airbus_sw_1 = "airbusSwitcher1"
    airbus_sw_2 = "airbusSwitcher2"
    # Частоты.
    airbus_adf_afrq_1 = "airbusAdfAfrq1"
    airbus_adf_sfrq_1 = "airbusAdfSfrq1"
    airbus_vor_afrq_1 = "airbusVorAfrq1"
    airbus_vor_sfrq_1 = "airbusVorSfrq1"
    airbus_adf_afrq_2 = "airbusAdfAfrq2"
    airbus_adf_sfrq_2 = "airbusAdfSfrq2"
    airbus_vor_afrq_2 = "airbusVorAfrq2"
    airbus_vor_sfrq_2 = "airbusVorSfrq2"


class NavaidTypes:
    vordme_dme = ["VORDME", "DME", "NDBDME"]
    vordme_ndb_ndbdme = ["VORDME", "NDB", "NDBDME"]


class ObjectSize(NamedTuple):
    x: int | float
    y: int | float

    def to_tuple(self) -> tuple:
        return self.x, self.y


class ChangeBoostType:
    up = 1
    down = 2
