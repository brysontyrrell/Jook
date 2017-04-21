Jook: A Jamf Pro webhook simulator
===================================

Jook allows you to create Python objects that can fire off HTTP requests that
mock webhook events from a Jamf Pro server.

Basic Usage
-----------

Getting started is easy:

.. code-block:: python

    >>> import jook
    >>> computer = jook.Computer('http://localhost', 'ComputerAdded')
    >>> computer.fire()
    >>>

Jook supports both ``JSON`` and ``XML`` formats for data to send (``JSON`` is the default):

.. code-block:: python

    >>> computer = jook.Computer('http://localhost', 'ComputerCheckIn', mode='xml')
    >>> computer.to_xml()
    '<?xml version="1.0" encoding="UTF-8" ?><JSSEvent><webhook><webhookEvent>ComputerAdded</webhookEvent><id>1</id><name></name></webhook><event><username>john.doe</username><deviceName>John Doe&apos;s Mac</deviceName><realName>John Doe</realName><macAddress></macAddress><udid>EE791769-7DE8-44B4-A777-8492D64E1D83</udid><serialNumber>CPVK83F3GV2M</serialNumber><building></building><alternateMacAddress></alternateMacAddress><phone>(555) 555-5555</phone><emailAddress>john.doe@anon.org</emailAddress><osBuild></osBuild><department>Information Technology</department><position>Intern</position><model></model><osVersion></osVersion><userDirectoryID>-1</userDirectoryID><jssID>1</jssID><room></room></event></JSSEvent>'
    >>> computer.to_json()
    '{"webhook": {"webhookEvent": "ComputerAdded", "id": 1, "name": ""}, "event": {"username": "john.doe", "deviceName": "John Doe\'s Mac", "realName": "John Doe", "macAddress": "", "udid": "EE791769-7DE8-44B4-A777-8492D64E1D83", "serialNumber": "CPVK83F3GV2M", "building": "", "alternateMacAddress": "", "phone": "(555) 555-5555", "emailAddress": "john.doe@anon.org", "osBuild": "", "department": "Information Technology", "position": "Intern", "model": "", "osVersion": "", "userDirectoryID": "-1", "jssID": 1, "room": ""}}'
    >>>

Create objects in ``randomize`` mode to generate unique data with every ``fire``:

.. code-block:: python

    >>> rand_comp = jook.Computer('http://localhost', 'ComputerInventoryCompleted', randomize=True)
    >>> rand_comp._generate()
    {'webhook': {'webhookEvent': 'ComputerAdded', 'id': 1, 'name': ''}, 'event': {'username': 'john.doe', 'deviceName': "John Doe's Mac", 'realName': 'John Doe', 'macAddress': '', 'udid': '0699A579-2835-4E5F-8847-944D9A477DDD', 'serialNumber': 'CPFQ2MXCG5ND', 'building': '', 'alternateMacAddress': '', 'phone': '(555) 555-5555', 'emailAddress': 'john.doe@anon.org', 'osBuild': '', 'department': 'Information Technology', 'position': 'Intern', 'model': '', 'osVersion': '', 'userDirectoryID': '-1', 'jssID': 1, 'room': ''}}
    >>> rand_comp._generate()
    {'webhook': {'webhookEvent': 'ComputerAdded', 'id': 1, 'name': ''}, 'event': {'username': 'john.doe', 'deviceName': "John Doe's Mac", 'realName': 'John Doe', 'macAddress': '', 'udid': '1ABE2310-4396-4ABC-AAA9-5B48E6CFC7F5', 'serialNumber': 'C1FK9EXSFKQT', 'building': '', 'alternateMacAddress': '', 'phone': '(555) 555-5555', 'emailAddress': 'john.doe@anon.org', 'osBuild': '', 'department': 'Information Technology', 'position': 'Intern', 'model': '', 'osVersion': '', 'userDirectoryID': '-1', 'jssID': 1, 'room': ''}}
    >>>

Set events to run in a loop with a set delay. This example sets a timer delay of
five seconds and then starts a loop of 10 ``fire`` calls:

.. code-block:: python

    >>> computer = jook.Computer('http://localhost', 'ComputerCheckIn', timer=5)
    >>> computer.start_timer(repeat=10)
    >>>