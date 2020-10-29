import csv
import psycopg2

connection = None
cursor = None

try:
    connection = psycopg2.connect(user="postgres",
                                  password="mysecretpassword",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")

    cursor = connection.cursor()

    # # Create table
    # cursor.execute("""
    #     CREATE TABLE zipcodes(
    #     zipcode integer PRIMARY KEY,
    #     class text
    # )
    # """)
    # connection.commit()

    def insert_data():

        zipcodes = {}

        with open('zipcodes.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                boundries = row[0].split("-")

                if len(boundries) > 1:
                    r = range(int(boundries[0]), int(boundries[1]) + 1)
                    for item in list(r):
                        zipcodes[item] = row[1]
                else:
                    zipcodes[boundries[0]] = row[1]

        # for key, value in zipcodes.items():
        #     cursor.execute("INSERT INTO zipcodes VALUES (%s, %s)", (key, value))
        #
        # connection.commit()


    # insert_data()

    cursor.execute('select * from zipcodes')
    for record in cursor.fetchall():
        print(record)

    # Print PostgreSQL Connection properties
    # print(connection.get_dsn_parameters(), "\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    # print("You are connected to - ", record, "\n")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
