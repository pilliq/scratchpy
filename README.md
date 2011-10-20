# scratchpy

A Python connection class for [Scratch](scratch.mit.edu)

## Getting Started

1. Start up Scratch

2. Enable remote sensor connections

3. Create a variable `foo`

```
>>> import scratch
>>> s = scratch.Scratch(host='localhost')
>>> s.broadcast(["Hello, Scratch!"])
>>> s.receive()
{'broadcast': [], 'sensor-update': {'foo': '0'}}
>>> 
```

