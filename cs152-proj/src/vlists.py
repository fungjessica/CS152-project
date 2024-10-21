import customtkinter as ctk
from utilities import clear_window

def view_lists(root, controller):
    """Displays the created grocery lists with options to view, rename, and delete."""
    clear_window(root)

    header = ctk.CTkLabel(root, text="View Grocery Lists", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    # If no lists, show a message
    if not controller.grocery_lists:
        empty_label = ctk.CTkLabel(root, text="No grocery lists created.", font=("Helvetica", 16))
        empty_label.pack(pady=20)
    else:
        # Show the created lists with options
        for idx, (list_name, items) in enumerate(controller.grocery_lists.items()):
            list_frame = ctk.CTkFrame(root)
            list_frame.pack(pady=5, padx=20, fill="x")

            list_frame.grid_columnconfigure(0, weight=1)

            list_label = ctk.CTkLabel(list_frame, text=list_name, font=("Helvetica", 14))
            list_label.grid(row=0, column=0, padx=10, sticky="w")

            # View button
            view_button = ctk.CTkButton(
                list_frame,
                text="View",
                width=40,
                height=20,
                corner_radius=10,
                font=("Helvetica", 12),
                command=lambda idx=idx: view_list_details(root, controller, idx)
            )
            view_button.grid(row=0, column=1, padx=5, sticky="e")

            # Rename button
            rename_button = ctk.CTkButton(
                list_frame,
                text="Rename",
                width=40,
                height=20,
                corner_radius=10,
                font=("Helvetica", 12),
                command=lambda idx=idx: rename_list(root, controller, idx)
            )
            rename_button.grid(row=0, column=2, padx=5, sticky="e")

            # Delete button
            delete_button = ctk.CTkButton(
                list_frame,
                text="Delete",
                width=40,
                height=20,
                corner_radius=10,
                font=("Helvetica", 12),
                command=lambda idx=idx: delete_list(root, controller, idx)
            )
            delete_button.grid(row=0, column=3, padx=5, sticky="e")

    # Back to homepage button
    back_button = ctk.CTkButton(
        root, 
        text="Back to Homepage", 
        command=controller.show_homepage,
        width=150, 
        height=40, 
        corner_radius=10,
        font=("Helvetica", 14)
    )
    back_button.pack(pady=20)

def view_list_details(root, controller, idx):
    """Displays the details of the selected list."""
    # Get the name of the selected list using its index and retrieve its items
    list_name = list(controller.grocery_lists.keys())[idx]
    items = controller.grocery_lists[list_name]

    clear_window(root)

    header = ctk.CTkLabel(root, text=f"List: {list_name}", font=("Helvetica", 24, "bold"))
    header.pack(pady=20)

    # Create a frame to display the list of items and their quantities
    items_frame = ctk.CTkFrame(root)
    items_frame.pack(fill="x", pady=10)

    # Make a grid to push the quantity controls to the far right
    items_frame.grid_columnconfigure(0, weight=1)

    # Display column headers: "Item" and "Quantity"
    ctk.CTkLabel(items_frame, text="Item", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(items_frame, text="Quantity", font=("Helvetica", 16)).grid(row=0, column=1, padx=10, pady=5, sticky="e")
    
    # Dictionary to store the checkbox variables for each item
    item_vars = {}

    # Loop through the items and display each item's name and quantity in the grid
    for row, (item, quantity) in enumerate(items.items(), start=1):
        ctk.CTkLabel(items_frame, text=item, font=("Helvetica", 14)).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(items_frame, text=str(quantity), font=("Helvetica", 14)).grid(row=row, column=1, padx=10, pady=5, sticky="e")

         # Create checkboxes for selecting items
        select_var = ctk.StringVar()
        checkbox = ctk.CTkCheckBox(items_frame, variable=select_var, text="", onvalue=item, offvalue="")
        checkbox.grid(row=row, column=2, padx=10, pady=5, sticky="e")
        item_vars[item + "_select"] = select_var

    display_done_and_delete_buttons(root, controller, list_name, item_vars)

    #TODO (NOT WORKING)
    # # Frame for displaying done items (initially hidden)
    # done_frame = ctk.CTkFrame(root)
    # done_frame.pack(fill="x", pady=20)
    # done_frame.pack_forget()  # Initially hide the done items frame

    # # Call the function to display done items (if any)
    # display_done_items(done_frame, controller, list_name)

    # Button to go back to the main list view
    back_button = ctk.CTkButton(
        root, 
        text="Back to Lists", 
        command=lambda: view_lists(root, controller),
        width=150, 
        height=40, 
        corner_radius=10,
        font=("Helvetica", 14)
    )
    back_button.pack(pady=10)

def display_done_and_delete_buttons(root, controller, list_name, item_vars):
    """Displays Done and Delete buttons for the selected items."""
    # Create a button to mark selected items as done
    done_button = ctk.CTkButton(
        root, 
        text="Done", 
        command=lambda: mark_items_done(root, controller, list_name, item_vars),
        width=150, 
        height=40, 
        corner_radius=10,
        font=("Helvetica", 14)
    )

    # Create a button to delete the selected items
    delete_button = ctk.CTkButton(
        root, 
        text="Delete", 
        command=lambda: delete_items_from_list(root, controller, list_name, item_vars),
        width=150, 
        height=40, 
        corner_radius=10,
        font=("Helvetica", 14)
    )

    # Initially hide the buttons
    done_button.pack_forget()
    delete_button.pack_forget()

    def check_selection():
        """Enable or disable the Done and Delete buttons based on selection."""
        if any(var.get() for var in item_vars.values()):
            done_button.pack(pady=10)
            delete_button.pack(pady=10)
        else:
            done_button.pack_forget()
            delete_button.pack_forget()

    # Monitor the checkboxes for selection changes
    for var in item_vars.values():
        var.trace_add("write", lambda *args: check_selection())

    # Initial check to set button visibility based on current selection
    check_selection()

#TODO (NOT WORKING)
# def mark_items_done(root, controller, list_name, item_vars):
#     """Move the selected items to the Done section."""
#     selected_items = [item for item, var in item_vars.items() if var.get()]
    
#     # Check if there is a "done" section for this list in the controller
#     if "done_items" not in controller.grocery_lists[list_name]:
#         controller.grocery_lists[list_name]["done_items"] = []

#     # Move selected items to "done" section
#     for item in selected_items:
#         controller.grocery_lists[list_name]["done_items"].append(item)
#         del controller.grocery_lists[list_name][item]

#     # Refresh the list details after marking items as done
#     view_list_details(root, controller, list(controller.grocery_lists.keys()).index(list_name))

# def delete_items_from_list(root, controller, list_name, item_vars):
#     """Delete the selected items from the list."""
#     selected_items = [item for item, var in item_vars.items() if var.get()]
    
#     # Delete the selected items from the grocery list
#     for item in selected_items:
#         del controller.grocery_lists[list_name][item]

#     # Refresh the list details after deleting items
#     view_list_details(root, controller, list(controller.grocery_lists.keys()).index(list_name))

# def display_done_items(done_frame, controller, list_name):
#     """Displays the items marked as done in a separate section."""
#     if "done_items" in controller.grocery_lists[list_name]:
#         done_items = controller.grocery_lists[list_name]["done_items"]
        
#         if done_items:
#             header = ctk.CTkLabel(done_frame, text="Done Items", font=("Helvetica", 20, "bold"))
#             header.pack(pady=10)

#             for item in done_items:
#                 item_label = ctk.CTkLabel(done_frame, text=item, font=("Helvetica", 14))
#                 item_label.pack(pady=5, padx=10)
            
#             # Show the done items frame after items are moved to done
#             done_frame.pack(fill="x", pady=20)
#     else:
#         done_frame.pack_forget()  # Hide if no done items

def rename_list(root, controller, idx):
    """Renames a grocery list based on user input."""
    # Get the current name of the list using its index
    list_name = list(controller.grocery_lists.keys())[idx]

    # Ask the user to input a new name for the list
    new_name = ctk.CTkInputDialog(title="Rename List", text="Enter new name:").get_input()

    # If the new name is valid (not blank), rename the list
    if new_name and new_name.strip():
        items = controller.grocery_lists.pop(list_name) # Remove the old list name
        controller.grocery_lists[new_name.strip()] = items # Add the list under the new name
        view_lists(root, controller) # Refresh the view after renaming
    else:
        # Show a warning if the user did not provide a valid name
        warning_label = ctk.CTkLabel(root, text="No valid name entered! Rename canceled.", font=("Helvetica", 12), fg="red")
        warning_label.pack(pady=5)

def delete_list(root, controller, idx):
    """Deletes a grocery list."""
    # Get the name of the list using its index and delete it
    list_name = list(controller.grocery_lists.keys())[idx]
    del controller.grocery_lists[list_name]

    # Refresh the list view after deleting the list
    view_lists(root, controller)
