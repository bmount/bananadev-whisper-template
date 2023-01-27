import torch
import whisper
from tempfile import mkstemp
import os
import base64
from io import BytesIO

# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"


# Tiny bit of extra indirection for testing locally
def get_model():
    model = whisper.load_model("large-v2")
    return model

def init():
    global model
    model = get_model()

def make_audio_tmpfile(payload, suffix:str) -> str:
    fd, pathname = mkstemp(suffix=suffix)
    f = os.fdopen(fd, 'wb')
    f.write(payload.getbuffer())
    f.close()
    return pathname

def input_to_tmpfile(model_inputs:dict) -> str:
    mp3_bytestring = model_inputs.get('mp3_b64', None)
    if mp3_bytestring is not None:
        mp3Bytes = BytesIO(base64.b64decode(mp3_bytestring.encode("ISO-8859-1")))
        return make_audio_tmpfile(mp3Bytes, '.mp3')
    wav_string = model_inputs.get('wav_b64', None)
    if wav_string is not None:
        wavBytes = BytesIO(base64.b64decode(wav_string.encode("ISO-8859-1")))
        return make_audio_tmpfile(wavBytes, '.wav')
    return None

# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs:dict) -> dict:
    global model

    # Parse out your arguments
    input_tmpfile = input_to_tmpfile(model_inputs)
    if input_tmpfile is None:
        return dict(error="Unable to find suitable audio input (checked 'mp3_b64' and 'wav_b64')")
    result = model.transcribe(input_tmpfile, initial_prompt=model_inputs.get('initial_prompt'))
    output = {"text":result["text"]}
    os.remove(input_tmpfile)
    # Return the results as a dictionary
    return result
