import traceback
import sys

class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)

    @staticmethod
    def get_detailed_error_message():
        pass
    pass