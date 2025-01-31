from faker import Faker
import os

def generate_text_data(size_in_bytes):
    """Generate text data of exact size using Faker."""
    text_generator = Faker()
    text = ""
    while len(text.encode('utf-8')) < size_in_bytes:
        remaining_bytes = size_in_bytes - len(text.encode('utf-8'))
        chunk_size = min(remaining_bytes, 1024)
        text += text_generator.text()
    return text[:size_in_bytes]

def verify_file_size(filename, target_size):
    """Verify if file is exactly target size."""
    if os.path.exists(filename):
        return os.path.getsize(filename) == target_size
    return False

def fix_file_size(filename, target_size):
    """Fix file to match target size."""
    with open(filename, 'rb+') as file:
        content = file.read()
        if len(content) > target_size:
            # Truncate
            file.seek(0)
            file.write(content[:target_size])
            file.truncate()
        else:
            # Pad
            file.seek(len(content))
            file.write(b' ' * (target_size - len(content)))

# Sizes in bytes to generate data for
sizes_in_bytes = [i for i in range(0, 250, 25)]

# Generate or verify files
for size in sizes_in_bytes:
    file_name = f"{size}bytes_text_data_faker.txt"
    
    if not verify_file_size(file_name, size):
        if os.path.exists(file_name):
            print(f"Fixing size of {file_name}")
            fix_file_size(file_name, size)
        else:
            print(f"Generating new file {file_name}")
            text_data = generate_text_data(size)
            with open(file_name, 'w') as file:
                file.write(text_data)
    else:
        print(f"File {file_name} exists with correct size")
