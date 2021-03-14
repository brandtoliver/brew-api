import logging
from bluepy import btle

DEFAULT_TIMEOUT = 1

_LOGGER = logging.getLogger(__name__)

class BTLEConnection(btle.DefaultDelegate):
    def __init__(self, mac_addr, auth_token, AUTH_HANDLE):
        btle.DefaultDelegate.__init__(self)

        self._conn = None
        self._mac = mac_addr
        self.auth_token = auth_token
        self.auth_handle = AUTH_HANDLE
        self._callbacks = {}

    def __enter__(self):
        """
        Context manager for connecting with ble
        """
        self._conn = btle.Peripheral()
        self._conn.withDelegate(self)
        _LOGGER.debug("Trying to connect to %s", self._mac)
        try:
            self._conn.connect(self._mac, addrType='random')
        except btle.BTLEException as ex:
            _LOGGER.debug("Unable to connect to %s, retrying: %s", self._mac, ex)
            try:
                self._conn.connect(self._mac, addrType='random')
            except btle.BTLEException as ex2:
                _LOGGER.debug("Unable to connect (2nd try) to %s, retrying: %s", self._mac, ex2)
                raise
        _LOGGER.debug("Connected to %s", self._mac)

        self.authenticate(self.auth_token, self.auth_handle)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            self._conn.disconnect()
            self._conn = None

    def handleNotification(self, cHandle, data):
        data = bytearray(data) # maybe not ness
        _LOGGER.debug("Got notification from %s: %s", cHandle, data)
        if cHandle in self._callbacks:
            self._callbacks[cHandle](data)

    def set_callback(self, handle, function):
        """Set the callback for a Notification handle. It will be called with the parameter data, which is binary."""
        self._callbacks[handle] = function

    def make_request(self, handle, value, timeout=DEFAULT_TIMEOUT, with_response=True, notification_handle=None):
        """Write a GATT Command without callback - not utf-8."""
        try:
            with self:
                if notification_handle:
                    self.allow_notifications(notification_handle)

                _LOGGER.debug("Writing to %s with with_response=%s", handle, with_response)
                self._conn.writeCharacteristic(handle, value, withResponse=with_response)
                if timeout:
                    _LOGGER.debug("Waiting for notifications for %s", timeout)
                    self._conn.waitForNotifications(timeout)
        except btle.BTLEException as ex:
            _LOGGER.debug("Got exception from bluepy while making a request: %s", ex)
            raise

    def make_read_request(self, handle):
        """read from handle"""
        try:
            with self:
                _LOGGER.debug("reading from handle %s", handle)
                return self._conn.readCharacteristic(handle)
        except btle.BTLEException as ex:
            _LOGGER.debug("Got exception from bluepy while making a request: %s", ex)
            raise
    
    def authenticate(self, auth_token, auth_handle, with_response=True):
        """Authenticate with token"""
        try:
            _LOGGER.debug("Authenticating to %s", auth_handle)
            self._conn.writeCharacteristic(auth_handle, auth_token, withResponse=with_response)
        except btle.BTLEException as ex:
            _LOGGER.debug("Authenticating failed, got exception from bluepy: %s", ex)
            raise

    def allow_notifications(self, handle, with_response=True):
        # TODO: write doc-string
        try:
            _LOGGER.debug("Turning on notification on handle %s", handle+1)
            self._conn.writeCharacteristic(handle+1, b"\x01\x00", withResponse=with_response)
        except btle.BTLEException as ex:
            _LOGGER.debug("Turning on notification, got exception from bluepy: %s", ex)
            raise