#!/usr/bin/env python3
"""
Script to update the Personal File Storage System to use an external hard drive.
This script will:
1. Update the database to point to the new storage location
2. Create necessary directories on the external drive
3. Move existing files to the new location
"""

import os
import sys
import sqlite3
import shutil
from pathlib import Path

# Configuration
CURRENT_DIR = Path(__file__).parent
DB_PATH = CURRENT_DIR / "personal_drive.db"

def get_external_drive_path():
    """Get the path to the external drive from user input"""
    print("\n=== External Drive Configuration ===")
    print("Please enter the path to your external drive.")
    print("Examples:")
    print("  - macOS: /Volumes/ExternalDrive")
    print("  - Windows: D:\\")
    print("  - Linux: /mnt/external")
    
    while True:
        drive_path = input("\nExternal drive path: ").strip()
        
        # Check if the path exists
        if not os.path.exists(drive_path):
            print(f"Error: Path '{drive_path}' does not exist. Please check and try again.")
            continue
            
        # Check if the path is writable
        try:
            test_file = os.path.join(drive_path, ".test_write_permission")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            return drive_path
        except Exception as e:
            print(f"Error: Cannot write to '{drive_path}'. Please check permissions.")
            print(f"Details: {str(e)}")

def setup_storage_directory(external_path):
    """Set up the storage directory on the external drive"""
    storage_path = os.path.join(external_path, "personal_drive_storage")
    
    print(f"\nCreating storage directory at: {storage_path}")
    os.makedirs(storage_path, exist_ok=True)
    
    return storage_path

def update_database(new_storage_path):
    """Update the database to use the new storage path"""
    print("\n=== Updating Database ===")
    
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get current root folder path
        cursor.execute("SELECT id, storage_path FROM folders WHERE parent_id IS NULL")
        root_folder = cursor.fetchone()
        
        if not root_folder:
            print("Error: Root folder not found in database.")
            conn.close()
            return False
            
        root_id, old_storage_path = root_folder
        
        # Update root folder storage path
        print(f"Updating root folder storage path from '{old_storage_path}' to '{new_storage_path}'")
        cursor.execute(
            "UPDATE folders SET storage_path = ? WHERE id = ?", 
            (new_storage_path, root_id)
        )
        
        # Update file storage paths
        print("Updating file storage paths...")
        cursor.execute("SELECT id, storage_path FROM files")
        files = cursor.fetchall()
        
        for file_id, old_file_path in files:
            # Extract the filename from the old path
            filename = os.path.basename(old_file_path)
            new_file_path = os.path.join(new_storage_path, filename)
            
            cursor.execute(
                "UPDATE files SET storage_path = ? WHERE id = ?",
                (new_file_path, file_id)
            )
            
        # Commit changes
        conn.commit()
        print(f"Updated {len(files)} file records in the database.")
        
        conn.close()
        return True, old_storage_path
        
    except Exception as e:
        print(f"Error updating database: {str(e)}")
        return False, None

def move_files(old_storage_path, new_storage_path):
    """Move existing files to the new storage location"""
    print("\n=== Moving Files ===")
    
    # Check if old storage path exists
    if not os.path.exists(old_storage_path):
        print(f"Warning: Old storage path '{old_storage_path}' does not exist.")
        print("Skipping file migration. You may need to manually restore files.")
        return
    
    try:
        # Get list of files in old storage
        files = [f for f in os.listdir(old_storage_path) 
                if os.path.isfile(os.path.join(old_storage_path, f))]
        
        print(f"Found {len(files)} files to move.")
        
        # Move each file
        for filename in files:
            src = os.path.join(old_storage_path, filename)
            dst = os.path.join(new_storage_path, filename)
            
            print(f"Moving: {filename}")
            shutil.copy2(src, dst)
            
        print(f"\nSuccessfully moved {len(files)} files to the new storage location.")
        print("Note: Original files were not deleted. You can manually remove them if needed.")
        
    except Exception as e:
        print(f"Error moving files: {str(e)}")

def update_config_file():
    """Update the config.py file to use the external drive path"""
    config_path = CURRENT_DIR / "backend" / "app" / "core" / "config.py"
    
    if not os.path.exists(config_path):
        print(f"Warning: Config file not found at {config_path}")
        return False
    
    try:
        with open(config_path, "r") as f:
            content = f.read()
        
        # Check if we need to modify the file
        if "STORAGE_DIR: str = os.path.join(ROOT_DIR, \"storage\")" in content:
            print("\n=== Updating Config File ===")
            print("The config file needs to be updated manually.")
            print("\nPlease edit the file: backend/app/core/config.py")
            print("Find the line with: STORAGE_DIR: str = os.path.join(ROOT_DIR, \"storage\")")
            print("And replace it with the path to your external drive storage.")
            
            return True
    except Exception as e:
        print(f"Error reading config file: {str(e)}")
    
    return False

def main():
    print("=" * 60)
    print("Personal File Storage System - External Drive Setup")
    print("=" * 60)
    
    # Check if database exists
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Get external drive path
    external_path = get_external_drive_path()
    
    # Set up storage directory
    storage_path = setup_storage_directory(external_path)
    
    # Update database
    success, old_storage_path = update_database(storage_path)
    if not success:
        print("Failed to update database. Aborting.")
        sys.exit(1)
    
    # Move files
    if old_storage_path:
        move_files(old_storage_path, storage_path)
    
    # Update config file
    update_config_file()
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print(f"\nYour Personal File Storage System is now configured to use:")
    print(f"  {storage_path}")
    print("\nNext steps:")
    print("1. Update the config.py file as mentioned above")
    print("2. Restart the backend server")
    print("3. Test file uploads and downloads")
    print("\nFor remote access setup, please refer to the NETWORK_OPTIONS.md file.")

if __name__ == "__main__":
    main()
