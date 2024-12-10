import psycopg2

DATABASE_URL = "postgresql://user:password@database:5432/chat_db"

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id SERIAL PRIMARY KEY,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_chat(prompt, response):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (prompt, response) VALUES (%s, %s)", (prompt, response))
    conn.commit()
    conn.close()

def get_response(prompt):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM chats WHERE prompt = %s", (prompt,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
