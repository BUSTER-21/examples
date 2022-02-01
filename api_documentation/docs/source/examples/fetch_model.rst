Get Live Models
===============================

Gets the live job list. This API can be used to get the id of the desired live model.

.. note::
  Jobs with **testLive** as **false** and **type** as **LIVE** are the live jobs for common model (i.e. M[0]).

.. http:get:: /api/1.2/accounts/(string:account_id)/jobs

  Query Parameters
  ++++++++++++++++

  :?type=:

    Filter the jobs by type. Set this to LIVE.

  :?status=:

    Filter the jobs by status. Set this to RUNNING.

  :?offset=:

    Index of the first item you want results for. Default value is 0.

  :?limit=:

    Number of items you want to include in each page result. There could be fewer items remaining than the specified value.

  **Example request**

  .. tabs::

    .. code-tab:: bash

      $ curl -H "Authorization: Bearer <token>" https://app3.falkonry.ai/api/1.2/accounts/xxxxxxxxxxxxxxx/jobs?type=LIVE&status=RUNNING&offset=0&limit=1000

    .. code-tab:: python

      import requests
      URL = 'https://app3.falkonry.ai/api/1.2/accounts/xxxxxxxxxxxxxxx/jobs?type=LIVE&status=RUNNING&offset=0&limit=1000'
      TOKEN = '<token>'
      HEADERS = {'Authorization': f'token {TOKEN}'}
      response = requests.get(URL, headers=HEADERS)
      print(response.json())

  **Example response**

  .. sourcecode:: json

    [
      {
        "id": "828301734731530240",
        "type": "entities.job",
        "jobType": "LIVE",
        "status": "RUNNING",
        "tenant": "xxxxxxxxxxxxxxx",
        "datastream": "yyyyyyyyyyyy",
        "assessment": "zzzzzzzzzzzz",
        "model": "mmmmmmmmmmmmmmm",
        "baseTimeUnit": "nanos",
        "spec": {
          "assessment": "zzzzzzzzzzzz",
          "datastream": "yyyyyyyyyyyy",
          "model": "mmmmmmmmmmmmmmm",
          "inputList": [
            {
              "id": "806836500704530433",
              "key": "ml5p13e93q",
              "name": "sensor1"
            }
          ],
          "outputList": [
            {
              "id": "821438338742902784",
              "key": "explanations-ml5p13e93q",
              "name": "Explanation-sensor1"
            },
            {
              "id": "821438338835177472",
              "key": "predictions",
              "name": "Predictions"
            },
            {
              "id": "821438338864537600",
              "key": "confidences",
              "name": "Confidences"
            },
            {
              "id": "821438338931646464",
              "key": "episodes",
              "name": "Episodes"
            }
          ]
        },
        "createTime": 1617552922662,
        "updateTime": 1617552949478,
        "createdBy": "740153935079641088",
        "updatedBy": "740153935079641088",
        "testLive": true,
        "messages": [],
        "currentState": {},
        "transitions": [],
        "links": []
      }
    ]

  .. note::

    To paginate through results, begin with a offset value of 0 and a limit value of N. To get the next page, set offset value to N, while the limit value stays the same. Subsequent pages start at 2N, 3N, 4N, and so on.