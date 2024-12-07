# Django Project Setup Guide

## Prerequisites
- Python 3.8+ installed
- pip installed
- Git (optional, but recommended)

## Project Setup Step-by-Step

### 1. Create Project Directory
```bash
# Create project directory
mkdir mydjangoproject
cd mydjangoproject
```

### 2. Create and Activate Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Django and Project Dependencies
```bash
# Upgrade pip (recommended)
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# If you haven't created requirements.txt yet, install Django and other core packages
pip install django

# Freeze dependencies (optional, but recommended)
pip freeze > requirements.txt
```

### 4. Django Project Initialization
```bash
# Create new Django project
django-admin startproject myproject .

# Create Django app
python3 manage.py startapp myapp
```

### 5. Database Setup
```bash
# Create database migrations
python3 manage.py makemigrations

# Apply database migrations
python3 manage.py migrate
```

### 6. Create Superuser
```bash
# Create admin superuser
python3 manage.py createsuperuser
```

### 7. Run Development Server
```bash
# Run server on default port (8000)
python3 manage.py runserver

# Run on a specific port
python3 manage.py runserver 8080
```

## Virtual Environment Management

### Deactivate Virtual Environment
```bash
# When you're done working on the project
deactivate
```

### Reinstall Dependencies on Another Machine
```bash
# Ensure you're in the project directory with requirements.txt
pip install -r requirements.txt
```

## Best Practices

1. **Never commit your `venv` directory to version control**
   - Add `venv/` to your `.gitignore` file

2. **Use a `.env` file for sensitive information**
   - Install `python-dotenv` for environment variable management
   - Never commit `.env` to version control

3. **Keep requirements.txt updated**
   ```bash
   pip freeze > requirements.txt
   ```

## Troubleshooting

- Ensure you're always in the virtual environment when working on the project
- If you encounter permission issues, use `sudo` cautiously or adjust your Python installation
- Check Python and pip versions: `python3 --version` and `pip --version`

## Common Commands Cheat Sheet

```bash
# Activate venv
source venv/bin/activate

# Install packages
pip install packagename

# Create migrations
python3 manage.py makemigrations

# Apply migrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser

# Run development server
python3 manage.py runserver
```
