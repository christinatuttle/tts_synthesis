#Synthesizes speech from the input file of text, with specified pitch and frequency

from google.cloud import texttospeech
import os
import sys

# Number of command line arguments (format: sythesize.py INPUT_FILE PITCH FREQUENCY [OUTPUT_FILE])
cmd_args = len(sys.argv)
if cmd_args < 4:
	print("Please provide arguments INPUT_FILE PITCH FREQUENCY [OUTPUT_FILE]")
	exit()

# Google Cloud Credentials: auth setup https://cloud.google.com/docs/authentication/getting-started
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/christinatuttle/Downloads/text-to-speech-service-account.json'

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
file = sys.argv[1]
with open(file, 'r') as f:
    text = f.read()
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

# Set pitch, range [-20.0, 20.0]
req_pitch = int(sys.argv[2])

# Set frequency, range [8000, 48000]
req_freq = int(sys.argv[3])

# Build the voice request, select the language code ("en-US") and the ssml voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3, pitch = req_pitch, sample_rate_hertz = req_freq
)

# Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# Set output file (default = output.mp3)
output = "output.mp3"
if cmd_args > 4:
	output = sys.argv[4]

# The response's audio_content is binary.
with open(output, "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "' + output + '"')