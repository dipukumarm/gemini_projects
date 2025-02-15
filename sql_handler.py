# sqlite as DB and insert few records using python

import sqlite3

#Connect to sqllite

connection = sqlite3.connect('student_data.db')

# Create a cursor to traverse through the DB and do CRUD operations

cursor = connection.cursor()

# create the table

table_info = """
CREATE TABLE student
(
    NAME VARCHAR(25)  PRIMARY KEY,
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
)
"""

cursor.execute(table_info)

# Insert some data
cursor.execute("INSERT INTO student VALUES ('Kumar', 'Data Science', 'A', 90)")
cursor.execute("INSERT INTO student VALUES ('John', 'Data Science', 'B', 100)")
cursor.execute("INSERT INTO student VALUES ('Doe', 'DEVOPS', 'A', 87)")
cursor.execute("INSERT INTO student VALUES ('Nair', 'Software Engineering', 'A', 60)")
cursor.execute("INSERT INTO student VALUES ('Katherine', 'Software Engineering', 'B', 66)")

# Display the data

print("Data in the table")

data = cursor.execute("SELECT * FROM student")

for row in data:
    print(row)


# Close the connection

connection.commit()
connection.close()