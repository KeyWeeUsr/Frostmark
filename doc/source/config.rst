Config
======

Modify how the application runs with the `Environment variables
<https://en.wikipedia.org/wiki/Environment_variable>`_.

React GUI
---------

``FROSTMARK_HOST``
    Specify what host you want to run the server layer between Frostmark
    and React frontend displaying the bookmarks.

Development
~~~~~~~~~~~

``REACT_PROXY``
    Specify the endpoint for all the requests attempted to fetch from with
    Node's ``fetch()``.

.. note:: Check firewall rules in case of not being able to proxy the requests.
