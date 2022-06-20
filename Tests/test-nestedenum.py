from enum import Enum, EnumMeta
#
#
# class SuperNestedEnum(Enum):
#     def __new__(cls, *args):
#         obj = object.__new__(cls)
#         value = None
#         # Normal Enumerator definition
#         if len(args) == 1:
#             value = args[0]
#
#         # Have a tuple of values, first de value and next the nested enum (I will set in __init__ method)
#         if len(args) == 2:
#             value = args[0]
#
#         if value:
#             obj._value_ = value
#
#         return obj
#
#     def __init__(self, name, nested=None):
#         # At this point you can set any attribute what you want
#         if nested:
#             # Check if is an Enumerator you can comment this if. if you want another object
#             if isinstance(nested, EnumMeta):
#                 for enm in nested:
#                     self.__setattr__(enm.name, enm)
#
# ###############################################################################
#
#
# class SetupCommands(Enum):
#     CONFIG_DATA = '0x00'
#     MAX_MIN_PRICES = '0x01'
#
#
# class VendCommands(Enum):
#     CONFIG_DATA = '0x00'
#     MAX_MIN_PRICES = '0x01'
#
#
# class ReaderCommands(Enum):
#     CONFIG_DATA = '0x00'
#     MAX_MIN_PRICES = '0x01'
#
#
# class ExpansionCommands(Enum):
#     CONFIG_DATA = '0x00'
#     MAX_MIN_PRICES = '0x01'
#
#
# class Command(SuperNestedEnum):
#     RESET = '0x1060'
#     SETUP = '0x1161', SetupCommands
#     POLL = '0x1262'
#     VEND = '0x1363', VendCommands
#     READER = '0x1464', ReaderCommands
#     EXPANSION = '0x1767', ExpansionCommands


from aenum import Enum, skip


class enumA(Enum):
    @skip
    class enumB(Enum):
        elementA = 'a'
        elementB = 'b'
    @skip
    class enumC(Enum):
        elementC = 'c'
        elementD = 'd'


if __name__ == '__main__':
    for e in enumA:
        print(e)
