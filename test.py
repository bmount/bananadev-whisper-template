# This file is used to verify your http server acts as expected
# Run it with `python3 test.py``

import requests
from io import BytesIO
import base64
import banana_dev as banana

#Needs test.wav file in directory
with open(f'test.wav','rb') as file:
    wav_buffer = BytesIO(file.read())
wav = base64.b64encode(wav_buffer.getvalue()).decode("ISO-8859-1")
model_payload = {"wav_b64":wav}

#use following to call deployed model on banana, model_payload is same as above
out = banana.run("apikey","modelkey",model_payload)
