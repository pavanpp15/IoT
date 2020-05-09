#!/bin/bash

echo "Converting Speech to Text..."
wget --server-response -q -U "Mozilla/5.0" --post-file test.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v1/recognize?lang=en-us&client=chromium" | cut -d\" -f12  > stt.txt
 
echo "You Said:"
value=`cat stt.txt`
echo "$value"

