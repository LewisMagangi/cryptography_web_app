#!/bin/bash

echo "Installing whitenoise..."
pip install whitenoise

echo "Setting up directories with correct permissions..."
# Remove existing staticfiles directory
sudo rm -rf staticfiles

# Create directories with proper permissions
sudo mkdir -p staticfiles
sudo mkdir -p static/blog/css static/blog/js static/admin

# Set initial permissions
sudo chown -R www-data:www-data staticfiles
sudo chown -R www-data:www-data static
sudo chmod -R 775 staticfiles
sudo chmod -R 775 static

# Add your user to www-data group (if not already done)
sudo usermod -a -G www-data $USER

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Final permission adjustments..."
sudo chown -R www-data:www-data staticfiles/
sudo chown -R www-data:www-data static/
sudo chmod -R 775 staticfiles/
sudo chmod -R 775 static/

echo "Restarting Apache..."
sudo systemctl restart apache2

echo "Done! Checking Apache error log..."
sudo tail -n 20 /var/log/apache2/error.log
