from scratch import Scratch, ScratchError, ScratchConnectionError

__version__ = '0.1.0'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['Scratch', 'ScratchError', 'ScratchConnectionError'] 
