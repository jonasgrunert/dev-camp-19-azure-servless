import logging
import json
import azure.functions as func
import requests

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
    r = requests.get('https://graph.facebook.com/v5.0/me/posts?fields=message&access_token='+token)
    msg = []
    for item in r.json()["data"]:
        try:
            msg.append(item["message"])
        except:
            pass
    return func.HttpResponse(
        json.dumps(msg)
    )