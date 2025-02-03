#!/bin/bash

echo "Cleaning up static files..."
# Remove all existing static files
sudo rm -rf staticfiles/*
sudo rm -rf static/admin/*

echo "Creating fresh static structure..."
# Create clean directory structure
mkdir -p static/blog/{css,js,images}
mkdir -p static/admin

echo "Collecting static files with optimization..."
# Collect static files with clear cache
python manage.py collectstatic --no-input --clear --ignore="*.pyc" --ignore="CVS"

echo "Setting permissions..."
# Set correct permissions
sudo chown -R www-data:www-data staticfiles/
sudo chmod -R 755 staticfiles/

echo "Restarting Apache..."
sudo systemctl restart apache2

echo "Verifying static files..."
ls -R staticfiles/
