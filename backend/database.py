import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://user:password@database:5432/chat_db"

def create_database_and_table():
    """Buat database dan tabel jika belum ada."""
    try:
        # Koneksi ke PostgreSQL tanpa database tertentu
        with psycopg2.connect(DATABASE_URL.replace("chat_db", "postgres")) as conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with conn.cursor() as cursor:
                # Buat database jika belum ada
                cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'chat_db'")
                exists = cursor.fetchone()
                if not exists:
                    cursor.execute("CREATE DATABASE chat_db")
                    logger.info("Database 'chat_db' created successfully.")
        
        # Setelah database dibuat, inisialisasi tabel di database
        init_db()
    except Exception as e:
        logger.error(f"Error creating database and table: {e}")

def init_db():
    """Inisialisasi tabel di database."""
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS chats (
                        id SERIAL PRIMARY KEY,
                        prompt TEXT NOT NULL,
                        response TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                logger.info("Table 'chats' initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing table: {e}")

def save_chat(prompt, response):
    """Simpan prompt dan respons ke database."""
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO chats (prompt, response) VALUES (%s, %s)",
                    (prompt, response)
                )
                conn.commit()
                logger.info(f"Chat saved: {prompt}")
    except Exception as e:
        logger.error(f"Error saving chat: {e}")

def save_chat_to_db(prompt, response):
    """Alias dari save_chat untuk menjaga konsistensi impor."""
    save_chat(prompt, response)

def get_response(prompt):
    """Ambil respons dari database berdasarkan prompt."""
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT response FROM chats WHERE prompt = %s", (prompt,))
                result = cursor.fetchone()
                return result[0] if result else None
    except Exception as e:
        logger.error(f"Error retrieving response: {e}")
        return None

def query_response_by_keyword(keyword):
    """Cari respons berdasarkan kata kunci di prompt."""
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT response FROM chats WHERE prompt ILIKE %s ORDER BY created_at DESC LIMIT 1",
                    (f"%{keyword}%",)
                )
                result = cursor.fetchone()
                return result["response"] if result else None
    except Exception as e:
        logger.error(f"Error querying response by keyword: {e}")
        return None

def get_all_chats():
    """Ambil semua chat dari database (untuk debugging atau audit)."""
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM chats ORDER BY created_at DESC")
                results = cursor.fetchall()
                return results
    except Exception as e:
        logger.error(f"Error retrieving all chats: {e}")
        return []
