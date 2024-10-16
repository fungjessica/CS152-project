import customtkinter as ct

class GroceryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery To-Do List")
        self.root.geometry("800x600")

        # Set initial appearance mode to "dark"
        self.appearance_mode = "dark"
        ctk.set_appearance_mode(self.appearance_mode)
        ctk.set_default_color_theme("dark-blue")  # Set default color theme

        # Grocery lists data (initially empty)
        self.grocery_lists = {}
        self.done_items = {}

        # Call homepage on start
        self.show_homepage()

    def show_homepage(self):
        """Displays the homepage with buttons."""
        self.clear_window()

        # Header label
        header = ctk.CTkLabel(self.root, text="Grocery To-Do List", font=("Helvetica", 24, "bold"))
        header.pack(pady=30)

        # Button to view existing grocery lists
        view_list_button = ctk.CTkButton(
            self.root, 
            text="View Lists", 
            command=self.view_lists,
            width=250, 
            height=50, 
            corner_radius=10,
            font=("Helvetica", 16)
        )
        view_list_button.pack(pady=20)

        # Button to create a new grocery list
        create_list_button = ctk.CTkButton(
            self.root, 
            text="Create a New List", 
            command=self.create_list_flow,
            width=250, 
            height=50, 
            corner_radius=10,
            font=("Helvetica", 16)
        )
        create_list_button.pack(pady=20)

        # Button to view saved recipes
        saved_recipes_button = ctk.CTkButton(
            self.root, 
            text="See Saved Recipes", 
            command=self.view_saved_recipes,
            width=250, 
            height=50, 
            corner_radius=10,
            font=("Helvetica", 16)
        )
        saved_recipes_button.pack(pady=20)

        # Button to browse grocery items
        browse_groceries_button = ctk.CTkButton(
            self.root, 
            text="Browse Groceries", 
            command=self.browse_groceries,
            width=250, 
            height=50, 
            corner_radius=10,
            font=("Helvetica", 16)
        )
        browse_groceries_button.pack(pady=20)

        # Mode Toggle Button (Bottom Left)
        self.mode_toggle_button = ctk.CTkButton(
            self.root, 
            text="Switch to Light Mode" if self.appearance_mode == "dark" else "Switch to Dark Mode", 
            command=self.toggle_mode,
            width=150, 
            height=30, 
            corner_radius=10,
            font=("Helvetica", 12)
        )
        self.mode_toggle_button.place(relx=0.05, rely=0.95, anchor="sw")  # Positioned bottom-left

    def create_list_flow(self):
        """Handles the creation of a new grocery list by first asking for the list name."""
        self.clear_window()

        # Header for the list name entry
        header = ctk.CTkLabel(self.root, text="Create a New Grocery List", font=("Helvetica", 24, "bold"))
        header.pack(pady=30)

        # Entry for the grocery list name
        self.list_name_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Enter list name")
        self.list_name_entry.pack(pady=20)

        # Button to proceed to the item selection step
        proceed_button = ctk.CTkButton(
            self.root, 
            text="Next: Choose Items", 
            command=self.save_list_name_and_continue,
            width=200, 
            height=40, 
            corner_radius=10,
            font=("Helvetica", 14)
        )
        proceed_button.pack(pady=10)

        # Back to homepage button
        back_button = ctk.CTkButton(
            self.root, 
            text="Back to Homepage", 
            command=self.show_homepage,
            width=150, 
            height=40, 
            corner_radius=10,
            font=("Helvetica", 14)
        )
        back_button.pack(pady=10)

    def save_list_name_and_continue(self):
        """Saves the list name and moves to the item selection flow."""
        # Save the list name entered by the user
        self.list_name = self.list_name_entry.get()

        # If list_name is valid, continue to item selection
        if self.list_name and self.list_name.strip():
            self.choose_items_flow()  # Proceed to item selection
        else:
            warning_label = ctk.CTkLabel(self.root, text="Please enter a valid list name!", font=("Helvetica", 12), fg="red")
            warning_label.pack(pady=5)

    def choose_items_flow(self):
        """Allows the user to choose grocery items without setting quantities."""
        if not self.list_name or not self.list_name.strip():
            warning_label = ctk.CTkLabel(self.root, text="Please enter a list name!", font=("Helvetica", 12), fg="red")
            warning_label.pack(pady=5)
            return

        self.clear_window()

        # Header for choosing items
        header = ctk.CTkLabel(self.root, text=f"Select Items for '{self.list_name}'", font=("Helvetica", 24, "bold"))
        header.pack(pady=30)

        # Predefined grocery items
        self.available_items = ["Milk", "Eggs", "Bread", "Butter", "Cheese", "Apples", "Bananas", "Chicken"]
        self.selected_items = {}

        for item in self.available_items:
            frame = ctk.CTkFrame(self.root)
            frame.pack(padx=20, pady=5, fill="x")

            frame.grid_columnconfigure(0, weight=1)

            item_label = ctk.CTkLabel(frame, text=item, font=("Helvetica", 14))
            item_label.grid(row=0, column=0, padx=10, sticky="w")

            # Checkbox for selecting items
            select_var = ctk.StringVar()
            checkbox = ctk.CTkCheckBox(frame, variable=select_var, text="", onvalue=item, offvalue="")
            checkbox.grid(row=0, column=1, padx=20, sticky="e")
            self.selected_items[item] = {"selected": select_var, "quantity": None}

        # Disable the Next button initially
        proceed_button = ctk.CTkButton(
            self.root, 
            text="Next: Set Quantities", 
            command=self.set_quantities_flow,
            width=200, 
            height=40, 
            corner_radius=10,
            font=("Helvetica", 14),
            state="disabled"  # Initially disabled
        )
        proceed_button.pack(pady=20)

        def check_selection():
            """Enable or disable the Next button based on item selection."""
            if any(var["selected"].get() for var in self.selected_items.values()):
                proceed_button.configure(state="normal")
            else:
                proceed_button.configure(state="disabled")

        # Monitor changes in each checkbox
        for var in self.selected_items.values():
            var["selected"].trace_add("write", lambda *args: check_selection())

        # Back button to go back to the list name step
        back_button = ctk.CTkButton(
            self.root, 
            text="Back to Name Entry", 
            command=self.create_list_flow,  
            width=150, 
            height=40, 
            corner_radius=10,
            font=("Helvetica", 14)
        )
        back_button.pack(pady=10)

        # Initial check to ensure the button state is correct
        check_selection()

    def set_quantities_flow(self):
        """Allows the user to set quantities for the selected items."""
        self.clear_window()

        # Header for setting quantities
        header = ctk.CTkLabel(self.root, text=f"Set Quantities for '{self.list_name}'", font=("Helvetica", 24, "bold"))
        header.pack(pady=30)

        # Display only the selected items with quantity controls
        for item, data in self.selected_items.items():
            # Check if the item was selected in the previous step
            if data["selected"].get():  # This checks if the item was checked
                frame = ctk.CTkFrame(self.root)
                frame.pack(padx=20, pady=5, fill="x")

                # Configure the grid to push the quantity frame to the far right
                frame.grid_columnconfigure(0, weight=1)

                # Item name label (left aligned)
                item_label = ctk.CTkLabel(frame, text=item, font=("Helvetica", 14))
                item_label.grid(row=0, column=0, padx=10, sticky="w")

                # Quantity control with + and - buttons (aligned to the right)
                quantity_frame = ctk.CTkFrame(frame)
                quantity_frame.grid(row=0, column=1, padx=20, sticky="e")

                minus_button = ctk.CTkButton(quantity_frame, text="-", width=30, command=lambda i=item: self.decrease_quantity(i))
                minus_button.pack(side="left")

                quantity_entry = ctk.CTkEntry(quantity_frame, width=50)
                quantity_entry.insert(0, "1")  # Default quantity
                quantity_entry.pack(side="left", padx=5)

                plus_button = ctk.CTkButton(quantity_frame, text="+", width=30, command=lambda i=item: self.increase_quantity(i))
                plus_button.pack(side="left")

                # Store the quantity entry in the selected_items structure (do not overwrite the 'selected' variable)
                self.selected_items[item]["quantity"] = quantity_entry

        # Button to create the list
        create_button = ctk.CTkButton(
            self.root, 
            text="Create List", 
            command=self.create_list,
            width=200, 
            height=40, 
            corner_radius=10,
            font=("Helvetica", 14)
        )
        create_button.pack(pady=20)

        # Back button to go back to the item selection step
        back_button = ctk.CTkButton(
            self.root, 
            text="Back to Item Selection", 
            command=self.choose_items_flow,
            width=150, 
            height=40, 
            corner_radius=10,
            font=("Helvetica", 14)
        )
        back_button.pack(pady=10)

    def increase_quantity(self, item):
        """Increase the quantity for a selected item."""
        current_qty = int(self.selected_items[item]["quantity"].get())
        self.selected_items[item]["quantity"].delete(0, "end")
        self.selected_items[item]["quantity"].insert(0, str(current_qty + 1))

    def decrease_quantity(self, item):
        """Decrease the quantity for a selected item."""
        current_qty = int(self.selected_items[item]["quantity"].get())
        if current_qty > 1:
            self.selected_items[item]["quantity"].delete(0, "end")
            self.selected_items[item]["quantity"].insert(0, str(current_qty - 1))

    def create_list(self):
        """Creates a grocery list with the selected items and their quantities."""
        # We only add items that have been selected and have a valid quantity
        try:
            self.grocery_lists[self.list_name] = {
                item: int(data["quantity"].get()) 
                for item, data in self.selected_items.items() 
                if data["quantity"] is not None and data["quantity"].get().isdigit()
            }

            # Refresh the view with the updated grocery lists
            self.view_lists()
        except AttributeError as e:
            # Catch any AttributeError and display a message
            error_label = ctk.CTkLabel(self.root, text="Error: Please ensure all selected items have a valid quantity.", font=("Helvetica", 12), fg="red")
            error_label.pack(pady=5)

    def view_lists(self):
        """Displays the created grocery lists with options to view, rename, and delete."""
        self.clear_window()

        header = ctk.CTkLabel(self.root, text="View Grocery Lists", font=("Helvetica", 24, "bold"))
        header.pack(pady=30)

        # If no lists, show a message
        if not self.grocery_lists:
            empty_label = ctk.CTkLabel(self.root, text="No grocery lists created.", font=("Helvetica", 16))
            empty_label.pack(pady=20)
        else:
            # Show the created lists with options
            for idx, (list_name, items) in enumerate(self.grocery_lists.items()):
                list_frame = ctk.CTkFrame(self.root)
                list_frame.pack(pady=5, padx=20, fill="x")

                # Configure grid to push buttons to the far right
                list_frame.grid_columnconfigure(0, weight=1)

                list_label = ctk.CTkLabel(list_frame, text=list_name, font=("Helvetica", 14))
                list_label.grid(row=0, column=0, padx=10, sticky="w")

                # View button
                view_button = ctk.CTkButton(
                    list_frame, text="View", width=80, height=30,
                    corner_radius=10, font=("Helvetica", 12),
                    command=lambda idx=idx: self.view_list_details(idx)
                )
                view_button.grid(row=0, column=1, padx=5, sticky="e")

                # Rename button
                rename_button = ctk.CTkButton(
                    list_frame, text="Rename", width=80, height=30,
                    corner_radius=10, font=("Helvetica", 12),
                    command=lambda idx=idx: self.rename_list(idx)
                )
                rename_button.grid(row=0, column=2, padx=5, sticky="e")

                # Delete button
                delete_button = ctk.CTkButton(
                    list_frame, text="Delete", width=80, height=30,
                    corner_radius=10, font=("Helvetica", 12),
                    command=lambda idx=idx: self.delete_list(idx)
                )
                delete_button.grid(row=0, column=3, padx=5, sticky="e")

        # Back to homepage button
        back_button = ctk.CTkButton(
            self.root, 
            text="Back to Homepage", 
            command=self.show_homepage,
            width=150, 
            height=40, 
            corner_radius=10,
            font=("Helvetica", 14)
        )
        back_button.pack(pady=20)

    def view_list_details(self, idx):
        """Displays the details of the selected list."""
        list_name = list(self.grocery_lists.keys())[idx]
        items = self.grocery_lists[list_name]

        self.clear_window()

        header = ctk.CTkLabel(self.root, text=f"List: {list_name}", font=("Helvetica", 24, "bold"))
        header.pack(pady=20)

        # Create two columns: Item Name and Checkbox
        items_frame = ctk.CTkFrame(self.root)
        items_frame.pack(fill="x", pady=10)

        # Column headers
        ctk.CTkLabel(items_frame, text="Item", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(items_frame, text="Quantity", font=("Helvetica", 16)).grid(row=0, column=1, padx=10, pady=5, sticky="e")

        # Column for checkboxes
        self.item_vars = {}
        for row, (item, quantity) in enumerate(items.items(), start=1):
            ctk.CTkLabel(items_frame, text=item, font=("Helvetica", 14)).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(items_frame, text=str(quantity), font=("Helvetica", 14)).grid(row=row, column=1, padx=10, pady=5, sticky="e")

            # Checkbox for selection
            select_var = ctk.StringVar()
            checkbox = ctk.CTkCheckBox(items_frame, variable=select_var, text="", onvalue=item, offvalue="")
            checkbox.grid(row=row, column=2, padx=10, pady=5, sticky="e")
            self.item_vars[item + "_select"] = select_var

        # Done and Delete buttons after selecting items
        self.done_button = None
        self.delete_button = None
        self.display_done_and_delete_buttons(list_name)

        # Back to lists button
        back_button = ctk.CTkButton(
            self.root, 
            text="Back to Lists", 
            command=self.view_lists,
            width=150, 
            height=40, 
            corner_radius=10,
            font=("Helvetica", 14)
        )
        back_button.pack(pady=10)

    def display_done_and_delete_buttons(self, list_name):
        """Displays Done and Delete buttons for the selected items."""
        if not self.done_button or not self.delete_button:
            self.done_button = ctk.CTkButton(
                self.root, 
                text="Done", 
                command=lambda: self.mark_items_done(list_name),
                width=150, 
                height=40, 
                corner_radius=10,
                font=("Helvetica", 14)
            )
            self.delete_button = ctk.CTkButton(
                self.root, 
                text="Delete", 
                command=lambda: self.delete_items_from_list(list_name),
                width=150, 
                height=40, 
                corner_radius=10,
                font=("Helvetica", 14)
            )

        if any(var.get() for var in self.item_vars.values()):
            self.done_button.pack(pady=10)
            self.delete_button.pack(pady=10)
        else:
            self.done_button.pack_forget()
            self.delete_button.pack_forget()

    def mark_items_done(self, list_name):
        """Move the selected items to the Done section."""
        selected_items = [item for item, var in self.item_vars.items() if "_select" in item and var.get()]
        for item in selected_items:
            self.done_items[list_name].append(item)
            del self.grocery_lists[list_name][item]

        self.view_list_details(list(self.grocery_lists.keys()).index(list_name))

    def delete_items_from_list(self, list_name):
        """Delete the selected items from the list."""
        selected_items = [item for item, var in self.item_vars.items() if "_select" in item and var.get()]
        for item in selected_items:
            del self.grocery_lists[list_name][item]

        self.view_list_details(list(self.grocery_lists.keys()).index(list_name))

    def rename_list(self, idx):
        """Renames a grocery list based on user input."""
        # Get the current list name based on the index
        list_name = list(self.grocery_lists.keys())[idx]

        # Ask the user for the new name using an input dialog
        new_name = ctk.CTkInputDialog(title="Rename List", text="Enter new name:").get_input()

        # Check if the new name is valid (not empty or spaces)
        if new_name and new_name.strip():  # Strip removes any leading or trailing spaces
            # Update the grocery list with the new name
            items = self.grocery_lists.pop(list_name)
            self.grocery_lists[new_name.strip()] = items  # Ensure the name has no leading/trailing spaces
            
            # Refresh the list view
            self.view_lists()
        else:
            # If no valid name was provided, just return (no action)
            warning_label = ctk.CTkLabel(self.root, text="No valid name entered! Rename canceled.", font=("Helvetica", 12), fg="red")
            warning_label.pack(pady=5)

    def delete_list(self, idx):
        """Deletes a grocery list."""
        list_name = list(self.grocery_lists.keys())[idx]
        del self.grocery_lists[list_name]
        self.view_lists()

    def view_saved_recipes(self):
        """Function to view saved recipes."""
        self.clear_window()
        header = ctk.CTkLabel(self.root, text="Saved Recipes", font=("Helvetica", 24, "bold"))
        header.pack(pady=30)

        # Add logic to view saved recipes here

        back_button = ctk.CTkButton(
            self.root, text="Back to Homepage", command=self.show_homepage,
            width=150, height=40, corner_radius=10, font=("Helvetica", 14)
        )
        back_button.pack(pady=20)

    def browse_groceries(self):
        """Function to browse grocery items."""
        self.clear_window()
        header = ctk.CTkLabel(self.root, text="Browse Grocery Items", font=("Helvetica", 24, "bold"))
        header.pack(pady=30)

        # Add logic to browse grocery items here

        back_button = ctk.CTkButton(
            self.root, text="Back to Homepage", command=self.show_homepage,
            width=150, height=40, corner_radius=10, font=("Helvetica", 14)
        )
        back_button.pack(pady=20)

    def clear_window(self):
        """Clears all widgets from the window to show new content."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def toggle_mode(self):
        """Switch between dark and light modes."""
        if self.appearance_mode == "dark":
            self.appearance_mode = "light"
            ctk.set_appearance_mode("light")
            self.mode_toggle_button.configure(text="Switch to Dark Mode")  # Change button text
        else:
            self.appearance_mode = "dark"
            ctk.set_appearance_mode("dark")
            self.mode_toggle_button.configure(text="Switch to Light Mode")  # Change button text


# Run the application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Set to dark mode for a modern, sleek look
    ctk.set_default_color_theme("dark-blue")  # Set default theme color
    root = ctk.CTk()  # Create the main window
    app = GroceryApp(root)  # Initialize the app
    root.mainloop()  # Start the main loop
