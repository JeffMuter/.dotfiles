"""
Initialize the PyDial database.
"""
from database import init_db

def main():
    print("Initializing PyDial database...")
    init_db()
    print("Database initialized successfully!")

if __name__ == '__main__':
    main() 