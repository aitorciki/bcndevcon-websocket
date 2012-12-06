WebSocket demo (BcnDevCon 2012)
===============================

If you've been in the talk, your know what this does: it's a very simple example of a WebSocket server-client interaction.

The server is a Python script. Just run it after installing some dependencies:

* Twisted==12.2.0
* autobahn==0.5.9
* psutil==0.6.1

The client is a webpage containing some JavaScript. You'll have to add d3.js to the same directory and serve it from a webserver.

With the server running, load the webpage. The WebSocket connection will be established and the server will push CPU usages to the webclient every second.

Happy hacking!
