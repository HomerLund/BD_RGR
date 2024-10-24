from pickle import TRUE
from model import Model
from view import View

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.table = ["Factory", "Device", "Component", "Component_category", "Buy"]
        self.attributes_name = []
        self.current_table = "None"
        

    def run(self):
        while True:
            choice = self.show_menu()
            if choice == 1:
                self.add_row()
            elif choice == 2:
                self.view_table()
            elif choice == 3:
                self.update_row()
            elif choice == 4:
                self.delete_row()
            elif choice == 5:
                break
    
    def show_menu_tabele(self):
        while(True):
            self.view.show_message("\nMenu:") 
            self.view.show_message("1. Factory")
            self.view.show_message("2. Device")
            self.view.show_message("3. Components")
            self.view.show_message("4. Component_category")
            self.view.show_message("5. Buy")      
        
            number_of_table = int(input("Enter your choice: ")) - 1
            if (number_of_table >= 0 and number_of_table < 5):   
                self.current_table = self.table[number_of_table]
                break
            else:
                self.view.show_message("\nError: not correct choice! Try again!")
    
    def show_menu_options(self):
        while(True):
            self.view.show_message("\nMenu:")
            self.view.show_message("1. Add " + self.current_table)
            self.view.show_message("2. View " + self.current_table)
            self.view.show_message("3. Update " + self.current_table)
            self.view.show_message("4. Delete " + self.current_table)
            self.view.show_message("5. Quit")
        
            option = int(input("Enter your choice: "))
            if (option >= 1 and option <= 5 ):   
                return option
            else:
                self.view.show_message("\nError: not correct choice! Try again!")
            
    def show_menu(self):
        self.show_menu_tabele()
        return self.show_menu_options()

    def get_attributes(self):
        self.attributes_name = self.model.get_attributes(self.current_table)
        
        if (self.attributes_name[0][-2:] == "id"):
            return self.attributes_name[1:]
        else:
            return self.attributes_name
        
    def add_row(self):
        try:
            self.attributes_name = self.get_attributes()
            attributes = self.view.get_table_input(self.attributes_name, self.current_table)
            self.model.add_row(attributes, self.attributes_name)
            self.view.show_message("Factory added successfully!")
        except Exception as e:     
            print(f"Error: {e}")
            self.model.query_rollback()

    def view_table(self):
        try:
            rows = self.model.get_all_rows(self.current_table)
            self.view.show_table(rows)
        except Exception as e:     
            print(f"Error: {e}")
            self.model.query_rollback()

    def update_row(self):
        try:
            row_id = self.view.get_row_id()
            self.attributes_name = self.get_attributes()
            attributes = self.view.get_table_input(self.attributes_name, self.current_table)
            self.model.update_row(row_id, attributes, self.attributes_name)
            self.view.show_message("Factory updated successfully!")
        except Exception as e:     
            print(f"Error: {e}")
            self.model.query_rollback()
            
    def delete_row(self):
        try:
            factory_id = self.view.get_row_id()
            self.model.delete_row(factory_id)
            self.view.show_message("Factory deleted successfully!")
        except Exception as e:     
            print(f"Error: {e}")
            self.model.query_rollback()
