from customtkinter import *
from PIL import Image
from datetime import datetime


class Utility:
    @staticmethod
    def format_currency(entry: CTkEntry) -> None:
        value = entry.get()

        value = value.replace(".", "").strip()

        if value:
            try:
                # Format as currency
                cursor_position = entry.index(INSERT)
                formatted_value = f"{int(value):,}".replace(",", ".")
                num_commas_before_cursor = (cursor_position - 1) // 3
                num_commas_after_cursor = len(formatted_value
                                              [:cursor_position + num_commas_before_cursor]) - cursor_position
                entry.delete(0, END)
                entry.insert(0, formatted_value)
                entry.icursor(cursor_position + num_commas_after_cursor)
            except ValueError:
                pass

    @staticmethod
    def format_currency_int(budget: int) -> str:
        formatted = f"{budget:,}".replace(",", ".")
        return "Rp" + formatted

    # def format_date(entry: CTkEntry) -> None:
    @staticmethod
    def create_ico():
        file = "../../img/" + input("Enter file name: ")

        img = Image.open(file)

        img = img.convert("RGBA")  # Ensure image is in RGB mode

        # Load the pixel data
        pixels = img.load()

        # Iterate through the pixels
        for i in range(img.width):
            for j in range(img.height):
                r, g, b, a = pixels[i, j]
                if a != 0:  # If the pixel is not transparent
                    pixels[i, j] = (255, 255, 255, a)  # Change to white, keep the same alpha

        size = int(input("Resize to: "))
        dim = (size, size)
        resized = img.resize(dim)

        newfile = "../../img/" + input("Enter output file name: ")

        resized.save(newfile)

    def resize_frame(root, frame: CTkFrame):
        frame_width = int(root.winfo_width() * 0.8)
        frame_height = int(root.winfo_height() * 0.8)
        frame.configure(width=frame_width, height=frame_height)

    @staticmethod
    def is_valid_date(date_str):
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False