import pyodbc


def get_db_connection():
    try:
        return pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                              "Server=localhost;"
                              "Database=Security;"
                              "Trusted_Connection=yes;")
    except Exception as e:
        print("Failed to Connect DB. Message: %s", e)
        return None


def insert_update(query, id_query, data=None):
    try:
        db = get_db_connection()
        if db is None:
            return False

        cursor = db.cursor()
        cursor.execute(query, data)
        id_ = cursor.execute(id_query).fetchval()
        db.commit()
        return id_

    except Exception as e:
        print("Failed to insert/update query. Message: %s", e)
        return False


def read(query):
    try:
        db = get_db_connection()
        if db is None:
            return False

        cursor = db.cursor()
        result = cursor.execute(query)

        columns = [column[0] for column in result.description]
        res = []

        for row in result.fetchall():
            res.append(dict(zip(columns, row)))

        return res

    except Exception as e:
        print("Failed to read query. Message: %s", e)
        return False
