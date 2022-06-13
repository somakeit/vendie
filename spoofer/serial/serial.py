from dataclasses import dataclass


@dataclass
class Serial:
    device: any
    baud: any
    timeout: int

    def flush(self):
        pass

    def flushInput(self):
        pass

    def flushOutput(self):
        pass

    def read(self, bytes):
        output = b'Test String'
        return output[:bytes]