import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests


def scrape_website():
    url = url_entry.get()
    selected_option = option_var.get()

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        if selected_option == "Text Content":
            content = soup.get_text()
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, content)
        elif selected_option == "Links":
            links = soup.find_all('a')
            result_text.delete(1.0, tk.END)
            for link in links:
                result_text.insert(tk.END, link.get('href') + '\n')
        elif selected_option == "Images":
            images = soup.find_all('img')
            result_text.delete(1.0, tk.END)
            for image in images:
                result_text.insert(tk.END, image.get('src') + '\n')
        elif selected_option == "Metadata":
            meta_tags = soup.find_all('meta')
            result_text.delete(1.0, tk.END)
            for meta_tag in meta_tags:
                result_text.insert(tk.END, meta_tag.attrs.get('content', '') + '\n')
        elif selected_option == "Tables":
            tables = soup.find_all('table')
            result_text.delete(1.0, tk.END)
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    for column in columns:
                        result_text.insert(tk.END, column.get_text() + '\t')
                    result_text.insert(tk.END, '\n')
                result_text.insert(tk.END, '\n')
        elif selected_option == "Forms":
            forms = soup.find_all('form')
            result_text.delete(1.0, tk.END)
            for form in forms:
                form_details = ""
                inputs = form.find_all('input')
                for input_tag in inputs:
                    form_details += f"Input: {input_tag.get('name')} Type: {input_tag.get('type')}\n"
                result_text.insert(tk.END, form_details + '\n')
    else:
        messagebox.showerror("Error", "Failed to retrieve the webpage.")


def save_to_file(data):
    filename = "scraped_data.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)


def save_data():
    data = result_text.get(1.0, tk.END)
    save_to_file(data)
    messagebox.showinfo("Success", "Data saved to file.")


root = tk.Tk()
root.title("Web Scraping Tool")

url_label = ttk.Label(root, text="Enter URL:")
url_label.grid(row=0, column=0, padx=5, pady=5)
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

option_label = ttk.Label(root, text="Select option:")
option_label.grid(row=1, column=0, padx=5, pady=5)
options = ["Text Content", "Links", "Images", "Metadata", "Tables", "Forms"]
option_var = tk.StringVar()
option_menu = ttk.OptionMenu(root, option_var, *options)
option_menu.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

scrape_button = ttk.Button(root, text="Scrape", command=scrape_website)
scrape_button.grid(row=2, column=1, padx=5, pady=5)

save_button = ttk.Button(root, text="Save", command=save_data)
save_button.grid(row=2, column=2, padx=5, pady=5)

result_text = tk.Text(root, height=20, width=80)
result_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
