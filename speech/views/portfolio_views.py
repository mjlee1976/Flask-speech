
from flask import Blueprint, render_template, request
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


import io
import os
import uuid
from azure.identity import DefaultAzureCredential


bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

from pydub import AudioSegment
from pydub.playback import play

SOURCE_FILE = 'SampleSource.txt'
DEST_FILE = 'BlockDestination.txt'

connection_string ="Zu0b39wpkf8DmdOQ+COVtKFDc5WPtvL1X/LBaorb2ELRjkX4iJmY5NEJK4teWYI/BdTMwmXgbjxh+ASt9kBI1w=="
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=msdocsstoragefunction083;AccountKey=Zu0b39wpkf8DmdOQ+COVtKFDc5WPtvL1X/LBaorb2ELRjkX4iJmY5NEJK4teWYI/BdTMwmXgbjxh+ASt9kBI1w==;EndpointSuffix=core.windows.net")
container_name="outputfile"



@bp.route('/sendstorage', methods=["POST"])
def sendstorage():

    f = request.files['audio_data']

    sound = AudioSegment.from_wav(f)
    audio_data =sound.export("bb.mp3", format="mp3")

    #play(sound)
    #pass
    print(audio_data)
    return audio_data



@bp.route('/upload', methods=["POST"])
def upload():
    # Create a local directory to hold blob data
    local_path = "./data"
    os.mkdir(local_path)

    # Create a file in the local data directory to upload and download
    local_file_name = str(uuid.uuid4()) + ".txt"
    upload_file_path = os.path.join(local_path, local_file_name)

    # Write text to the file
    file = open(file=upload_file_path, mode='w')
    file.write("Hello, World!")
    file.close()

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

    print(blob_client.url)
    return blob_client.url

@bp.route('/audioupload', methods=["POST"])
def audioupload():
    # Create a local directory to hold blob data
    f = request.files['audio_data']
    reftext = request.form.get("reftext")

    data=f

    local_file_name = str(uuid.uuid4()) + ".wav"

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    blob_client.upload_blob(data,blob_type="BlockBlob")

    print(blob_client.url)
    returnData = {'result': 'OK', 'filename': blob_client.url}

    return returnData

@bp.route('/mp3upload', methods=["POST"])
def mp3upload():
    # Create a local directory to hold blob data
    f = request.files['audio_data']
    reftext = request.form.get("reftext")

    sound = AudioSegment.from_wav(f)
    #sound = AudioSegment.from_mp3(f)
    file_name = str(uuid.uuid4()) + ".mp3"
    audio_data =sound.export(file_name, format="mp3")

    data=audio_data

    local_file_name = str(uuid.uuid4()) + ".mp3"

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    blob_client.upload_blob(data,blob_type="BlockBlob")


    returnData = {'result': 'OK', 'filename': blob_client.url}


    if os.path.isfile(file_name): os.remove(file_name)

    return returnData

@bp.route('/pngupload', methods=["POST"])
def pngupload():
    ff = request.files['audio_data']

    data=ff

    local_file_name = str(uuid.uuid4()) + ".png"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    blob_client.upload_blob(data, blob_type="BlockBlob")
    returnData = {'result': 'OK', 'filename': blob_client.url}

    return returnData