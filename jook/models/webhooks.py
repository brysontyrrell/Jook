"""
This module contains the main classes that will be interacted with directly.
"""

import json
import time
from urlparse import urlparse

from dicttoxml import dicttoxml
import requests

from .data_sets import DeviceData, LocationData
from ..exceptions import InvalidDeviceType, InvalidEvent, InvalidMode, InvalidURL


class Jook(object):
    """The Jook class is an object for managing and creating large numbers of
    webhook objects and firing them as a group.
    """
    def __init__(self, url, fire_mode):
        pass


class BaseWebhook(object):
    """The base webhook object.

    Contains all shared methods used by child objects.
    """
    valid_events = ('',)

    def __init__(self, url, event, webhook_id=1, webhook_name='', mode='json',
                 randomize=False, timer=0, *args, **kwargs):
        """
        :param str url: The target URL (must contain the scheme)

        :param str event: The type of webhook event. The available event types
            are defined in the ``valid_event`` attribute for the object.

        :param str mode: The type of data to send when calling
            :func:`fire() <jook.models.BaseWebhook.fire>`.

            Can only be 'json' or 'xml'

        :param bool randomize: Values for the webhook object's ``data`` are
            randomly generated every time when set to ``True``.

            If ``False`` certain values are generated during the object's
            creation and stored. These values will be the same each time
            :func:`fire() <jook.models.BaseWebhook.fire>` is called.

            If ``True`` those values will be set to ``None`` and generated
            at the time :func:`fire() <jook.models.BaseWebhook.fire>` is called.

        :param int timer: An optional value in seconds to specify the delay when
            using :func:`start_timer() <jook.models.BaseWebhook.start_timer>`.

        :param int webhook_id: An optional ID value for the webhook event.

        :param str webhook_name: An optional name for the webhook event.

        :raises InvalidEvent:
        :raises: InvalidMode
        :raises InvalidURL:
        :raises TypeError:
        """
        if not url or not urlparse(url).scheme:
            raise InvalidURL(
                "Must contain a scheme (e.g. 'http://', 'https://')."
            )
        else:
            self.url = url

        if event not in self.valid_events:
            raise InvalidEvent(
                'Must be one of: {}'.format(', '.join(self.valid_events))
            )
        else:
            self.event = event

        self.id = int(webhook_id)
        self.name = webhook_name
        self.random = randomize

        if mode in ('json', 'xml'):
            self.mode = mode
        else:
            raise InvalidMode("Must be 'json' or 'xml'")

        self.timer = int(timer)

    @property
    def data(self):
        """This method generates the object data in JSON or XML format which is
        set by the ``data_type`` attributes.

        This method should be overridden by children that inherit this object.
        """
        return {}

    def to_json(self):
        """
        Return the object's ``data`` as JSON.

        :param dict data: ``data`` as a dictionary object

        :return: JSON string
        :rtype: str
        """
        return json.dumps(self.data)

    def to_xml(self):
        """Return the object's ``data`` as XML.

        :return: XML string
        :rtype: str
        """
        return dicttoxml(
            self.data,
            custom_root='JSSEvent',
            attr_type=False
        )

    def fire(self):
        """Send a POST request containing the object's data in the specified
        data type to the stored URL.
        """
        headers = {
            'Content-Type': (
                'application/json'
                if self.mode == 'json'
                else 'text/xml'
            )
        }

        data = self.to_json() if self.mode == 'json' else self.to_xml()

        request = requests.post(self.url, headers=headers, data=data)

        if not request.ok:
            request.raise_for_status()

    def start_timer(self, repeat=1):
        """Start a series of :method: ``fire`` calls delayed by the  value of
        ``timer`` in seconds for the number of times specified by ``repeat``.

        :param int repeat: Number of times to execute :method: ``fire``
        """
        for x in range(repeat):
            self.fire()
            time.sleep(self.timer)


class BaseDevice(BaseWebhook):
    """Base class for computer and mobile device webhooks."""
    device_type = ''

    def __init__(self, *args, **kwargs):
        """If ``randomize`` has been set to ``True`` and a :class:`DeviceData`
        object has not been passed, the instatiated :class:`DeviceData` object
        will be created with the ``randomized`` argument set.

        :param DeviceData device:
        :param LocationData location:
        """
        super(BaseDevice, self).__init__(*args, **kwargs)

        device = kwargs.pop('device', None)
        location = kwargs.pop('location', None)

        if device and isinstance(device, DeviceData):
            self.device = device
        else:
            self.device = DeviceData(
                device_type=self.device_type, randomize=self.random
            )

        if location and isinstance(location, LocationData):
            self.location = location
        else:
            self.location = LocationData()


class Computer(BaseDevice):
    """The base BaseWebhook object for 'Computer' events."""
    device_type = 'computer'

    valid_events = (
        'ComputerAdded',
        'ComputerCheckIn',
        'ComputerInventoryCompleted',
        'ComputerPolicyFinished',
        'ComputerPushCapabilityChanged'
    )

    @property
    def data(self):
        """Return ``data`` for the object as a dictionary.

        :return: ``data`` as a dictionary object
        :rtype: str
        """
        return {
            "webhook": {
                "id": self.id,
                "name": self.name,
                "webhookEvent": self.event
            },
            "event": {
                "udid": self.device.uuid,
                "deviceName": "",
                "model": "",
                "macAddress": self.device.mac_address,
                "alternateMacAddress": self.device.mac_address_alt,
                "serialNumber": self.device.serial_number,
                "osVersion": "",
                "osBuild": "",
                "userDirectoryID": "-1",
                "username": "{}".format(self.location.username),
                "realName": "{}".format(self.location.realname),
                "emailAddress": "{}".format(self.location.email),
                "phone": "".format(self.location.phone),
                "position": "{}".format(self.location.position),
                "department": "{}".format(self.location.department),
                "building": "{}".format(self.location.building),
                "room": "{}".format(self.location.room),
                "jssID": 1
            }
        }


class MobileDevice(BaseDevice):
    """The base Webhook object for 'Mobile Device' events."""
    device_type = 'mobile'

    valid_events = (
        'MobileDeviceCheckIn',
        'MobileDeviceCommandCompleted',
        'MobileDeviceEnrolled',
        'MobileDevicePushSent',
        'MobileDeviceUnEnrolled'
    )

    @property
    def data(self):
        """Return ``data`` for the object as a dictionary.

        :return: ``data`` as a dictionary object
        :rtype: str
        """
        return {
            "webhook": {
                "id": self.id,
                "name": self.name,
                "webhookEvent": self.event
            },
            "event": {
                "udid": self.device.uuid,
                "deviceName": "",
                "version": "",
                "model": "",
                "bluetoothMacAddress": self.device.mac_address_alt,
                "wifiMacAddress": self.device.mac_address,
                "imei": "",
                "icciID": "",
                "product": "",
                "serialNumber": self.device.serial_number,
                "userDirectoryID": "-1",
                "room": self.location.room,
                "osVersion": "",
                "osBuild": "",
                "modelDisplay": "",
                "username": self.location.username,
                "jssID": 1
            }
        }