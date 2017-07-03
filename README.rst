Install Jook
------------

You can install Jook from the Pyhon Package Index:

.. code-block:: bash

    $ pip install jook

Basic Usage
-----------

Jook allows you to create Python objects that can fire off HTTP requests that
mock webhook events from a Jamf Pro server.

Getting started is easy:

.. code-block:: python

    >>> import jook
    >>> computer = jook.Computer('http://localhost', 'ComputerAdded')
    >>> computer.fire()


Jook supports both ``JSON`` and ``XML`` formats for data to send (``JSON`` is the default):

.. code-block:: python

    >>> computer = jook.Computer('http://localhost', 'ComputerCheckIn', mode='xml')
    >>> computer.to_xml()
    '<?xml version="1.0" encoding="UTF-8" ?><JSSEvent><webhook><webhookEvent>ComputerCheckIn</webhookEvent>...</JSSEvent>'
    >>> computer.to_json()
    '{"webhook": {"webhookEvent": "ComputerCheckIn", "id": 1, "name": ""}, "event": {...}'


Create objects in ``randomize`` mode to generate unique data with every ``fire``:

.. code-block:: python

    >>> rand_comp = jook.Computer('http://localhost', 'ComputerInventoryCompleted', randomize=True)
    >>> rand_comp.data
    {'webhook': {...}, 'event': {..., 'udid': '0699A579-2835-4E5F-8847-944D9A477DDD', 'serialNumber': 'CPFQ2MXCG5ND', ...}}
    >>> rand_comp.data
    {'webhook': {...}, 'event': {..., 'udid': '1ABE2310-4396-4ABC-AAA9-5B48E6CFC7F5', 'serialNumber': 'C1FK9EXSFKQT', ...}}


Create ``DeviceData`` and ``LocationData`` objects to pass into webhooks to control
the data sent in the mock events:

.. code-block:: python

    >>> my_device = DeviceData('computer')
    >>> my_device.serial_number
    'CPFQMEE3HYFH'
    >>> comp1 = Computer('http://localhost', 'ComputerAdded', device=my_device)
    >>> comp1.device.serial_number
    'CPFQMEE3HYFH'
    >>> comp2 = Computer('http://localhost', 'ComputerCheckIn', device=my_device)
    >>> comp1.device.serial_number
    'CPFQMEE3HYFH'


Set events to run in a loop with a set delay. This example sets a timer delay of
five seconds and then starts a loop of 10 ``fire`` calls:

.. code-block:: python

    >>> computer = jook.Computer('http://localhost', 'ComputerCheckIn', timer=5)
    >>> computer.start_timer(repeat=10)

