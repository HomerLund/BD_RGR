from tabulate import tabulate
class View:
    def show_table(self, rows, attributes_name, table):
        print(table + ":") 
        table = tabulate(rows, attributes_name, tablefmt="grid")
        print(table)

    def get_table_input(self, attributes_name, table):
        attributes = []      
        for attribute in attributes_name:
            attributes.append(input("Enter " + table + " " + attribute + ": "))
        
        
        return attributes

    def get_row_id(self, table):
        return int(input("Enter " + table + " ID: "))

    def show_message(self, message):
        print(message)
