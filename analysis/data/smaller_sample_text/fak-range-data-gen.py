from faker import Faker

def generate_text_data(size_in_bytes):
    text = ''
    text_generator = Faker()
    while len(text.encode('utf-8')) < size_in_bytes:
        remaining_bytes = size_in_bytes - len(text.encode('utf-8'))
        chunk_size = min(remaining_bytes, 1024)  # Chunk size of 1024 bytes or remaining bytes, whichever is smaller
        text += text_generator.text()  # Faker text generator
    return text[:size_in_bytes]  # Ensure we do not exceed the required size

# Sizes in bytes to generate data for
sizes_in_bytes = [i for i in range(0, 501, 50)]  # 0, 50, 100, ..., 500 bytes

# Generate text data for each size and save it into a separate file
for size in sizes_in_bytes:
    text_data = generate_text_data(size)
    file_name = f"{size}bytes_text_data_faker.txt"
    with open(file_name, 'w') as file:
        file.write(text_data)
    print(f"Generated {size} bytes of text data using faker and saved it into {file_name}")
