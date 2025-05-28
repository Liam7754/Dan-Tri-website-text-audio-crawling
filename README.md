# 🕷️ DanTri Article Scraper with Audio Downloader

This Python script automates the process of scraping articles from the [Dân Trí](https://dantri.com.vn) news website. It extracts article titles, content, and downloadable audio files, saving them into organized folders.

## 📌 Features

- Crawls multiple pages of articles.
- Extracts article title and content.
- Switches voice options.
- Downloads audio files for each article.
- Saves both text and audio in separate folders.

## 🛠️ Requirements

- Python 3.12+
- Google Chrome
- ChromeDriver matching your Chrome version

## 🧰 Installation

Install the required Python packages:


pip install selenium requests

## 🚀 Usage


python dan_tri_crawl.py /path/to/chromedriver https://dantri.com.vn/
Arguments
/path/to/chromedriver: Absolute path to your chromedriver binary.

https://dantri.com.vn/: URL of the Dân Trí article listing page to start crawling from.

Output
Text_Content/: Contains .txt files with article titles and content.

Audio/: Contains .mp3 files of the text-to-speech audio.

## 📂 Folder Structure

css

├── scraper.py
├── Audio/
│   └── article-title.mp3
├── Text_Content/
│   └── article-title.txt

## ⚠️ Notes

Make sure the ChromeDriver version matches your installed version of Chrome.
The script uses class and attribute selectors that may change if Dân Trí updates their website layout.
Pages with no audio or missing elements will be skipped or logged with errors.

