import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import date

class Pet:
    def __init__(self, name, breed, age, weight, health_records=None, vaccinations=None, appointments=None):
        self.name = name
        self.breed = breed
        self.age = age
        self.weight = weight
        self.health_records = health_records if health_records else []
        self.vaccinations = vaccinations if vaccinations else []
        self.appointments = appointments if appointments else []

    def to_dict(self):
        return {
            "name": self.name, 
            "breed": self.breed, 
            "age": self.age,
            "weight": self.weight, 
            "health_records": self.health_records, 
            "vaccinations": self.vaccinations,
            "appointments": self.appointments
        }

class User:
    def __init__(self, username, password, pets_data=None):
        self.username = username
        self.password = password
        self.pets = []
        
        if pets_data:
            for p in pets_data:
                self.pets.append(Pet(
                    p['name'], p['breed'], p['age'], p['weight'], 
                    p.get('health_records'), p.get('vaccinations'), p.get('appointments')
                ))

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "pets": [p.to_dict() for p in self.pets]
        }

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class PetHealthApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pet Health Tracker")
        self.geometry("800x600")
        
        self.users = []
        self.current_user = None
        self.load_data()

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_login_screen()

    def load_data(self):
        if os.path.exists('data.json'):
            with open('data.json', 'r') as f:
                data = json.load(f)
                for u_data in data:
                    self.users.append(User(u_data['username'], u_data['password'], u_data['pets']))

    def save_data(self):
        data = [u.to_dict() for u in self.users]
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def show_login_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Welcome Back", font=("Roboto", 24, "bold")).pack(pady=40)

        self.entry_user = ctk.CTkEntry(self.main_frame, placeholder_text="Username", width=250)
        self.entry_user.pack(pady=10)
        
        self.entry_pass = ctk.CTkEntry(self.main_frame, placeholder_text="Password", show="*", width=250)
        self.entry_pass.pack(pady=10)

        ctk.CTkButton(self.main_frame, text="Login", command=self.login_logic).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Register", command=self.register_logic, fg_color="transparent", border_width=2).pack(pady=5)

    def show_dashboard(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(self.main_frame, height=50, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=f"Hello, {self.current_user.username}!", font=("Roboto", 20, "bold")).pack(side="left")
        ctk.CTkButton(header, text="Logout", width=80, fg_color="red", command=self.logout).pack(side="right")

        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True, pady=10)

        self.tab_pets = self.tabview.add("My Pets")
        self.tab_add = self.tabview.add("Add New Pet")

        self.setup_pets_tab()
        self.setup_add_tab()

    def login_logic(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                self.show_dashboard()
                return
        
        messagebox.showerror("Error", "Invalid username or password")

    def register_logic(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        if any(u.username == username for u in self.users):
            messagebox.showerror("Error", "User already exists")
            return
        
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_data()
        messagebox.showinfo("Success", "Account created! Please login.")

    def logout(self):
        self.current_user = None
        self.show_login_screen()

    def setup_pets_tab(self):
        for widget in self.tab_pets.winfo_children():
            widget.destroy()

        if not self.current_user.pets:
            ctk.CTkLabel(self.tab_pets, text="No pets found. Go to 'Add New Pet' tab!").pack(pady=20)
            return

        scroll_frame = ctk.CTkScrollableFrame(self.tab_pets)
        scroll_frame.pack(fill="both", expand=True)

        for pet in self.current_user.pets:
            self.create_pet_card(scroll_frame, pet)

    def create_pet_card(self, parent, pet):
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", pady=5, padx=5)

        info_text = f"{pet.name} ({pet.breed}) - {pet.age} yrs"
        ctk.CTkLabel(card, text=info_text, font=("Roboto", 14, "bold")).pack(side="left", padx=10)
        
        btn = ctk.CTkButton(card, text="Add Entry", width=120, height=30, 
                            command=lambda p=pet: self.open_add_entry_window(p))
        btn.pack(side="right", padx=10, pady=10)

        btn_view = ctk.CTkButton(card, text="View Records", width=100, height=30, fg_color="gray",
                                 command=lambda p=pet: self.view_pet_info(p))
        btn_view.pack(side="right", padx=5, pady=10)

    def setup_add_tab(self):
        ctk.CTkLabel(self.tab_add, text="Pet Details").pack(pady=10)
        
        self.entry_pet_name = ctk.CTkEntry(self.tab_add, placeholder_text="Pet Name")
        self.entry_pet_name.pack(pady=5)
        
        self.entry_pet_breed = ctk.CTkEntry(self.tab_add, placeholder_text="Breed")
        self.entry_pet_breed.pack(pady=5)

        self.entry_pet_age = ctk.CTkEntry(self.tab_add, placeholder_text="Age")
        self.entry_pet_age.pack(pady=5)

        self.entry_pet_weight = ctk.CTkEntry(self.tab_add, placeholder_text="Weight")
        self.entry_pet_weight.pack(pady=5)

        ctk.CTkButton(self.tab_add, text="Save Pet", fg_color="green", command=self.save_new_pet).pack(pady=20)

    def save_new_pet(self):
        name = self.entry_pet_name.get()
        breed = self.entry_pet_breed.get()
        age = self.entry_pet_age.get()
        weight = self.entry_pet_weight.get()

        if name:
            new_pet = Pet(name, breed, age, weight)
            self.current_user.pets.append(new_pet)
            self.save_data()
            self.entry_pet_name.delete(0, "end")
            
            self.setup_pets_tab()
            self.tabview.set("My Pets")
        else:
            messagebox.showwarning("Missing Info", "Please enter at least a name.")

    def open_add_entry_window(self, pet):
        self.add_win = ctk.CTkToplevel(self)
        self.add_win.title(f"Add Entry for {pet.name}")
        self.add_win.geometry("400x350")
        self.add_win.attributes('-topmost', True)

        ctk.CTkLabel(self.add_win, text="Select Type:", font=("Roboto", 14)).pack(pady=5)
        self.type_var = ctk.StringVar(value="Health Record")
        type_seg = ctk.CTkSegmentedButton(self.add_win, values=["Health Record", "Vaccination", "Appointment"],
                                          variable=self.type_var)
        type_seg.pack(pady=5)

        self.entry_date = ctk.CTkEntry(self.add_win, placeholder_text="Date (YYYY-MM-DD)")
        self.entry_date.insert(0, str(date.today()))
        self.entry_date.pack(pady=10)

        self.entry_desc = ctk.CTkEntry(self.add_win, placeholder_text="Description / Notes", width=300)
        self.entry_desc.pack(pady=10)

        ctk.CTkButton(self.add_win, text="Save Entry", fg_color="green", 
                      command=lambda: self.save_entry_logic(pet)).pack(pady=20)

    def save_entry_logic(self, pet):
        record_type = self.type_var.get()
        date_str = self.entry_date.get()
        desc = self.entry_desc.get()

        if not desc or not date_str:
            messagebox.showwarning("Input Error", "Date and Description are required.")
            return

        final_entry = {"date": date_str, "description": desc}

        if record_type == "Health Record":
            pet.health_records.append(final_entry)
        elif record_type == "Vaccination":
            pet.vaccinations.append(final_entry)
        elif record_type == "Appointment":
            pet.appointments.append(final_entry)

        self.save_data()
        self.add_win.destroy()
        messagebox.showinfo("Success", f"{record_type} added successfully.")

    def view_pet_info(self, pet):
        info_window = ctk.CTkToplevel(self)
        info_window.title(f"{pet.name} Info")
        info_window.geometry("500x600")
        info_window.attributes('-topmost', True)

        ctk.CTkLabel(info_window, text=f"{pet.name}", font=("Roboto", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(info_window, text=f"Weight: {pet.weight} | Age: {pet.age}").pack()

        scroll = ctk.CTkScrollableFrame(info_window)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scroll, text="--- Vaccinations ---", text_color="cyan", font=("Roboto", 16, "bold")).pack(pady=(10, 5))
        if not pet.vaccinations:
            ctk.CTkLabel(scroll, text="None").pack()
        else:
            for rec in pet.vaccinations:
                ctk.CTkLabel(scroll, text=f"[{rec['date']}] {rec['description']}").pack(anchor="w", padx=10)

        ctk.CTkLabel(scroll, text="--- Health Records ---", text_color="cyan", font=("Roboto", 16, "bold")).pack(pady=(20, 5))
        if not pet.health_records:
            ctk.CTkLabel(scroll, text="None").pack()
        else:
            for rec in pet.health_records:
                ctk.CTkLabel(scroll, text=f"[{rec['date']}] {rec['description']}").pack(anchor="w", padx=10)

        ctk.CTkLabel(scroll, text="--- Appointments ---", text_color="cyan", font=("Roboto", 16, "bold")).pack(pady=(20, 5))
        if not pet.appointments:
            ctk.CTkLabel(scroll, text="None").pack()
        else:
            for rec in pet.appointments:
                ctk.CTkLabel(scroll, text=f"[{rec['date']}] {rec['description']}").pack(anchor="w", padx=10)

if __name__ == "__main__":
    app = PetHealthApp()
    app.mainloop()