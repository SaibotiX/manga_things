import deepl
from pathlib import Path
import os
import time
from voicevox import Client
import asyncio
from playsound import playsound

async def wav(var):
    async with Client() as client:
        audio_query = await client.create_audio_query(var, speaker=1)
        with open("../tools/voice.wav", "wb") as f:
            f.write(await audio_query.synthesis(speaker=1))

        playsound('../tools/voice.wav')

path = '../tools/sentences.txt'

auth_key = "c1c893eb-38dd-4296-9a0e-1e9993662069:fx"
            
translator = deepl.Translator(auth_key)

open(path, 'w').close()

time_c = os.path.getctime(path)

mod_file = time.ctime(time_c)
mod_time = time.ctime(time_c)

vocabulary = "abc"

while True:
    if mod_time != mod_file:
        time.sleep(0.2)
        if os.path.getsize(path) > 0:
            with open(path, 'r') as line:
                vocabulary = line.readlines()[-1]
                
        asyncio.run(wav(vocabulary))

        result = translator.translate_text(vocabulary, target_lang="EN-US")

        print(vocabulary.strip() + "  -  " + result.text, end="\n")
        open(path, 'w').close()        
        time_c = os.path.getctime(path)
        mod_file = time.ctime(time_c)
        mod_time = mod_file
        
    else:
        time_c = os.path.getctime(path)
        mod_file = time.ctime(time_c)
        time.sleep(0.5)
