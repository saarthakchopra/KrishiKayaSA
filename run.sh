#!/bin/bash

# Navigate to the Django project directory and run migrations
cd Backend/inventoryMarketPlace
python manage.py makemigrations
python manage.py migrate

# Start Django server
python manage.py runserver &

# Navigate to the Frontend directory and start Node server
cd ../../Frontend
npm start &

# Wait for both processes to finish
wait
