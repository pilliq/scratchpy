from enum import Enum
from .compat import json

class Block(object):
    def __init__(
        self, name, block_type, block_format, defaults=None, handler=None):
        self.name = name
        self.block_type = block_type
        self.block_format = block_format
        self.defaults = [] if defaults is None else defaults
        self._handler = handler

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return 'Block(name={!r},block_type={!r})'.format(
            self.name,
            self.block_type)

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, value):
        self._handler = value

    def to_json(self):
        block = [str(self.block_type), self.block_format, self.name]
        block.extend(self.defaults)
        return json.dumps(block)


class BlockType(Enum):
        command = (" ", "command")
        wait_command = ("w", "wait command")
        reporter = ("r", "number reporter")
        boolean = ("b", "boolean reporter")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return str(self.name)
