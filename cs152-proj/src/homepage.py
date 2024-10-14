#using customtkinter by Tom Schimansky
import customtkinter as ctk

class groceryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Grocery To-Do List")
        self.master.minsize(500, 500)
        self.master.grid_columnconfigure((0), weight=1)

        self.create_home_page()

    def create_home_page(self):
        header_label = ctk.CTkLabel(self.master, text="Homepage")
        header_label.grid(padx=5, pady=5)

        recipe_button = ctk.CTkButton(self.master, text="See Saved Recipes", command=self.open_recipe_window)
        recipe_button.grid(pady=10)

        grocery_button = ctk.CTkButton(self.master, text="See Grocery List", command=self.open_grocery_window)
        grocery_button.grid(pady=10)

    def open_recipe_window(self):
        recipe_window = ctk.CTkToplevel(self.master)
        recipe_window.title("Saved Recipes")
        recipe_window.minsize(500, 500)
        recipe_window.transient(self.master)

        header_label = ctk.CTkLabel(recipe_window, text="Saved Recipes")
        header_label.grid(pady=5)

    def open_grocery_window(self):
        grocery_window = ctk.CTkToplevel(self.master)
        grocery_window.title("Saved Groceries")
        grocery_window.minsize(500, 500)
        grocery_window.transient(self.master)

        header_label = ctk.CTkLabel(grocery_window, text="Grocery List")
        header_label.grid(pady=5)

        purchase_history_button = ctk.CTkButton(grocery_window, text="See Purchase History", command=self.show_purchase_history)
        purchase_history_button.grid(pady=10)

    def show_purchase_history(self):
        purchase_history_window = ctk.CTkToplevel(self.master)
        purchase_history_window.title("Purchase History")
        purchase_history_window.minsize(500, 500)
        purchase_history_window.transient(self.master)

        header_label = ctk.CTkLabel(purchase_history_window, text="Purchase History")
        header_label.grid(pady=5)

if __name__ == "__main__":
    root = ctk.CTk()
    app = groceryApp(root)

    root.mainloop()
