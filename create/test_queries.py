import mysql.connector
import pytest

@pytest.fixture(scope="module")
def test_db():
    # اتصال اولیه به MySQL (بدون مشخص کردن database)
    conn = mysql.connector.connect(
        host="localhost", user="root", password="mahdi", autocommit=True
    )
    cursor = conn.cursor()

    # ساخت دیتابیس تست
    cursor.execute("DROP DATABASE IF EXISTS test_db")
    cursor.execute("CREATE DATABASE test_db")
    cursor.close()
    conn.close()

    # اتصال به دیتابیس تست
    conn = mysql.connector.connect(
        host="localhost", user="root", password="mahdi", database="test_db"
    )
    cursor = conn.cursor(dictionary=True)

    # اجرای فایل کوئری
    with open("query.sql", "r") as f:
        queries = f.read().split(";")
        for query in queries:
            if query.strip():
                cursor.execute(query)

    conn.commit()

    yield cursor

    # پاکسازی بعد از تست
    cursor.close()
    conn.close()

    # حذف دیتابیس
    conn = mysql.connector.connect(
        host="localhost", user="root", password="mahdi", autocommit=True
    )
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS test_db")
    cursor.close()
    conn.close()


def test_user_lastname(test_db):
    test_db.execute("SELECT last_name FROM User WHERE user_id = 1")
    result = test_db.fetchone()
    assert result["last_name"] == "Redington"
