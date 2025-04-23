import pymysql
import pytest
from datetime import datetime, timedelta

@pytest.fixture(scope="module")
def test_db():
    # اتصال به دیتابیس تست
    conn = pymysql.connect(
        host='localhost',
        user='test_user',
        password='test_pass',
        database='test_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    # ایجاد جداول و داده‌های تستی
    with conn.cursor() as cursor:
        # اجرای تمام فایل‌های SQL برای ایجاد ساختار
        sql_files = [
        'city.sql',
        'terminal.sql',
        'user.sql',
        'transport_company.sql',
        'vehicle_detail.sql',
        'bus_detail.sql',
        'train_detail.sql',
        'flight_detail.sql',
        'travel.sql',
        'ticket.sql',
        'reservation.sql',
        'payment.sql',
        'reservation_change.sql',
        'report.sql'
    ]
        
        for file in sql_files:
            with open(file, 'r') as f:
                for statement in f.read().split(';'):
                    if statement.strip():
                        cursor.execute(statement)
        
        # وارد کردن داده‌های تستی
        setup_test_data(cursor)
    
    yield conn
    
    # پاکسازی پس از تست
    with conn.cursor() as cursor:
        tables = [
            'Report', 'ReservationChange', 'Payment', 'Reservation',
            'Ticket', 'Travel', 'BusDetail', 'TrainDetail', 'FlightDetail',
            'VehicleDetail', 'TransportCompany', 'User', 'Terminal', 'City'
        ]
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
    conn.close()

def setup_test_data(cursor):
    # داده‌های پایه
    cursor.execute("INSERT INTO City (province_name, city_name) VALUES ('Tehran', 'Tehran'), ('Ardebil', 'Ardebil')")
    cursor.execute("INSERT INTO Terminal (city_id, terminal_name, terminal_type) VALUES (1, 'Tehran Terminal', 'bus_terminal'), (2, 'Ardebil Airport', 'airport')")
    cursor.execute("INSERT INTO TransportCompany (company_name, transport_type) VALUES ('Mahan Air', 'airplane'), ('Iran Air', 'airplane'), ('Seiro Safar', 'bus')")
    cursor.execute("INSERT INTO VehicleDetail (vehicle_type) VALUES ('train'), ('flight'), ('bus')")
    cursor.execute("INSERT INTO FlightDetail (flight_id, airline_name, flight_class, flight_number, origin_airport, destination_airport) VALUES (2, 'Mahan Air', 'business', 'W5-1001', 'THR', 'ADU')")
    cursor.execute("INSERT INTO BusDetail (bus_id, bus_company, bus_type, seat_arrangement) VALUES (3, 'Seiro Safar', 'VIP', '1+2')")
    
    # کاربران
    cursor.execute("""
        INSERT INTO User (first_name, last_name, email, phone_number, user_type, password_hash, city_id, account_status)
        VALUES 
            ('Ali', 'Prs', 'ali@test.com', '09123456789', 'CUSTOMER', 'hash1', 1, 'ACTIVE'),
            ('Mehdi', 'Salman', 'mehdi@test.com', '09123456780', 'CUSTOMER', 'hash2', 1, 'ACTIVE'),
            ('Support', 'User', 'support@test.com', '09123456781', 'SUPPORT', 'hash3', 2, 'ACTIVE'),
            ('Admin', 'User', 'admin@test.com', '09123456782', 'ADMIN', 'hash4', 2, 'ACTIVE')
    """)
    
    # سفرها
    now = datetime.now()
    cursor.execute(f"""
        INSERT INTO Travel (
            transport_type, departure_time, arrival_time, total_capacity, remaining_capacity,
            price, travel_class, departure_terminal_id, destination_terminal_id, transport_company_id
        ) VALUES 
            ('plane', '{now}', '{now + timedelta(hours=2)}', 100, 50, 500000, 'business', 1, 2, 1),
            ('bus', '{now + timedelta(days=1)}', '{now + timedelta(days=1, hours=5)}', 50, 20, 200000, 'VIP', 1, 2, 3)
    """)
    
    # بلیط‌ها
    cursor.execute("INSERT INTO Ticket (travel_id, vehicle_id, seat_number) VALUES (1, 2, 10), (1, 2, 11), (2, 3, 1)")
    
    # رزرواسیون‌ها
    cursor.execute(f"""
        INSERT INTO Reservation (user_id, ticket_id, status, expiration_time, reservation_time)
        VALUES 
            (1, 1, 'paid', '{now + timedelta(days=1)}', '{now}'),
            (1, 2, 'reserved', '{now + timedelta(days=1)}', '{now}'),
            (2, 3, 'paid', '{now + timedelta(days=2)}', '{now - timedelta(days=1)}')
    """)
    
    # پرداخت‌ها
    cursor.execute(f"""
        INSERT INTO Payment (user_id, reservation_id, amount, payment_method, payment_status, payment_date)
        VALUES 
            (1, 1, 500000, 'credit_card', 'completed', '{now}'),
            (2, 3, 200000, 'wallet', 'completed', '{now - timedelta(days=1)}')
    """)
    
    # تغییرات رزرواسیون
    cursor.execute(f"""
        INSERT INTO ReservationChange (reservation_id, support_id, prev_status, next_status)
        VALUES 
            (2, 3, 'reserved', 'canceled'),
            (1, 3, 'reserved', 'paid')
    """)
    
    # گزارش‌ها
    cursor.execute(f"""
        INSERT INTO Report (user_id, ticket_id, report_category, report_text, status, report_time)
        VALUES 
            (1, 1, 'payment_issue', 'Problem with payment', 'pending', '{now}'),
            (2, 3, 'travel_delay', 'Bus was late', 'reviewed', '{now - timedelta(days=1)}')
    """)

# تست‌های کوئری‌ها
def test_query_1_unpaid_or_no_reservations(test_db):
    with test_db.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT user.first_name, user.last_name
            FROM user
            LEFT JOIN reservation ON user.user_id = reservation.user_id
            WHERE reservation.status != 'paid' OR reservation.user_id IS NULL
        """)
        results = cursor.fetchall()
        assert len(results) >= 1  # کاربر با رزرو پرداخت نشده

def test_query_2_paid_reservations(test_db):
    with test_db.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT user.first_name, user.last_name
            FROM user
            LEFT JOIN reservation ON user.user_id = reservation.user_id
            WHERE reservation.status = 'paid' AND reservation.user_id IS NOT NULL
        """)
        results = cursor.fetchall()
        assert len(results) >= 2  # دو کاربر با رزرو پرداخت شده

def test_query_3_monthly_payments(test_db):
    with test_db.cursor() as cursor:
        cursor.execute("""
            SELECT 
                u.user_id, 
                CONCAT(u.first_name, ' ', u.last_name) AS name, 
                YEAR(p.payment_date) AS year,
                MONTH(p.payment_date) AS month, 
                SUM(p.amount) AS total_paid
            FROM user u
            JOIN payment p ON u.user_id = p.user_id
            GROUP BY u.user_id, name, year, month
            ORDER BY year DESC, month DESC, total_paid DESC
        """)
        results = cursor.fetchall()
        assert len(results) >= 1
        assert 'total_paid' in results[0]

# ... تست‌های مشابه برای سایر کوئری‌ها (4 تا 22)

def test_query_17_support_cancel_percentage(test_db):
    with test_db.cursor() as cursor:
        cursor.execute("""
            SELECT 
                CONCAT(u.first_name, ' ', u.last_name) AS support_name,
                COUNT(CASE WHEN rc.next_status = 'canceled' THEN 1 END) / COUNT(*) * 100 AS canceled_percent
            FROM ReservationChange rc
            JOIN User u ON rc.support_id = u.user_id
            WHERE u.user_type = 'SUPPORT'
            GROUP BY u.user_id
            ORDER BY canceled_percent DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        assert result is not None
        assert 'canceled_percent' in result

def test_query_18_update_redington(test_db):
    with test_db.cursor() as cursor:
        cursor.execute("""
            UPDATE User
            SET last_name = 'Redington'
            WHERE user_id = (
                SELECT * FROM (
                    SELECT u.user_id
                    FROM User u
                    JOIN Reservation r ON u.user_id = r.user_id
                    JOIN ReservationChange rc ON r.reservation_id = rc.reservation_id
                    WHERE rc.next_status = 'canceled'
                    GROUP BY u.user_id
                    ORDER BY COUNT(*) DESC
                    LIMIT 1
                ) AS max_user
            )
        """)
        assert cursor.rowcount == 1

# ... ادامه تست‌های UPDATE و DELETE

def test_query_22_report_categories_for_top_ticket(test_db):
    with test_db.cursor() as cursor:
        cursor.execute("""
            SELECT r.report_category, COUNT(*) AS report_count
            FROM Report r
            WHERE r.ticket_id = (
                SELECT ticket_id
                FROM Report
                GROUP BY ticket_id
                ORDER BY COUNT(*) DESC
                LIMIT 1
            )
            GROUP BY r.report_category
        """)
        results = cursor.fetchall()
        assert len(results) >= 1
