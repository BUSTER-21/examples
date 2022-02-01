Get Live Output Data
===========================

The output data is in the form of predictions, episodes, confidence score and explanation score. Each type of output data has its own identity and endpoint. :doc:`Raw points API <examples/raw_points>` can be used to retrieve the output data. Each output data type is referenced as Connected Source with an unique identity for each entity. This Connected Source ID can be found in **LiveContext** object.

.. http:get:: /api/1.2/accounts/(string:account_id)/livecontexts

  Query Parameters
  ++++++++++++++++

  :?model=:

    Filter the livecontexts by model. Set this to model id retrieved from the :doc:`Jobs API <examples/fetch_model>`.

  :?offset=:

    Index of the first item you want results for. Default value is 0.

  :?limit=:

    Number of items you want to include in each page result. There could be fewer items remaining than the specified value.

  **Example request**

  .. tabs::

    .. code-tab:: bash

      $ curl -H "Authorization: Bearer <token>" https://app3.falkonry.ai/api/1.2/accounts/xxxxxxxxxxxxxxx/livecontexts?model=mmmmmmmmmmmmmmm&offset=0&limit=1000

    .. code-tab:: python

      import requests
      URL = 'https://app3.falkonry.ai/api/1.2/accounts/xxxxxxxxxxxxxxx/livecontexts?model=mmmmmmmmmmmmmmm&offset=0&limit=1000'
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
        "stagedDataPath": "s3a://falkonry-dev-workspace/ephemeral/796650829893505024/919887302483791872/FLOWDATA/938027163418734592/SORTEDDATA",
        "links": []
      }
    ]

  .. note::

    The API response will have a unique **LiveContext** object for each entity. Use the context id of corresponding output data type within **outputContexts** JSON array to get the output for an entity via :doc:`Raw points API <examples/raw_points>`.
