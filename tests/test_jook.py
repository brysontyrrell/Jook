import json
import xml.etree.ElementTree as Et

import pytest
import responses

import jook
from jook.models.webhooks import BaseWebhook
from jook.exceptions import InvalidEvent, InvalidURL


URL = 'http://localhost'


def test_url_scheme_required():
    with pytest.raises(InvalidURL):
        BaseWebhook('localhost', '')


def test_events():
    events = (
        jook.Computer,
        jook.MobileDevice,
        jook.JamfPro
    )

    for event in events:
        for valid_event in event.valid_events:
            assert event(URL, valid_event)

        with pytest.raises(InvalidEvent):
            event(URL, 'InvalidEvent')


def test_event_required():
    events = (
        jook.Computer,
        jook.MobileDevice,
        jook.JamfPro
    )

    with pytest.raises(TypeError):
        for event in events:
            event(URL)


def test_event_not_required():
    events = (
        jook.PatchTitle,
    )

    for event in events:
        assert event(URL)


def test_static_device_data():
    computer = jook.Computer(URL, 'ComputerAdded')
    assert computer.data == computer.data

    mobile = jook.MobileDevice(URL, 'MobileDeviceCheckIn')
    assert mobile.data == mobile.data


def test_random_device_data():
    computer = jook.Computer(URL, 'ComputerCheckIn', randomize=True)
    assert computer.data != computer.data

    mobile = jook.MobileDevice(
        URL, 'MobileDeviceCommandCompleted', randomize=True)
    assert mobile.data != mobile.data


def test_data_modes():
    events = (
        jook.Computer(URL, 'ComputerInventoryCompleted'),
        jook.MobileDevice(URL, 'MobileDeviceEnrolled'),
        jook.JamfPro(URL, 'JSSShutdown'),
        jook.PatchTitle(URL)
    )

    for event in events:
        assert json.loads(event.to_json())
        assert Et.fromstring(event.to_xml())
