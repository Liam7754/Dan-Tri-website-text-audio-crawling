import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from  selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import requests
import random
import time
import re
import os

def get_current_url():
    article_urls = set()
    while True:
        ### show current link ###
        ### show current link ###
        ### show current link ###
        print(f"📄 Crawling page: {DRIVER.current_url}")
        time.sleep(2)
        try:
            #Get element by class name article.list
            article_container = DRIVER.find_element(By.CLASS_NAME, "article.list")
            #Get property values of elements
            links = article_container.find_elements(By.TAG_NAME,"a")

            new_urls = {
                link.get_attribute("href")
                for link in links
            }

            print(f"➕ Found {len(new_urls)} new URLs on this page.")
            article_urls.update(new_urls)
        except Exception as e:
            print("❌ Error finding articles:", e)

        # Try to find and click the next page button
        try:
            next_button = DRIVER.find_element(By.CSS_SELECTOR, 'a.page-item.next')
            next_url = next_button.get_attribute("href")
            #check page
            if next_url is None:
                print("⛔ No more pages.")
                break
            DRIVER.get(next_url)
        except NoSuchElementException:
            print("✅ No 'Next' button found. Finished crawling.")
            break
        except Exception as e:
            print("❌ Error moving to next page:", e)
            break
    return article_urls

#Helper function to sanitize filenames
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)[:100]

# Download and save audio
def save_in_folder(audio_src,content,safe_title,title):
    cwd = os.getcwd()
    text_dir = os.path.join(cwd, "Text_Content")
    audio_dir = os.path.join(cwd, "Audio")
    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    try:
        audio_data = requests.get(audio_src).content
        audio_file_path = os.path.join(audio_dir, f"{safe_title}.mp3")
        with open(audio_file_path, "wb") as f:
            f.write(audio_data)
        print(f"💾 Saved audio to {audio_file_path}")
        # Save text content
        text_file_path = os.path.join(text_dir, f"{safe_title}.txt")
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n\n{content}")
        print(f"📁 Saved text to {text_file_path}")
    except Exception as e:
        print(f"⚠️ Failed to save audio: {e}")



#Get text and audio
def get_text_audio(article_urls):
    for url in article_urls:
        DRIVER.get(url)
        time.sleep(2)
        print(f"\n📄 Crawling: {url}")
        #Get title
        try:
            title = DRIVER.find_element(By.TAG_NAME,"h1").text
        except:
            title = "No title found"
        safe_title = sanitize_filename(title)

        ### Extract article content ###
        ### Extract article content ###
        ### Extract article content ###
        try:
            content = DRIVER.find_element(By.CLASS_NAME, "singular-sapo").text + "\n" + DRIVER.find_element(By.CLASS_NAME, "singular-content").text
        except:
            content = None

        ### Attempt to change voice ###
        ### Attempt to change voice ###
        ### Attempt to change voice ###
        previous_voice_text = None
        selected_voice_text = None
        try:
            voice_button = WebDriverWait(DRIVER, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Giọng đọc"]'))
            )
            voice_button.click()

            dropdown_ul = WebDriverWait(DRIVER, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[class*="tocgrbW68IWPB0ZbjBd8"]'))
            )

            voice_options = dropdown_ul.find_elements(By.TAG_NAME, "li")
            if len(voice_options) >= 3:
                selected_voice = random.choice(voice_options[:3])
                time.sleep(1)
                selected_voice_text = selected_voice.text
                selected_voice.click()
                print(f"🔄 Switched to voice: {selected_voice_text}")
                time.sleep(1)
            else:
                print("⚠️ Not enough voice options to switch.")
        except TimeoutException:
            print("❌ Voice dropdown or options did not appear in time.")
        except Exception as e:
            print("❌ Failed to switch voice:", e)

        # Determine if 'Đọc' button needs to be clicked
        need_to_click_doc = selected_voice_text is None or selected_voice_text == previous_voice_text
        previous_voice_text = selected_voice_text

        if need_to_click_doc:
            try:
                doc_button = WebDriverWait(DRIVER, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Đọc"]'))
                )
                DRIVER.execute_script("arguments[0].scrollIntoView({block: 'center'});", doc_button)
                time.sleep(0.5)

                try:
                    doc_button.click()
                except Exception:
                    print("⚠️ Standard click failed, trying JS click...")
                print("✅ Clicked Đọc (read aloud) button")
                time.sleep(1)
            except Exception as e:
                print("❌ Failed to click Đọc button:", e)
        else:
            time.sleep(3)

        ### Get audio source ###
        ### Get audio source ###
        ### Get audio source ###
        audio_src = ""
        try:
            audio_tag = DRIVER.find_element(By.TAG_NAME, 'audio')
            audio_src = audio_tag.get_attribute('src')
            print("🎧 Audio URL:", audio_src)
        except Exception as e:
            print("❌ No audio found:", e)

        if audio_src and content:
            save_in_folder(audio_src,content,safe_title,title)


def main():
    article_urls = get_current_url()
    get_text_audio(article_urls)

if __name__ == "__main__":
    args = sys.argv
    if args is not None:
        if len(args) != 3:
            raise Exception("You must pass a chrome driver path and dan tri url path - only.")
        else:
            service_path, url_path = args[1:]
    else:
        service_path = ""
        url_path = ""
    if service_path and url_path:
        SERVICE = Service(executable_path=service_path)
        DRIVER = webdriver.Chrome(service=SERVICE)
        BASE_URL = url_path
        DRIVER.get(BASE_URL)
        main()



