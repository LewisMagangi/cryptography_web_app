import os
from faker import Faker

def generate_exact_1mb():
    """Generate exactly 1MB text block"""
    MB = 1024 * 1024
    fake = Faker()
    text = ""
    while len(text.encode('utf-8')) < MB:
        text += fake.text()
    return text.encode('utf-8')[:MB].decode('utf-8')

def verify_size(filename, target_mb):
    """Verify file is exactly target size"""
    expected = target_mb * 1024 * 1024
    actual = os.path.getsize(filename)
    return actual == expected

def adjust_file_size(filename, target_mb):
    """Truncate or pad file to exact size"""
    target_bytes = target_mb * 1024 * 1024
    with open(filename, 'rb+') as f:
        content = f.read()
        if len(content) > target_bytes:
            # Truncate
            f.seek(0)
            f.write(content[:target_bytes])
            f.truncate()
        elif len(content) < target_bytes:
            # Pad with spaces
            f.seek(len(content))
            f.write(b' ' * (target_bytes - len(content)))

def create_mb_file(mb_size):
    """Create file of exact MB size"""
    filename = f"{mb_size}mb_text_data_faker.txt"
    base_block = generate_exact_1mb()
    
    with open(filename, 'w', encoding='utf-8') as f:
        for _ in range(mb_size):
            f.write(base_block)
    
    # Verify and adjust if needed
    if not verify_size(filename, mb_size):
        adjust_file_size(filename, mb_size)
    return verify_size(filename, mb_size)

def handle_file(mb_size):
    """Handle file existence, verification and creation"""
    filename = f"{mb_size}mb_text_data_faker.txt"
    
    # Check if file exists
    if os.path.exists(filename):
        print(f"Checking {filename}...")
        if verify_size(filename, mb_size):
            print(f"{filename} is correct size")
            return True
        else:
            print(f"Fixing {filename} size...")
            adjust_file_size(filename, mb_size)
            return verify_size(filename, mb_size)
    else:
        print(f"Generating {filename}...")
        return create_mb_file(mb_size)

def main():
    # Process all sizes
    sizes = [1, 2, 5, 10, 20, 30, 40, 50]
    
    for size in sizes:
        if handle_file(size):
            print(f"{size}MB file processed successfully")
        else:
            print(f"Error processing {size}MB file")

if __name__ == "__main__":
    main()