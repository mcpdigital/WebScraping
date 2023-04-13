import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json


class WebScraper:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraper")
        
        self.url_label = ttk.Label(master, text="URL:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.url_entry = ttk.Entry(master)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.search_label = ttk.Label(master, text="Search Term:")
        self.search_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.search_entry = ttk.Entry(master)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.submit_button = ttk.Button(master, text="Search", command=self.scrape)
        self.submit_button.grid(row=2, column=0, padx=5, pady=5)
        
        self.result_label = ttk.Label(master, text="Results:")
        self.result_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.result_textbox = tk.Text(master, height=10, width=50)
        self.result_textbox.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        self.save_button = ttk.Button(master, text="Save", command=self.save)
        self.save_button.grid(row=4, column=1, padx=5, pady=5)
        
        self.result_list = []  # list to save scraped results
    
    def scrape(self):
        url = self.url_entry.get()
        search_term = self.search_entry.get()
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all(string=lambda text: search_term in text.lower())
        self.result_list = [str(result) for result in results]
        self.result_textbox.delete('1.0', tk.END)  # clear the textbox
        self.result_textbox.insert('1.0', '\n'.join(self.result_list))  # insert results into the textbox
        
    def save(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, 'w', encoding='utf-8') as file:
                selected_results = []  # list to save selected results
                for i, result in enumerate(self.result_list):
                    # create a checkbox for each result to allow selection
                    var = tk.BooleanVar(value=False)
                    checkbox = ttk.Checkbutton(self.master, variable=var)
                    checkbox.grid(row=i+4, column=0, padx=5, pady=5, sticky="w")
                    self.master.update()
                    # wait for the user to select which results to save
                    self.master.wait_variable(var)
                    checkbox.destroy()
                    # add selected result to list
                    if var.get():
                        selected_results.append(result)
                # save selected results to file
                file.write(json.dumps(selected_results, ensure_ascii=False, indent=4))
        

if __name__ == '__main__':
    root = tk.Tk()
    app = WebScraper(root)
    root.mainloop()
