# Maintenancier App

## About
This app can be used to manage machines and related maintenance task for a shop or shops
It utilizes Django for the backend and Alpine.js and Bootstrap for the UX.

## Development Environment
Developed using Python 3.15 is pipenv and/or venv
See requirements.txt for package requirements

## How to use it

1. Create a user account
2. Log in using the credentials you created
3. Create a shop
4. Add machines to the shop
5. Add maintenance tasks to your machines
6. Upcoming pending maintenance log entries will be created automatically
7. Upcoming tasks will be displayed in the shop dashboard
8. Tasks can be marked complete or dismissed

### Local test data
If you want to kickstart the app with a bunch of prepopulated data, you can run 
`python manage.py generate_test_data`
