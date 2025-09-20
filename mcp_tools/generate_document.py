# MCP Tool 4: Generate Complete Document

from flask import jsonify, request
from models.models import db, Template, Placeholder, Prompt, User

def generate_complete_document():
    """
    Generate the complete design document
    Requires: template_id, api_key
    """
    data = request.json
    template_id = data.get('template_id')
    api_key = data.get('api_key')
    
    if not template_id or not api_key:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Check if user exists by API key
    user = User.query.filter_by(auth_token=api_key).first()
    if not user:
        return jsonify({'error': 'Invalid API key'}), 401
    
    # Check if template belongs to user or is public
    template = Template.query.get(template_id)
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    if template.user_id != user.id and not template.is_public:
        return jsonify({'error': 'Access denied to private template'}), 403
    
    # Check if all prompts are completed
    incomplete_prompts = Prompt.query.filter_by(
        template_id=template_id, 
        completed=False
    ).count()
    
    if incomplete_prompts > 0:
        return jsonify({
            'error': 'Not all steps are completed',
            'incomplete_steps': incomplete_prompts
        }), 400
    
    # Get all placeholders for this template
    placeholders = Placeholder.query.filter_by(template_id=template_id).all()
    
    # Generate the document by replacing placeholders
    document_content = template.content
    for placeholder in placeholders:
        placeholder_key = f"{{{{{placeholder.name}}}}}"
        document_content = document_content.replace(
            placeholder_key, 
            placeholder.content or f"[{placeholder.name} content not provided]"
        )
    
    # In a real implementation, you would either:
    # 1. Save to a file and return the path
    # 2. Send to user's email
    # 3. Return in response
    
    return jsonify({
        'message': 'Document generated successfully',
        'document_content': document_content
    })