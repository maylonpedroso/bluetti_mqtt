from typing import List
from ..commands import ReadHoldingRegisters
from .bluetti_device import BluettiDevice
from .struct import DeviceStruct


class AC2A(BluettiDevice):
    def __init__(self, address: str, sn: str):
        self.struct = DeviceStruct()

        # Core device properties
        self.struct.add_uint_field('total_battery_percent', 102)
        self.struct.add_swap_string_field('device_type', 110, 6)
        self.struct.add_sn_field('serial_number', 116)
        self.struct.add_decimal_field('power_generation', 154, 1)

        # AC/DC output on/off states found in bit 3/4
        # self.struct.add_uint_field('ac_output_on', 1131) # bit 3
        # self.struct.add_uint_field('dc_output_on', 1131) # bit 4

        # Input power
        self.struct.add_uint_field('dc_input_power', 1200)
        self.struct.add_uint_field('ac_input_power', 1313)

        # Output power
        self.struct.add_uint_field('dc_output_power', 1400)
        self.struct.add_uint_field('ac_output_power', 1420)

        # ac_output_power_on is the electrical relay (delay of ~1s to ac_output_on)
        # self.struct.add_bool_field('ac_output_power_on', 1509)
        # self.struct.add_uint_field('ac_output_power', 1510)

        # Output buttons
        self.struct.add_bool_field('dc_output_on', 2012)
        self.struct.add_bool_field('ac_output_on', 2011)

        super().__init__(address, "AC2A", sn)

    @property
    def logging_commands(self) -> List[ReadHoldingRegisters]:
        return [
            ReadHoldingRegisters(100, 62),  # Device info
            # ReadHoldingRegisters(1100, 51),  # AC/DC output on/off
            ReadHoldingRegisters(1200, 90),  # DC input power
            ReadHoldingRegisters(1300, 31),  # AC input power

            ReadHoldingRegisters(1400, 48),  # AC/DC output power

            # ReadHoldingRegisters(1500, 30),  # AC output power and on/of

            ReadHoldingRegisters(2000, 67),  # DC output on/off

            # ReadHoldingRegisters(2200, 29),
            # ReadHoldingRegisters(6000, 31),
            # ReadHoldingRegisters(6100, 100),
            # ReadHoldingRegisters(6300, 52),
        ]
