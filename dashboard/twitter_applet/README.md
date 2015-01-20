This example shows how to create a simple applet in Bokeh, which can
be viewed in two different ways:

* running directly on a bokeh-server
* embedded into a separate Flask application

You will need to first download some sample data, then follow the
instructions for running the example.

Running
=======

Bokeh Server
------------

To view this applet directly from a bokeh server, you simply need to
run a bokeh-server and point it at the stock example script:

    bokeh-server --script twitter_app.py

Now navigate to the following URL in a browser:

    http://localhost:5006/bokeh/twitter

Flask Application (NOT CURRENTLY FUNCTIONING. BXX 20 JAN 2015)
-----------------

To embed this applet into a Flask application, first you need to run
a bokeh-server and point it at the stock example script. In this
directory, execute the command:

    bokeh-server --script twitter_app.py

Next you need to run the flask server that embeds the stock applet:

    python flask_server.py

Now you can see the stock correlation applet by navigating to the following
URL in a browser:

    http://localhost:5050/
