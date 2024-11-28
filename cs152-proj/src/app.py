import customtkinter as ctk
from homepage import show_homepage
from clist import create_list_flow
from vlists import view_lists
from bgroceries import browse_groceries
from srecipes import view_saved_recipes
from brecipes import browse_recipes
import json
import os

class AppController:
    def __init__(self, root):
        self.root = root
        self.grocery_lists = self.load_data("grocery_lists.json")  # Load grocery lists
        self.saved_recipes = self.load_data("saved_recipes.json")  # Load saved recipes

        # Initialize the appearance mode to dark by default
        self.appearance_mode = "dark"
        ctk.set_appearance_mode(self.appearance_mode)
        ctk.set_default_color_theme("dark-blue")  # Set default color theme

        # Set window properties
        self.root.geometry("800x600")
        self.root.title("Grocery To-Do List")

        # Save data on initialization
        self.save_data(self.grocery_lists, "grocery_lists.json")
        self.save_data(self.saved_recipes, "saved_recipes.json")

        # Load the homepage
        self.show_homepage()

    def save_data(self, data, file_name):
        """Save data to a JSON file."""
        try:
            file_path = os.path.join(os.path.dirname(__file__), file_name)
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving data to {file_name}: {e}")

    def load_data(self, file_name):
        """Load data from a JSON file."""
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {file_name}. Returning empty data.")
            except Exception as e:
                print(f"Error loading data from {file_name}: {e}")
        return {}


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
