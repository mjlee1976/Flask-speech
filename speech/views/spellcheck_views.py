

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os
from pprint import pprint
import requests
import urllib.parse

from flask import Flask, jsonify, render_template, request, make_response,Blueprint

'''
This sample uses the Bing Spell Check API to check the spelling of query words 
and then suggests corrections with a scored confidence.
Bing Spell Check API: https://dev.cognitive.microsoft.com/docs/services/5f7d486e04d2430193e1ca8f760cd7ed/operations/57855119bca1df1c647bc358 
'''

# Add your Bing Spell Check subscription key and endpoint to your environment variables.
#key = os.environ['e969c065dce7417aa329b28449ac1b32']
#endpoint = os.environ['https://api.bing.microsoft.com/'] + '/bing/v7.0/spellcheck'


#subscription_key = "e969c065dce7417aa329b28449ac1b32"
subscription_key = "d509fe1373fb40679e64288e418e9507"
assert subscription_key

search_url = "https://api.bing.microsoft.com/v7.0/spellcheck"
#search_url = "https://api.bing.microsoft.com/bing/v7.0/spellcheck/"
search_term = "Microsoft Bing Search Services"

bp = Blueprint('spellcheck', __name__, url_prefix='/spellcheck')

# Query you want spell-checked.
query = 'Microsoft B0ng Searh'


# Construct request
@bp.route("/getspell", methods=["POST"])
def getspell():

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


