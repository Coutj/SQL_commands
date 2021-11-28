from pandas.io.sql import execute
from sqlalchemy import create_engine
import pandas as pd
from faker import Faker
from random import randint


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
    query = "DROP TABLE IF EXISTS employes, supervisors, branch;"

    execute_query(query)

def creating_tables():

    query_supervisor = (
        "CREATE TABLE supervisors( "
            "id SERIAL PRIMARY KEY, "
            "name VARCHAR "
        ");"
    )

    execute_query(query_supervisor)
    print('Supervisors table created...')

    query_branch = (
        "CREATE TABLE branch( "
            "id INT PRIMARY KEY, "
            "branch_name VARCHAR "
        ");"
    )

    execute_query(query_branch)
    print('Branch table created...')

    query_employ = (
        "CREATE TABLE employes( "
            "id INT PRIMARY KEY NOT NULL, "
            "name VARCHAR NOT NULL DEFAULT 'JOAO', "
            "job VARCHAR NULL, "
            "salary INT, "
            "supervisor_id INT, "
            "branch_id INT "
        ");"
    )
    
    execute_query(query_employ)
    print('Employes table created...')

    fk_query = (
        "ALTER TABLE employes "
        "ADD FOREIGN KEY(supervisor_id) "
        "REFERENCES supervisors(id) "
        "ON DELETE SET NULL; "
        "ALTER TABLE employes "

        "ADD FOREIGN KEY(branch_id) "
        "REFERENCES branch(id) "
        "ON DELETE SET NULL; "

    )

    execute_query(fk_query)
    print('Foreign keys added...')

    
def populate_data():

    conn = db_connection()

    fake = Faker()

    supervisors = {
        'id': [id for id in range(10)],
        'name': [fake.name() for index in range(10)]
    }

    supervisors_df = pd.DataFrame(supervisors)
    supervisors_df.to_sql('supervisors', if_exists='append', con=conn, index=False)
    print('Supervisors table filled with fake data...')

    branch = {
        'id': [id for id in range(10)],
        'branch_name': [fake.company() for index in range(10)]
    }

    branch_df = pd.DataFrame(branch)
    branch_df.to_sql('branch', if_exists='append', con=conn, index=False)
    print('Branch table filled with fake data...')

    employes = {
        'id': [index for index in range(500)],
        'name': [fake.name() for index in range(500)],
        'job': [fake.job() for index in range(500)],
        'salary': [randint(1000, 10000) for index in range(500)],
        'supervisor_id': [
            supervisors_df.sample(n=1).iloc[0, 0] for index in range(500)
        ],
        'branch_id': [branch_df.sample(n=1).iloc[0,0] for i in range(500) ]
    }

    employes_df = pd.DataFrame(employes)
    employes_df.to_sql('employes', if_exists='append', con=conn, index=False)
    print('Employes table filled with fake data...')


    conn.close()


if __name__ == '__main__':
    clean_db()
    creating_tables()
    populate_data()
