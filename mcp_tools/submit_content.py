# MCP Tool 3: Submit Placeholder Content

from flask import jsonify, request
from models.models import db, Placeholder, Template, User

def submit_placeholder_content():
    """
    Submit content for placeholders
    Requires: placeholder_id, content, api_key
    """
    data = request.json
    placeholder_id = data.get('placeholder_id')
    content = data.get('content')
    api_key = data.get('api_key')
    
    if not placeholder_id or content is None or not api_key:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Check if user exists by API key
    user = User.query.filter_by(auth_token=api_key).first()
    if not user:
        return jsonify({'error': 'Invalid API key'}), 401
    
    # Find the placeholder
    placeholder = Placeholder.query.get(placeholder_id)
    if not placeholder:
        return jsonify({'error': 'Placeholder not found'}), 404
    
    # Check if placeholder belongs to user's template
    template = Template.query.get(placeholder.template_id)
    if template.user_id != user.id:
        return jsonify({'error': 'Access denied to this placeholder'}), 403
    
    # Update the placeholder content
    placeholder.content = content
    db.session.commit()
    
    return jsonify({
        'message': 'Content submitted successfully',
        'placeholder_id': placeholder_id
    })