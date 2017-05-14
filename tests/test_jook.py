import json
import xml.etree.ElementTree as Et

import pytest
import responses

import jook
from jook.exceptions import InvalidEvent, InvalidURL


def test_url_scheme_required():
    with pytest.raises(InvalidURL):
        jook.Computer('localhost', 'ComputerAdded')


def test_valid_events():
    for event in jook.Computer.valid_events:
        jook.Computer('http://localhost', event)

    with pytest.raises(InvalidEvent):
        jook.Computer('http://localhost', 'SomeEvent')


def test_static_data():
    comp = jook.Computer('http://localhost', 'ComputerAdded')
    assert comp._data is not None
    assert comp.get_data() == comp.get_data()


def test_random_data():
    comp = jook.Computer('http://localhost', 'ComputerAdded', randomize=True)
    assert comp._data is None
    assert comp.get_data() != comp.get_data()


def test_mode():
    comp = jook.Computer('http://localhost', 'ComputerAdded')
    json.loads(comp.to_json())
    Et.fromstring(comp.to_xml())

