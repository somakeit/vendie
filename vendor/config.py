from .api import TestApi, RealApi

# Serial Devices
PORT_DESCRIPTIONS = {
    'card_reader': 'USB2.0-Serial',
    'vendor': 'FT232R USB UART - FT232R USB UART'
}
API_TO_USE = TestApi  # Change between TestApi / RealApi

ENCODING = 'utf-8'

# Debugging
DEBUG = False
SHOW_ENTER_EXIT = True
