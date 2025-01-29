import os
from faker import Faker

def generate_exact_size_text(size_mb):
    """Generate text data of exact size in megabytes"""
    size_bytes = size_mb * 1024 * 1024
    fake = Faker()
    text = ''
    while len(text.encode('utf-8')) < size_bytes:
        text += fake.text()
    return text.encode('utf-8')[:size_bytes].decode('utf-8')

def get_size_combinations(size_mb):
    """Break down sizes > 10MB into combinations of smaller sizes"""
    base_sizes = [10, 5, 2, 1]
    combination = []
    remaining = size_mb
    for base in base_sizes:
        while remaining >= base:
            combination.append(base)
            remaining -= base
    return combination

def combine_files(target_size, combination):
    """Combine files to create larger sizes"""
    output_file = f"{target_size}mb_text_data_faker.txt"
    with open(output_file, 'wb') as outfile:
        for size in combination:
            infile = f"{size}mb_text_data_faker.txt"
            with open(infile, 'rb') as f:
                outfile.write(f.read())
    return output_file

def verify_file_size(size_mb):
    """Verify if file exists and has exact size"""
    filename = f"{size_mb}mb_text_data_faker.txt"
    if not os.path.exists(filename):
        return None
    actual_size = os.path.getsize(filename)
    expected_size = size_mb * 1024 * 1024
    return actual_size == expected_size

def fix_file_size(size_mb):
    """Fix file to exact size by truncating"""
    filename = f"{size_mb}mb_text_data_faker.txt"
    expected_size = size_mb * 1024 * 1024
    try:
        with open(filename, 'rb+') as f:
            f.truncate(expected_size)
        return verify_file_size(size_mb)
    except Exception as e:
        print(f"Error fixing {filename}: {e}")
        return False

def get_needed_base_files(target_sizes):
    """Determine which base files are actually needed"""
    needed = set()
    for size in target_sizes:
        if size <= 10:
            needed.add(size)
        else:
            # For larger sizes, we need 10MB files
            needed.add(10)
    return sorted(list(needed))

def handle_base_file(size_mb):
    """Handle base file: check, fix or generate"""
    filename = f"{size_mb}mb_text_data_faker.txt"
    
    # Check if file exists
    if os.path.exists(filename):
        if verify_file_size(size_mb):
            print(f"{size_mb}MB file exists and has correct size")
            return True
        else:
            print(f"Fixing size of existing {size_mb}MB file...")
            return fix_file_size(size_mb)
    else:
        print(f"Generating new {size_mb}MB file...")
        text_data = generate_exact_size_text(size_mb)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text_data)
        return verify_file_size(size_mb)

def main():
    # Target sizes
    target_sizes = [10, 20, 30, 40, 50]
    needed_base_files = [2, 5, 10]  # Only files we'll actually use
    
    # Handle base files first
    for size in needed_base_files:
        handle_base_file(size)
    
    # Now handle larger files
    files_to_process = []
    for size in target_sizes:
        if not verify_file_size(size):
            print(f"{size}MB file needs processing")
            files_to_process.append(size)

    if not files_to_process:
        print("All files exist and have correct sizes")
        return

    # Generate larger files by combining
    for target_size in files_to_process:
        if target_size > 10:
            print(f"Creating {target_size}MB file...")
            combination = get_size_combinations(target_size)
            print(f"Using combination: {combination}MB")
            combine_files(target_size, combination)
            if not verify_file_size(target_size):
                fix_file_size(target_size)

if __name__ == "__main__":
    main()
