.. Jook documentation master file, created by
   sphinx-quickstart on Thu Apr 20 22:09:35 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Jook's documentation!
================================

.. automodule:: jook


Interface
=========

The Jook Object
---------------

.. autoclass:: jook.models.Jook
   :members:


Base Webhook Object
-------------------

.. autoclass:: jook.models.Webhook
   :members:


Models
------

.. autoclass:: jook.models.Computer
   :members:


Helper Functions
----------------

.. autofunction:: jook.identifiers.generate_serial


Exceptions
----------

.. autoexception:: jook.exceptions.JookException
.. autoexception:: jook.exceptions.InvalidEvent
.. autoexception:: jook.exceptions.InvalidMode
.. autoexception:: jook.exceptions.InvalidURL
