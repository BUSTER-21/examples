Get Episodes
==============

Gets the Episodes created by the live jobs. This API can be used to get all Episodes or filter by datastream, assessment and model.

.. http:get:: /api/1.2/accounts/(string:account_id)/episodes

  Query Parameters
  ++++++++++++++++

  :?episodeType=:

    Filter the Episodes by type. Set this to **NOVEL** to get Novel Episodes or set this to **NOTIFICATION** to get Alert type Episodes.

  :?episodeStatus=:

    Filter the Episodes by status. Set this to **OPEN** to get open Episodes or set this to **ASSIGNED** to get resolved Episodes.

  :?isFinalized=:

    Filter the Episodes that are ready for review. Set this to **true** to get Episodes ready for review.

  :?datastream=:

    Filter the Episodes by Datastream. Set this to **Datastream ID**.

  :?assessment=:

    Filter the Episodes by Assessment. Set this to **Assessment ID**.

  :?model=:

    Filter the Episodes by Model. Set this to **Model ID**.

  :?offset=:

    Index of the first item you want results for. Default value is **0**.

  :?limit=:

    Number of items you want to include in each page result. There could be fewer items remaining than the specified value.

  :?sort=:

    Sort the items by time. Set this to **-createTime** to get the latest item first.

  :?denorm=:

    Expand the details of the allowed properties. Set this to **predictedCondition** to get the Condition label. Allowed properties are: entity, predictedCondition, model and latestDispositionCondition.

  **Example request**

  .. tabs::

    .. code-tab:: bash

      $ curl -H "Authorization: Bearer <token>" https://app3.falkonry.ai/api/1.2/accounts/xxxxxxxxxxxxxxx/episodes?episodeType=NOVEL&episodeStatus=OPEN&isFinalized=true&offset=0&limit=1000&sort=-createTime&denorm=predictedCondition

    .. code-tab:: python

      import requests
      URL = 'https://app3.falkonry.ai/api/1.2/accounts/xxxxxxxxxxxxxxx/episodes?episodeType=NOVEL&episodeStatus=OPEN&isFinalized=true&offset=0&limit=1000&sort=-createTime&denorm=predictedCondition'
      TOKEN = '<token>'
      HEADERS = {'Authorization': f'token {TOKEN}'}
      response = requests.get(URL, headers=HEADERS)
      print(response.json())

  **Example response**

  .. sourcecode:: json

    [
      {
        "id": "933626660376842240",
        "type": "entities.episode",
        "tenant": "xxxxxxxxxxxxxxx",
        "datastream": "yyyyyyyyyyyy",
        "assessment": "zzzzzzzzzzzz",
        "entity": "eeeeeeeeeeee",
        "start": "2016-02-21T03:00:43.000000Z",
        "end": "2016-02-21T03:01:52.000381Z",
        "episodeType": "NOVEL",
        "episodeStatus": "OPEN",
        "predictedCondition": "806841407679500288",
        "model": "mmmmmmmmmmmmmmm",
        "episodeEvaluation": "933627336762888192",
        "learningEvaluation": "918812733184331776",
        "description": "Episode created from event.value=unknown, event.id=827148546171158528",
        "tags": [],
        "createTime": 1642664341782,
        "updateTime": 1642762091361,
        "isFinalized": true,
        "links": [
          {
            "name": "predictedCondition",
            "key": "938382022781591552",
            "url": "/api/1.2/accounts/xxxxxxxxxxxxxxx/datastreams/yyyyyyyyyyyy/conditions/806841407679500288",
            "type": "entities.condition",
            "ref": "predictedCondition",
            "object": {
              "tenant": "xxxxxxxxxxxxxxx",
              "createTime": 1612436381979,
              "label": "unknown",
              "conditionType": "SYSTEM",
              "key": "unknown",
              "id": "806841407679500288",
              "notificationRequested": false,
              "datastream": "yyyyyyyyyyyy",
              "updateTime": 1612436381979
            }
          }
        ]
      },
      {
        "id": "915900048938082305",
        "type": "entities.episode",
        "tenant": "xxxxxxxxxxxxxxx",
        "datastream": "yyyyyyyyyyyy",
        "assessment": "zzzzzzzzzzzz",
        "entity": "eeeeeeeeeeee",
        "start": "2017-04-12T06:50:11.574124Z",
        "end": "2018-04-12T06:50:11.574124Z",
        "episodeType": "NOVEL",
        "episodeStatus": "OPEN",
        "predictedCondition": "854013689468981248",
        "model": "mmmmmmmmmmmmmmm",
        "episodeEvaluation": "915926754674286592",
        "learningEvaluation": "854011558875795456",
        "description": "Episode created from event.value=warning, event.id=854007453365211136",
        "tags": [],
        "createTime": 1638437988268,
        "updateTime": 1638444560476,
        "isFinalized": true,
        "links": [
          {
            "name": "predictedCondition",
            "key": "938382022789980160",
            "url": "/api/1.2/accounts/xxxxxxxxxxxxxxx/datastreams/yyyyyyyyyyyy/conditions/854013689468981248",
            "type": "entities.condition",
            "ref": "predictedCondition",
            "object": {
              "tenant": "xxxxxxxxxxxxxxx",
              "createTime": 1623683130377,
              "label": "warning",
              "conditionType": "USER",
              "key": "warning",
              "id": "854013689468981248",
              "notificationRequested": false,
              "type": "entities.condition",
              "datastream": "yyyyyyyyyyyy",
              "updateTime": 1623683130377
            }
          }
        ]
      }
    ]

  .. note::

    To paginate through results, begin with an offset value of 0 and a limit value of N. To get the next page, set offset value to N, while the limit value stays the same. Subsequent pages start at 2N, 3N, 4N, and so on.