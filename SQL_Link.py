import mysql.connector as sqlconnect


def command(
    query: str,
    Password: str,
    database: str,
    User: str = "root",
    Host: str = "localhost"
    ):
    
    try :
        db = sqlconnect.connect(
            user     = User,
            password = Password,
            host     = Host
        )
    except :
        return False

    cursor = db.cursor()

    try :
        cursor.execute(f"create database {database}")
    except  :
        pass

    cursor.execute(f"use {database}")

    try :
        cursor.execute(query)
    except :
        print(f"Wrong Input\n{database = }\n{query = }")

    x = cursor.fetchall()
    
    try :
        db.commit()
    except  :
        pass

    return x
    
