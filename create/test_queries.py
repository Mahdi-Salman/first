import mysql.connector
import re

# تنظیمات اتصال
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',  # رمزت رو بذار
)
cursor = conn.cursor(dictionary=True)

# ایجاد دیتابیس تستی
test_db_name = 'test_db_query'
cursor.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
cursor.execute(f"CREATE DATABASE {test_db_name}")
cursor.execute(f"USE {test_db_name}")
print(f"✅ Created test database `{test_db_name}`")

# خواندن کوئری‌ها از فایل
with open("query.sql", "r", encoding="utf-8") as f:
    content = f.read()

queries = [q.strip() for q in content.split("---------------------------------------------------------------") if q.strip()]
print(f"🔍 Found {len(queries)} queries.")

# اجرای هر کوئری و تست پایه‌ای
for idx, query in enumerate(queries, 1):
    print(f"\n🚀 Running Query #{idx}:")
    try:
        cursor.execute(query)
        conn.commit()

        if re.match(r"(?i)\s*SELECT", query):  # اگر SELECT بود
            result = cursor.fetchall()
            print(f"🔹 Rows returned: {len(result)}")
            assert len(result) > 0, f"❌ Query #{idx} returned no results"

        elif re.match(r"(?i)\s*(INSERT|UPDATE|DELETE)", query):
            affected = cursor.rowcount
            print(f"🔹 Rows affected: {affected}")
            assert affected > 0, f"❌ Query #{idx} affected no rows"

        else:
            print("ℹ️ Query executed (DDL or unknown type).")

        print(f"✅ Query #{idx} passed.")

    except Exception as e:
        print(f"❌ Error in Query #{idx}: {e}")

# حذف دیتابیس تستی
cursor.execute(f"DROP DATABASE {test_db_name}")
print(f"\n🧹 Test database `{test_db_name}` dropped.")
