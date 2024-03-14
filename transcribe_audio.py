#!/usr/bin/env python3

import subprocess
import sys
import json
import time

from vosk import Model, KaldiRecognizer, SetLogLevel


SAMPLE_RATE = 16000

SetLogLevel(0)

def transcribeAudio(audio_filepath, out_filepath, audio_language="en-us", model_name=None):
    if model_name:
        model = Model(model_name=model_name, lang=audio_language)
    else:
        model = Model(lang=audio_language)
    rec = KaldiRecognizer(model, SAMPLE_RATE)

    outfile = open(out_filepath, 'w')

    with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                                audio_filepath,
                                "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                                stdout=subprocess.PIPE) as process:

        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                outfile.write(res["text"] + "\n")
            # else:
            #     print(rec.PartialResult())

        res = json.loads(rec.FinalResult())
        outfile.write(res["text"] + "\n")

    outfile.close()

    print("\n Output written to " + out_filepath)

def main():
    model_name = None
    if len(sys.argv) == 4:
        audio_language = sys.argv[1]
        audio_filepath = sys.argv[2]
        model_name = sys.argv[3]
    elif len(sys.argv) == 3:
        audio_language = sys.argv[1]
        audio_filepath = sys.argv[2]
    elif len(sys.argv) == 2:
        audio_language = "en-us"
        audio_filepath = sys.argv[1]
    else:
        print(len(sys.argv))
        raise RuntimeError("Atleast one argument is required")

    out_filename = audio_filepath.split('/')[-1]
    while(out_filename[-1] != '.'):
        out_filename = out_filename[:-1]
    out_filename += "txt"

    out_filepath = '/'.join(audio_filepath.split('/')[:-1]) + "/outputs/" + out_filename

    start_time = time.process_time()
    transcribeAudio(audio_filepath, out_filepath, audio_language, model_name)
    print("Time taken to transcribe audio: ", time.process_time() - start_time)

if __name__ == "__main__":
    main()
