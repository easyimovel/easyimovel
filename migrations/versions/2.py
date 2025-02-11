import sys
import os

projeto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(projeto_dir)

from app.utils.db import DB

db = DB()

async def up():
	await db.query("""
		CREATE TABLE IF NOT EXISTS urls (
			id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
			url VARCHAR(250) NOT NULL UNIQUE,
			platform VARCHAR(50) NOT NULL,
			disable BOOLEAN DEFAULT FALSE,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
			INDEX idx_url (url)
		);
	""")

async def down():
	await db.query("DROP TABLE urls;")