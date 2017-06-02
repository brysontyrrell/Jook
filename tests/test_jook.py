import json
import xml.etree.ElementTree as Et

import pytest
import responses

import jook
from jook.exceptions import InvalidEvent, InvalidURL


URL = 'http://localhost'


def test_url_scheme_required():
    with pytest.raises(InvalidURL):
        jook.Computer('localhost', 'ComputerAdded')


def test_valid_events():
    for event in jook.Computer.valid_events:
        jook.Computer(URL, event)

    for event in jook.MobileDevice.valid_events:
        jook.MobileDevice(URL, event)

    for event in jook.JamfPro.valid_events:
        jook.JamfPro(URL, event)

    with pytest.raises(InvalidEvent):
        jook.Computer(URL, 'SomeEvent')
        jook.MobileDevice(URL, 'SomeEvent')
        jook.JamfPro(URL, 'SomeEvent')


def test_static_data():
    computer = jook.Computer(URL, 'ComputerAdded')
    assert computer.data == computer.data

    mobile = jook.MobileDevice(URL, 'MobileDeviceCheckIn')
    assert mobile.data == mobile.data


def test_random_data():
    computer = jook.Computer(URL, 'ComputerAdded', randomize=True)
    assert computer.data != computer.data

    mobile = jook.MobileDevice(URL, 'MobileDeviceCheckIn', randomize=True)
    assert mobile.data != mobile.data


def test_data_modes():
    events = (
        jook.Computer(URL, 'ComputerAdded'),
        jook.MobileDevice(URL, 'MobileDeviceCheckIn'),
        jook.JamfPro(URL, 'JSSShutdown')
    )

    for event in events:
        json.loads(event.to_json())
        Et.fromstring(event.to_xml())
