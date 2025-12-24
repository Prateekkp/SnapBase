import mysql.connector

def connect_server(host, user, password):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        connection_timeout=10
    )

def connect_database(host, user, password, database):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        connection_timeout=10
    )