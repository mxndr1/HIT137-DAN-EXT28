'''

Group Name: DAN/EXT 28

Group Members:
FATEEN RAHMAN - s387983
HENDRICK DANG (VAN HOI DANG)- s395598
KEVIN ZHU (JIAWEI ZHU) - s387035
MEHRAAB FERDOUSE - s393148

'''

"""
Small mixins used by adapters.

- LoggingMixin: prints simple log messages with the class name
- ValidationMixin: checks if a file path exists before using it
"""

import os


class LoggingMixin:
    """
    Add a very small helper to print log messages.
    - It shows the class name and the message
    - Useful for seeing what the adapters are doing
    """
    def log(self, msg: str) -> None:
        # print the message with a clear prefix
        print(f"[log] {self.__class__.__name__}: {msg}")


class ValidationMixin:
    """
    Add a small helper to check if a file exists.
    - If the file does not exist, raise a FileNotFoundError
    - This prevents model calls from failing silently
    """
    def ensure_file_exists(self, path: str) -> None:
        # check if the file path points to a real file
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
