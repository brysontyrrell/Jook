"""Classes and objects to hold sets of data for webhook events."""
from collections import namedtuple

from ..exceptions import InvalidDeviceType
from ..identifiers import generate_mac_address, generate_serial, generate_uuid


class DeviceData(object):
    """An object representing device identifiers for computer and monbile
    device webhooks.
    """
    def __init__(self, device_type='computer', mac_address=None,
                 mac_address_alt=None, serial_number=None, uuid=None,
                 randomize=False):
        if device_type in ('computer', 'mobile'):
            self.mode = device_type
        else:
            raise InvalidDeviceType("Must be 'computer' or 'mobile'")

        if not randomize:
            self.set_mac_address()
            self.set_mac_address_alt()
            self.set_serial_number(self.mode)
            self.set_uuid()
        else:
            self._mac_address = mac_address
            self._mac_address_alt = mac_address_alt
            self._serial_number = serial_number
            self._uuid = uuid

    @property
    def mac_address(self):
        return self._mac_address if self._mac_address else \
            generate_mac_address()

    def set_mac_address(self, mac_address=None):
        self._mac_address = mac_address if mac_address else \
            generate_mac_address()

    @property
    def mac_address_alt(self):
        return self._mac_address_alt if self._mac_address_alt else \
            generate_mac_address()

    def set_mac_address_alt(self, mac_address=None):
        self._mac_address_alt = mac_address if mac_address else \
            generate_mac_address()

    @property
    def serial_number(self):
        return self._serial_number if self._serial_number else \
            generate_serial(self.mode)

    def set_serial_number(self, serial_number=None):
        self._serial_number = serial_number if serial_number else \
            generate_serial(self.mode)

    @property
    def uuid(self):
        return self._uuid if self._uuid else generate_uuid()

    def set_uuid(self, uuid=None):
        self._uuid = uuid if uuid else generate_uuid()


LocationData = namedtuple('Location', (
        'username', 'realname', 'email', 'phone',
        'position', 'department', 'building', 'room'
))

LocationData.__new__.__defaults__ = ('',) * len(LocationData._fields)
