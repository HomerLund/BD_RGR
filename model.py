import psycopg
import time

class Model:
    def __init__(self):
        self.conn = psycopg.connect(
            dbname='lab1',
            user='postgres',
            password='0000',
            host='localhost',
            port=5432
        )

    def get_attributes(self, table):
        c = self.conn.cursor()
        c.execute(f"SELECT * FROM " + table.lower() + " LIMIT 0")
        return [desc[0] for desc in c.description]
        
    def add_row(self, attributes, attributes_name, table):
        c = self.conn.cursor()
        quary = ''
        s = ''
        for name in attributes_name:
            quary += name + ', '
            s += '%s, '
        quary = quary.rstrip(', ')
        s = s.rstrip(', ')
        
        query = 'INSERT INTO ' + table.lower() + ' (' + quary + ') VALUES (' + s + ')'
        values = attributes
        
        c.execute(query, values)
        self.conn.commit()

    def get_DeviceOfFactory(self, FK):
        c = self.conn.cursor()
        
        start_time = time.time()
        
        query = """ SELECT f.factory_id,  f.name, f.address, d.name, COUNT(*) as count FROM device d
                    JOIN factory f ON d.factory_id = f.factory_id
                    WHERE f.factory_id = """ + str(FK) + """
                    GROUP BY f.factory_id, d.name
                    ORDER BY f.factory_id ASC;"""
        c.execute(query)
        
        end_time = time.time()
        duration = end_time - start_time
        
        rows = c.fetchall()
    
        column_names = [desc[0] for desc in c.description]
        
        return rows, column_names, duration * 1000
    
    def get_ComponentsOfDevice(self, FK):
        c = self.conn.cursor()
        
        start_time = time.time()
        
        query = """ SELECT d.device_id,  d.name, c.name, AVG(c.weight) as avg_weight FROM device d
                    JOIN components c ON d.device_id = c.device_id
                    WHERE d.device_id = """ + str(FK) + """
                    GROUP BY d.device_id, c.name
                    ORDER BY d.device_id ASC;"""
        c.execute(query)
        
        end_time = time.time()
        duration = end_time - start_time
        
        rows = c.fetchall()
    
        column_names = [desc[0] for desc in c.description]
        
        return rows, column_names, duration * 1000
    
    def get_BuyOfComponents(self, first_date, second_date, FK):
        c = self.conn.cursor()
        
        start_time = time.time()
        
        query = """ SELECT f.factory_id,  f.name, c.component_id, c.name, b.date, b.price FROM buy b
                    JOIN factory f ON b.factory_id = f.factory_id
                    JOIN components c ON b.component_id = c.component_id
                    WHERE b.date BETWEEN '""" + first_date + """' AND '""" + second_date + """'
                    AND f.factory_id = """ + str(FK) + """
                    ORDER BY f.factory_id ASC;"""
        c.execute(query)
        
        end_time = time.time()
        duration = end_time - start_time
        
        rows = c.fetchall()
    
        column_names = [desc[0] for desc in c.description]
        
        return rows, column_names, duration * 1000
    
    def get_all_rows(self, table):
        c = self.conn.cursor()
        c.execute('SELECT * FROM ' + table.lower())
        return c.fetchall()

    def update_row(self, row_id, PK, attributes, attributes_name, table):
        c = self.conn.cursor()
        
        quary = ''
        for name in attributes_name:
            quary += name + '=%s, '
        quary = quary.rstrip(', ')
        
        query = 'UPDATE ' + table.lower() + ' SET ' + quary + ' WHERE ' + PK + '=%s'
        values = attributes
        values.append(row_id)

        c.execute(query, values)
        self.conn.commit()
          

    def delete_row(self, row_id, PK, table):
        c = self.conn.cursor()
        c.execute('DELETE FROM ' + table.lower() + ' WHERE ' + PK + '=%s', (row_id,))
        self.conn.commit()
        
    def reset_identity(self, table):
        c = self.conn.cursor()
        c.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = %s 
            AND is_identity = 'YES'
            ORDER BY ordinal_position 
            LIMIT 1;
        """, (table.lower(),))
        result = c.fetchone()
        
        if result:
            identity_column = result[0]
            c.execute(f"ALTER TABLE {table} ALTER COLUMN {identity_column} RESTART WITH 1;")


    
    def delete_table(self, table):
        c = self.conn.cursor()
        query = 'TRUNCATE TABLE ' + table.lower() + ' CASCADE'
        c.execute(query)
        self.reset_identity(table)
        self.conn.commit()
        
    def random_table(self, counts, table):
        c = self.conn.cursor()
        query = 'CALL random_' + table.lower() + '(' + str(counts) + ')'
        c.execute(query)
        self.conn.commit()

    def query_rollback(self):
        self.conn.rollback()