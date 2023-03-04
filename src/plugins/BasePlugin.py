from Controller import Controller
from typing import Tuple

class BasePlugin:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def exec(self, controller: "Controller", text: str) -> Tuple[bool, bool]:
        """
        Execute the plugin.
        :param controller: The controller.
        :param text: The text to process.
        :return: A tuple of (plugin has done something, did the plugin need to have next text).
        """
        raise NotImplementedError
