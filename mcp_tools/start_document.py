# MCP Tool 1: Start Document Generation

from flask import jsonify, request
from models.models import db, User, Template

def start_document_generation():
    """
    Start generating a design document
    Requires: project_root_path, api_key
    """
    data = request.json
    project_root_path = data.get('project_root_path')
    api_key = data.get('api_key')
    
    # Validate inputs
    if not project_root_path or not api_key:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Check if user exists by API key
    user = User.query.filter_by(auth_token=api_key).first()
    if not user:
        return jsonify({'error': 'Invalid API key'}), 401
    
    # Here you would implement the logic to start document generation
    # For now, we'll just return a success message
    return jsonify({
        'message': 'Document generation started successfully',
        'project_root_path': project_root_path,
        'user_id': user.id
    })