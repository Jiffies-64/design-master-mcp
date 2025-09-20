from flask import Flask, jsonify, request, render_template, redirect, url_for, session, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
import time
import json
from functools import wraps
from models.models import db, User, Template, Placeholder, Prompt, Resource

# Import MCP tools
from mcp_tools.start_document import start_document_generation
from mcp_tools.get_next_step import get_next_step
from mcp_tools.submit_content import submit_placeholder_content
from mcp_tools.generate_document import generate_complete_document

# Initialize Flask app
app = Flask(__name__, template_folder='web_templates')
app.secret_key = 'your-secret_key_here_2025'  # In production, use a secure secret key

# Configure database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Authentication decorator for MCP tools
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Missing Authorization header'}), 401
        
        # Check if it's a Bearer token
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid Authorization header format'}), 401
        
        # Extract token
        token = auth_header.split(' ')[1]
        
        # Validate token against stored tokens
        user = User.query.filter_by(auth_token=token).first()
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user to request context for use in MCP tools
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function

# User authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('templates_market'))
        else:
            return render_template('login.html', error="用户名或密码错误")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="用户名已存在")
        
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error="邮箱已被注册")
        
        # Create new user
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Template management routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('templates_market'))
    return redirect(url_for('login'))

@app.route('/templates/market')
def templates_market():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get all public templates and user's own templates
    public_templates = Template.query.filter_by(is_public=True).all()
    user_templates = Template.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('templates_market.html', 
                          public_templates=public_templates, 
                          user_templates=user_templates,
                          username=session['username'])

@app.route('/templates/create', methods=['GET', 'POST'])
def create_template():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        description = request.form['description']
        is_public = 'is_public' in request.form
        
        # Create new template
        template = Template(
            name=name,
            content=content,
            description=description,
            user_id=session['user_id'],
            is_public=is_public
        )
        db.session.add(template)
        db.session.commit()
        
        # Process placeholders
        placeholders_data = request.form.get('placeholders', '')
        if placeholders_data:
            placeholders = placeholders_data.split('\n')
            for placeholder_line in placeholders:
                if ':' in placeholder_line:
                    parts = placeholder_line.split(':', 1)
                    name = parts[0].strip()
                    desc = parts[1].strip() if len(parts) > 1 else ''
                    if name:
                        placeholder = Placeholder(
                            name=name,
                            description=desc,
                            template_id=template.id
                        )
                        db.session.add(placeholder)
        
        # Process prompts
        prompts_data = request.form.get('prompts', '')
        if prompts_data:
            prompts = prompts_data.split('\n')
            for i, prompt_content in enumerate(prompts):
                if prompt_content.strip():
                    prompt = Prompt(
                        order=i,
                        content=prompt_content.strip(),
                        template_id=template.id
                    )
                    db.session.add(prompt)
        
        db.session.commit()
        
        return redirect(url_for('templates_market'))
    
    return render_template('create_template.html', username=session['username'])

@app.route('/templates/<int:template_id>')
def view_template(template_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    template = Template.query.get_or_404(template_id)
    
    # Check if user can view this template (own template or public)
    if template.user_id != session['user_id'] and not template.is_public:
        return "访问被拒绝", 403
    
    placeholders = Placeholder.query.filter_by(template_id=template_id).all()
    prompts = Prompt.query.filter_by(template_id=template_id).order_by(Prompt.order).all()
    
    return render_template('template_detail.html', 
                          template=template, 
                          placeholders=placeholders, 
                          prompts=prompts,
                          username=session['username'])

if __name__ == '__main__':
    # Bind to all interfaces to allow external access
    app.run(debug=True, host='0.0.0.0', port=5000)