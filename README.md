# Waiya CUP 2025

## Overview
An unofficial web application tracking the **Waiya CUP 2025** football tournament in **Jayapura Regency**. This platform provides match schedules, standings, and player statistics for the community tournament.

## Features
- **Match Schedule & Results**: View upcoming and completed matches with scores  
- **Group Standings**: Track team rankings across different groups  
- **Player Statistics**: Top scorers, most assists, and combined goal contributions  
- **Community Contributions**: Allow fans to submit match results and statistics  

## Technology Stack
- **Django 4.2** (Python web framework)  
- **HTML/CSS** with **Tailwind CSS** for responsive design

## Installation
```sh
# Clone the repository
git clone https://github.com/papuaopensource/waiya-cup.git
cd waiyacup

# Create and activate virtual environment
uv venv
source .venv/bin/activate  
.venv\Scripts\activate # On Windows: 

# Install dependencies using uv
uv pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## Contributing
This is a community-driven project. To contribute:
- Submit match results through the contribution form  
- Report issues or suggest improvements via GitHub issues  
- Submit pull requests for code improvements  

## Project Structure
- `core` – Main application with views, models, and templates  
- `templates` – HTML templates with Tailwind CSS styling  
- `static` – Static files (CSS, JavaScript, images)  

## License
MIT License

## Acknowledgements
This project is a fan initiative to support local football in Jayapura, created by football enthusiasts for the community.
