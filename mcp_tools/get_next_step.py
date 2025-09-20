# MCP Tool 2: Get Next Step

from flask import jsonify, request
from models.models import db, Prompt

def get_next_step():
    """
    Get the next prompt in the sequence
    Requires: template_id
    """
    template_id = request.args.get('template_id')
    
    if not template_id:
        return jsonify({'error': 'Missing template_id parameter'}), 400
    
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