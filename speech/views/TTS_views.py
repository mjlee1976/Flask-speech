import requests
import base64
import json
import time
import random
import string
import threading
import azure.cognitiveservices.speech as speechsdk

from flask import Flask, jsonify, render_template, request, make_response,Blueprint

bp = Blueprint('TTS', __name__, url_prefix='/TTS')

subscription_key ='966eba947712427e93903588333cee4b'
region = "koreacentral"
language = "en-US"
languageNew = "en-AU"
voice = "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)"
auvoice = "Microsoft Server Speech Text to Speech Voice (en-AU, AnnetteNeural)"


@bp.route("/gettts", methods=["POST"])
def gettts():
    reftext = request.form.get("reftext")
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voice

    offsets = []

    def wordbound(evt):
        offsets.append(evt.audio_offset / 10000)


    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)


    speech_synthesizer.synthesis_word_boundary.connect(wordbound)

    result = speech_synthesizer.speak_text_async(reftext).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:

        audio_data = result.audio_data


        response = make_response(audio_data)
        response.headers['Content-Type'] = 'audio/wav'
        response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
        # response.headers['reftext'] = reftext
        response.headers['offsets'] = offsets
        return response

    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return jsonify({"success": False})


@bp.route("/getttsforword", methods=["POST"])
def getttsforword():
    word = request.form.get("word")

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voice


    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = speech_synthesizer.speak_text_async(word).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:

        audio_data = result.audio_data


        response = make_response(audio_data)
        response.headers['Content-Type'] = 'audio/wav'
        response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
        # response.headers['word'] = word
        return response

    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return jsonify({"success": False})


@bp.route("/getttsforwordsteam", methods=["POST"])
def getttsforwordsteam():
    word = request.form.get("word")

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voice
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3)
    # speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff44100Hz16BitMonoPcm)

    # speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    pull_stream = speechsdk.audio.PullAudioOutputStream()
    stream_config = speechsdk.audio.AudioOutputConfig(stream=pull_stream)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=stream_config)

    result = speech_synthesizer.speak_text_async(word).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # print("Speech synthesized for text [{}]".format(reftext))
        # print(offsets)
        audio_data = result.audio_data
        print(len(audio_data))
        response = audio_data
        # response = make_response(audio_data)
        # response.headers['Content-Type'] = 'audio/mpeg'
        # response.headers['X-Microsoft-OutputFormat'] = 'raw-44100hz-16bit-mono-pcm'
        # response.headers['Content-Disposition'] = 'attachment; filename=outputaudio.mp3'
        # response.headers['word'] = word
        return response
        # return jsonify({"success":True})

    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return jsonify({"success": False})


@bp.route("/getttsforwordsteamau", methods=["POST"])
def getttsforwordsteamau():
    word = request.form.get("word")

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = auvoice
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3)
    # speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff44100Hz16BitMonoPcm)

    # speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    pull_stream = speechsdk.audio.PullAudioOutputStream()
    stream_config = speechsdk.audio.AudioOutputConfig(stream=pull_stream)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=stream_config)

    result = speech_synthesizer.speak_text_async(word).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # print("Speech synthesized for text [{}]".format(reftext))
        # print(offsets)
        audio_data = result.audio_data
        print(len(audio_data))
        response = audio_data
        # response = make_response(audio_data)
        # response.headers['Content-Type'] = 'audio/mpeg'
        # response.headers['X-Microsoft-OutputFormat'] = 'raw-44100hz-16bit-mono-pcm'
        # response.headers['Content-Disposition'] = 'attachment; filename=outputaudio.mp3'
        # response.headers['word'] = word
        return response
        # return jsonify({"success":True})

    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return jsonify({"success": False})