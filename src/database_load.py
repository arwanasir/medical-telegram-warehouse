import os
import json
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

def create_raw_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw_telegram_data (
            id SERIAL PRIMARY KEY,
            message_id BIGINT,
            channel_name TEXT,
            message_date TIMESTAMP,
            message_text TEXT,
            has_media BOOLEAN,
            image_path TEXT,
            views INTEGER,
            forwards INTEGER,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def load_json_to_db():
    conn = connect_db()
    cur = conn.cursor()
    
 
    raw_path = '../data/raw/telegram_messages'
    
    for root, dirs, files in os.walk(raw_path):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    
                    values = [
                        (m.get('message_id'), m.get('channel_name'), m.get('message_date'),
                         m.get('message_text'), m.get('has_media'), m.get('image_path'),
                         m.get('views'), m.get('forwards'))
                        for m in data
                    ]
                    
                    query = """
                        INSERT INTO raw_telegram_data 
                        (message_id, channel_name, message_date, message_text, has_media, image_path, views, forwards)
                        VALUES %s
                    """
                    extras.execute_values(cur, query, values)
    
    conn.commit()
    print(f"Successfully loaded data into raw_telegram_data table.")
    cur.close()
    conn.close()
    

if __name__ == "__main__":
    create_raw_table()
    load_json_to_db()