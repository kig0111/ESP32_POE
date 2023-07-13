#création base de données avec sqlite3

import sqlite3
from pathlib import Path
from sqlite3 import Error
 

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print("Error : ",e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = 'C:/Users/drbstag/Desktop/BDD/test_V2.db'
    #creation des colonnes 
    sql_create_donnees_table = """ CREATE TABLE IF NOT EXISTS donnees (
                                        id integer PRIMARY KEY,
                                        unique_id text NOT NULL,
                                        timestamp date,
                                        T_centr text,
                                        humidite text,
                                        t_air text,
                                        rwp text,
                                        d_skin text,
                                        lum text
                                        NL text,
                                        CHP text,
                                        W_date text
                                    ); """


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create donnees table
        create_table(conn, sql_create_donnees_table)

        # create tasks table
        # create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()