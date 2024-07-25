# VentifyAPI
## Overview
Ventify is a mental health support platform api designed to foster a sense of community and well-being. It provides users with a space to express themselves, connect with others, and access resources for mental health support.

## Installation
1. Clone the repository:
```
git clone https://github.com/eTRVPMAX/ventify.git
```

2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
```
source venv/bin/activate  # For Unix-like systems
venv\Scripts\activate  # For Windows
```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Set up environment variables: Create a .env file and add necessary environment variables (e.g., database URL, secret key).
Run migrations:
```
python manage.py migrate
```

6. Start the development server:
```
python manage.py runserver
```

## Usage
Access the api through a web browser at http://127.0.0.1:8000

## Features
- Create and share vents
- Like vents
- Discover therapists
- Feedback system

## Technologies Used
- Python
- Django

## Contributors
- [Mohamed Ehab](https://github.com/eTRVPMAX)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
