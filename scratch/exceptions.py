
class ScratchException(Exception):
    """There was an ambiguous exception that occured"""

class ScratchConnectionError(ScratchException):
    """A connection error occured"""
