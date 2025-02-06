import os
import sys
import django
from tests.setup_test_env import setup_test_environment

def run_tests():
    # Setup test environment first
    setup_test_environment()
    
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptography_web_app.settings')
    django.setup()
    
    # Run tests
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test'])

if __name__ == '__main__':
    run_tests()
