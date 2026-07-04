#================/@/==================
#.         import the modules 
#.         defining universal things
#================/@/==================

import os
import json

FILE_NAME = "contacts_database.json"
contacts = {}

#================/@/==================
# file handling
#================/@/==================

#To load data
def load_data():
    global contacts
    
    if os.path.exists(FILE_NAME):      
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                contacts = {int(k): v for k, v in data.items()}
        
        except Exception as e:
            print(f"❌ Error loading Data : {e}")
            contacts = {}
    
    else:
        contacts = {}
        
#to save data
def save_data():
    global contacts
    
    all_contacts = list(contacts.values())
    sorted_contacts = sorted(all_contacts, key = lambda x : x.get('Name', '').strip().lower())
    contacts = {i + 1 : contact for i, contact in enumerate(sorted_contacts)}
    
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(contacts, file, indent=4)
    
    except Exception as e:
        print(f"❌ Error Saving the data: {e}")


#================/@/==================
# funtion to add convenient 
#================/@/==================

def print_contact(key):
    print(int(key))
    print(f"    Name  :  {contacts[key]["Name"]}")
    print(f"    Phone  :  +91 {contacts[key]["Phone"]}")
    print(f"    Email  :  {contacts[key]["Email"]}")
    print(f"    Address  :  {contacts[key]["Address"]}")

def check_database():
    if contacts:
        return False
    
    else:
        print("No contacts found in the database")
        return True

#================/@/==================
# Input Validation
#================/@/==================

def check_input(prompt, max_val = 10, min_val = 1, num_in = False, name_in = False, allow_blank = False):   
    while True:
        value = input(prompt)
        value = value.strip()
        
        try:
            int(value)
            if num_in:
                
                if len(value) == 10:
                    return int(value)
                
                else:
                    print("Please enter a valid number that contains 10 digits only. You don't need to enter country code")
                
            elif min_val <= int(value) <= max_val:
                return int(value)
            
            else:
                print(f"Enter the value between 1 and {max_val}")
        
        except ValueError:
            
            if value == "" and allow_blank:
                return ""
                
            if name_in:
                value = value.lower()
                return value
            
            print(f"Invalid Input! Enter a valid integral value under {max_val}")

def email_input():
    while True:
        value = input("Emain Id: ")
        value = value.strip()
        
        if value == "":
            return ""
        
        if (value.count("@") != 1) or (" " in value) or (value.endswith(".")) or (value.endswith("@")) or (value.startswith(".")) or (value.startswith("@")) or (value.count(".") < 1):
            print ("Invalid email! Please enter valid email")
        else: 
            value = value.lower()
            return value
    
    
def contact_conformation(prompt):
    value = input(f"Enter the mobile number or name of the contact you want to {prompt}").lower()
    
    number = []
    found = False
    
    for key, value in contacts.items():
        list = contacts[key]
        search_list = [list["Name"], list["Phone"]]
        
        for contact in search_list:
            if value in contact.lower():
                print_contact(key)
                print("__________________________________")
                found = True
                number.append(key)
    
    return found, number


#================/@/==================
# CRUD funtions for contact book
#================/@/==================

def add_contact():
    while True:
        print("__________________________________")
        print("Enter details below. \n(field with ' * ' are cumpolsary to be filled and  you can leave other field blank)")
    
        contact_id = None
        if contacts:
            contact_id = int(list(contacts.keys())[-1])
            contact_id += 1
        else:
            contact_id = 1
        
        name = check_input("*Name: ", name_in = True)
        number = check_input("*Number: ", num_in = True)
        email = email_input()
        address = check_input("Address: ", name_in = True, allow_blank = True)
    
        contacts[contact_id] = {"Name" : name.title(), "Phone" : str(number), "Email" : email, "Address" : address.title()}
        save_data()
        print("Contact Added succesfully☺️")
    
        print("_______________________________________")
        print("Your next move\n1. Add another contact\n2. View Contact list\n3. Return to previous menu\n4. Exit")
        next_move = check_input("Enter: ", max_val = 4)
    
        if next_move == 2:
            return view_all_contacts()
        
        elif next_move == 3:
            return True
        
        elif next_move == 4:
            return False


def view_all_contacts():
    if check_database():
        return True
    for key, value in contacts.items():
        print("___________________________________________")
        print_contact(key)
    
    print("___________________________________________")
    user_choice = check_input("Select appropriate option:-\n1. Add new contact.  \n2. Update any contact\n3. Delete any contact\n4. Return to main menu\n5. Exit\nEnter choice: ", max_val = 5)
    
    if user_choice == 1:
        return add_contact()
    
    elif user_choice == 2:
        return update_contact()
        
    elif user_choice == 3:
        return delete_contact()
        
    elif user_choice == 4:
        return True
    
    else:
        return False
        

def update_contact():
    while True:
        
        if check_database():
            return True
            
        print("_______________________________")
        found, number = contact_conformation("Search: ")
        
        if not found:
            print("No match found for your search")
            print("_______________________________")
        
        else:
            if len(number) != 1:
                while True:
                    user_preference = check_input("Please enter the the code above the contact you want to delete: ", max_val = max(number))
                
                    if user_preference in number:
                        number = [user_preference]
                        break
                    
                    else:
                        print("Please enter the value that are listed above your contact")
        
            while True:
                print("What do you want to update for this contact")
                user_choice = check_input("1. Name\n2. Number\n3. Email\n4. Address\n5. Return to previous menu \nEnter Choice: ", max_val = 5)
        
                update_value = None
                update_category = None
                
                if user_choice == 1:
                    update_value = check_input("Enter new name for the contact: ", name_in = True)
                    update_value = update_value.title()
                    update_category = "Name"
                
                elif user_choice == 2:
                    update_value = str(check_input("Enter new number for the contact: ", num_in = True))
                    update_category = "Phone"
                    
                elif user_choice == 3:
                    update_value = email_input()
                    update_category = "Email"
                
                elif user_choice == 4:
                    update_value = check_input("Enter new address for the contact: ", name_in = True, allow_blank = True).title()
                    update_category = "Address"
                
                else: 
                    break
                    
                print(f"Are you sure you want to update {update_category} ")
                user_preference = check_input("1. Yes\n2. No\nEnter choice: ", max_val = 2)
                
                if user_preference == 1:
                    contacts[number[0]][update_category] = update_value
                    save_data()
                    print(f"{update_category} updation is succesfull🙂‍↕️")
                    print("_____________________________________")
                
                user_next = check_input("Do you want to update any other information for this contact\n1. Yes\n2. No\nEnter Choice: ", max_val = 2)
                print("_____________________________________")
                if user_next == 2:
                    break

        next_choice = check_input("1. Update Another contact\n2. View all contacts\n3. Return to main menu \n4. Exit\nEnter your choice: ", max_val = 4)
        if next_choice == 2:
            return view_all_contacts()
            
        elif next_choice == 3:
            return True
            
        elif next_choice == 4:
            return False


def delete_contact():
    while True:
        
        if check_database():
            return True
            
        print("_______________________________")
        found, number = contact_conformation("Delete: ")
        
        if not found:
            print("No match found for your search")
            print("_______________________________")
        
        else:
            if len(number) != 1:
                while True:
                    user_preference = check_input("Please enter the the code above the contact you want to delete: ", max_val = max(numbers))
                
                    if user_preference in number:
                        number = [user_preference]
                        break
                    
                    else:
                        print("Please enter the value that are listed above your contact")
        
            print("Are you sure you want to delete the contact")
            user_choice = check_input("1. Yes\n2. No \nEnter Choice: ", max_val = 2)
        
            if user_choice == 1:
                del contacts[number[0]]
                save_data()
                print("Contact deletion completed ")
                print("____________________________")
        
        print("Select appropriate option")
        user_preference = check_input("1. Delete another contact\n2. View contact list \n3. Return to main menu\n4. Exit", max_val = 4)
        
        if user_preference == 2:
            return view_all_contacts()
        
        elif user_preference == 3:
            return True
        
        elif user_preference == 4:
            return False
            
       
#================/@/==================
# Addition features 
#================/@/==================

def search_contact():
    if check_database():
        return True
    
    while True:
        print("_______________________________")
        found, number = contact_conformation("Search: ")
        
        if not found:
            print("No contact found for your search")
            print("_______________________________")
        
        user_choice = check_input("1. Search for different contact\n2. View all contacts\n3. Return to main menu\n4. Exit\nEnter your choice: ", max_val = 4)
        if user_choice == 2:
            return view_all_contacts()
        
        elif user_choice == 3:
            return True
        
        elif user_choice == 4:
            return False
        
#================/@/==================
# main menu 
#================/@/==================

def main_menu():
    print("=================================")
    print("Contact Book")
    print("=================================")
    
    user_preference = check_input("1. Add new contact\n2. View Contact list\n3. Search contact\n4. Delete Comtact\n5. Update contact list\n6. Exit", max_val = 6)
    if user_preference == 1:
        return add_contact()
    
    elif user_preference == 2:
        return view_all_contacts()
    
    elif user_preference == 3:
        return search_contact()
    
    elif user_preference == 4:
        return delete_contact()
    
    elif user_preference == 5:
        return update_contact()
    
    else:
        return False

#================/@/==================
# start the contact book
#================/@/==================

load_data()

while True:
    if not main_menu():
        print("Thanks ❤️, For using contact book\nVisit again😼")
        break

