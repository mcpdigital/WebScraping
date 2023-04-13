from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import json
import tkinter as tk
from tkinter import ttk


class WebScraper(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Web Scraper")

        # Create search input field
        self.search_label = ttk.Label(self, text="Search:")
        self.search_label.pack(side="left")
        self.search_entry = ttk.Entry(self, width=30)
        self.search_entry.pack(side="left")

        # Create dropdown for search options
        self.option_label = ttk.Label(self, text="Search Options:")
        self.option_label.pack(side="left")
        self.search_options = ttk.Combobox(self, width=15, values=["Text", "Class", "Tag", "none"])
        self.search_options.pack(side="left")

        # Create dropdown for save options
        self.save_label = ttk.Label(self, text="Save Results As:")
        self.save_label.pack(side="left")
        self.save_options = ttk.Combobox(self, width=15, values=["None", "CSV", "JSON"])
        self.save_options.pack(side="left")

        # Create submit button
        self.submit_button = ttk.Button(self, text="Scrape", command=self.save_results)
        self.submit_button.pack(side="left")

        # Create output field
        self.output = tk.Text(self, height=20, width=50)
        self.output.pack(side="bottom")

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

        # Save results to file if option is selected
        save_option = self.save_options.get()
        if save_option != "None":
            filename = f"{search}_{option}_{scraper}_results"
            if save_option == "CSV":
                with open(f"{filename}.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    for item in result:
                        writer.writerow([item])
            elif save_option == "JSON":
                with open(f"{filename}.json", 'w') as file:
                    json.dump(result, file)








