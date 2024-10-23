import customtkinter as ctk
from homepage import show_homepage
from clist import create_list_flow
from vlists import view_lists
from bgroceries import browse_groceries
from srecipes import view_saved_recipes
from brecipes import browse_recipes

class AppController:
    def __init__(self, root):
        self.root = root
        self.grocery_lists = {}  # Central storage for all grocery lists
        self.done_items = {}     # Storage for completed items

        # Initialize the appearance mode to dark by default
        self.appearance_mode = "dark"
        ctk.set_appearance_mode(self.appearance_mode)
        ctk.set_default_color_theme("dark-blue")  # Set default color theme

        # Set window properties
        self.root.geometry("800x600")
        self.root.title("Grocery To-Do List")

        # Load the homepage
        self.show_homepage()

    def show_homepage(self):
        show_homepage(self.root, self)  # Passing self for access to central storage and navigation

    def show_create_list(self):
        create_list_flow(self.root, self)

    def show_view_lists(self):
        view_lists(self.root, self)

    def show_browse_groceries(self):
        browse_groceries(self.root, self)

    def show_saved_recipes(self):
        view_saved_recipes(self.root, self)

    def show_browse_recipes(self):
        browse_recipes(self.root, self)

def run_app():
    root = ctk.CTk()  # Initialize the main window
    app_controller = AppController(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()