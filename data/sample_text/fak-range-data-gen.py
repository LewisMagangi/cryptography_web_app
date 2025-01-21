import os
from faker import Faker

def generate_text_data(size_in_mb):
    text = ''
    size_in_bytes = size_in_mb * 1024 * 1024  # Convert MB to bytes
    text_generator = Faker()
    while len(text.encode('utf-8')) < size_in_bytes:
        remaining_bytes = size_in_bytes - len(text.encode('utf-8'))
        chunk_size = min(remaining_bytes, 1024)  # Chunk size of 1024 bytes or remaining bytes, whichever is smaller
        text += text_generator.text()
    return text

# Sizes to generate text data for
sizes = [1, 2, 3, 4, 5]

# Generate text data for each size and save it into a separate file
for size in sizes:
    text_data = generate_text_data(size)
    file_name = f"{size}mb_text_data_faker.txt"
    with open(file_name, 'w') as file:
        file.write(text_data)
    print(f"Generated {size}MB of text data using faker and saved it into {file_name}")