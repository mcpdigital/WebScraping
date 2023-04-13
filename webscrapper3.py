import tkinter as tk
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class WebScraper:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraper")

        # URL input field
        self.url_label = tk.Label(master, text="Enter URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(master, width=100)
        self.url_entry.pack()

        # Search input field
        self.search_label = tk.Label(master, text="Enter Search Term:")
        self.search_label.pack()
        self.search_entry = tk.Entry(master, width=100)
        self.search_entry.pack()

        # Search options dropdown
        self.options_label = tk.Label(master, text="Select Search Option:")
        self.options_label.pack()
        self.options = tk.StringVar(master)
        self.options.set("Text")  # default value
        self.options_dropdown = tk.OptionMenu(master, self.options, "Text", "Class", "Tag", "none")
        self.options_dropdown.pack()

        # Scraper selection dropdown
        self.scraper_label = tk.Label(master, text="Select Scraper:")
        self.scraper_label.pack()
        self.scraper = tk.StringVar(master)
        self.scraper.set("BeautifulSoup")  # default value
        self.scraper_dropdown = tk.OptionMenu(master, self.scraper, "BeautifulSoup", "Selenium")
        self.scraper_dropdown.pack()

        # Scrape button
        self.scrape_button = tk.Button(master, text="Scrape", command=self.scrape)
        self.scrape_button.pack()

        # Output field
        self.output = tk.Text(master, width=100, height=30)
        self.output.pack()

    def scrape(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'Content-Type': 'text/html'}

        url = self.url_entry.get()
        search = self.search_entry.get()
        option = self.options.get()
        scraper = self.scraper.get()

        if scraper == "BeautifulSoup":
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            if option == "Text":
                result = [text for text in soup.stripped_strings if search in text]
                #result = soup.find_all(string=search)
            elif option == "Class":
                result = soup.find_all(class_=search)
            elif option == "Tag":
                result = soup.find_all(search)
            elif option == "none":
                result = soup.find_all(string=search)

        elif scraper == "Selenium":
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('user-agent=' + headers['User-Agent'])
            options.add_argument('content-type=' + headers['Content-Type'])

            browser = webdriver.Chrome(options=options)
            browser.get(url)

            if option == "Text":
                result = browser.find_elements(By.XPATH, "//*[contains(text(), '{}')]".format(search))
            elif option == "Class":
                result = browser.find_elements_by_class_name(search)
            elif option == "Tag":
                result = browser.find_elements_by_tag_name(search)
            elif option == "none":
                result = "Nothing"

            browser.quit()

        self.output.delete('1.0', tk.END)
        self.output.insert(tk.END, result)
        


root = tk.Tk()
web_scraper = WebScraper(root)
root.mainloop()
