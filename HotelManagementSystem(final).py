import tkinter as tk
from tkinter import messagebox

# Class Hotel
class Hotel:
    def __init__(self, name, location, rating, rooms_available):
        self.__name = name
        self.__location = location
        self.__rating = rating
        self.__rooms_available = rooms_available
        self.__bookings = {}

    def get_name(self):
        return self.__name

    def get_location(self):
        return self.__location

    def get_rating(self):
        return self.__rating

    def get_rooms_available(self):
        return self.__rooms_available

    def set_name(self, name):
        self.__name = name

    def set_location(self, location):
        self.__location = location

    def set_rating(self, rating):
        self.__rating = rating

    def set_rooms_available(self, rooms_available):
        self.__rooms_available = rooms_available

    def add_booking(self, user_cnic, rooms_booked):
        if user_cnic in self.__bookings:
            self.__bookings[user_cnic] += rooms_booked
        else:
            self.__bookings[user_cnic] = rooms_booked
            self.__rooms_available -= rooms_booked

    def get_total_bookings_by_user(self, user_cnic):
        if user_cnic in self.__bookings:
            return self.__bookings[user_cnic]
        return 0

    def formatted_string(self):
        return (f"Hotel Name: {self.__name}\n"
                f"Location: {self.__location}\n"
                f"Rating: {self.__rating}\n"
                f"Rooms Available: {self.__rooms_available}")

# Class User
class User:
    def __init__(self, cnic, name, age, gender, review, booked_hotel=None):
        self.__cnic = cnic
        self.__name = name
        self.__age = age
        self.__gender = gender
        self.__review = review
        self.__booked_hotel = booked_hotel

    def get_cnic(self):
        return self.__cnic

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def get_gender(self):
        return self.__gender

    def get_review(self):
        return self.__review

    def get_booked_hotel(self):
        return self.__booked_hotel

    def set_booked_hotel(self, booked_hotel):
        self.__booked_hotel = booked_hotel

    def formatted_string(self):
        return (f"User Cnic: {self.__cnic}\n"
                f"Name: {self.__name}\n"
                f"Age: {self.__age}\n"
                f"Gender: {self.__gender}\n"
                f"Review: {self.__review}\n"
                f"Booked Hotel: {self.__booked_hotel}")

# Class Bookinginfo
class Bookinginfo:
    def __init__(self, user_cnic, hotel_name, rooms_booked):
        self.__user_cnic = user_cnic
        self.__hotel_name = hotel_name
        self.__rooms_booked = rooms_booked

    def formatted_string(self):
        return (f"User Cnic: {self.__user_cnic}\n"
                f"Hotel Name: {self.__hotel_name}\n"
                f"Rooms Booked: {self.__rooms_booked}")

# Class HotelManagementsystem
class HotelManagementsystem:
    def __init__(self):
        self.hotels = []
        self.users = []
        self.userinfo = []

    def add_hotel(self, name, location, rating, rooms_available):
        hotel = Hotel(name, location, rating, rooms_available)
        self.hotels.append(hotel)

    def add_user(self, cnic, name, age, gender, review, booked_hotel_name, rooms_booked):
        hotel = None
        for h in self.hotels:
            if h.get_name() == booked_hotel_name:
                hotel = h
                break

        if not hotel:
            print(f"Hotel '{booked_hotel_name}' Not Found!")
            return

        user = None
        for u in self.users:
            if u.get_cnic() == cnic:
                user = u
                break

        if user:
            previous_bookings = hotel.get_total_bookings_by_user(cnic)
            if user.get_booked_hotel() == booked_hotel_name:
                discount = 100 - (previous_bookings / (previous_bookings + rooms_booked)) * 100
                print(f"Applying a discount for {name} of {discount:.2f}%")
            hotel.add_booking(cnic, rooms_booked)
            user.set_booked_hotel(booked_hotel_name)
        else:
            new_user = User(cnic, name, age, gender, review, booked_hotel_name)
            self.users.append(new_user)
            hotel.add_booking(cnic, rooms_booked)

        booking_info = Bookinginfo(cnic, booked_hotel_name, rooms_booked)
        self.userinfo.append(booking_info)

    def sort_hotels_by_name(self):
        self.hotels.sort(key=lambda hotel: hotel.get_name())

    def sort_hotels_by_rating(self):
        self.hotels.sort(key=lambda hotel: hotel.get_rating(), reverse=True)

    def sort_hotels_by_rooms_available(self):
        self.hotels.sort(key=lambda hotel: hotel.get_rooms_available(), reverse=True)

    def print_hotels(self):
        return [hotel.formatted_string() for hotel in self.hotels]

    def print_users(self):
        return [user.formatted_string() for user in self.users]

    def print_booking_info(self):
        return [info.formatted_string() for info in self.userinfo]

# Tkinter GUI Integration
class HotelGUI:
    def __init__(self, root, hms):
        self.root = root
        self.hms = hms  # Connect to backend
        self.color_scheme()  # Set up the color scheme
        self.main_menu()

    def color_scheme(self):
        # Set window background color
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Define color variables
        self.bg_color = "#d3e0ea"  # Light blue-gray for background
        self.btn_color = "#3aafa9"  # Teal for buttons
        self.btn_text_color = "white"  # White for button text
        self.label_color = "#2b7a78"  # Dark teal for labels
        self.entry_bg_color = "#def2f1"  # Light teal for entry boxes

    def clear_window(self):
        """Clear the current window content"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Hotel Management System", font=("Arial", 16), 
                 bg=self.bg_color, fg=self.label_color).pack(pady=20)

        tk.Button(self.root, text="Hotel Menu", command=self.hotel_menu, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)
        tk.Button(self.root, text="User Menu", command=self.user_menu, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)
        tk.Button(self.root, text="Admin Menu", command=self.admin_menu, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)

    def hotel_menu(self):
        self.clear_window()
        tk.Label(self.root, state="disabled",text="Hotel Menu", font=("Arial", 14), 
                 bg=self.bg_color, fg=self.label_color).pack(pady=10)

        tk.Button(self.root, text="Add Hotel", command=self.add_hotel_gui, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)
        tk.Button(self.root, text="Print Hotels", command=self.show_hotels, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)
        tk.Button(self.root, text="Sort Hotels by Name", command=self.sort_hotels_by_name, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)
        tk.Button(self.root, text="Sort Hotels by Rating", command=self.sort_hotels_by_rating, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)
        tk.Button(self.root, text="Sort Hotels by Rooms Available", command=self.sort_hotels_by_rooms, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)

    def add_hotel_gui(self):
        self.clear_window()
        tk.Label(self.root, text="Add Hotel", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Name:").pack()
        self.hotel_name_entry = tk.Entry(self.root)
        self.hotel_name_entry.pack()

        tk.Label(self.root, text="Location:").pack()
        self.hotel_location_entry = tk.Entry(self.root)
        self.hotel_location_entry.pack()

        tk.Label(self.root, text="Rating:").pack()
        self.hotel_rating_entry = tk.Entry(self.root)
        self.hotel_rating_entry.pack()

        tk.Label(self.root, text="Rooms Available:").pack()
        self.rooms_available_entry = tk.Entry(self.root)
        self.rooms_available_entry.pack()

        tk.Button(self.root, text="Add Hotel", command=self.add_hotel, bg=self.btn_color, 
                  fg=self.btn_text_color).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.hotel_menu, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)

    def add_hotel(self):
        name = self.hotel_name_entry.get()
        location = self.hotel_location_entry.get()
        rating = float(self.hotel_rating_entry.get())
        rooms_available = int(self.rooms_available_entry.get())
        self.hms.add_hotel(name, location, rating, rooms_available)
        messagebox.showinfo("Success", "Hotel added successfully!")
        self.hotel_menu()

    def show_hotels(self):
        hotels = self.hms.print_hotels()
        self.clear_window()
        tk.Label(self.root, text="List of Hotels", font=("Arial", 14)).pack(pady=10)
        for hotel in hotels:
            tk.Label(self.root, text=hotel, bg=self.bg_color).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.hotel_menu, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=10)

    def sort_hotels_by_name(self):
        self.hms.sort_hotels_by_name()
        messagebox.showinfo("Success", "Hotels sorted by name!")
        self.hotel_menu()

    def sort_hotels_by_rating(self):
        self.hms.sort_hotels_by_rating()
        messagebox.showinfo("Success", "Hotels sorted by rating!")
        self.hotel_menu()

    def sort_hotels_by_rooms(self):
        self.hms.sort_hotels_by_rooms_available()
        messagebox.showinfo("Success", "Hotels sorted by rooms available!")
        self.hotel_menu()

    def user_menu(self):
        self.clear_window()
        tk.Label(self.root, text="User Menu", font=("Arial", 14), 
                 bg=self.bg_color, fg=self.label_color).pack(pady=10)

        tk.Button(self.root, text="Add User", command=self.add_user_gui, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)

    def add_user_gui(self):
        self.clear_window()
        tk.Label(self.root, text="Add User", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="CNIC:").pack()
        self.user_cnic_entry = tk.Entry(self.root)
        self.user_cnic_entry.pack()

        tk.Label(self.root, text="Name:").pack()
        self.user_name_entry = tk.Entry(self.root)
        self.user_name_entry.pack()

        tk.Label(self.root, text="Age:").pack()
        self.user_age_entry = tk.Entry(self.root)
        self.user_age_entry.pack()

        tk.Label(self.root, text="Gender:").pack()
        self.user_gender_entry = tk.Entry(self.root)
        self.user_gender_entry.pack()

        tk.Label(self.root, text="Review:").pack()
        self.user_review_entry = tk.Entry(self.root)
        self.user_review_entry.pack()

        tk.Label(self.root, text="Booked Hotel:").pack()
        self.booked_hotel_entry = tk.Entry(self.root)
        self.booked_hotel_entry.pack()

        tk.Label(self.root, text="Rooms Booked:").pack()
        self.rooms_booked_entry = tk.Entry(self.root)
        self.rooms_booked_entry.pack()

        tk.Button(self.root, text="Add User", command=self.add_user, bg=self.btn_color, 
                  fg=self.btn_text_color).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.user_menu, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)

    def add_user(self):
        cnic = self.user_cnic_entry.get()
        name = self.user_name_entry.get()
        age = int(self.user_age_entry.get())
        gender = self.user_gender_entry.get()
        review = self.user_review_entry.get()
        booked_hotel_name = self.booked_hotel_entry.get()
        rooms_booked = int(self.rooms_booked_entry.get())
        self.hms.add_user(cnic, name, age, gender, review, booked_hotel_name, rooms_booked)
        messagebox.showinfo("Success", "User added successfully!")
        self.user_menu()

    def admin_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Admin Menu", font=("Arial", 14), 
                 bg=self.bg_color, fg=self.label_color).pack(pady=10)

        tk.Button(self.root, text="Print Users", command=self.show_users, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)
        tk.Button(self.root, text="Print Booking Info", command=self.show_booking_info, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=5)

    def show_users(self):
        users = self.hms.print_users()
        self.clear_window()
        tk.Label(self.root, text="List of Users", font=("Arial", 14)).pack(pady=10)
        for user in users:
            tk.Label(self.root, text=user, bg=self.bg_color).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.admin_menu, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=10)

    def show_booking_info(self):
        bookings = self.hms.print_booking_info()
        self.clear_window()
        tk.Label(self.root, text="Booking Info", font=("Arial", 14)).pack(pady=10)
        for booking in bookings:
            tk.Label(self.root, text=booking, bg=self.bg_color).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.admin_menu, width=20, 
                  bg=self.btn_color, fg=self.btn_text_color).pack(pady=10)

# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    hms = HotelManagementsystem()
    gui = HotelGUI(root, hms)
    root.title("Hotel Management System")
    root.geometry("600x500")
    root.mainloop()
