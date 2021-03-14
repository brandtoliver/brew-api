import logging

from connection import BTLEConnection

# for testing only
from config import AUTH_TOKEN, MAC 

_LOGGER = logging.getLogger(__name__)

PROP_NTFY_HANDLE = 38
AUTH_HANDLE = 20
BREW_WRITE_HANDLE = 36


class Nespresso:
    """TODO: write doc-string"""
    
    def __init__(self, _mac, auth_token, connection_cls=BTLEConnection):
        """Initialize the nespresso machine"""
        self.status = {}

        self._conn = connection_cls(_mac, auth_token, AUTH_HANDLE)
        self._conn.set_callback(PROP_NTFY_HANDLE, self.handle_status_notification)
        # add more callbacks here

    def handle_status_notification(self, data):
        """Handle Callback from a Bluetooth (GATT) request."""
        _LOGGER.debug("Received notification from the device: %s", data[0])

        # status notification
        if data[0] == 195:
            self.status[0] = 'Slider error'
        elif data[0] == 129:
            self.status[0] = 'OK'
        elif data[0] == 131:
            self.status[0] = 'Brewing'

        else:
            _LOGGER.debug("Unknown notification %s", data[0])    

    def query_brew(self, brew_type): 
        #TODO: fix brew types
        _LOGGER.debug("Querying brewing..")
        if brew_type == 'ristretto':
            value = b'\x03\x05\x07\x04\x00\x00\x00\x00\x00\x01' #fix
        elif brew_type == 'espresso':
            value = b'\x03\x05\x07\x04\x00\x00\x00\x00\x00\x01' #fix
        elif brew_type == 'lungo':
            value = b'\x03\x05\x07\x04\x00\x00\x00\x00\x00\x01' #fix
        else:
            _LOGGER.debug("Unknown brew type %s", brew_type)
            return False

        self._conn.make_request(BREW_WRITE_HANDLE, value, notification_handle=PROP_NTFY_HANDLE)
        return True

    def get_status(self):
        _LOGGER.debug("Querying status..")
        data = self._conn.make_read_request(PROP_NTFY_HANDLE)
        _LOGGER.debug("Received status data from the device: %s", data[0])

        # status
        if data[0] == 195:
            self.status[0] = 'Slider error'
        elif data[0] == 129:
            self.status[0] = 'OK'
        elif data[0] == 131:
            self.status[0] = 'Brewing'
        else:
            _LOGGER.debug("Unknown status data %s", data[0])
            return False

        return self.status  

if __name__ == "__main__":
    # test
    logging.basicConfig(level=logging.DEBUG)
    nespresso = Nespresso(MAC, AUTH_TOKEN)
    print(nespresso.get_status())
    #nespresso.query_brew('ristretto')
    #print(nespresso.status)