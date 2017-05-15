"""
This module contains functions for generating unique identifiers for objects.
"""

import random
import uuid

from .exceptions import InvalidMode

MOBILE_SERIAL_CHARACTER_SETS = [
    ['F', 'D', 'C', 'H'],
    ['4', 'L', 'Q', '7', 'M', '3', 'K', 'N', '2', '9', '5', 'C', '8', '1', 'X', 'Y', '6', '0', 'J', 'F', 'T', 'G', 'D',
     'A', 'P', 'R'],
    ['L', 'X', 'T', '8', 'Q', '9', 'K', 'V', 'P', '7', 'R', 'J', 'F', '6', 'G', 'N', '3', 'M', '5', 'Y', 'W', '4', '1',
     'H', '2', 'C', 'D'],
    ['K', 'M', 'L', 'J', 'H', 'G', 'N', 'F', '3', 'P', 'B', 'Q', 'R', 'S', 'A'],
    ['H', '6', '4', 'C', 'G', 'V', 'J', '5', 'T', 'R', 'N', 'K', 'X', '1', 'F', 'L', '9', 'Q', '8', 'W', 'M', '2', 'P',
     'D', '7', '3', 'Y', 'A'],
    ['J', '1', '2', '8', 'B', 'W', '0', 'C', '4', '7', 'F', '5', '6', 'M', '3', 'G', 'A', 'E', 'Q', 'S', 'N', 'R', 'D',
     'Z', 'X', '9', 'P', 'K', 'V', 'Y', 'H', 'U', 'T', 'L'],
    ['3', '2', 'S', 'Y', 'V', 'R', 'M', 'Q', 'F', 'J', '1', '8', '9', 'L', '6', 'H', 'W', 'A', '4', '0', 'E', 'T', 'U',
     '5', 'N', '7', 'X', 'Z', 'K', 'G', 'B', 'D', 'C', 'P'],
    ['V', '7', 'Z', 'R', 'P', 'C', 'G', '8', 'A', '2', 'J', 'X', 'Q', '4', 'D', 'E', 'N', 'B', '9', '0', 'H', 'K', 'Y',
     '3', '6', '1', 'L', 'T', '5', 'M', 'W', 'F', 'U', 'S'],
    ['F', 'D', 'G', '9', '7', 'H', '1'],
    ['1', 'C', 'N', 'K', 'F', 'J', '8', 'R', 'T', '2', 'P', 'V', '3', 'L', '4', 'H', '5', '0', '6', 'D', 'M', 'X', '9',
     'G'],
    ['9', 'M', 'D', '1', 'J', 'H', '8', 'C', '2', 'F', 'P', 'G', 'W', 'T', 'Y', '5', 'R', 'Q', '7', '3', 'V', 'N', 'K',
     'X', 'L', '6', '0'],
    ['6', '5', 'K', '4', 'J', 'W', 'T', '2', '0', 'V', 'M', 'Y', '9', 'N', '8', '3', '1', 'H', 'Q', 'L', 'D', 'R', '7',
     'P', 'G', 'C', 'F', 'X'],
    ]

COMPUTER_SERIAL_CHARACTER_SETS = [
        ['C'],
        ['0', '2', '1', 'P'],
        ['7', '2', 'V', 'M', 'W', 'F', 'Q', 'X'],
        ['K', 'L', 'F', 'G', 'M', 'N', 'J', 'H', 'D', 'P', 'Q', 'R', 'S'],
        ['8', 'G', '5', '7', 'L', 'T', 'M', '2', 'P', '9', 'X', '4', 'K', 'J', 'D', 'W', 'C', 'H', 'F', 'Q', 'V', 'N',
         'R', '3', '6', '1', 'Y'],
        ['1', '9', '0', '7', '5', '2', '6', 'B', 'A', 'P', '4', 'E', '3', 'K', 'F', 'R', 'G', 'U', 'W', 'C', 'L', 'V',
         '8', 'J', 'D', 'T', 'X', 'Y', 'M', 'Z', 'N', 'S', 'H'],
        ['9', 'U', '2', 'S', 'Q', 'H', 'M', 'V', 'Z', 'J', 'G', 'P', 'D', 'N', '5', 'Y', 'X', '7', '3', 'E', '6', '0',
         'K', 'T', '4', 'L', 'C', 'F', '8', 'A', 'B', 'W', '1', 'R'],
        ['4', 'E', 'N', 'C', 'Y', 'H', 'F', 'A', 'G', '1', 'B', '3', '0', '5', '8', 'M', 'J', 'W', 'L', 'T', 'S', 'D',
         'V', 'P', 'R', 'K', 'U', '6', 'Z', '2', 'Q', '7', '9', 'X'],
        ['D', 'F', 'G', 'H'],
        ['Y', '6', 'D', 'R', 'H', '5', 'W', 'G', 'F', '0', '8', 'T', 'K', 'V', 'L', '2', 'N', '3', 'J', '9', '1', 'C',
         'Q'],
        ['3', 'T', 'Q', '0', 'Y', 'P', '5', 'V', 'R', '8', '4', '2', 'J', '7', '1', 'C', 'M', 'H', 'N', 'D', 'F', '6',
         'G', 'W'],
        ['H', '6', 'X', '4', '5', 'W', 'L', 'J', '8', 'G', '3', 'P', '7', 'T', 'N', '9', '1', 'F', 'M', 'V', '0', 'D',
         'R', 'K', '2', 'C', 'Y']
    ]

SERIAL_CHAR_SETS = {
    'computer': COMPUTER_SERIAL_CHARACTER_SETS,
    'mobile': MOBILE_SERIAL_CHARACTER_SETS
}


def generate_mac_address():
    """Generate a mock MAC address for a device."""
    return "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def generate_serial(mode):
    """Generate a mock serial number for a device.

    :param str mode:
        Serial number to return.

        Accepted values:
           * computer
           * mobile

    :return: Serial number
    :rtype: str
    """
    try:
        char_set = SERIAL_CHAR_SETS[mode]
    except KeyError as err:
        raise InvalidMode(err.message)

    return ''.join([random.choice(char_set[i]) for i in range(12)])


def generate_uuid():
    """Return a UUID value as a string"""
    return str(uuid.uuid4()).upper()
