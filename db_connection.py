import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aman@2001",
        database="shree_sadguru_coaching_classes"
    )