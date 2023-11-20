# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 10:40:16 2023

@author: Ravit
"""

import boto3
import json
import os
# In[]
os.environ.get('SAGE_ROLE')

bedrock = boto3.client(service_name='bedrock-runtime')

with open(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\tech_list\prompts\18Oct2023_claude_prompt_meta_techs.txt', encoding='utf-8') as f:
    prompt = f.read()

# In[]
body = json.dumps({
    "prompt": f"\n\nHuman:{prompt}\n\nAssistant:",
    "max_tokens_to_sample": 1000,
    "temperature": 0.1,
    "top_p": 0.9,
})

modelId = 'anthropic.claude-v2'
accept = 'application/json'
contentType = 'application/json'

response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

response_body = json.loads(response.get('body').read())
# text
print(response_body.get('completion'))