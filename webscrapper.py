import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tkinter import *


class WebScraper:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraper")

        # URL input field
        self.url_label = Label(master, text="Enter URL:")
        self.url_label.pack()
        self.url_entry = Entry(master, width=100)
        self.url_entry.pack()

        # Search input field
        self.search_label = Label(master, text="Enter Search Term:")
        self.search_label.pack()
        self.search_entry = Entry(master, width=100)
        self.search_entry.pack()

        # Search options dropdown
        self.options_label = Label(master, text="Select Search Option:")
        self.options_label.pack()
        self.options = StringVar(master)
        self.options.set("Text")  # default value
        self.options_dropdown = OptionMenu(master, self.options, "Text", "Class", "Tag")
        self.options_dropdown.pack()

        # Scraper selection dropdown
        self.scraper_label = Label(master, text="Select Scraper:")
        self.scraper_label.pack()
        self.scraper = StringVar(master)
        self.scraper.set("BeautifulSoup")  # default value
        self.scraper_dropdown = OptionMenu(master, self.scraper, "BeautifulSoup", "Selenium")
        self.scraper_dropdown.pack()

        # Scrape button
        self.scrape_button = Button(master, text="Scrape", command=self.scrape)
        self.scrape_button.pack()

        # Output field
        self.output = Text(master, width=100, height=30)
        self.output.pack()

    def scrape(self):
        url = self.url_entry.get()
        search = self.search_entry.get()
        option = self.options.get()
        scraper = self.scraper.get()

        if scraper == "BeautifulSoup":
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            if option == "Text":
                result = soup.find_all(text=search)
            elif option == "Class":
                result = soup.find_all(class_=search)
            elif option == "Tag":
                result = soup.find_all(search)

        elif scraper == "Selenium":
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')

            browser = webdriver.Chrome(options=options)
            browser.get(url)

            if option == "Text":
                result = browser.find_elements_by_xpath("//*[contains(text(), '{}')]".format(search))
            elif option == "Class":
                result = browser.find_elements_by_class_name(search)
            elif option == "Tag":
                result = browser.find_elements_by_tag_name(search)

            browser.quit()

        self.output.delete('1.0', END)
        self.output.insert(END, result)


root = Tk()
web_scraper = WebScraper(root)
root.mainloop()
