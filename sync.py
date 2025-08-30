from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3
import pymysql

# SQLite setup
SQLITE_DB_PATH = "local_data.db"

# MySQL setup
MYSQL_URL = "mysql+pymysql://root:Sri0512@@localhost:3306/water_db"
mysql_engine = create_engine(MYSQL_URL)
MySQLSession = sessionmaker(bind=mysql_engine, autoflush=False, autocommit=False)

def sync_to_mysql():
    # Connect to SQLite
    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    sqlite_cursor = sqlite_conn.cursor()

    # Connect to MySQL
    mysql_db = MySQLSession()

    try:
        # Read from SQLite
        sqlite_cursor.execute("SELECT id, latitude, longitude, hpi, hei FROM water_results")
        rows = sqlite_cursor.fetchall()

        # Insert into MySQL
        for row in rows:
            mysql_db.execute(
                "INSERT INTO water_results (id, latitude, longitude, hpi, hei) VALUES (%s, %s, %s, %s, %s) "
                "ON DUPLICATE KEY UPDATE latitude=VALUES(latitude), longitude=VALUES(longitude), hpi=VALUES(hpi), hei=VALUES(hei)",
                row
            )

        mysql_db.commit()

        print("✅ Data synced successfully from SQLite → MySQL!")

        # Fetch back from MySQL to check
        result = mysql_db.execute("SELECT * FROM water_results").fetchall()
        print("\n📊 Current data in MySQL water_results:")
        for r in result:
            print(r)

    except Exception as e:
        print("❌ Error during sync:", e)
        mysql_db.rollback()
    finally:
        sqlite_conn.close()
        mysql_db.close()

if __name__ == "__main__":
    sync_to_mysql()
