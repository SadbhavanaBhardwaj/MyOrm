import psycopg2

#establishing the connection
def create_db(name):
    
    try:

        conn = psycopg2.connect(
        user='postgres', password='admin@1234', host='127.0.0.1', port= '5432'
        )
        conn.autocommit = True

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

        try:   
            #Preparing query to create a database
            sql = "CREATE database {name};".format(name=name)
            #Creating a database
            cursor.execute(sql)
            print("Database created successfully........")
        except Exception as e:
            print(e)
        
        return cursor
    except Exception as e:
        print(e)


def get_connection_cursor(db_name):
    conn = psycopg2.connect(
        database=db_name, user='postgres', password='admin@1234', host='127.0.0.1', port= '5432'
        )
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    return cursor