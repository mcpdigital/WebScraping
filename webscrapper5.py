import tkinter as tk
from tkinter import ttk, filedialog
import requests
from bs4 import BeautifulSoup

class ScraperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraper")

        self.url_label = ttk.Label(master, text="URL:")
        self.url_entry = ttk.Entry(master, width=80)
        self.url_entry.insert(0, "https://")
        self.select_label = ttk.Label(master, text="Select:")
        self.select_entry = ttk.Entry(master, width=80)
        self.scrape_button = ttk.Button(master, text="Scrape", command=self.scrape)
        self.result_text = tk.Text(master, wrap="word")
        #self.result_text = tk.Text(master)
        self.save_button = ttk.Button(master, text="Save", command=self.save)
        self.save = self.save
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        # self.url_label.grid(row=0, column=0, sticky="w")
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.select_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.select_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        self.scrape_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.save_button.grid(row=2, column=1, padx=100, pady=5, sticky="w")
                # Configure rows and columns to resize automatically
        master.rowconfigure(3, weight=1)
        master.columnconfigure(1, weight=1)
       # master.rowconfigure(4, weight=1)
        #self.result_text.configure(state='disabled')

    def scrape(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'Content-Type': 'text/html'}
        url = self.url_entry.get()
        select = self.select_entry.get()

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        if select.startswith("."):
            results = soup.select(select)
        else:
            results = soup.find_all(select)

        self.result_text.configure(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"Found {len(results)} results:\n\n")

        count = 1
        for result in results:
            self.result_text.insert(tk.END, f"{select}{count}: {result}\n\n")
            count += 1

        self.result_text.configure(state='disabled')

    def save(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(self.result_text.get('1.0', tk.END))

root = tk.Tk()
scraper = ScraperGUI(root)
root.mainloop()
