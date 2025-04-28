import mysql.connector
import env


class DBhelper:
    def __init__(self):
        print("Connecting to the database...")
        try:
            self.conn = mysql.connector.connect(
                host=env.host,
                user=env.user,
                password=env.password,
                database=env.database,
            )
            self.mycursor = self.conn.cursor()
            print('Connected to Database')
        except mysql.connector.Error as e:
            print("Some error occurred. Could not connect to the database.")
            print(f"Error details: {e}")

    def register(self, first_name, last_name, username, phone, email, password,role):
        try:
            # Check if the username, email, or phone already exists
            self.mycursor.execute("SELECT * FROM users WHERE username=%s OR email=%s OR phone=%s",
                                  (username, email, phone))
            if self.mycursor.fetchone():
                return -1  # User already exists

            self.mycursor.execute(
    "INSERT INTO users (first_name, last_name, username, phone, email, password, `role`) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    (first_name, last_name, username, phone, email, password, role)
)
            self.conn.commit()
            return self.mycursor.lastrowid  # Return the ID of the newly created user
        except mysql.connector.Error as e:
            print(f"Error during registration: {e}")
            return -1

    def search(self, identifier, password):
        # Searching by email, phone, or username
        self.mycursor.execute("""
        SELECT * FROM users WHERE (email = %s OR phone = %s OR username = %s) AND password = %s
        """, (identifier, identifier, identifier, password))

        data = self.mycursor.fetchall()
        return data
