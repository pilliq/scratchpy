import unittest
from scratch import Scratch

class ParsingTests(unittest.TestCase):
    """
    Must have Scratch running with remote sensor connections enabled
    """
    def setUp(self):
	self.client = Scratch()

    def test_broadcast(self):
	self.assertEquals(
	    self.client._parse('\x00\x00\x00\x0fbroadcast "a b"'), 
	    ('broadcast', 'a b')
	)
	self.assertEquals(
	    self.client._parse('\x00\x00\x00\x13broadcast """a b"""'),
	    ('broadcast', '"a b"')
	)
	self.assertEquals(
	    self.client._parse('\x00\x00\x00\x17broadcast """""a b"""""'),
	    ('broadcast', '""a b""')
	)
	self.assertEquals(
	    self.client._parse('\x00\x00\x00\x13broadcast """a"" b"'),
	    ('broadcast', '"a" b')
	)
	self.assertEquals(
	    self.client._parse('\x00\x00\x00\x17broadcast """a"" ""b"""'),
	    ('broadcast', '"a" "b"')
	)

    def test_sensorupdate(self):
	self.assertEquals(
	    self.client._parse('\x00\x00\x00\x14sensor-update "a" 0 '), 
	    ('sensor-update', {'a': 0})
	)
	self.assertEquals(
	    self.client._parse('\x00\x00\x00\x16sensor-update "a" "c" '), 
	    ('sensor-update', {'a': 'c'})
	)
	self.assertEquals(
	    self.client._parse('\x00\x00\x00\x16sensor-update "a b" 0 '), 
	    ('sensor-update', {'a b': 0})
	)
	self.assertEquals(
	    self.client._parse('\x00\x00\x00\x1asensor-update """a b""" 0 '), 
	    ('sensor-update', {'"a b"': 0})
	)
	self.assertEquals(
	    self.client._parse('\x00\x00\x003sensor-update """a b""" "hello hi" "a" "c" "a b" 0 '), 
	    ('sensor-update', {'"a b"': 'hello hi', 'a': 'c', 'a b': 0})
	)
	self.assertEquals(
	    self.client._parse('\x00\x00\x00\x1esensor-update """a"" ""b""" 0 '), 
	    ('sensor-update', {'"a" "b"': 0})
	)
	self.assertEquals(
	    self.client._parse('\x00\x00\x00*sensor-update """a"" ""b""" """c"" ""d""" '), 
	    ('sensor-update', {'"a" "b"': '"c" "d"'})
	)

    def test_is_msg(self):
	self.assertTrue(self.client._is_msg('\x00\x00\x00\x14sensor-update "a" 0 '))
	self.assertTrue(self.client._is_msg('\x00\x00\x00\x0ebroadcast "hi"'))
	self.assertFalse(self.client._is_msg('\x00\x00\x00\x14sensor-update "a"'))
	self.assertFalse(self.client._is_msg('\x00\x00\x00\x14benbor-update "a" 0 '))
	self.assertFalse(self.client._is_msg(''))
	self.assertFalse(self.client._is_msg(None))
	self.assertFalse(self.client._is_msg('\x00\x00\x00\x00'))
	self.assertFalse(self.client._is_msg('\x00\x00\x00'))
    
    def test_escape(self):
	self.assertEquals(self.client._escape(''), '')
	self.assertEquals(self.client._escape('"a"'), '""a""')

    def test_unescape(self):
	self.assertEquals(self.client._unescape(''), '')
	self.assertEquals(self.client._unescape('a'), 'a')
	self.assertEquals(self.client._unescape('""a""'), '"a"')
	self.assertEquals(self.client._unescape(0), 0)

if __name__ == '__main__':
    unittest.main()
