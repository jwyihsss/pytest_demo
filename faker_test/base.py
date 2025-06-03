import pymysql
import logging
from faker import Faker

logging.basicConfig(level=logging.INFO)


def connect_db():
    try:
        db = pymysql.connect(host='localhost', user='root', password='123456', db='mysql', charset='utf8')
        return db
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        raise

def delete_data(table_name, where_clause):
    db = None
    cursor = None

    try:
        # Connect to the database
        db = connect_db()
        cursor = db.cursor()

        # Prepare the SQL statement
        sql = f'DELETE FROM {table_name} WHERE {where_clause}'

        # Execute the SQL command
        cursor.execute(sql)

        # Commit your changes in the database
        db.commit()
        logging.info(f"Data deleted successfully with condition: {where_clause}")
    except Exception as e:
        # Rollback in case there is any error
        if db:
            db.rollback()
        logging.error(f"Error deleting data: {e}")
    finally:
        # Close the connection
        if cursor:
            cursor.close()
        if db:
            db.close()

# Call the function to delete data
if __name__ == '__main__':
    table_name = 'users'
    where_clause = 'id > 2'
    delete_data(table_name, where_clause)
