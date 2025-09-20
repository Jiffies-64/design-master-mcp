from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User model for storing user information"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    auth_token = db.Column(db.String(120), unique=True, nullable=True)  # Authentication token for MCP tools
    resources = db.relationship('Resource', backref='user', lazy=True)
    templates = db.relationship('Template', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Template(db.Model):
    """Template model for storing document templates"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    placeholders = db.relationship('Placeholder', backref='template', lazy=True)
    prompts = db.relationship('Prompt', backref='template', lazy=True)

    def __repr__(self):
        return f'<Template {self.name}>'

class Placeholder(db.Model):
    """Placeholder model for template placeholders"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    example = db.Column(db.Text)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    content = db.Column(db.Text)  # Content submitted by user

    def __repr__(self):
        return f'<Placeholder {self.name}>'

class Prompt(db.Model):
    """Prompt model for document creation steps"""
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Prompt {self.order}>'

class Resource(db.Model):
    """Resource model for storing user resources"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Resource {self.name}>'