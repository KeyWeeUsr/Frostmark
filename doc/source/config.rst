Config
======

Modify how the specific parts of the application run with the `Environment
variables <https://en.wikipedia.org/wiki/Environment_variable>`_. The values
have to be set before the application is started.

React GUI
---------

``FROSTMARK_HOST``
    Specify what host you want to run the server layer between Frostmark
    and React frontend displaying the bookmarks.

    .. code:: shell

        FROSTMARK_HOST=192.168.1.100 fmgui

Development
~~~~~~~~~~~

``REACT_PROXY``
    Specify the endpoint for all the requests attempted to fetch from path
    starting with ``/api`` via Node's ``fetch()``. For more info see the proxy
    config for specific routes in ``src/setupProxy.js``

    .. code:: shell

        REACT_PROXY=http://192.168.1.100:5000 ./run_frontend.sh

.. note:: Check firewall rules in case of not being able to proxy the requests.
