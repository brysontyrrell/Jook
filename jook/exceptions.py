"""
This module contains Jook Exceptions.
"""


class JookException(Exception):
    """Base Jook Exception."""


class InvalidEvent(JookException):
    """Invalid webhook event has been provided."""


class InvalidMode(JookException):
    """Invalid mode option has been provided."""


class InvalidURL(JookException):
    """The URL provided does not contain a scheme."""
