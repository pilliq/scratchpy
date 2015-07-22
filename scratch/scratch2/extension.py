from .blocks import Block
from .compat import json
from .. import exceptions

class Extension(object):

    def __init__(self, name, port, blocks=None, menus=None):
        self.name = name
        self.port = port
        self.blocks = [] if blocks is None else blocks
        self.menus = {} if menus is None else menus

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return 'Extension(name={!r},port={!r})'.format(self.name, self.port)

    @staticmethod
    def load(fp):
        obj = json.load(fp)

    @staticmethod
    def loads(s):
        obj = json.loads(s)

    def to_json(self):
        blocks = [json.loads(b.to_json()) for b in self.blocks]
        extension = {
            'extensionName': self.name,
            'extensionPort': self.port,
            'blockSpecs': blocks,
            'menus': self.menus
        }
        return json.dumps(extension)

    def save(self, fp):
        fp.write(self.to_json())

    def run(self):
        pass

    def stop(self):
        pass
