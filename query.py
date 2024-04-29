#handles huggingface model api requests

import os
import json
import requests

huggingface_token = os.environ['HUGGINGFACE_TOKEN']

API_URL = 'https://api-inference.huggingface.co/models/'
model_name = 'facebook/blenderbot-400M-distill'
# format the header in our request to Hugging Face
request_headers = {'Authorization': 'Bearer {}'.format(huggingface_token)}
api_endpoint = API_URL + model_name
# retrieve the secret API token from the system environment

def query(payload):
  model_name = 'facebook/blenderbot-400M-distill'
  api_endpoint = API_URL + model_name
  data = json.dumps(payload)
  response = requests.post(api_endpoint, headers=request_headers, data=data)
  ret = json.loads(response.content.decode('utf-8'))
  return ret


def toxicClassify(payload):
  model_name = 's-nlp/roberta_toxicity_classifier'
  api_endpoint = API_URL + model_name
  data = json.dumps(payload)
  response = requests.post(api_endpoint, headers=request_headers, data=data)
  ret = json.loads(response.content.decode('utf-8'))
  return ret
