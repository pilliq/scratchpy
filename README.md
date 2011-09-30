# scratchpy

A Python connection class for Scratch (scratch.mit.edu)

## Getting Started

Start up Scratch

Enable remote sensor connections

Create a variable named 'foo'

	>>> import scratch
 	>>> s = scratch.Scratch(host='localhost')
	>>> s.broadcast(["Hello, Scratch!"])
	>>> s.receive()
	{'broadcast': [], 'sensor-update': {'foo': '0'}}
	>>> 

## ToDo
Parse messages that contain quotes (")
Clean up message parsing
