import sys
import os

projeto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(projeto_dir)

from app.utils.db import DB

db = DB()


async def up():
    column_exists = await db.column_exists("urls", "scrap_done")
    if not column_exists:
        await db.query("""
            ALTER TABLE urls ADD COLUMN scrap_done BOOLEAN DEFAULT FALSE AFTER `platform`;
        """)

async def down():
    column_exists = await db.column_exists("urls", "scrap_done")
    if column_exists:
	    await db.query("ALTER TABLE urls DROP COLUMN scrap_done;")