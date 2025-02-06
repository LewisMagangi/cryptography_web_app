import os

def setup_test_environment():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create required directories
    dirs = [
        os.path.join(base_dir, 'data', 'sample_text'),
        os.path.join(base_dir, 'data', 'results'),
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # Create a sample text file
    sample_file = os.path.join(base_dir, 'data', 'sample_text', 'test.txt')
    with open(sample_file, 'w') as f:
        f.write("This is a sample text for testing cryptographic functions.")

if __name__ == '__main__':
    setup_test_environment()
