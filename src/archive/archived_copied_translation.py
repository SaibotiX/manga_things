import deepl
from pathlib import Path
import os
import time
from voicevox import Client
import asyncio
from playsound import playsound
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

vocabulary = ""

options = Options()

service = Service(executable_path="/snap/bin/geckodriver")
profile = FirefoxProfile()

#  profile.set_preference("javascript.enabled", False)

options.profile = "/home/zuckram/snap/firefox/common/.cache/mozilla/firefox/mrkq3e7p.test"

driver = webdriver.Firefox(options=options, service=service)
#driver.set_window_size(1920, 1080)
driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://jisho.org")

voc_count = 0
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

        scrape_keyword = driver.find_element(By.NAME, "keyword")
        scrape_keyword.send_keys(vocabulary)

        mag_glass = driver.find_element(By.CLASS_NAME, "submit")
        mag_glass.click()

        time.sleep(0.5)
        iterate_vocab = driver.find_elements(By.CLASS_NAME, "japanese_word__text_wrapper")

        count = 0

#        full_dict = {}
#        keys = ["Kana", "Kana_Kanji", "Value", "English"]

#        voc_dict = {key: None for key in keys}

#        voc_dict["English" ] = {}
        for voc in iterate_vocab:
            value = 0
            voc.click()

            time.sleep(0.5)
            
            linkable = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//li[@class='clearfix japanese_word']")))
            
            value = linkable[count].get_attribute("data-pos")

#            voc_dict["Value"] = value
                        
            large_eight = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "large-8")))

            concept_light = large_eight.find_elements(By.CLASS_NAME, "concept_light")
            for element in concept_light:
                kana = element.find_element(By.CLASS_NAME, "furigana")
                text = element.find_element(By.CLASS_NAME, "text")
                english_voc = element.find_elements(By.CLASS_NAME, "meanings-wrapper")

#                voc_dict["Kana"] = kana.text
#                voc_dict["Kana_Kanji"] = text.text
#                if len(english_voc) > 3:
#                    english_voc = english_voc[:3]

                for element in english_voc:
#                    vocabulary_count = "Vocabulary"
#                    voc_dict["English"][vocabulary_count] = {}
                    
                    vocab = element.find_elements(By.CLASS_NAME, "meaning-meaning")
                    attribute = element.find_elements(By.CLASS_NAME, "meaning-tags")

                    if len(vocab) > 3:
#                        vocab = vocab[:3]
#                        attribute = attribute[:3]
                        
                    for att, voc in zip(attribute, vocab):
#                        key_voc = "Voc"
#                        key_att = "Att"

#                        value_voc = voc.text
#                        value_att = att.text

#                        voc_dict["English"][vocabulary_count][key_voc] = value_voc
#                        voc_dict["English"][vocabulary_count][key_att] = value_att

#                    v_count = f"Voc{voc_count}"
#                    full_dict[v_count] = voc_dict
#                    voc_count = voc_count + 1

#        with open("manga_voc.json", "w") as json_file:
#            json.dump(full_dict, json_file, indent=4)
                            
        clear = driver.find_element(By.CLASS_NAME, "search-form_clear-button_js").click()
    else:
        time_c = os.path.getctime(path)
        mod_file = time.ctime(time_c)
        time.sleep(0.5)
