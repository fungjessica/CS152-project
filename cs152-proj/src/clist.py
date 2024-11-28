import customtkinter as ctk
from utilities import clear_window
from bgroceries import browse_groceries
from recipe_data import saved_groceries

def create_list_flow(root, controller):
    """Flow to enter the grocery list name and save it immediately."""
    clear_window(root)

    header = ctk.CTkLabel(root, text="Create a New Grocery List", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    # Entry for the grocery list name
    list_name_entry = ctk.CTkEntry(root, width=200, justify="center", placeholder_text="Enter list name")
    list_name_entry.pack(pady=10)

    # Warning label for blank entry, initially hidden
    warning_label = ctk.CTkLabel(root, text="", font=("Helvetica", 12), text_color="red")
    warning_label.pack(pady=10)

    # Button to proceed to the groceries page (and save the list)
    proceed_button = ctk.CTkButton(
        root,
        text="Next: Browse Groceries",
        command=lambda: validate_and_create_list(root, controller, list_name_entry, warning_label),
        width=200,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14)
    )
    proceed_button.pack(pady=10)

    # Back button to return to the homepage
    back_button = ctk.CTkButton(
        root, 
        text="Back to Homepage", 
        command=controller.show_homepage, 
        width=150, 
        height=40, 
        corner_radius=10, 
        font=("Helvetica", 14)
    )
    back_button.pack(pady=10)

def validate_and_create_list(root, controller, list_name_entry, warning_label):
    """Validates the list name and creates the list if valid."""
    list_name = list_name_entry.get().strip()

    if not list_name:  # If the list name is blank
        warning_label.configure(text="List name cannot be blank! Please enter a name.")
        root.after(2000, lambda: warning_label.configure(text=""))
    else:
        # If valid, create the list and save it, then go to browse groceries
        create_list(root, controller, list_name)



def choose_items_flow(root, controller, list_name):
    """Allows the user to choose grocery items without setting quantities."""
    clear_window(root)

    header = ctk.CTkLabel(root, text=f"Select Items for '{list_name}'", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    available_items = ["Milk", "Eggs", "Bread", "Butter", "Cheese", "Apples", "Bananas", "Chicken"]
    selected_items = {}

    for item in available_items:
        frame = ctk.CTkFrame(root)
        frame.pack(padx=20, pady=5, fill="x")

        # Make a grid to push the checkboxes to the far right
        frame.grid_columnconfigure(0, weight=1)

        item_label = ctk.CTkLabel(frame, text=item, font=("Helvetica", 14))
        item_label.grid(row=0, column=0, padx=10, sticky="w")

        # Checkbox for selecting items
        select_var = ctk.StringVar()
        checkbox = ctk.CTkCheckBox(frame, variable=select_var, text="", onvalue=item, offvalue="")
        checkbox.grid(row=0, column=1, padx=20, sticky="e")
        selected_items[item] = {"selected": select_var, "quantity": None}

    # Disable the Next button initially
    proceed_button = ctk.CTkButton(
        root,
        text="Next: Set Quantities",
        command=lambda: set_quantities_flow(root, controller, list_name, selected_items),
        width=200,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14),
        state="disabled"  # Initially disabled
    )
    proceed_button.pack(pady=20)

    # Back button to return to the list name entry step
    back_button = ctk.CTkButton(
        root, 
        text="Back to Name Entry", 
        command=lambda: create_list_flow(root, controller),  
        width=150, 
        height=40, 
        corner_radius=10,
        font=("Helvetica", 14)
    )
    back_button.pack(pady=10)

    # Function to check if any checkboxes are selected and enable/disable the Next button
    def check_selection():
        """Enable or disable the Next button based on item selection."""
        if any(var["selected"].get() for var in selected_items.values()):
            proceed_button.configure(state="normal")  # Enable button
        else:
            proceed_button.configure(state="disabled")  # Disable button

    # Monitor changes in each checkbox and trigger the check_selection function
    for var in selected_items.values():
        var["selected"].trace_add("write", lambda *args: check_selection())

    # Initial check to ensure the button state is correct
    check_selection()

def set_quantities_flow(root, controller, list_name, selected_items):
    """Allows the user to set quantities for selected grocery items."""
    clear_window(root)

    header = ctk.CTkLabel(root, text=f"Set Quantities for '{list_name}'", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    # Loop through each selected item
    for item, data in selected_items.items():
        # Only display items that were selected in the previous step
        if data["selected"].get(): # This checks if the item was checked
            frame = ctk.CTkFrame(root)
            frame.pack(padx=20, pady=5, fill="x")

            # Make a grid to push the quantity controls to the far right
            frame.grid_columnconfigure(0, weight=1)

            # Item name label (left aligned)
            item_label = ctk.CTkLabel(frame, text=item, font=("Helvetica", 14))
            item_label.grid(row=0, column=0, padx=10, sticky="w")

            # Quantity control with + and - buttons
            quantity_frame = ctk.CTkFrame(frame)
            quantity_frame.grid(row=0, column=1, padx=20, sticky="e")

            # Create a minus button for decreasing quantity
            minus_button = ctk.CTkButton(quantity_frame, text="-", width=30, command=lambda i=item: decrease_quantity(i, selected_items))
            minus_button.pack(side="left")

            # Quantity entry field, defaulting to 1
            quantity_entry = ctk.CTkEntry(quantity_frame, width=50)
            quantity_entry.insert(0, "1")
            quantity_entry.pack(side="left", padx=5)

            # Create a plus button for increasing quantity
            plus_button = ctk.CTkButton(quantity_frame, text="+", width=30, command=lambda i=item: increase_quantity(i, selected_items))
            plus_button.pack(side="left")

            # Store the quantity entry in the selected_items structure
            selected_items[item]["quantity"] = quantity_entry

    # Button to create the list
    create_button = ctk.CTkButton(
        root, 
        text="Create List", 
        command=lambda: create_list(root, controller, list_name, selected_items), 
        width=200, 
        height=40, 
        corner_radius=10, 
        font=("Helvetica", 14)
    )
    create_button.pack(pady=20)

    # Back to items selection button
    back_button = ctk.CTkButton(
        root, 
        text="Back to Item Selection", 
        command=lambda: choose_items_flow(root, controller, list_name),  
        width=150, 
        height=40, 
        corner_radius=10, 
        font=("Helvetica", 14)
    )
    back_button.pack(pady=10)

def increase_quantity(item, selected_items):
    """Increase the quantity for a selected item."""
    # Retrieve the current quantity and increment it
    current_qty = int(selected_items[item]["quantity"].get())
    selected_items[item]["quantity"].delete(0, "end")
    selected_items[item]["quantity"].insert(0, str(current_qty + 1))

def decrease_quantity(item, selected_items):
    """Decrease the quantity for a selected item."""
    # Retrieve the current quantity and decrement it if greater than 1
    current_qty = int(selected_items[item]["quantity"].get())
    if current_qty > 1:
        selected_items[item]["quantity"].delete(0, "end")
        selected_items[item]["quantity"].insert(0, str(current_qty - 1))

def create_list(root, controller, list_name, selected_items=None):
    """Creates a grocery list and immediately saves it to the controller."""
    if list_name:
        # Create an empty grocery list and save it under the provided list name
        controller.grocery_lists[list_name] = {}  # Empty list (no items selected yet)
        print(f"Created and saved empty list: {list_name}")  # Debug: show the list was saved
        
        # Now, navigate to the Browse Groceries page
        browse_groceries(root, controller, list_name)
    else:
        print("List name cannot be empty")  # Debug: Handle the empty list name scenario
