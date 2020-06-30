#Synthesizes speech from the input file of text, with specified pitch and frequency

import os
import sys
import html
from google.cloud import texttospeech

def text_to_ssml(inputfile, req_pitch, req_rate):
    # Generates SSML text from plaintext.
    # Given an input filename, this function converts the contents of the text
    # file into a string of formatted SSML text. This function formats the SSML
    # string so that, when synthesized, the synthetic audio will pause for two
    # seconds between each line of the text file. This function also handles
    # special text characters which might interfere with SSML commands.
    #
    # Args:
    # inputfile: string name of plaintext file
    #
    # Returns:
    # A string of SSML text based on plaintext input

    # Parses lines of input file
    with open(inputfile, "r") as f:
        raw_lines = f.read()

    # Replace special characters with HTML Ampersand Character Codes
    # These Codes prevent the API from confusing text with
    # SSML commands
    # For example, '<' --> '&lt;' and '&' --> '&amp;'

    escaped_lines = html.escape(raw_lines)

    <prosody rate="slow" pitch="-2st">Can you hear me now?</prosody>

    # Convert plaintext to SSML
    # Wait two seconds between each address
    ssml = "<speak><prosody rate="slow" pitch="-2st">{}</prosody></speak>".format(
        escaped_lines.replace("\n", '\n<break time="2s"/>')
    )

    # Return the concatenated string of ssml script
    return ssml



def ssml_to_audio(ssml_text, outfile):

    # Google Cloud Credentials: auth setup https://cloud.google.com/docs/authentication/getting-started
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/christinatuttle/Downloads/text-to-speech-service-account.json'

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Build the voice request, select the language code ("en-US") and the ssml voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(outfile, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "' + outfile + '"')


def main():
    # Number of command line arguments (format: sythesize.py INPUT_FILE PITCH FREQUENCY [OUTPUT_FILE])
    cmd_args = len(sys.argv)
    assert (cmd_args >= 4),"Please provide arguments INPUT_FILE PITCH FREQUENCY [OUTPUT_FILE]"


    # Set pitch
    # Legal values are: 
    #   a number followed by "Hz", 
    #   a relative change 
    #   or "x-low", "low", "medium", "high", "x-high", or "default".
    req_pitch = sys.argv[2]
    #assert (req_pitch >= -20 and req_pitch <= 20),"Pitch range [-20.0, 20.0]"

    # Set rate
    # Legal values are: 
    #  a non-negative percentage
    #  or "x-slow", "slow", "medium", "fast", "x-fast", or "default".
    req_rate = sys.argv[3]
    #assert (req_freq >= 8000 and req_freq <= 48000),"Frequency range [8000, 48000]"


    # Input file
    ssml_text = text_to_ssml(sys.argv[1], req_pitch, req_rate)

    # Set output file (default = output.mp3)
    outfile = "output.mp3"
    if cmd_args > 4:
        outfile = sys.argv[4]


    ssml_to_audio(ssml_text, outfile)
    


if __name__ == "__main__":
    main()

