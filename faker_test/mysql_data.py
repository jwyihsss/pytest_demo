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


def insert_fake_data(table_name, columns, data_count):
    fake = Faker('zh-CN')
    db = None
    cursor = None
    data_generators = {
        'username': fake.unique.name,
        'email': fake.email,
        'age': lambda: fake.random_int(min=18, max=99),
        'password': fake.password,
        'last_login': fake.date_time_this_month,
        'is_superuser': lambda: fake.boolean(chance_of_getting_true=5),
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        "is_staff": lambda: fake.boolean(chance_of_getting_true=10),
        'is_active': lambda: fake.boolean(chance_of_getting_true=95),
        'date_joined': fake.date_time_this_year,
        'nickname': fake.unique.name
    }

    try:
        db = connect_db()
        cursor = db.cursor()

        for _ in range(data_count):
            data = [data_generators[col]() for col in columns]
            placeholders = ', '.join(['%s'] * len(columns))
            sql = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'
            cursor.execute(sql, data)

        db.commit()
        logging.info(f"{data_count} records inserted successfully.")
    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        if db:
            db.rollback()
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


if __name__ == '__main__':
    table_name = 'users'
    columns = ['username', 'email', 'password', 'last_login', 'is_superuser', 'first_name', 'last_name',
               "is_staff", 'is_active', 'date_joined', 'nickname']
    data_count = 1000
    insert_fake_data(table_name, columns, data_count)
