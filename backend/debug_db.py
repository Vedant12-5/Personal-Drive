#!/usr/bin/env python3
"""
Debug script to fix database paths and check database integrity.
"""

import os
import sqlite3
import sys
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def connect_db():
    db_path = ROOT_DIR / "personal_drive.db"
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        sys.exit(1)
    
    return sqlite3.connect(db_path)

def show_folders():
    print_header("FOLDERS")
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, path, storage_path, parent_id FROM folders")
    folders = cursor.fetchall()
    
    print(f"{'ID':<5} {'Name':<20} {'Path':<30} {'Storage Path':<50} {'Parent ID'}")
    print("-" * 110)
    
    for folder in folders:
        folder_id, name, path, storage_path, parent_id = folder
        print(f"{folder_id:<5} {name:<20} {path:<30} {storage_path:<50} {parent_id}")
    
    conn.close()

def show_files():
    print_header("FILES")
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, path, storage_path, folder_id FROM files LIMIT 10")
    files = cursor.fetchall()
    
    print(f"{'ID':<5} {'Name':<30} {'Path':<40} {'Storage Path':<50} {'Folder ID'}")
    print("-" * 130)
    
    for file in files:
        file_id, name, path, storage_path, folder_id = file
        print(f"{file_id:<5} {name:<30} {path:<40} {storage_path:<50} {folder_id}")
    
    if len(files) == 10:
        print("\n(Showing first 10 files only)")
    
    conn.close()

def update_storage_paths():
    print_header("UPDATE STORAGE PATHS")
    
    # Get current storage directory
    current_storage_dir = os.path.join(ROOT_DIR, "storage")
    print(f"Current storage directory: {current_storage_dir}")
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Get root folder
    cursor.execute("SELECT id, storage_path FROM folders WHERE parent_id IS NULL")
    root_folder = cursor.fetchone()
    
    if not root_folder:
        print("Error: Root folder not found in database.")
        conn.close()
        return
    
    root_id, old_storage_path = root_folder
    print(f"Root folder (ID: {root_id}) current storage path: {old_storage_path}")
    
    # Ask for confirmation
    confirm = input(f"\nUpdate all paths from '{old_storage_path}' to '{current_storage_dir}'? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        conn.close()
        return
    
    # Update root folder
    cursor.execute(
        "UPDATE folders SET storage_path = ? WHERE id = ?",
        (current_storage_dir, root_id)
    )
    
    # Update file paths
    cursor.execute("SELECT id, storage_path FROM files")
    files = cursor.fetchall()
    
    updated_count = 0
    for file_id, old_file_path in files:
        if old_storage_path in old_file_path:
            # Replace old path with new path
            new_file_path = old_file_path.replace(old_storage_path, current_storage_dir)
            
            cursor.execute(
                "UPDATE files SET storage_path = ? WHERE id = ?",
                (new_file_path, file_id)
            )
            updated_count += 1
    
    # Commit changes
    conn.commit()
    print(f"Updated root folder and {updated_count} file records in the database.")
    
    conn.close()

def check_file_existence():
    print_header("CHECK FILE EXISTENCE")
    
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, storage_path FROM files")
    files = cursor.fetchall()
    
    missing_files = []
    for file_id, name, storage_path in files:
        if not os.path.exists(storage_path):
            missing_files.append((file_id, name, storage_path))
    
    if missing_files:
        print(f"Found {len(missing_files)} missing files:")
        for file_id, name, path in missing_files:
            print(f"ID: {file_id}, Name: {name}, Path: {path}")
    else:
        print("All files in the database exist on disk.")
    
    conn.close()

def main():
    print_header("DATABASE DEBUG UTILITY")
    
    while True:
        print("\nOptions:")
        print("1. Show folders")
        print("2. Show files")
        print("3. Update storage paths to current directory")
        print("4. Check file existence")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            show_folders()
        elif choice == '2':
            show_files()
        elif choice == '3':
            update_storage_paths()
        elif choice == '4':
            check_file_existence()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
