"""
Utility functions
"""
import os

from collections import UserList


def clear_screen():
    """Clear console screen"""
    if os.name == "posix":
        # Unix, Linux, macOS, BSD
        os.system('clear')
    elif os.name == "nt":
        # Windows
        os.system('cls')


class History(UserList):
    """List with history. If length > max_length, last element will be removed"""
    def __init__(self, max_length):
        super().__init__([])
        self.max_length = max_length

    def append(self, value):
        if len(self.data) == self.max_length:
            self.data.pop(0)
        self.data.append(value)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __str__(self):
        return str(self.data)
