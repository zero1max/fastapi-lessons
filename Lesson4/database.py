import psycopg2

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            database="fastapi",
            user="postgres",
            password="1",
            host="localhost",
            port=5432
        )
        self.cursor = self.connection.cursor()

    # def create_table(self):
    #     self.cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS users (
    #         id SERIAL PRIMARY KEY,
    #         fullname VARCHAR(255) NOT NULL,
    #         username VARCHAR(100) UNIQUE NOT NULL,
    #         email VARCHAR(255) UNIQUE NOT NULL,
    #         password VARCHAR(255) NOT NULL
    #     )
    #     """)
    #     self.connection.commit()

    def add_user(self, fullname, username, email, password):
        self.cursor.execute(
            "INSERT INTO users (fullname, username, email, password) VALUES (%s, %s, %s, %s)",
            (fullname, username, email, password)
        )
        self.connection.commit()  


    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        return users

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return self.cursor.fetchone()

    def update_user(self, user_id, fullname, username, email, password):
        self.cursor.execute("""
            UPDATE users 
            SET fullname = %s, username = %s, email = %s, password = %s
            WHERE id = %s
        """, (fullname, username, email, password, user_id))
        self.connection.commit()
        return True

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        self.connection.commit()
