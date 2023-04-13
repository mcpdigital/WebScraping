import tkinter as tk
from tkinter import ttk, filedialog
import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd



class ScraperGUI:
    def __init__(self, master):
        self.master = master
        master.title("EDA Web Scraper Standalone - Marcelo C. Plaza")
        master.geometry("1280x720")
       
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
        # if(select.rfind(".") == -1):
        if select.startswith(".") or select.rfind(".") != -1 or select.rfind(" ") != -1:
            results = soup.select(select)
        else:
            results = soup.find_all(select)
        
        self.result_text.configure(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_list = []  # save all results in a class attribute
        count = 1
        for result in results:
            result_dict = {'Result Number': count, 'Result Text': str(result)}
            self.result_list.append(result_dict)  # add result to list
            self.result_text.insert(tk.END, f"{select}{count}: {result}\n\n")
            count += 1
        
        self.result_text.configure(state='disabled')
        
    def save(self):
        # use file dialog to get the filename and file type to save
        filetypes = [('JSON files', '*.json'), ('CSV files', '*.csv')]
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=filetypes)

        if filename:
            selected_results = []  # list to save selected results

            # create a Toplevel window to display checkboxes for each result
            top = tk.Toplevel(self.master)
            top.title("Select Results to Save")
            top.geometry("1280x720")

            # create a canvas to hold the checkboxes
            canvas = tk.Canvas(top)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # add a scrollbar to the canvas
            yscrollbar = ttk.Scrollbar(top, orient=tk.VERTICAL, command=canvas.yview)
            yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.configure(yscrollcommand=yscrollbar.set)

            # create a frame to hold the checkboxes inside the canvas
            checkbox_frame = tk.Frame(canvas)
            checkbox_frame.columnconfigure(0, weight=1)
            canvas.create_window((0, 0), window=checkbox_frame, anchor=tk.NW)

            # create a checkbox for each result
            checkboxes = []
            for i, result in enumerate(self.result_list):
                var = tk.BooleanVar(value=True)
                checkbox = ttk.Checkbutton(checkbox_frame, text=f"{result['Result Text']}", variable=var)
                checkbox.grid(row=i+2, column=0, padx=5, pady=5, sticky="w")
                checkboxes.append(var)

            # update the canvas scroll region
            checkbox_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox(tk.ALL))

            # create a button to save selected results and close the window
            def save_selected():
                for i, checkbox in enumerate(checkboxes):
                    if checkbox.get():
                        selected_results.append(self.result_list[i])
                with open(filename, 'w', encoding='utf-8') as file:
                    if filename.endswith('.json'):
                        file.write(json.dumps(selected_results, ensure_ascii=False, indent=4))
                    elif filename.endswith('.csv'):
                        writer = csv.writer(file)
                        writer.writerow(['Result Number', 'Result Text'])
                        for result in selected_results:
                            writer.writerow([result['Result Number'], result['Result Text']])
                top.destroy()
                # create a pandas dataframe from the selected results
                df = pd.DataFrame(selected_results)

                # perform any desired operations on the dataframe
                # example: print the first 5 rows of the dataframe
                print(df.head())

        save_button = ttk.Button(checkbox_frame, text="Save Selected Results", command=save_selected)
        save_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")



root = tk.Tk()
# create a style object
style = ttk.Style()

# set the theme
style.theme_use('vista')
scraper = ScraperGUI(root)
root.mainloop()