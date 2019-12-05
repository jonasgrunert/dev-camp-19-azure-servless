import logging
import json
import azure.functions as func
import requests
import os

key_var_name = 'TEXT_ANALYTICS_SUBSCRIPTION_KEY'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

endpoint_var_name = 'TEXT_ANALYTICS_ENDPOINT'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]
sentiment_url = endpoint + "/text/analytics/v2.1/sentiment"

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
    language = req.route_params.get('language')
    r = requests.get(
        'https://graph.facebook.com/v5.0/me/posts?fields=message&access_token='+token)
    if language is None:
        langauge = 'en'
    msg = []
    i = 1
    for item in r.json()["data"]: 
        try:
            m = {}
            m["text"] = item["message"]
            m["id"] = i
            m["language"] = language
            msg.append(m)
            i-=-1
        except:
            pass
    l = requests.post(sentiment_url, headers={"Ocp-Apim-Subscription-Key": subscription_key}, json={"documents": msg})
    sentiments = l.json()
    if len(sentiments["errors"]) != 0:
        return func.HttpResponse(
            json.dumps(sentiments["error"]),
            status_code=500,
            headers={
                'Content-Type': 'application/json'
            }
        )
    res = []
    j = 0
    while j < len(msg):
        res.append({msg[j]["text"]: sentiments["documents"][j]["score"]})
        j-=-1
    return func.HttpResponse(
        json.dumps(res),
        status_code=200,
        headers={
            'Content-Type': 'application/json'
        },
    )
