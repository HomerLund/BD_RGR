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
        
    def add_row(self, attributes, attributes_name):
        c = self.conn.cursor()
        quary = ''
        s = ''
        for name in attributes_name:
            quary += name + ', '
            s += '%s, '
        quary = quary.rstrip(', ')
        s = s.rstrip(', ')
        
        query = 'INSERT INTO factory (' + quary + ') VALUES (' + s + ')'
        values = attributes
        
        c.execute(query, values)
        self.conn.commit()

    def get_all_rows(self, table):
        c = self.conn.cursor()
        c.execute('SELECT * FROM ' + table.lower())
        return c.fetchall()

    def update_row(self, row_id, attributes, attributes_name):
        c = self.conn.cursor()
        
        quary = ''
        for name in attributes_name:
            quary += name + '=%s, '
        quary = quary.rstrip('=%s, ')
        
        query = 'UPDATE factory SET name=%s, specialization=%s, address=%s WHERE factory_id=%s'
        values = attributes
        values.append(row_id)

        c.execute(query, values)
        self.conn.commit()
          

    def delete_row(self, factory_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM factory WHERE factory_id=%s', (factory_id,))
        self.conn.commit()

    def query_rollback(self):
        self.conn.rollback()