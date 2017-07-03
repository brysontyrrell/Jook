"""Jook: A Jamf Pro webhook simulator"""
from .models.webhooks import Computer, MobileDevice, JamfPro, PatchTitle
from .models.data_sets import DeviceData, LocationData


__title__ = 'jook'
__version__ = '0.4.3'
__author__ = 'Bryson Tyrrell'
__copyright__ = '(c) 2017 Bryson Tyrrell'
