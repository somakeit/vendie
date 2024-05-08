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
    """Testing API for development/testing of changes"""

    API_ENDPOINT = "https://dev.c83.co/smi/vend_api.php"

    def __init__(self):
        with open('./Vender/data/test_cards.json') as jsonfile:
            self.card_data = json.load(jsonfile)

    def validate_card(self, data: dict) -> bool:  # dict = data to send method
        # Returns whether the card UID is found in the test_cards.json file
        return self.card_data.get(data['card_uid'], None) is not None

    # See page 96 of docs about vending, VMC Command, Cashless Devide, Results table!!

    def check_request_amount(self, data):
        """Check that the required funds are available"""
        pass

    def send_vend_request(self):
        pass






class RealApi(Api):
    """Real API that connects to the actual cards/balance/API"""

    def validate_card(self, data: dict) -> bool:  # dict = data to send method
        pass


if __name__ == '__main__':
    api = TestApi()