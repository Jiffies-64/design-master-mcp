# MCP Tool 3: Submit Placeholder Content

from flask import jsonify, request
from models.models import db, Placeholder

def submit_placeholder_content():
    """
    Submit content for placeholders
    Requires: placeholder_id, content
    """
    data = request.json
    placeholder_id = data.get('placeholder_id')
    content = data.get('content')
    
    if not placeholder_id or content is None:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Find the placeholder
    placeholder = Placeholder.query.get(placeholder_id)
    if not placeholder:
        return jsonify({'error': 'Placeholder not found'}), 404
    
    # Update the placeholder content
    placeholder.content = content
    db.session.commit()
    
    return jsonify({
        'message': 'Content submitted successfully',
        'placeholder_id': placeholder_id
    })