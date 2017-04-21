"""
This module contains the main classes that will be interacted with directly.
"""

import json
import time
from urlparse import urlparse

from dicttoxml import dicttoxml
import requests

from .exceptions import InvalidEvent, InvalidMode, InvalidURL
from .identifiers import generate_serial, generate_uuid


class Jook(object):
    """The Jook class is an object for managing and creating large numbers of
    webhook objects and firing them as a group.
    """
    def __init__(self, url, mode):
        pass


class Webhook(object):
    """The base webhook object.

    Contains all shared methods used by child objects.
    """
    valid_events = ('',)

    def __init__(
            self,
            url,
            event,
            webhook_id=1,
            webhook_name='',
            mode='json',
            randomize=False,
            timer=0
    ):
        """
        :param str url: The target URL (must contain the scheme)

        :param str event: The type of webhook event. The available event types
            are defined in the ``valid_event`` attribute for the object.

        :param str mode: The type of data to send.

            Can only be 'json' or 'xml'

        :param bool randomize: Values for the webhook object's ``data`` are
            randomly generated.

            If ``False`` certain values are generated during the object's
            creation and stored. These values will be the same each time
            :func:`fire() <jook.models.Webhook.fire>` is called.

            If ``True`` those values will be set to ``None`` and generated
            at the time :func:`fire() <jook.models.Webhook.fire>` is called.

        :param int timer: An optional value in seconds to specify the delay when
            using :func:`start_timer() <jook.models.Webhook.start_timer>`.

        :param int webhook_id: An optional ID value for the webhook event.

        :param str webhook_name: An optional name for the webhook event.

        :raises InvalidEvent:
        :raises InvalidURL:
        :raises TypeError:
        """
        if not urlparse(url).scheme:
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

        self._data = None
        self.timer = int(timer)

    def to_json(self):
        """
        Return the object's ``data`` as JSON.

        :param dict data: ``data`` as a dictionary object

        :return: JSON string
        :rtype: str
        """
        return json.dumps(self.get_data())

    def to_xml(self):
        """Return the object's ``data`` as XML.

        :return: XML string
        :rtype: str
        """
        return dicttoxml(
            self.get_data(),
            custom_root='JSSEvent',
            attr_type=False
        )

    def get_data(self):
        """This method generates the object data in JSON or XML format which is
        set by the ``data_type`` attributes.

        This method should be overridden by children that inherit this object.
        """
        return self._data

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


class Computer(Webhook):
    """The base Webhook object for 'Computer' events."""
    valid_events = (
        'ComputerAdded',
        'ComputerCheckIn',
        'ComputerInventoryCompleted',
        'ComputerPolicyFinished',
        'ComputerPushCapabilityChanged'
    )

    def __init__(self, *args, **kwargs):
        """Initialize a Computer Webhook object.

        :param args: Arguments accepted by
            :class:`Webhook <jook.models.Webhook>`
        :param kwargs: Keyword arguments accepted by
            :class:`Webhook <jook.models.Webhook>`
        """
        super(Computer, self).__init__(*args, **kwargs)

        if self.random:
            self._serial = None
            self._uuid = None
        else:
            self._serial = generate_serial('computer')
            self._uuid = generate_uuid()
            self._data = self.get_data()

    def _get_serial(self):
        """Return a serial number value.

        If the ``_serial`` attribute is set, that value will be returned. If
        not, a randomized serial number will be generated.

        :returns: Serial number
        :rtype: str
        """
        return self._serial if self._serial else generate_serial('computer')

    def _get_uuid(self):
        """Return a UUID value.

        If the ``_uuid`` attribute is set, that value will be returned. If
        not, a randomized UUID will be generated.

        :returns: UUID
        :rtype: str
        """
        return self._uuid if self._uuid else generate_uuid()

    def get_data(self):
        """Return ``data`` for the object as JSON or XML.

        :return: ``data`` as a dictionary object
        :rtype: str
        """
        if self._data:
            return self._data
        else:
            return {
                "webhook": {
                    "id": self.id,
                    "name": self.name,
                    "webhookEvent": self.event
                },
                "event": {
                    "udid": self._get_uuid(),
                    "deviceName": "John Doe's Mac",
                    "model": "",
                    "macAddress": "",
                    "alternateMacAddress": "",
                    "serialNumber": self._get_serial(),
                    "osVersion": "",
                    "osBuild": "",
                    "userDirectoryID": "-1",
                    "username": "john.doe",
                    "realName": "John Doe",
                    "emailAddress": "john.doe@anon.org",
                    "phone": "(555) 555-5555",
                    "position": "Intern",
                    "department": "Information Technology",
                    "building": "",
                    "room": "",
                    "jssID": 1
                }
            }
