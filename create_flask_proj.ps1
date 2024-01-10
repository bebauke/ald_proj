# Create a new directory for the project
$projectName = "your_project"
New-Item -ItemType Directory -Path $projectName
Set-Location $projectName

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate the virtual environment (Windows)
.\venv\Scripts\Activate

# Install Flask
pip install Flask

# Create project structure
New-Item -ItemType Directory -Path "app"
New-Item -ItemType Directory -Path "app\static"
New-Item -ItemType Directory -Path "app\templates"
New-Item -ItemType File -Path "app\__init__.py"
New-Item -ItemType File -Path "app\routes.py"
New-Item -ItemType File -Path "config.py"
New-Item -ItemType File -Path "run.py"

# Initialize Flask app in __init__.py
@"
from flask import Flask

app = Flask(__name__)

from app import routes
"@ | Out-File -FilePath "app\__init__.py"

# Define a sample route in routes.py
@"
from app import app

@app.route('/')
def index():
    return 'Hello, Flask!'
"@ | Out-File -FilePath "app\routes.py"

# Create a simple configuration in config.py
@"
class Config:
    DEBUG = True  # Enable debugging
"@ | Out-File -FilePath "config.py"

# Create run.py script
@"
from app import app

if __name__ == '__main__':
    app.run(debug=True)
"@ | Out-File -FilePath "run.py"

# Inform the user
Write-Host "Flask project structure created successfully."
Write-Host "To run your Flask app, activate the virtual environment and execute 'python run.py'."
