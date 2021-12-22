Get Raw Data
=============

Gets the raw data points for the requested Connected Source or Signal.

Get Raw Data of Connected Source
--------------------------------

.. http:get:: /api/1.2/data/accounts/(string:account_id)/connectedsources/(string:connectedsource_id)/raw_points

	Query Parameters:
	++++++++++++++++

	:?start=:

	   Start time of the data in nanoseconds.

	:?end=:

	   End time of the data in nanoseconds.

	:?limit=:

	   Limit the data points in response. Default value is 1000.

	:?reverse=:

	   Order the data points by time (allowed values: True or False)

	** Example request **:

	.. tabs::

        .. code-tab:: bash

            $ curl -H "Authorization: Bearer <token>" https://app3.falkonry.ai/api/1.2/data/accounts/xxxxxxxxxxxxxxx/connectedsources/yyyyyyyyyyyy/raw_points?start=1640168850582000000&end=1640169850582000000

        .. code-tab:: python

            import requests
            URL = 'https://app3.falkonry.ai/api/1.2/data/accounts/xxxxxxxxxxxxxxx/connectedsources/yyyyyyyyyyyy/raw_points?start=1640168850582000000&end=1640169850582000000'
            TOKEN = '<token>'
            HEADERS = {'Authorization': f'token {TOKEN}'}
            response = requests.get(URL, headers=HEADERS)
            print(response.json())

    **Example response**:

    .. sourcecode:: json

        {
            "records": {
            	"1640168850582000000": {
            		"value": 2.456
            	},
            	"1640168850583000000": {
            		"value": 3.16
            	}
            },
		    "metadata": {
		        "length": 2,
		        "next": "/api/1.2/data/accounts/xxxxxxxxxxxxxxx/connectedsources/yyyyyyyyyyyy/raw_points?start=1640168850583000001&end=1640169850582000000&limit=80237&reverse=False"
		    }

        }

    .. note::

    	The :next: field in the response is to indicate that there is more data in the range and the mentioned endpoint can be used to get the following data.

