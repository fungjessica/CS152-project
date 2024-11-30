import customtkinter as ctk
from utilities import clear_window
from clist import save_grocery_lists_to_file
from clist import choose_items_flow
from clist import is_creating_list

def view_lists(root, controller):
    controller.set_creating_list(False)

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

    done_items = controller.grocery_lists[list_name].get("done_items", [])
    
    active_items = {k: v for k, v in items.items() if k not in done_items}

    clear_window(root)

    header = ctk.CTkLabel(root, text=f"List: {list_name}", font=("Helvetica", 24, "bold"))
    header.pack(pady=20)

    scrollable_frame = ctk.CTkScrollableFrame(root, width=600, height=300, corner_radius=10)
    scrollable_frame.pack(fill="both", pady=10, padx=20, expand=True)

    scrollable_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(scrollable_frame, text="Items", font=("Helvetica", 16, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ctk.CTkLabel(scrollable_frame, text="Quantity", font=("Helvetica", 16, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="e")

    item_vars = {}

    for row, (item, data) in enumerate(active_items.items(), start=1):
        ctk.CTkLabel(scrollable_frame, text=item, font=("Helvetica", 14)).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(scrollable_frame, text=str(data['quantity']), font=("Helvetica", 14)).grid(row=row, column=1, padx=40, pady=5, sticky="e")

        select_var = ctk.StringVar()
        checkbox = ctk.CTkCheckBox(scrollable_frame, variable=select_var, text="", onvalue=item, offvalue="")
        checkbox.grid(row=row, column=2, padx=10, pady=5, sticky="e")
        item_vars[item + "_select"] = select_var

    display_done_and_delete_buttons(root, controller, list_name, item_vars)

    add_more_button = ctk.CTkButton(
        root,
        text="Add More Groceries",
        command=lambda: choose_items_flow(root, controller, list_name),  
        width=200,
        height=40,
        corner_radius=10,
        font=("Helvetica", 14)
    )
    add_more_button.pack(pady=10)

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

    delete_button = ctk.CTkButton(
        root, 
        text="Delete", 
        command=lambda: delete_items_from_list(root, controller, list_name, item_vars),
        width=150, 
        height=40, 
        corner_radius=10,
        font=("Helvetica", 14)
    )

    delete_button.pack_forget()

    def check_selection():
        if any(var.get() for var in item_vars.values()):
            delete_button.pack(pady=10)
        else:
            delete_button.pack_forget()

    for var in item_vars.values():
        var.trace_add("write", lambda *args: check_selection())

    check_selection()

def mark_items_done(root, controller, list_name, item_vars):
    selected_items = [var.get() for var in item_vars.values() if var.get()]
    
    if not selected_items:
        return

    if "done_items" not in controller.grocery_lists[list_name]:
        controller.grocery_lists[list_name]["done_items"] = {}

    for item in selected_items:
        if item in controller.grocery_lists[list_name]:
            quantity = controller.grocery_lists[list_name].pop(item)
            controller.grocery_lists[list_name]["done_items"][item] = quantity

    view_list_details(root, controller, list(controller.grocery_lists.keys()).index(list_name))

def delete_items_from_list(root, controller, list_name, item_vars):
    selected_items = [var.get() for var in item_vars.values() if var.get()]
    
    if not selected_items:
        return

    for item in selected_items:
        if item in controller.grocery_lists[list_name]:
            del controller.grocery_lists[list_name][item]

    save_grocery_lists_to_file(controller.grocery_lists)
    view_list_details(root, controller, list(controller.grocery_lists.keys()).index(list_name))

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
            save_grocery_lists_to_file(controller.grocery_lists)
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
    save_grocery_lists_to_file(controller.grocery_lists)
    view_lists(root, controller)