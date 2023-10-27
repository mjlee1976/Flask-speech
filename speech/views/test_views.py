import requests
import base64
import json
import time
import random
import string
import threading
from flask import Blueprint, render_template, request

bp = Blueprint('test', __name__, url_prefix='/test')

from pydub import AudioSegment
from pydub.playback import play

@bp.route('/voice', methods=["POST"])
def voice():

    f = request.files['audio_data']

    sound = AudioSegment.from_wav(f)
    audio_data =sound.export("bb.mp3", format="mp3")

    #play(sound)
    #pass
    print(audio_data)
    return audio_data