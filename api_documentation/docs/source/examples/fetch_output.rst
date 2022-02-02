Get Live Output Data
===========================

The output data is in the form of Predictions, Episodes, Confidence Score and Explanation Score. Each type of output data has its own identity and endpoint. :doc:`Signal Data API </examples/raw_points>` can be used to retrieve the output data. Each output data type is referenced as Connected Source with an unique identity for each entity. This Connected Source ID can be found in **Live Context** object.

.. note::

  Refer :doc:`Episodes API </examples/fetch_episode>` section, to get the Episode data.


.. http:get:: /api/1.2/accounts/(string:account_id)/livecontexts

  Query Parameters
  ++++++++++++++++

  :?model=:

    Filter the Live Contexts by model. Set this to **model id** retrieved from the :doc:`Jobs API </examples/fetch_model>`.

  :?isCommonModel=:

    Get list of Live Contexts each corresponding to a live common model (i.e. M[0]) and a live entity. Set this to **true** if you do not have a specific model id.

  :?offset=:

    Index of the first item you want results for. Default value is **0**.

  :?limit=:

    Number of items you want to include in each page result. There could be fewer items remaining than the specified value.

  :?sort=:

    Sort the items by time. Set this to **-createTime** to get latest item first.

  **Example request**

  .. tabs::

    .. code-tab:: bash

      $ curl -H "Authorization: Bearer <token>" https://app3.falkonry.ai/api/1.2/accounts/xxxxxxxxxxxxxxx/livecontexts?isCommonModel=true&offset=0&limit=1000

    .. code-tab:: python

      import requests
      URL = 'https://app3.falkonry.ai/api/1.2/accounts/xxxxxxxxxxxxxxx/livecontexts?isCommonModel=true&offset=0&limit=1000'
      TOKEN = '<token>'
      HEADERS = {'Authorization': f'token {TOKEN}'}
      response = requests.get(URL, headers=HEADERS)
      print(response.json())

  **Example response**

  .. sourcecode:: json

    [
      {
        "id": "938027869534007296",
        "tenant": "xxxxxxxxxxxxxxx",
        "model": "mmmmmmmmmmmmmmm",
        "entity": "eeeeeeeeeeee",
        "type": "entities.livecontext",
        "contextIds": [],
        "inputContexts": [],
        "outputContexts": [
          {
            "context": "919892128240259072.919887302722867200",
            "type": "Numeric",
            "signal": "919892128240259072",
            "signalKey": "explanations-orz7kd747m",
            "signalName": "Explanation-sensor2"
          },
          {
            "context": "919892128361893888.919887302722867200",
            "type": "Numeric",
            "signal": "919892128361893888",
            "signalKey": "explanations-onz6216rgo",
            "signalName": "Explanation-sensor3"
          },
          {
            "context": "919892128395448320.919887302722867200",
            "type": "Numeric",
            "signal": "919892128395448320",
            "signalKey": "explanations-qwl3573r9m",
            "signalName": "Explanation-sensor1"
          },
          {
            "context": "919892128768741376.919887302722867200",
            "type": "Categorical",
            "signal": "919892128768741376",
            "signalKey": "predictions",
            "signalName": "Predictions"
          },
          {
            "context": "919892128873598976.919887302722867200",
            "type": "Numeric",
            "signal": "919892128873598976",
            "signalKey": "confidences",
            "signalName": "Confidences"
          },
          {
            "context": "919892129074925568.919887302722867200",
            "type": "Events",
            "signal": "919892129074925568",
            "signalKey": "episodes",
            "signalName": "Episodes"
          }
        ],
        "datastream": "yyyyyyyyyyyy",
        "assessment": "zzzzzzzzzzzz",
        "createTime": 1643713671812,
        "updateTime": 1643713671812,
        "isCommonModel": true,
        "links": []
      }
    ]

  .. note::

    The API response will have a unique **Live Context** object for each entity. Use the context id (also referred as Connected Source id) of corresponding output data type within **outputContexts** JSON array to get the output for an entity via :doc:`Signal Data API </examples/raw_points>`.

    For example, use **919892128768741376.919887302722867200** as Connected Source id to get predictions data for entity **eeeeeeeeeeee**.
