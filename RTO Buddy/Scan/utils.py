import os

def does_directory_exists(path):
    """"Checks and returns bool if directory exists."""
    return os.path.exists(path)

def create_directory(path):
    """"Creates a new directory."""
    if not does_directory_exists(path):
        os.makedirs(path)

def delete_file(path):
    """Deletes a file"""
    if does_directory_exists(path):
        os.remove(path)

def get_file_size_in_kb(path):
    """Return file size"""
    return round(os.path.getsize(path) / 1000)