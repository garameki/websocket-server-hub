================
websocket-server
================

Prepare:
--------
1.Clone and Install  <https://github.com/Pithikos/python-websocket-server>

2.Clone <https://github.com/garameki/websocket-server/blob/master/hub/hub.py>

execute:
--------
$ python3 hub.py


message functions:
----------

  Messages can involve any commands what you want websocket-server take.

  1.to give client roll name

    2 examples:

      co6

      ma6

  2.to send message to specific roll of client(s)
    2 examples:

      toM

      toC

Usage (keep order):
------
  1.on terminal 1:

    co6

  2.on terminal 2:

    ma6

  3.on terminal 1:

     toM Hello MAX31856!

  4.on terminal 2:

    toC Hello CONTROLLER!

Feature:
--------

  You can add more command.
