import json
import requests
import urllib
import subprocess
import argparse
import pycurl
import StringIO
import os.path


def speak_text(language, phrase):
    tts_url = "http://translate.google.com/translate_tts?tl=" + language + "&q=" + phrase
    subprocess.call(["mplayer", tts_url], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def transcribe():
    key = '[Google API Key]'# Write your key here
    stt_url = 'https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=' + key
    filename = 'test.flac'
    print "Say Something!"
    os.system(
        'arecord -D plughw:0,0 -f cd -c 1 -t wav -d 0 -q -r 16000 -d 3 | flac - -s -f --best --sample-rate 16000 -o ' + filename)
    
    # send the file to google speech api
    c = pycurl.Curl()
    c.setopt(pycurl.VERBOSE, 0)
    c.setopt(pycurl.URL, stt_url)
    fout = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, fout.write)

    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: audio/x-flac; rate=16000'])

    file_size = os.path.getsize(filename)
    c.setopt(pycurl.POSTFIELDSIZE, file_size)
    fin = open(filename, 'rb')
    c.setopt(pycurl.READFUNCTION, fin.read)
    c.perform()

    response_data = fout.getvalue()

    start_loc = response_data.find("transcript")
    temp_str = response_data[start_loc + 13:]
    end_loc = temp_str.find("\"")
    final_result = temp_str[:end_loc]
    c.close()
    return final_result


class Translator(object):
    oauth_url = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
    translation_url = 'http://api.microsofttranslator.com/V2/Ajax.svc/Translate?'

    def __init__(self):
        oauth_args = {
            'client_id': '',  # input  your client_id here
            'client_secret': '[Microsoft Client Secret]',# input your client seceret id here
            'scope': 'http://api.microsofttranslator.com',
            'grant_type': 'client_credentials'
        }
        oauth_junk = json.loads(requests.post(Translator.oauth_url, data=urllib.urlencode(oauth_args)).content)
        self.headers = {'Authorization': 'Bearer ' + oauth_junk['access_token']}

    def translate(self, origin_language, destination_language, text):
        german_umlauts = {
            0xe4: u'ae',
            ord(u'ö'): u'oe',
            ord(u'ü'): u'ue',
            ord(u'ß'): None,
        }

        translation_args = {
            'text': text,
            'to': destination_language,
            'from': origin_language
        }
        translation_result = requests.get(Translator.translation_url + urllib.urlencode(translation_args),
                                          headers=self.headers)
        translation = translation_result.text[2:-1]
        if destination_language == 'de':
            translation = translation.translate(german_umlauts)
        print(f'Source: {translation.src}')
        print(f'Destination: {translation.dest}') ", 
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translator.')
    parser.add_argument('-o', '--origin_language', help='Origin Language', required=True)
    parser.add_argument('-d', '--destination_language', help='Destination Language', required=True)
    args = parser.parse_args()
    while True:
        Translator().translate(args.origin_language, args.destination_language, transcribe())