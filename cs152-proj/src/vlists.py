import customtkinter as ctk
from utilities import clear_window

def view_lists(root, controller):
    clear_window(root)

    header = ctk.CTkLabel(root, text="View Grocery Lists", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    if not controller.grocery_lists:
        empty_label = ctk.CTkLabel(root, text="No grocery lists created.", font=("Helvetica", 16))
        empty_label.pack(pady=20)
    else:
        for idx, (list_name, items) in enumerate(controller.grocery_lists.items()):
            list_frame = ctk.CTkFrame(root)
            list_frame.pack(pady=5, padx=20, fill="x")

            list_frame.grid_columnconfigure(0, weight=1)

            list_label = ctk.CTkLabel(list_frame, text=list_name, font=("Helvetica", 14))
            list_label.grid(row=0, column=0, padx=10, sticky="w")

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
    list_name = list(controller.grocery_lists.keys())[idx]
    items = controller.grocery_lists[list_name]

    # Get the done items
    done_items = controller.grocery_lists[list_name].get("done_items", [])

    # Remove the done items from the main list
    active_items = {k: v for k, v in items.items() if k not in done_items}

    clear_window(root)

    header = ctk.CTkLabel(root, text=f"List: {list_name}", font=("Helvetica", 24, "bold"))
    header.pack(pady=20)

    items_frame = ctk.CTkFrame(root)
    items_frame.pack(fill="x", pady=10)

    items_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(items_frame, text="Item", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(items_frame, text="Quantity", font=("Helvetica", 16)).grid(row=0, column=1, padx=10, pady=5, sticky="e")
    
    item_vars = {}

    # Display active (non-done) items
    for row, (item, quantity) in enumerate(active_items.items(), start=1):
        ctk.CTkLabel(items_frame, text=item, font=("Helvetica", 14)).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(items_frame, text=str(quantity), font=("Helvetica", 14)).grid(row=row, column=1, padx=10, pady=5, sticky="e")

        select_var = ctk.StringVar()
        checkbox = ctk.CTkCheckBox(items_frame, variable=select_var, text="", onvalue=item, offvalue="")
        checkbox.grid(row=row, column=2, padx=10, pady=5, sticky="e")
        item_vars[item + "_select"] = select_var

    display_done_and_delete_buttons(root, controller, list_name, item_vars)

    # --- Done Items Section ---
    #done_frame = ctk.CTkFrame(root)
    #done_frame.pack(fill="x", pady=20)

    # Call the function to display done items (now separated)
    #display_done_items(done_frame, controller, list_name)

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
    #done_button = ctk.CTkButton(
    #    root, 
    #    text="Done", 
    #    command=lambda: mark_items_done(root, controller, list_name, item_vars),
    #    width=150, 
    #    height=40, 
    #    corner_radius=10,
    #    font=("Helvetica", 14)
    #)

    delete_button = ctk.CTkButton(
        root, 
        text="Delete", 
        command=lambda: delete_items_from_list(root, controller, list_name, item_vars),
        width=150, 
        height=40, 
        corner_radius=10,
        font=("Helvetica", 14)
    )

    #done_button.pack_forget()
    delete_button.pack_forget()

    def check_selection():
        if any(var.get() for var in item_vars.values()):
            #done_button.pack(pady=10)
            delete_button.pack(pady=10)
        else:
            #done_button.pack_forget()
            delete_button.pack_forget()

    for var in item_vars.values():
        var.trace_add("write", lambda *args: check_selection())

    check_selection()

def mark_items_done(root, controller, list_name, item_vars):
    """Move the selected items to the Done section."""
    selected_items = [var.get() for var in item_vars.values() if var.get()]
    
    if not selected_items:
        return

    # Ensure the "done_items" section exists for this list
    if "done_items" not in controller.grocery_lists[list_name]:
        controller.grocery_lists[list_name]["done_items"] = {}

    # Move selected items to the "done_items" section with their quantities
    for item in selected_items:
        if item in controller.grocery_lists[list_name]:
            quantity = controller.grocery_lists[list_name].pop(item)
            controller.grocery_lists[list_name]["done_items"][item] = quantity

    # Refresh the list details after marking items as done
    view_list_details(root, controller, list(controller.grocery_lists.keys()).index(list_name))

def delete_items_from_list(root, controller, list_name, item_vars):
    """Delete the selected items from the list."""
    selected_items = [var.get() for var in item_vars.values() if var.get()]
    
    if not selected_items:
        return

    # Delete the selected items
    for item in selected_items:
        if item in controller.grocery_lists[list_name]:
            del controller.grocery_lists[list_name][item]

    # Refresh the list details
    view_list_details(root, controller, list(controller.grocery_lists.keys()).index(list_name))

#def display_done_items(done_frame, controller, list_name):
#    """Displays the items marked as done in a separate section."""
#    done_items = controller.grocery_lists[list_name].get("done_items", {})
#    
    # Clear the frame before displaying done items
#    for widget in done_frame.winfo_children():
#        widget.destroy()
#
#    if done_items:
#        header = ctk.CTkLabel(done_frame, text="Done Items", font=("Helvetica", 20, "bold"))
#        header.pack(pady=10)
#
#        for item, quantity in done_items.items():
#            item_label = ctk.CTkLabel(done_frame, text=f"{item} - {quantity}", font=("Helvetica", 14))
#            item_label.pack(pady=5, padx=10)

def rename_list(root, controller, idx):
    list_name = list(controller.grocery_lists.keys())[idx]

    dialog_window = ctk.CTkToplevel(root)
    dialog_window.title("Rename List")
    dialog_window.geometry("300x180")

    dialog_window.lift()
    
    dialog_window.attributes('-topmost', True)

    dialog_window.focus()

    label = ctk.CTkLabel(dialog_window, text="Enter new name:")
    label.pack(pady=10)

    list_name_entry = ctk.CTkEntry(dialog_window)
    list_name_entry.pack(pady=5)

    warning_label = ctk.CTkLabel(dialog_window, text="", text_color="red")
    warning_label.pack(pady=(5,5))

    def confirm_rename():
        new_name = list_name_entry.get().strip()  

        if new_name:  
            items = controller.grocery_lists.pop(list_name)
            controller.grocery_lists[new_name] = items
            view_lists(root, controller) 
            dialog_window.destroy()  
        else:
            warning_label.configure(text="Name cannot be empty!")

            root.after(2000, lambda: warning_label.configure(text=""))

    ok_button = ctk.CTkButton(
        dialog_window, text="Ok", command=confirm_rename
    )
    ok_button.pack(side="left", padx=10, pady=(0,10))

    cancel_button = ctk.CTkButton(
        dialog_window, text="Cancel", command=dialog_window.destroy
    )
    cancel_button.pack(side="right", padx=10, pady=(0,10))

def delete_list(root, controller, idx):
    list_name = list(controller.grocery_lists.keys())[idx]
    del controller.grocery_lists[list_name]

    view_lists(root, controller)