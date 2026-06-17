import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.database.sqlite import initialize_database, seed_database


if __name__ == "__main__":
    initialize_database()
    seed_database()
    print("Seeded ERA SQLite database.")
