#!/usr/bin/env python3

"""
Initialize the PyDial database.
"""
from database.db import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!") 