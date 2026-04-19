import requests
import os
import webbrowser
import math
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk

CURRENT_VERSION = "1.0.0"

VERSION_URL = "https://raw.githubusercontent.com/JDizzle9/CraftingCalculator/main/version.txt"
DOWNLOAD_PAGE = "https://github.com/JDizzle9/CraftingCalculator/releases/latest"


class Result:
    def __init__(self, max_crafts, leftover_m1, leftover_m2, leftover_m3,
                 converted_m1, converted_m2):
        self.max_crafts = max_crafts
        self.leftover_m1 = leftover_m1
        self.leftover_m2 = leftover_m2
        self.leftover_m3 = leftover_m3

        self.converted_m1 = math.ceil(converted_m1 / 100)
        self.converted_m2 = math.ceil(converted_m2 / 50)

    def __str__(self):
        return (
            f"Max Crafts: {self.max_crafts}\n"
            f"Convert Ancient Relic: {self.converted_m1} Times\n"
            f"Convert Rare Relic: {self.converted_m2} Times\n"
            f"Leftover Ancient Relic: {self.leftover_m1}\n"
            f"Leftover Rare Relic: {self.leftover_m2}\n"
            f"Leftover Abidos Relic: {self.leftover_m3}"
        )


def calculate_with_conversion(m1, m2, m3, req_m1, req_m2, req_m3):
    m1_to_dust = 0.8
    m2_to_dust = 1.6
    dust_to_m3 = 0.1

    for crafts in range(1000, 0, -1):
        needed_m1 = req_m1 * crafts
        needed_m2 = req_m2 * crafts
        needed_m3 = req_m3 * crafts

        max_convertable_m1 = m1 - needed_m1
        max_convertable_m2 = m2 - needed_m2

        if max_convertable_m1 < 0 or max_convertable_m2 < 0:
            continue

        missing_m3 = max(0, needed_m3 - m3)
        dust_needed = missing_m3 / dust_to_m3

        for converted_m1 in range(max_convertable_m1 + 1):
            dust_from_m1 = converted_m1 * m1_to_dust
            remaining_dust_needed = dust_needed - dust_from_m1

            converted_m2 = 0
            if remaining_dust_needed > 0:
                converted_m2 = math.ceil(remaining_dust_needed / m2_to_dust)

            if converted_m2 <= max_convertable_m2:
                final_m1_left = m1 - needed_m1 - converted_m1
                final_m2_left = m2 - needed_m2 - converted_m2
                final_m3_left = (
                    m3
                    + int((dust_from_m1 + converted_m2 * m2_to_dust) * dust_to_m3)
                    - needed_m3
                )

                return Result(
                    crafts,
                    final_m1_left,
                    final_m2_left,
                    final_m3_left,
                    converted_m1,
                    converted_m2
                )

    return None


def create_tab(parent, req_m1, req_m2, req_m3):
    frame = tk.Frame(parent, bg="#616161")

    # Center container
    content = tk.Frame(frame, bg="#616161")
    content.place(relx=0.5, rely=0.5, anchor="center")

    # --- Fields ---
    tk.Label(content, text="Ancient Relic:", bg="#383838", fg="#ffffff").grid(row=0, column=0, pady=(0, 2))
    field1 = tk.Entry(content, justify="center", width=20)
    field1.grid(row=1, column=0, pady=(0, 10))

    tk.Label(content, text="Rare Relic:", bg="#383838", fg="#ffffff").grid(row=2, column=0, pady=(0, 2))
    field2 = tk.Entry(content, justify="center", width=20)
    field2.grid(row=3, column=0, pady=(0, 10))

    tk.Label(content, text="Abidos Relic:", bg="#383838", fg="#ffffff").grid(row=4, column=0, pady=(0, 2))
    field3 = tk.Entry(content, justify="center", width=20)
    field3.grid(row=5, column=0, pady=(0, 15))

    # Result box
    result_area = scrolledtext.ScrolledText(content, width=40, height=8)
    result_area.grid(row=7, column=0, pady=10)
    result_area.configure(state="disabled")

    # --- Logic ---
    def on_calculate():
        try:
            m1 = int(field1.get())
            m2 = int(field2.get())
            m3 = int(field3.get())

            result = calculate_with_conversion(m1, m2, m3, req_m1, req_m2, req_m3)

            result_area.configure(state="normal")
            result_area.delete("1.0", tk.END)

            if result:
                result_area.insert(tk.END, str(result))
            else:
                result_area.insert(tk.END, "No valid crafting solution found.")

            result_area.configure(state="disabled")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")

    # Button (AFTER function is defined)
    tk.Button(content, text="Calculate", command=on_calculate).grid(row=6, column=0, pady=10)

    return frame

def check_for_update():
    try:
        latest_version = requests.get(VERSION_URL, timeout=5).text.strip()

        if latest_version != CURRENT_VERSION:
            return latest_version
    except:
        pass

    return None


def main():
    latest = check_for_update()

    if latest:
        response = messagebox.askyesno(
            "Update Available",
            f"A new version ({latest}) is available.\n\nDo you want to download it?"
        )

        if response:
            webbrowser.open(DOWNLOAD_PAGE)
    root = tk.Tk()
    root.title("Crafting Calculator")
    root.geometry("600x450")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Tabs
    tab1 = create_tab(notebook, 86, 45, 33)
    notebook.add(tab1, text="Abidos Fusion Material")

    tab2 = create_tab(notebook, 112, 59, 43)
    notebook.add(tab2, text="Superior Abidos Fusion Material")

    root.mainloop()


if __name__ == "__main__":
    main()

