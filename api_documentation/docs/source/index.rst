Falkonry APIs
=============

The Falkonry APIs use :abbr:`REST (Representational State Transfer)`. JSON is returned by all API responses including errors and HTTP response status codes are to designate success and failure. 

Note: You can view the swagger styled API documentation `here <https://app3.falkonry.ai/api/1.2/swagger.app>`__.

Authentication and authorization
--------------------------------

All the requests to the Falkonry APIs require authentication.

Token
~~~~~

The ``Authorization`` HTTP header can be specified with ``Bearer <your-access-token>``
to authenticate as a user and have the same permissions as the user itself.

.. note::

  You can find your :access token: under API Tokens section.


API Examples
------------

Following are the API examples for a quick integration with Falkonry's output:

.. toctree::
  :hidden:

   self

.. toctree::
  :maxdepth: 1
  :glob:

  examples/raw_points
  examples/fetch_model
  examples/fetch_output