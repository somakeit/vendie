from abc import ABC, abstractmethod


class Api(ABC):
    """Testing card response base"""
    @abstractmethod
    def validate_card(self, data: dict) -> bool:
        pass

class TestApi(Api):
    """Sub class"""

    API_ENDPOINT = "https://dev.c38.co/smi/vend_api.php"
    def validate_card(self, data: dict) -> bool:  # dict = data to send method
        pass


class RealApi(Api):
    """Sub class"""
    def validate_card(self, data: dict) -> bool:  # dict = data to send method
        pass