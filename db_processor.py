import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="zluri"
)


def insert_catalog(val):
    """
    insert product catalog, where all three column values are present
    :param val:
    :return:
    """
    cursor = db.cursor()
    sql = "INSERT INTO catalog (sku, name, description) VALUES (%s, %s, %s) " \
          "ON DUPLICATE KEY UPDATE name=VALUES(name), description=VALUES(description)"
    cursor.execute(sql, val)
    db.commit()


def log_error(row):
    """
    insert into error table incompatible rows
    :param row:
    :return:
    """
    cursor = db.cursor()
    sql = "INSERT INTO error_catalog (id, item) VALUES (%s, %s)"
    cursor.execute(sql, (cursor.lastrowid, row))
    db.commit()


def get_count_by_name():
    """
    Get row counts by name
    :return:
    """
    cursor = db.cursor()
    sql = "SELECT name, count(*) as count from zluri.catalog group by name order by count desc"
    cursor.execute(sql)
    print(cursor.fetchall())
