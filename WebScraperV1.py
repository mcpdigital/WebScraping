import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd

class ScraperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraper - Marcelo C. Plaza")
        master.geometry("1280x1100")

        self.url_label = ttk.Label(master, text="URL:")
        self.url_entry = ttk.Entry(master, width=80)
        self.url_entry.insert(0, "https://mercadolivre.com.br/")
        self.select_label = ttk.Label(master, text="Search html tags, css classes:")
        self.select_entry = ttk.Entry(master, width=80)
        self.columns_label = ttk.Label(master, text="Columns Names:\nLeave blank defaults to\nsearch string")

        # Add 5 input fields for saving columns
        self.save_entries = [ttk.Entry(master, width=80) for _ in range(5)]

        # Add 5 input fields for custom column names
        self.column_name_entries = [ttk.Entry(master, width=20) for _ in range(5)]

        self.scrape_button = ttk.Button(master, text="Scrape", command=self.scrape)
        self.search_button = ttk.Button(master, text="Search", command=self.search)
        self.result_text = tk.Text(master, wrap="word")
        self.save_button = ttk.Button(master, text="Save", command=self.save)

        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.select_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.select_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        self.columns_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.search_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.save_button.grid(row=2, column=1, padx=100, pady=5, sticky="w")
        # Place the save entries in the grid
        for i, entry in enumerate(self.save_entries):
            entry.grid(row=i + 3, column=1, padx=5, pady=5, sticky="we")

        # Place the column name entries in the grid
        for i, entry in enumerate(self.column_name_entries):
            entry.grid(row=i + 3, column=0, padx=5, pady=5, sticky="w")

        
        self.scrape_button.grid(row=9, column=1, padx=5, pady=5, sticky="w")
        self.result_text.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        

        master.rowconfigure(10, weight=1)
        master.columnconfigure(1, weight=1)




    def search(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'Content-Type': 'text/html'}
        url = self.url_entry.get()
        select = self.select_entry.get()

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        # if(select.rfind(".") == -1):
        if (select.startswith(".") or select.rfind(".") != -1 or select.rfind(" ") != -1):
            results = soup.select(select)
        else:
            results = soup.find_all(select)
        
        
        self.result_text.configure(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_list = []  # save all results in a class attribute
        count = 1
        for result in results:
            
            result_dict = {'Result Number': count, 'Result Text': str(result.text.strip())}
            self.result_list.append(result_dict)  # add result to list
            self.result_text.insert(tk.END, f"{select}  #{count}: {result} -> {result.text.strip()}\n\n")
            count += 1
        
        self.result_text.configure(state='disabled')

    def scrape(self):
        # Combine the column names and values from the save_entries
        columns = [entry.get() for entry in self.save_entries if entry.get()]
        if not columns:
            messagebox.showerror("Error", "No columns to save.")
            return

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Content-Type": "text/html",
        }
        url = self.url_entry.get()
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Perform searches for each of the columns
        column_results = []
        for column in columns:
            if column.startswith(".") or column.rfind(".") != -1 or column.rfind(" ") != -1:
                results = soup.select(column)
            else:
                results = soup.find_all(column)

            column_results.append([result.text.strip() for result in results])

        # Create a pandas dataframe with the results
        max_rows = max([len(column_data) for column_data in column_results])
        data = []
        for row_idx in range(max_rows):
            row = [column_data[row_idx] if row_idx < len(column_data) else '' for column_data in column_results]
            data.append(row)
        df = pd.DataFrame(data, columns=columns)

        # Replace default column names with custom names if provided
        custom_columns = [entry.get() for entry in self.column_name_entries]
        final_columns = {default: custom if custom else default for custom, default in zip(custom_columns, columns)}
        df.rename(columns=final_columns, inplace=True)

        # Save the results as a CSV file
        filetypes = [('JSON files', '*.json'), ('CSV files', '*.csv')]
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=filetypes)

        if filename:
            if filename.endswith('.csv'):
                df.to_csv(filename, index=False, encoding='utf-8')
            elif filename.endswith('.json'):
                df.to_json(filename, index=False, encoding='utf-8')

            # Perform any desired operations on the dataframe
            # Example: print the first 5 rows of the dataframe
            print(df.head())


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
style = ttk.Style()
style.theme_use('vista')
scraper = ScraperGUI(root)
root.mainloop()

# USE THIS TO FIND PRICE IN MERCADOLIVRE.COM div.dynamic-carousel__item-container span.dynamic-carousel__price span
# USE THIS TO FIND TITULO IN MERCADOLIVRE.COM div.dynamic-carousel__item-container h3.dynamic-carousel__title