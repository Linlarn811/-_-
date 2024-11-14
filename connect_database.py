import pyodbc

def connect_to_database():
    try:
        connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=AAA;"
            "DATABASE=在线教学系统;"
            "UID=sa;"
            "PWD=Lin20050221;"
        )
        print("Database connected successfully!")
        return connection
    except pyodbc.Error as e:
        print("Error connecting to database:", e)
        return None
