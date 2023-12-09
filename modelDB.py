import sqlite3
PATH="bd_app.db"

def insertarobservacion(hostname,power,rssi,x,y):

    try:
        sqliteConnection = sqlite3.connect(PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        """INSERT INTO "main"."observacion"("hostname","power","rssi","x","y") VALUES (NULL,NULL,NULL,NULL,NULL);
        """
        sqlite_insert_query = f"""INSERT INTO "main"."observacion"
                                ("hostname","power","rssi","x","y")
                                VALUES
                                ('{hostname}',{power},{rssi},{x},{y})"""


        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into observaciones table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")