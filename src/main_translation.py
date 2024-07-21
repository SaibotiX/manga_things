import deepl
from pathlib import Path
import os
import time
from voicevox import Client
import asyncio
from playsound import playsound
import json
import keyboard

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

running = True

async def wav(var):
    async with Client() as client:
        audio_query = await client.create_audio_query(var, speaker=1)
        with open("../tools/voice.wav", "wb") as f:
            f.write(await audio_query.synthesis(speaker=1))

        playsound('../tools/voice.wav')

def is_element_empty(element):
    try:
        inner_html = element.get_attribute('innerHTML').strip()
        return inner_html == ''
    except NoSuchElementException:
        return True
    
def on_hotkey(driver):
    global running
    running = False

    driver.quit()

def Get_Last_Entry_Point(infile_instance):
    infile = open(infile_instance)

    data = json.load(infile)

    nested_dict = data[0]

    last_key = list(nested_dict.keys())[-1]
    last_value = nested_dict[last_key]

    last_entry_point = last_value["Instance Count"] + 1
    
    return last_entry_point

def Read_Json(File_Path):
    data = []
    with open(File_Path, 'r') as J_file:
        data = json.load(J_file)

    return data

def Check_Keys(File_Path, Curr_Word):
    infile = open(File_Path)

    data = json.load(infile)

    nested_dict = data[0]

    keys = list(nested_dict.keys())
    for i in keys:
        if i == Curr_Word:
            return False
    return True

path = '../tools/sentences.txt'

auth_key = "c1c893eb-38dd-4296-9a0e-1e9993662069:fx"
            
translator = deepl.Translator(auth_key)

open(path, 'w').close()

time_c = os.path.getctime(path)

mod_file = time.ctime(time_c)
mod_time = time.ctime(time_c)

vocabulary = ""

options = Options()

#options.add_argument("-headless")
service = Service(executable_path="/snap/bin/geckodriver")
profile = FirefoxProfile()

#  profile.set_preference("javascript.enabled", False)

options.profile = "/home/zuckram/snap/firefox/common/.cache/mozilla/firefox/mrkq3e7p.test"

driver = webdriver.Firefox(options=options, service=service)
#driver.set_window_size(1920, 1080)
driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://jisho.org")

keyboard.add_hotkey('ctrl+shift+a', lambda: on_hotkey(driver))

Object_Count = 0
if os.path.getsize("manga.json") != 3:
    Object_Count = Get_Last_Entry_Point("manga.json")

print("RDY")

while running:
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


        count = 0

        Curr_Iteration = {
        }

        try:
            driver.implicitly_wait(0)
            Only_One_Result = WebDriverWait(driver, 0.1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "focus"))
            )
            driver.implicitly_wait(10)
        except TimeoutException:
            continue

        Japanese_Word = driver.find_elements(By.CLASS_NAME, "japanese_word")

        for voc in Japanese_Word:

            voc.click()
            time.sleep(0.5)
            count = 0
            
#            linkable = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//li[@class='clearfix japanese_word']")))


            try:
                driver.implicitly_wait(0)
                no_matches = WebDriverWait(driver, 0.1).until(
                    EC.presence_of_element_located((By.ID, "no-matches"))
                )
                driver.implicitly_wait(10)
                continue
            except TimeoutException:
                pass

            element_test = driver.find_element(By.CLASS_NAME, "large-8")
            
            if is_element_empty(element_test):
                continue
            else:
                pass

            try:
                is_clickable = voc.find_element(By.TAG_NAME, 'a')
            except NoSuchElementException:
                continue
            
            KANJI = None
            FURIGANA = None
            try:
                driver.implicitly_wait(0)
                KANJI = WebDriverWait(voc, 0.1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "japanese_word__text_wrapper"))).text
                driver.implicitly_wait(10)
            except TimeoutException:
                continue
            
            try:
                driver.implicitly_wait(0)
                FURIGANA = WebDriverWait(voc, 0.1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "japanese_word__furigana_wrapper"))).text
                driver.implicitly_wait(10)
            except TimeoutException:
                continue

            try:
                if KANJI:
                    if not Check_Keys("manga.json", KANJI):
                        continue
                elif FURIGANA:
                    if not Check_Keys("manga.json", FURIGANA):
                        continue
            except IndexError:
                pass
            
            large_eight = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "large-8")))

            concept_light = large_eight.find_elements(By.CLASS_NAME, "concept_light")
            concept_light = concept_light[:3]
            count = 0

            Main_Japanese_Vocab_Driver = concept_light[0].find_elements(By.CLASS_NAME, "concept_light-representation")

            Main_English_Vocab_Driver = concept_light[0].find_elements(By.CLASS_NAME, "meaning-meaning")
            
            Main_Vocab_FURIGANA = Main_Japanese_Vocab_Driver[0].find_element(By.CLASS_NAME, "furigana")
            Main_Vocab_SPAN = Main_Vocab_FURIGANA.find_elements(By.TAG_NAME, "span")
            Main_Vocab_KANJI = Main_Japanese_Vocab_Driver[0].find_element(By.CLASS_NAME, "text").text

            picked_furigana = ""

            for i in Main_Vocab_SPAN:
                if i.text.strip():
                    picked_furigana += i.text
                else:
                    picked_furigana += "x"

                picked_furigana += ' '

            Main_Vocab_FURIGANA = picked_furigana
            
            if KANJI == "":
                KANJI = FURIGANA
                
            Curr_Iteration[KANJI] = {}
            Curr_Iteration[KANJI]["Instance Count"] = Object_Count
            if(FURIGANA):
                Curr_Iteration[KANJI]["Furigana"] = FURIGANA
                
            Curr_Iteration[KANJI]["Main Result"] = {}
            Curr_Iteration[KANJI]["Main Result"][Main_Vocab_KANJI] = {}
            Curr_Iteration[KANJI]["Main Result"][Main_Vocab_KANJI]["Furigana"] = Main_Vocab_FURIGANA
            Curr_Iteration[KANJI]["Main Result"][Main_Vocab_KANJI]["English Translation"] = {}
            Object_Count = Object_Count + 1
           
            some_count = 0
            for i in Main_English_Vocab_Driver[:3]:
                Vocab_Count = f"Vocab{some_count}"
                some_count = some_count + 1
                Curr_Iteration[KANJI]["Main Result"][Main_Vocab_KANJI]["English Translation"][Vocab_Count] = i.text

        File_Content = Read_Json("manga.json")

        try:
            File_Content[0].update(Curr_Iteration)

        except IndexError:
            File_Content.append(Curr_Iteration)
            
        with open("manga.json", 'w') as outfile:
            json.dump(File_Content, outfile, indent=4, ensure_ascii=False)

        clear = driver.find_element(By.CLASS_NAME, "search-form_clear-button_js").click()
    else:
        time_c = os.path.getctime(path)
        mod_file = time.ctime(time_c)

        time.sleep(0.5)
