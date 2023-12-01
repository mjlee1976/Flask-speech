import json
import requests
import urllib.parse
from flask import Blueprint, render_template, request

bp = Blueprint('grammar', __name__, url_prefix='/grammar')

@bp.route("/getgrammar", methods=["POST"])
def getgrammar():

    reftext = request.form.get("reftext")
    data = {'text': reftext}
    print(reftext)


    params = urllib.parse.urlencode({'mkt': 'en-US', 'mode': 'proof'})
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/x-www-form-urlencoded'}

    try:
        #response = requests.get(search_url, headers=headers, params=params)
        response = requests.post(search_url, headers=headers, params=params, data=data)
        #response.raise_for_status()

        json_response = response.json()

       # print("\nHeaders:\n")
       # print(response.headers)

        print("\nJSON Response:\n")
        print(json.dumps(json_response, indent=4))




        #print(response.json())
        return json_response
    except Exception as ex:
        raise ex