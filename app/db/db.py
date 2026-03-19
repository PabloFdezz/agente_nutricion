import sqlite3

def init_db():
    conn = sqlite3.connect("planes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            plan JSON,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def guardar_plan(usuario, plan_json):
    conn = sqlite3.connect("planes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO planes (usuario, plan) VALUES (?, ?)",
                   (usuario, plan_json))
    conn.commit()
    conn.close()