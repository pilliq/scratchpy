#!/usr/bin/python

import scratch

scratch = scratch.Scratch()
scratch.connect()
while 1:
	print(scratch.receive())

