from abc import ABC, abstractmethod
import json


class Api(ABC):
    """Testing card response base"""

    @property
    @abstractmethod
    def API_ENDPOINT(self):
        raise NotImplementedError

    @abstractmethod
    def validate_card(self, data: dict) -> bool:
        pass


class TestApi(Api):
    """Sub class"""

    API_ENDPOINT = "https://dev.c38.co/smi/vend_api.php"

    def __init__(self):
        with open('.data/test_cards.json') as jsonfile:
            self.card_data = json.load(jsonfile)

    def validate_card(self, data: dict) -> bool:  # dict = data to send method
        return self.card_data.get(data['card_uid'], None) is not None


class RealApi(Api):
    """Sub class"""

    def validate_card(self, data: dict) -> bool:  # dict = data to send method
        pass


if __name__ == '__main__':
    api = TestApi()