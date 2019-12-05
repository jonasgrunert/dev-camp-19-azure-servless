import logging
import json
import azure.functions as func
import requests
from flair.models import TextClassifier
from flair.data import Sentence


def main(req: func.HttpRequest) -> func.HttpResponse:
    token = req.headers.get('Authorization')
    if not token:
        return func.HttpResponse(
            json.dumps({
                'code': 'Unauthorized',
                'message': 'No Authorization header found'
            }),
            headers={
                'Content-Type': 'application/json'
            },
            status_code=403
        )

    # provider = req.params.get('provider')
    # if not provider:
    #     return func.HttpResponse(
    #         "Please pass a provider",
    #         status_code=400
    #     )
    r = requests.get(
        'https://graph.facebook.com/v5.0/me/posts?fields=message&access_token='+token)
    msg = []
    for item in r.json()["data"]:
        try:
            msg.append(item["message"])
            try:
                classifier = TextClassifier.load('en-sentiment')
                sentence = Sentence(msg[0])
                classifier.predict(sentence)
                # print sentence with predicted labels
                print('Sentence above is: ', sentence.labels)
            except:
                pass
        except:
            pass
    return func.HttpResponse(
        status_code=200,
        headers={
            'Content-Type': 'application/json'
        },
        json.dumps({
            sentence.labels
        })
    )
