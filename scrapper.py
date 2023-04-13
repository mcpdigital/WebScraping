import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

class ScraperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraper")

        self.label_url = tk.Label(master, text="Enter website URL (up to 100 characters):")
        self.label_url.pack()

        self.entry_url = tk.Entry(master, width=100)
        self.entry_url.pack()

        self.label_tags = tk.Label(master, text="Enter HTML tags (up to 100 characters):")
        self.label_tags.pack()

        self.entry_tags = tk.Entry(master, width=100)
        self.entry_tags.pack()

        self.label_method = tk.Label(master, text="Select scraping method:")
        self.label_method.pack()

        self.method = tk.StringVar()
        self.method.set("Selenium")  # default value
        self.dropdown_method = tk.OptionMenu(master, self.method, "Selenium", "BeautifulSoup")
        self.dropdown_method.pack()

        self.button_scrape = tk.Button(master, text="Scrape", command=self.scrape)
        self.button_scrape.pack()

        self.result = tk.StringVar()
        self.label_result = tk.Label(master, textvariable=self.result)
        self.label_result.pack()

    def scrape(self):
        url = self.entry_url.get()
        tags = self.entry_tags.get()
        method = self.method.get()

        if method == "Selenium":
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            driver.get(url)

            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, tags))
                )
                result = element.text
            finally:
                driver.quit()
        elif method == "BeautifulSoup":
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            element = soup.select_one(tags)
            result = element.text

        self.result.set(result)

root = tk.Tk()
scraper_gui = ScraperGUI(root)
root.mainloop()
