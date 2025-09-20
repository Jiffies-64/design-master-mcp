# MCP Tool 2: Get Next Step

from flask import jsonify, request
from models.models import db, Prompt, Template, User

def get_next_step():
    """
    Get the next prompt in the sequence
    Requires: template_id, api_key
    """
    template_id = request.args.get('template_id')
    api_key = request.args.get('api_key')
    
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
    
    # Find the next incomplete prompt
    next_prompt = Prompt.query.filter_by(
        template_id=template_id, 
        completed=False
    ).order_by(Prompt.order).first()
    
    if not next_prompt:
        return jsonify({'message': 'No more steps available'}), 200
    
    return jsonify({
        'prompt_id': next_prompt.id,
        'content': next_prompt.content,
        'order': next_prompt.order
    })