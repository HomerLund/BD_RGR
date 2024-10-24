class View:
    def show_table(self, rows):
        print("Tasks:")
        for row in rows:
            print(f"factory_id: {row[0]}, name: {row[1]}, specialization: {row[2]}, address: {row[3]}")

    def get_table_input(self, attributes_name, table):
        attributes = []      
        for attribute in attributes_name:
            attributes.append(input("Enter " + table + " " + attribute + ": "))
        
        
        return attributes

    def get_row_id(self):
        return int(input("Enter Factory ID: "))

    def show_message(self, message):
        print(message)
