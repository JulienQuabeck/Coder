Coderr

Description

    Coderr is a freelancer platform that allows developers and clients to connect. Developers can list their services as offers, which clients can book. After completing a project, clients have the opportunity to rate the provider and leave a review.

Installation

    1. Clone the repository

        git clone https://github.com/JulienQuabeck/Coder.git

    2. Navigate to the project directory

        cd Coder

    3. Create and activate a virtual environment (recommended)

        python -m venv venv
        source venv/bin/activate  # macOS/Linux
        venv\Scripts\activate  # Windows

    4. Install dependencies

        pip install -r requirements.txt

    5. Apply database migrations

        python manage.py makemigrations
        python manage.py migrate

    6. Create a superuser (optional, for admin access)

        python manage.py createsuperuser

    7. Start the server

        python manage.py runserver

        Access the platform at http://127.0.0.1:8000/ in your browser.

Features

    Developers can create offers

    Clients can book offers

    Clients can rate providers and leave reviews after project completion

    User registration and authentication

Technologies

    Frontend: HTML, CSS, JavaScript

    Backend: Django REST Framework (DRF), Python

    Database: SQLite

Developer Commands

    Database migrations

        python manage.py makemigrations
        python manage.py migrate

    Create a superuser

        python manage.py createsuperuser

    Collect static files (if needed)

        python manage.py collectstatic

License & Contributors

    This project has no license and is not currently being developed by a team.
