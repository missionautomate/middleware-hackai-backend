import psycopg2

conn_string = "postgres://missionautomate:Parola1234%23@postgre-db-server.postgres.database.azure.com:5432/postgres"

# print the connection string we will use to connect
print ("Connecting to database\n	->%s" % (conn_string))

# get a connection, if a connect cannot be made an exception will be raised here
conn = psycopg2.connect(conn_string)

# conn.cursor will return a cursor object, you can use this cursor to perform queries
cursor = conn.cursor()
command = """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_fname VARCHAR(255) NOT NULL,
            user_lname VARCHAR(255) NOT NULL,
            user_email VARCHAR(255) NOT NULL
        )
        """
print ("Connected!\n")

cursor.execute(command)
cursor.close()
conn.commit()