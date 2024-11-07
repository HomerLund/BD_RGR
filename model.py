import psycopg


class Model:
    def __init__(self):
        self.conn = psycopg.connect(
            dbname='lab1',
            user='postgres',
            password='0000',
            host='localhost',
            port=5432
        )
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS factory (
                factory_id SERIAL PRIMARY KEY,
                name VARCHAR(30) NOT NULL,
                specialization VARCHAR(60) NOT NULL,
                address VARCHAR(70) NOT NULL UNIQUE
            )
        ''')

        # Check if the table exists
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tasks')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Table does not exist, so create it
            c.execute('''
                CREATE TABLE tasks (
                    factory_id SERIAL PRIMARY KEY,
                    name VARCHAR(30) NOT NULL,
                    specialization VARCHAR(60) NOT NULL,
                    address VARCHAR(70) NOT NULL UNIQUE        
                )
            ''')

        self.conn.commit()

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
        query = """ SELECT d.device_id, d.name, f.factory_id, f.name, f.address FROM device d
                    JOIN factory f ON d.factory_id = f.factory_id
                    WHERE f.factory_id = """ + str(FK) + """
                    GROUP BY f.address
                    ORDER BY d.device_id ASC;"""
        c.execute(query)
        
        rows = c.fetchall()
    
        column_names = [desc[0] for desc in c.description]
        
        return rows, column_names
    
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