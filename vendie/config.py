from decouple import config

MDB_SERIAL_PORT = config('MDB_SERIAL_PORT', default=None)
RFID_SERIAL_PORT = config('RFID_SERIAL_PORT', default=None)

MDB_SERIAL_PORT_DESCRIPTION = config('MBD_SERIAL_PORT_DESCRIPTION', default="FT232R USB UART - FT232R USB UART")
RFID_SERIAL_PORT_DESCRIPTION = config('RFID_CARD_READER_SERIAL_PORT_DESCRIPTION', default='USB2.0-Serial')