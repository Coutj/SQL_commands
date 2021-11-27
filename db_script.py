from sqlalchemy import create_engine
import pandas as pd
from faker import Faker


def db_connection():
    conn_string = "postgresql://admin:admin@localhost:5000/learning_sql"
    engine = create_engine(conn_string)

    conn = engine.connect()

    return conn

def execute_query(query):
    conn = db_connection()

    conn.execute(query)

    conn.close()


def clean_db():
    query = "DROP TABLE IF EXISTS students;"

    execute_query(query)

def creating_tables():

    query = (
        "CREATE TABLE students( "
            "student_id INT PRIMARY KEY, "
            "name VARCHAR, "
            "major VARCHAR "
        ");"
    )

    print('\nStudent table created...')

    execute_query(query)

    
def populate_data():

    conn = db_connection()

    fake = Faker()

    students = {
        'student_id': [],
        'name': [],
        'major': [],
    }

    for index in range(1000):
        students['student_id'].append(index)
        students['name'].append(fake.name())
        students['major'].append(fake.job())


    students_df = pd.DataFrame(students)
    students_df.to_sql('students', if_exists='append', con=conn, index=False)
    print('Student table filled with fake data...')


if __name__ == '__main__':
    clean_db()
    creating_tables()
    populate_data()
