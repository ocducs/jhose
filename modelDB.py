import sqlite3
from datetime import datetime
PATH="bd_app.db"

def insertarobservacion(imei,hostname,power,rssi,x,y):

    try:
        sqliteConnection = sqlite3.connect(PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        """INSERT INTO "main"."observacion"("imei","hostname","power","rssi","x","y") VALUES (NULL,NULL,NULL,NULL,NULL);
        """
        ## Guardamos la observacion-estimacion
        sqlite_insert_query = f"""INSERT INTO "main"."observacion"
                                ("imei","hostname","power","rssi","x","y")
                                VALUES
                                ('{imei}','{hostname}',{power},{rssi},{x},{y})"""

        
        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into observaciones table ", cursor.rowcount)
        
        fecha = datetime.now()
        ## Guardamos la estimación
        sqlite_insert_localizacion = f"""INSERT INTO "main"."localizacion"
                                ("imei","longitud","latitud","fecha")
                                VALUES
                                ('{imei}',{x},{y},{datetime.timestamp(fecha)})"""
        
        count = cursor.execute(sqlite_insert_localizacion)
        sqliteConnection.commit()
        print("Record inserted successfully into localizacion table ", cursor.rowcount)
        
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
    
def insertarLocalizacion(imei,x,y):

    try:
        sqliteConnection = sqlite3.connect(PATH)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        """INSERT INTO "main"."observacion"("imei","hostname","power","rssi","x","y") VALUES (NULL,NULL,NULL,NULL,NULL);
        """
        ## Guardamos la observacion-estimacion
        
        fecha = datetime.now()
        ## Guardamos la estimación
        sqlite_insert_localizacion = f"""INSERT INTO "main"."localizacion"
                                ("imei","longitud","latitud","fecha")
                                VALUES
                                ('{imei}',{x},{y},{datetime.timestamp(fecha)})"""
        
        count = cursor.execute(sqlite_insert_localizacion)
        sqliteConnection.commit()
        print("Record inserted successfully into localizacion table ", cursor.rowcount)
        
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")