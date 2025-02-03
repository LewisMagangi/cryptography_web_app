#!/bin/bash

# Install whitenoise for better static file handling
pip install whitenoise

# Clear and recreate static directories
sudo rm -rf staticfiles/*
mkdir -p static/blog/css static/blog/js static/admin

# Collect static files
python manage.py collectstatic --no-input --clear

# Fix permissions
sudo find . -type d -exec chmod 755 {} \;
sudo find . -type f -exec chmod 644 {} \;
sudo chown -R www-data:www-data staticfiles/
sudo chown -R www-data:www-data static/

# Restart Apache
sudo systemctl restart apache2

# Check for errors
echo "Checking Apache error log..."
sudo tail -n 20 /var/log/apache2/error.log
