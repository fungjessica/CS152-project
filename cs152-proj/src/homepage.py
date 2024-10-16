#using customtkinter by Tom Schimansky
import customtkinter as ctk
import tkinter.font as tkf

class groceryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Grocery To-Do List")
        self.master.minsize(500, 500)
        self.master.grid_columnconfigure((0), weight=1)

        self.saved_groceries = []
        self.purchased_groceries = []

        self.create_home_page()

    #function to create homepage window
    def create_home_page(self):
        header_label = ctk.CTkLabel(self.master, text="Homepage", font=("Helvetica", 20, "bold"))
        header_label.grid(padx=5, pady=5)

        recipe_button = ctk.CTkButton(self.master, text="See Saved Recipes", command=self.open_recipe_window)
        recipe_button.grid(pady=10)

        grocery_button = ctk.CTkButton(self.master, text="See Grocery List", command=self.open_grocery_window)
        grocery_button.grid(pady=10)

        browse_groceries_button = ctk.CTkButton(self.master, text="Browse Groceries", command=self.browse_groceries_window)
        browse_groceries_button.grid(pady=10)

    #function to create browseable grocery window
    def browse_groceries_window(self):
        all_groceries_window = ctk.CTkToplevel(self.master)
        all_groceries_window.title("Grocery Shopping")
        all_groceries_window.minsize(500,500)
        all_groceries_window.transient(self.master)
        all_groceries_window.grid_columnconfigure((0), weight=1)

        header_label = ctk.CTkLabel(all_groceries_window, text="Add Groceries", font=("Helvetica", 20, "bold"))
        header_label.grid(padx=5, pady=5)

        groceries_list = ["Lettuce", "Potatos", "Tomatoes", "Apples", "Bananas", "Ice Cream"]

        #iterate through grocery list and add to checkbox
        self.select_groceries = {}
        row_index = 1
        for item in groceries_list:
            var = ctk.StringVar()
            checkbox = ctk.CTkCheckBox(all_groceries_window, text=item, variable=var, onvalue=item, offvalue="")
            checkbox.grid(row=row_index, column=0, pady=5)
            self.select_groceries[item]=var
            row_index+=1

        self.popup_label = ctk.CTkLabel(all_groceries_window, text="")
        self.popup_label.grid(pady=10)

        save_groceries_button = ctk.CTkButton(all_groceries_window, text="Save Selected Groceries", command=self.save_selected_groceries)
        save_groceries_button.grid(pady=10)
   
    #function to hide label
    def hide_label(self):
        self.popup_label.configure(text="")

    #function to save selected groceries and shows pop up label
    def save_selected_groceries(self):
        for grocery, var in self.select_groceries.items():
            if var.get():
                if grocery not in self.saved_groceries:
                    self.saved_groceries.append(grocery)

        self.popup_label.configure(text="Groceries Saved")
        self.popup_label.grid(pady=10)
        self.master.after(5000, self.hide_label)

    #function to save groceries to purchase history window
    def update_purchased_groceries(self):
        for grocery, var in self.updated_groceries.items():
            if var.get():
                if grocery not in self.purchased_groceries:
                    self.purchased_groceries.append(grocery)

    #function to create recipe window
    def open_recipe_window(self):
        recipe_window = ctk.CTkToplevel(self.master)
        recipe_window.title("Saved Recipes")
        recipe_window.minsize(500, 500)
        recipe_window.transient(self.master)
        recipe_window.grid_columnconfigure((0), weight=1)

        header_label = ctk.CTkLabel(recipe_window, text="Saved Recipes", font=("Helvetica", 20, "bold"))
        header_label.grid(padx=5, pady=5)

    #function to create saved groceries window
    def open_grocery_window(self):
        grocery_window = ctk.CTkToplevel(self.master)
        grocery_window.title("Saved Groceries")
        grocery_window.minsize(500, 500)
        grocery_window.transient(self.master)
        grocery_window.grid_columnconfigure((0), weight=1)

        header_label = ctk.CTkLabel(grocery_window, text="Grocery List", font=("Helvetica", 20, "bold"))
        header_label.grid(row=0, column=0,pady=5)
        purchased_label = ctk.CTkLabel(grocery_window, text="Purchased?", font=("Helvetica", 20, "bold"))
        purchased_label.grid(row=0, column=1, padx=5, pady=5)

        #placeholder rows
        grocery_window.grid_rowconfigure(1, weight=1)
        grocery_window.grid_rowconfigure(2, weight=1)
        grocery_window.grid_rowconfigure(3, weight=1)
        grocery_window.grid_rowconfigure(4, weight=1)

        '''
        self.input_groceries = ctk.CTkTextbox(grocery_window, height=25)
        self.input_groceries.insert("0.0", "insert personal items")
        self.input_groceries.grid(row=5, pady=10)
        '''

        #grocery_window.grid_rowconfigure(5, weight=1)
        update_button = ctk.CTkButton(grocery_window, text="Update Items", command=self.update_purchased_groceries)
        update_button.grid(row=5, column=1, sticky="s", pady=5)

        #add_button = ctk.CTkButton(grocery_window, text="Add", command=self.add_text)
        #add_button.grid(row=5, padx=10)

        purchase_history_button = ctk.CTkButton(grocery_window, text="See Purchase History", command=self.show_purchase_history)
        purchase_history_button.grid(row=5, column=0, sticky="s", pady=5)

        self.updated_groceries={}
        #iterate through saved groceries and show label
        if self.saved_groceries:
            for idx, grocery in enumerate(self.saved_groceries, start=1):
                grocery_label = ctk.CTkLabel(grocery_window, text=grocery)
                purchase_checkbox = ctk.CTkCheckBox(grocery_window, text="Yes")
                grocery_label.grid(row=idx, column=0)
                purchase_checkbox.grid(row=idx, column=1)

                self.updated_groceries[grocery] = purchase_checkbox

    '''
    def add_text(self):
        user_input = self.input_groceries.get("1.0", "end")
        if user_input:
            self.saved_groceries.append(user_input)
            self.updated_groceries()
    '''
    
    #function to create purchase history window
    def show_purchase_history(self):
        purchase_history_window = ctk.CTkToplevel(self.master)
        purchase_history_window.title("Purchase History")
        purchase_history_window.minsize(500, 500)
        purchase_history_window.transient(self.master)
        purchase_history_window.lift()
        purchase_history_window.focus_force()
        purchase_history_window.grid_columnconfigure((0), weight=1)

        header_label = ctk.CTkLabel(purchase_history_window, text="Purchase History", font=("Helvetica", 20, "bold"))
        header_label.grid(pady=5)

        if self.purchased_groceries:
            for idx, grocery in enumerate(self.purchased_groceries, start=1):
                grocery_label = ctk.CTkLabel(purchase_history_window, text=grocery)
                grocery_label.grid(row=idx, column=0)

        

#leave at bottom!! makes program run
if __name__ == "__main__":
    root = ctk.CTk()
    app = groceryApp(root)

    root.mainloop()
