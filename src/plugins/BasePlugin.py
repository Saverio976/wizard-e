from typing import Tuple


def not_implemented(*_) -> Tuple[bool, bool]:
    raise NotImplementedError


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
        return not_implemented(self, controller, text)


from Controller import Controller
