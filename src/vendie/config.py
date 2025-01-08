from decouple import config

VENDING_MACHINE_MDB_SERIAL_PORT: str = config("VENDING_MACHINE_MDB_SERIAL_PORT")
CARD_READER_SERIAL_PORT: str = config("CARD_READER_SERIAL_PORT")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
MAXIMUM_CREDIT: str = config("MAXIMUM_CREDIT", default="FFFF")