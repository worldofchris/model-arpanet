"""
A node's state can be displayed on a wired or wireless neopixel display
or on an ascii display.  Might do a vector one too for the model PDP-1

A node's state is derived from the messages currently located there.

When we step a message through it's route we update the node to indicate
that the message is there.  The node can then update its display.

OR

Nodes have no state.  messages have state.  When a message moves to a new
node we tell the corresponding node display so it can update _its_ state.

A display looks like this:

0 0 0

If it has a message:

* 0 0

We have some options as to whether we use the three neopixels to show
the message moving:

* 0 0
0 * 0
0 0 *

or show the number of messages at each node:

* 0 0
* * 0
* * *

then if a node is full we could shut down the link into it or show it over
flowing:

X X X

We could use different colours to show multiple messages

We could show a message moving across:

* 0 0
0 * 0

Then coming to rest:

0 0 *

And then subsequent messages backing up behind it

0 * *
* * *

messages could then empty out as they are processed:

0 * *
0 0 *
0 0 0

or overflow:

X X X

Not sure about split of state between message and node / node display

"""
