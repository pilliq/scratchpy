# scratchpy

A Python client for [Scratch](scratch.mit.edu)

## Getting Started

1. Start up Scratch

2. [Enable remote sensor connections](http://wiki.scratch.mit.edu/wiki/Remote_Sensor_Connections#Enabling), or "Host Mesh" in [BYOB](http://byob.berkeley.edu/)

3. Create a variable for all sprites named `foo`

```
>>> import scratch
>>> s = scratch.Scratch()
>>> s.broadcast("Hello, Scratch!")
>>> s.receive()
('sensor-update', {'foo': 0})
>>> 
```

## Installation
```
# pip install scratchpy
```

Or

```
# easy_install scratchpy
```

If you're installing from source, you can untar the source tarball, `cd` into the project directory and run

```
# make install
```

## Usage

### Connecting 
Constructing a new `Scratch` object will automatically connect to Scratch

```
import scratch
s = scratch.Scratch()
```

This will create a connection on `localhost` port 42001 and set `s.connected` to `True`. If you want to change the host or port, you can provide them to the constructor

```
s = scratch.Scratch(host='0.0.0.0', port=40000) 
```

If you are disconnected, you can reconnect using the `connect` method

```
s.connect()
```

### Broadcasting
Broadcasting messages to Scratch will function like a broadcast block in Scratch. You can broadcast either a single message

```
s.broadcast('Hello, Scratch!')
```

Or a list of messages

```
s.broadcast(['Hello, Scratch!', 'How are you doing?'])
```

Actually, you can give `broadcast` any iterable object (list, tuple, set, generator, etc.). 

### Sensor updates
Sending sensor updates to Scratch will create new sensors in the Sensing category, or update sensors with new values. The `sensorupdate` method accepts a dict whose keys are sensor names, and values are sensor values. 

```
s.sensorupdate({'temperature' : 75})
```

### Receiving
Use the `receive` method to receive messages from Scratch

```
msg = s.receive()
```

A call to `receive` will block until it reads a message from Scratch. If the call is successful, it returns a tuple of the message received. If the call failed, it raises an exception. If the message received is not a proper Scratch message, `receive` returns `None`. 

The first element of the tuple will be the message type and the second element will be the message data. 

Two types of messages can be received: broadcast messages and sensor update messages. 

#### Broadcasts
Broadcast messages are received anytime a broadcast block is executed in Scratch. The message data is a string of the message that was broadcast. An example broadcast message returned from `receive` looks like this:

```
('broadcast', 'Hello, Python!')
```

#### Sensor updates
Sensor updates are received when global variables (i.e. variables created for all sprites) are created, or when their value changes. The message data is a dict that maps global variable names to their values. Suppose you created two variables, `foo` and `bar`. Upon their creation, `receive` would return a message that looks like this:

```
('sensor-update', {'foo': 0, 'bar': 0})
```

#### Handling Multiple Messages
`receive` returns only one message. If Scratch has sent more than one message, they will stay on the network buffer until `receive` is called again. To receive all the messages from Scratch you must repeatedly call `receive`. A nice way to handle this is to have a generator function that yields a message everytime it receives, and exits on error. 

```
def listen():
    while True:
	try:
	    yield s.receive()
	except scratch.ScratchError:
	    raise StopIteration
```

Now you can iterate over all the messages from Scratch

```
for msg in listen():
    if msg[0] == 'broadcast':
	# code to handle broadcasts
    elif msg[0] == 'sensor-update':
	# code to handle sensor updates
```

If an error occurs or the connection to Scratch is closed, Python simply exits the loop. 

### Disconnecting
To close a connection to Scratch

```
s.disconnect()
```

A disconnection may occur without an explicit call to `disconnect`. These usually happen when either Scratch is closed, remote sensor connections are disabled, or when there is something up with the network.

### Errors
There are two kinds of errors that can be caught in `connect`, `receive`, `broadcast`, and `sensorupdate`:

`ScratchError` is raised when there are errors with the network (e.g. connection refused, connection established, etc. basically any error from [errno](http://docs.python.org/2/library/errno.html)). The error message returned is the error message from `errno`.

`ScratchConnectionError` is raised when reading or writing data has no effect (i.e. reading from Scratch returns an empty string, or writing to Scratch writes 0 bytes). This is usually a sign that Scratch has been disconnected. 

If you do not care about the difference, you can just except `ScratchError` and it will also catch `ScratchConnectionError`.

## License
MIT
