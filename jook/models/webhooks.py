"""
This module contains the main classes that will be interacted with directly.
"""
import datetime
import json
import time
from urlparse import urlparse

from dicttoxml import dicttoxml
import requests

from .data_sets import DeviceData, LocationData
from ..exceptions import InvalidEvent, InvalidMode, InvalidURL


class Jook(object):
    """The Jook class is an object for managing and creating large numbers of
    webhook objects and firing them as a group.

    NOT IMPLEMENTED
    """
    def __init__(self):
        pass


class BaseWebhook(object):
    """The base webhook object.

    Contains all shared methods used by child objects.
    """
    valid_events = ('',)

    def __init__(self, url, event, webhook_id=1, webhook_name='Webhook',
                 mode='json', randomize=False, timer=0, *args, **kwargs):
        """
        :param str url: The target URL (must contain the scheme)

        :param str event: The type of webhook event. The available event types
            are defined in the ``valid_event`` attribute for the object.

        :param str mode: The type of data to send when calling
            :func:`fire() <jook.models.webhooks.BaseWebhook.fire>`.

            Can only be 'json' or 'xml'

        :param bool randomize: Values for the webhook object's ``data`` are
            randomly generated every time when set to ``True``.

            If ``False`` certain values are generated during the object's
            creation and stored. These values will be the same each time
            :func:`fire() <jook.models.webhooks.BaseWebhook.fire>` is called.

            If ``True`` those values will be set to ``None`` and generated
            at the time :func:`fire() <jook.models.webhooks.BaseWebhook.fire>`
            is called.

        :param int timer: An optional value in seconds to specify the delay when
            using :func:`start_timer()
            <jook.models.webhooks.BaseWebhook.start_timer>`.

        :param int webhook_id: An optional ID value for the webhook event.

        :param str webhook_name: An optional name for the webhook event.

        :raises InvalidEvent:
        :raises InvalidMode:
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

        self._webhook_data = {
            "webhook": {
                "id": self.id,
                "name": self.name,
                "webhookEvent": self.event
            }
        }

    @property
    def data(self):
        """This method generates the object data in JSON or XML format which is
        set by the ``data_type`` attributes.

        This method should be overridden by children that inherit this object.
        
        The ``data`` object contains the event specific key-values. It is then
        updated with the key-values from ``_base_data``.
        """
        data = {"event": {}}
        data.update(self._webhook_data)
        return data

    def to_json(self):
        """
        Return the object's ``data`` as JSON.

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
        object has not been passed, the instantiated :class:`DeviceData` object
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
        :rtype: dict
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
        :rtype: dict
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


class JamfPro(BaseWebhook):
    """The base Webhook object for 'JSS' events."""
    valid_events = ('JSSShutdown', 'JSSStartup')

    def __init__(self, *args, **kwargs):
        """
        :param str institution: The name of the organization the server is
            registered to (defaults to 'Example Org').
        
        :param str host_address: The IP address of the originating server
            (defaults to ``10.0.0.1``).
        
        :param str web_app_path: The root path of the web app for the server
            (defaults to ``/``).
        
        :param bool is_master: Is the originating server a cluster master
            (defaults to ``True``).
        
        :param str server_url: The URL of the originating server (defaults to
            ``https://jss.example.org``).
        """
        super(JamfPro, self).__init__(*args, **kwargs)

        self.institution = kwargs.pop('institution', 'Example Org')
        self.host_address = kwargs.pop('host_address', '10.0.0.1')
        self.web_app_path = kwargs.pop('web_app_path', '/')
        self.is_master = bool(kwargs.pop('is_master', True))
        self.server_url = kwargs.pop('server_url', 'https://jss.example.org')

    @property
    def data(self):
        """Return ``data`` for the object as a dictionary.

        :return: ``data`` as a dictionary object
        :rtype: dict
        """
        return {
            "webhook": {
                "id": self.id,
                "name": self.name,
                "webhookEvent": self.event
            },
            "event": {
                "institution": self.institution,
                "hostAddress": self.host_address,
                "webApplicationPath": self.web_app_path,
                "isClusterMaster": self.is_master,
                "jssUrl": self.server_url
            }
        }


class PatchTitle(BaseWebhook):
    """The base webhook object for 'Patch Title' events."""
    valid_events = ('PatchSoftwareTitleUpdated',)

    def __init__(self, *args, **kwargs):
        """
        
        :param int jss_id: ID of the Patch Title in Jamf Pro (defaults to 1).
        
        :param str patch_name: The Patch Title name (defaults to 'Flash').
        
        :param str patch_version: The new Patch Title version (defaults to 1).
        
        :param str report_url: The URL to the Patch Title's report in Jamr Pro
            (Defaults to 'https://jss.example.org/patch.html?id=' + the JSS ID).
            
        :param int timestamp: The UNIX timestamp of when the Patch Title was
            updated. If not provided, or not a valid timestamp, it will be
            set to the current time.
        """
        super(PatchTitle, self).__init__(
            event='PatchSoftwareTitleUpdated', *args, **kwargs)

        self.jss_id = kwargs.pop('jss_id', 1)
        self.patch_name = kwargs.pop('patch_name', 'Flash')
        self.patch_version = kwargs.pop('patch_version', '1')
        self.patch_report_url = kwargs.pop(
            'report_url',
            'https://jss.example.org/patch.html?id={}'.format(self.jss_id)
        )
        self.patch_timestamp = kwargs.pop('timestamp', None)

        try:
            datetime.datetime.fromtimestamp(self.patch_timestamp)
        except TypeError:
            self.patch_timestamp = int(time.time() * 1000)

    @property
    def data(self):
        """Return ``data`` for the object as a dictionary.

        :return: ``data`` as a dictionary object
        :rtype: dict
        """
        data = {
            "event": {
                "name": self.patch_name,
                "latestVersion": self.patch_version,
                "lastUpdate": self.patch_timestamp,
                "reportUrl": self.patch_report_url,
                "jssID": self.jss_id
            }
        }
        data.update(self._webhook_data)
        return data


class SmartGroup(BaseWebhook):
    pass
