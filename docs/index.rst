.. Jook documentation master file, created by
   sphinx-quickstart on Thu Apr 20 22:09:35 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Jook's documentation!
================================

.. include:: ../README.rst


Interface
=========

The Jook Object
---------------

.. autoclass:: jook.models.webhooks.Jook
   :members:


Base Webhook Object
-------------------

.. autoclass:: jook.models.webhooks.BaseWebhook
   :members:


Device Models
-------------

.. autoclass:: jook.models.webhooks.Computer
   :members:

.. autoclass:: jook.models.webhooks.MobileDevice
   :members:


Data Sets
---------

.. autoclass:: jook.models.data_sets.DeviceData
   :members:

.. autoclass:: jook.models.data_sets.LocationData


Exceptions
----------

.. autoexception:: jook.exceptions.InvalidDeviceType
.. autoexception:: jook.exceptions.InvalidEvent
.. autoexception:: jook.exceptions.InvalidMode
.. autoexception:: jook.exceptions.InvalidURL
