from app import app
from models.models import db, User, Template, Placeholder, Prompt
from werkzeug.security import generate_password_hash

def init_sample_data():
    """Initialize the database with sample data"""
    with app.app_context():
        # Check if we already have data
        if User.query.first() is not None:
            print("Sample data already exists")
            return
        
        # Create a sample user with hashed password
        hashed_password = generate_password_hash("password123")
        user = User(username="testuser", email="test@example.com", password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        # Create a sample template
        template_content = """# {{project_name}} Design Document

## Overview
{{overview}}

## Architecture
{{architecture}}

## Components
{{components}}

## Database Schema
```plantuml
{{database_schema}}
```

## API Endpoints
{{api_endpoints}}

## Security Considerations
{{security_considerations}}

## Deployment
{{deployment}}
"""
        
        template = Template(
            name="Default Design Template",
            content=template_content,
            description="A default template for software design documents",
            user_id=user.id,
            is_public=True
        )
        db.session.add(template)
        db.session.commit()
        
        # Create placeholders
        placeholders = [
            ("project_name", "Name of the project", "MyProject"),
            ("overview", "Brief description of the project", "This project is a web application for managing tasks."),
            ("architecture", "System architecture description", "The system follows a microservices architecture."),
            ("components", "List of system components", "1. Frontend: React application\n2. Backend: Flask API\n3. Database: PostgreSQL"),
            ("database_schema", "Database schema in PlantUML format", "@startuml\nentity User {\n  id: int\n  username: string\n}\nentity Task {\n  id: int\n  title: string\n  user_id: int\n}\nUser ||--o{ Task\n@enduml"),
            ("api_endpoints", "List of API endpoints", "GET /api/tasks - Get all tasks\nPOST /api/tasks - Create a new task"),
            ("security_considerations", "Security considerations", "Authentication with JWT tokens\nPassword hashing with bcrypt"),
            ("deployment", "Deployment instructions", "Deploy using Docker containers with docker-compose")
        ]
        
        for name, description, example in placeholders:
            placeholder = Placeholder(
                name=name,
                description=description,
                example=example,
                template_id=template.id
            )
            db.session.add(placeholder)
        
        db.session.commit()
        
        # Create prompts
        prompt_contents = [
            "Provide the project name and a brief overview of what the project does.",
            "Describe the system architecture, including any patterns or principles used.",
            "List the main components of the system and describe their responsibilities.",
            "Design the database schema using PlantUML notation.",
            "Define the API endpoints with their HTTP methods and parameters.",
            "Identify security considerations for the system.",
            "Describe how the system will be deployed and any infrastructure requirements."
        ]
        
        for i, content in enumerate(prompt_contents):
            prompt = Prompt(
                order=i,
                content=content,
                template_id=template.id
            )
            db.session.add(prompt)
        
        db.session.commit()
        
        print("Sample data initialized successfully!")

if __name__ == "__main__":
    init_sample_data()