import json
import os
import customtkinter as ctk
from utilities import clear_window
from PIL import Image

#load groceries from groceries.json
def load_groceries():
    file_path = os.path.join(os.path.dirname(__file__), 'groceries.json')

    try:
        with open(file_path, "r") as file:
            groceries_data = json.load(file)
        return groceries_data
    except json.JSONDecodeError:
        print("Error with JSON file")
        return {}

selected_groceries = None

#function to allow user to browse for groceries
def browse_groceries(root, controller):
    clear_window(root)

    header = ctk.CTkLabel(root, text="Browse Groceries", font=("Helvetica", 24, "bold"))
    header.pack(pady=20)

    main_container = ctk.CTkFrame(root)
    main_container.pack(pady=10, padx=10, fill="both", expand=True)

    sidebar_frame = ctk.CTkFrame(main_container, width=125, height=600, corner_radius=10)
    sidebar_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

    sidebar_frame.grid_propagate(False)
    sidebar_frame.pack_propagate(False)

    main_container.grid_columnconfigure(0, weight=0, minsize=100)  
    main_container.grid_columnconfigure(1, weight=1)  
    main_container.grid_rowconfigure(0, weight=1) 

    groceries_data = load_groceries()

    #show groceries from JSON
    def show_groceries(category=None, search_query=""):
        global selected_groceries

        for widget in groceries_frame.winfo_children():
            widget.destroy()

        header.configure(text="Groceries")

        if category:
            groceries_to_display = groceries_data.get(category,[])
        else:
            groceries_to_display=[]
            for category, groceries in groceries_data.items():
                for grocery in groceries:
                    if search_query.lower() in grocery["name"].lower():
                        groceries_to_display.append(grocery)
        
        #show groceries in grid format
        for idx, item in enumerate(groceries_to_display):
                row = idx // 4
                column = idx % 4

                image_path = os.path.join(os.path.dirname(__file__), "images", item["image"])
                item_image = ctk.CTkImage(Image.open(image_path), size=(50, 50))  

                item_button = ctk.CTkButton(
                    groceries_frame,
                    image=item_image,
                    text=item["name"], 
                    font=("Helvetica", 14), 
                    compound="top",  
                    command=lambda item=item: set_selected_groceries(item),
                    fg_color="transparent",
                    border_width=0
                )
                item_button.grid(row=row, column=column, padx=30, pady=30)

    button1 = ctk.CTkButton(
        sidebar_frame, 
        text="Fruits", 
        command=lambda: show_groceries("Fruits"),
        width=120,
        height=40,
        corner_radius=10
    )
    button1.pack(pady=10, padx=10, anchor="w")

    button2 = ctk.CTkButton(
        sidebar_frame, 
        text="Vegetables", 
        command=lambda: show_groceries("Vegetables"),
        width=120,
        height=40,
        corner_radius=10
    )
    button2.pack(pady=10, padx=10, anchor="w")

    button3 = ctk.CTkButton(
        sidebar_frame, 
        text="Meat", 
        command=lambda: show_groceries("Meat"),
        width=120,
        height=40,
        corner_radius=10
    )
    button3.pack(pady=10, padx=10, anchor="w")

    button4 = ctk.CTkButton(
        sidebar_frame, 
        text="Dairy", 
        command=lambda: show_groceries("Dairy"),
        width=120,
        height=40,
        corner_radius=10
    )
    button4.pack(pady=10, padx=10, anchor="w")

    save_button = ctk.CTkButton(
        sidebar_frame, 
        text="Save", 
        command=save_groceries,
        width=120,
        height=40,
        corner_radius=10
    )
    save_button.pack(pady=20, padx=10, anchor="w")

    main_frame = ctk.CTkFrame(main_container, width=600, height=600, corner_radius=10)
    main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    
    search_entry = ctk.CTkEntry(main_frame, placeholder_text="Search for groceries...", width=520)
    search_entry.pack(pady=10)

    #allow search bar input
    def on_search_change(event=None):
        search_query = search_entry.get()
        show_groceries(search_query=search_query)
    search_entry.bind("<KeyRelease>", on_search_change)

    groceries_frame = ctk.CTkScrollableFrame(main_frame, width=520, height=400, corner_radius=10)
    groceries_frame.pack(fill="both", expand=True, padx=20, pady=20)

    show_groceries()

    back_button = ctk.CTkButton(
        sidebar_frame, 
        text="Back", 
        command=controller.show_homepage,
        width=120, 
        height=40, 
        corner_radius=10,
        font=("Helvetica", 10)
    )
    back_button.pack(padx=10, pady=50)

#add selected groceries to array
def set_selected_groceries(item):
    global selected_groceries
    selected_groceries = item
    print(f"selected {selected_groceries}")

#save groceries to array (not used)
def save_groceries():
    global set_selected_groceries
    if selected_groceries:
        saved_groceries.append(selected_groceries)
        print(f"saved: {selected_groceries}")
    else:
        print("no groceries selected") 