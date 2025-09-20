# MCP Tool 4: Generate Complete Document

from flask import jsonify, request
from models.models import db, Template, Placeholder, Prompt

def generate_complete_document():
    """
    Generate the complete design document
    Requires: template_id
    """
    data = request.json
    template_id = data.get('template_id')
    
    if not template_id:
        return jsonify({'error': 'Missing template_id parameter'}), 400
    
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
    
    # Get the template
    template = Template.query.get(template_id)
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
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