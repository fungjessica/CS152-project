import customtkinter as ctk
from utilities import clear_window

def create_list_flow(root, controller):
    """Flow to enter the grocery list name."""
    clear_window(root)

    header = ctk.CTkLabel(root, text="Create a New Grocery List", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    list_name_entry = ctk.CTkEntry(root, width=200,justify="center", placeholder_text="Enter list name")
    list_name_entry.pack(pady=10)

    warning_label = ctk.CTkLabel(root, text="", font=("Helvetica", 12), text_color="red")
    warning_label.pack(pady=10)

    proceed_button = ctk.CTkButton(
        root,
        text="Next: Choose Items",
        command=lambda: validate_list_name(root, controller, list_name_entry, warning_label),
        width=200,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14)
    )
    proceed_button.pack(pady=10)

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

def validate_list_name(root, controller, list_name_entry, warning_label):
    list_name = list_name_entry.get().strip()  

    if not list_name: 
        warning_label.configure(text="List name cannot be blank! Please enter a name.")  

        root.after(2000, lambda: warning_label.configure(text=""))
    else:
        choose_items_flow(root, controller, list_name)

def choose_items_flow(root, controller, list_name):
    clear_window(root)

    header = ctk.CTkLabel(root, text=f"Select Items for '{list_name}'", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    available_items = ["Milk", "Eggs", "Bread", "Butter", "Cheese", "Apples", "Bananas", "Chicken"]
    selected_items = {}

    for item in available_items:
        frame = ctk.CTkFrame(root)
        frame.pack(padx=20, pady=5, fill="x")

        frame.grid_columnconfigure(0, weight=1)

        item_label = ctk.CTkLabel(frame, text=item, font=("Helvetica", 14))
        item_label.grid(row=0, column=0, padx=10, sticky="w")

        select_var = ctk.StringVar()
        checkbox = ctk.CTkCheckBox(frame, variable=select_var, text="", onvalue=item, offvalue="")
        checkbox.grid(row=0, column=1, padx=20, sticky="e")
        selected_items[item] = {"selected": select_var, "quantity": None}

    proceed_button = ctk.CTkButton(
        root,
        text="Next: Set Quantities",
        command=lambda: set_quantities_flow(root, controller, list_name, selected_items),
        width=200,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14),
        state="disabled"  
    )
    proceed_button.pack(pady=20)

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

    def check_selection():
        if any(var["selected"].get() for var in selected_items.values()):
            proceed_button.configure(state="normal")  
        else:
            proceed_button.configure(state="disabled")  

    for var in selected_items.values():
        var["selected"].trace_add("write", lambda *args: check_selection())

    check_selection()

def set_quantities_flow(root, controller, list_name, selected_items):
    clear_window(root)

    header = ctk.CTkLabel(root, text=f"Set Quantities for '{list_name}'", font=("Helvetica", 24, "bold"))
    header.pack(pady=30)

    for item, data in selected_items.items():
        if data["selected"].get(): 
            frame = ctk.CTkFrame(root)
            frame.pack(padx=20, pady=5, fill="x")

            frame.grid_columnconfigure(0, weight=1)

            item_label = ctk.CTkLabel(frame, text=item, font=("Helvetica", 14))
            item_label.grid(row=0, column=0, padx=10, sticky="w")

            quantity_frame = ctk.CTkFrame(frame)
            quantity_frame.grid(row=0, column=1, padx=20, sticky="e")

            minus_button = ctk.CTkButton(quantity_frame, text="-", width=30, command=lambda i=item: decrease_quantity(i, selected_items))
            minus_button.pack(side="left")

            quantity_entry = ctk.CTkEntry(quantity_frame, width=50)
            quantity_entry.insert(0, "1")
            quantity_entry.pack(side="left", padx=5)

            plus_button = ctk.CTkButton(quantity_frame, text="+", width=30, command=lambda i=item: increase_quantity(i, selected_items))
            plus_button.pack(side="left")

            selected_items[item]["quantity"] = quantity_entry

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
    current_qty = int(selected_items[item]["quantity"].get())
    selected_items[item]["quantity"].delete(0, "end")
    selected_items[item]["quantity"].insert(0, str(current_qty + 1))

def decrease_quantity(item, selected_items):
    current_qty = int(selected_items[item]["quantity"].get())
    if current_qty > 1:
        selected_items[item]["quantity"].delete(0, "end")
        selected_items[item]["quantity"].insert(0, str(current_qty - 1))

def create_list(root, controller, list_name, selected_items):
    try:
        controller.grocery_lists[list_name] = {
            item: int(data["quantity"].get())
            for item, data in selected_items.items()
            if data["quantity"] is not None and data["quantity"].get().isdigit()
        }

        controller.show_view_lists()  
    except AttributeError:
        error_label = ctk.CTkLabel(root, text="Error: Please ensure all selected items have a valid quantity.", font=("Helvetica", 12), fg="red")
        error_label.pack(pady=5)