#!/usr/bin/env python3
"""
基于FastMCP标准的MCP服务实现
支持多种传输方式：STDIO、SSE、StreamableHTTP
"""

from fastmcp import FastMCP
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import asyncio

# Create an MCP server
mcp = FastMCP("DesignMaster")

# Initialize Flask app for database access
app = Flask(__name__)

# Configure database (same as main app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Import models after db initialization
from models.models import User, Template, Placeholder, Prompt

# Add tools for design document generation
@mcp.tool()
def start_document_generation(project_root_path: str, user_id: int) -> dict:
    """Start generating a design document"""
    try:
        with app.app_context():
            # Validate inputs
            if not project_root_path or not user_id:
                return {'error': 'Missing required parameters'}
            
            # Check if user exists
            user = User.query.get(user_id)
            if not user:
                return {'error': 'User not found'}
            
            # Here you would implement the logic to start document generation
            # For now, we'll just return a success message
            return {
                'message': 'Document generation started successfully',
                'project_root_path': project_root_path,
                'user_id': user_id
            }
    except Exception as e:
        return {'error': str(e)}

@mcp.tool()
def get_next_step(template_id: int) -> dict:
    """Get the next prompt in the sequence"""
    try:
        with app.app_context():
            if not template_id:
                return {'error': 'Missing template_id parameter'}
            
            # Find the next incomplete prompt
            next_prompt = Prompt.query.filter_by(
                template_id=template_id, 
                completed=False
            ).order_by(Prompt.order).first()
            
            if not next_prompt:
                return {'message': 'No more steps available'}
            
            return {
                'prompt_id': next_prompt.id,
                'content': next_prompt.content,
                'order': next_prompt.order
            }
    except Exception as e:
        return {'error': str(e)}

@mcp.tool()
def submit_placeholder_content(placeholder_id: int, content: str) -> dict:
    """Submit content for placeholders"""
    try:
        with app.app_context():
            if not placeholder_id or content is None:
                return {'error': 'Missing required parameters'}
            
            # Find the placeholder
            placeholder = Placeholder.query.get(placeholder_id)
            if not placeholder:
                return {'error': 'Placeholder not found'}
            
            # Update the placeholder content
            placeholder.content = content
            db.session.commit()
            
            return {
                'message': 'Content submitted successfully',
                'placeholder_id': placeholder_id
            }
    except Exception as e:
        return {'error': str(e)}

@mcp.tool()
def generate_complete_document(template_id: int) -> dict:
    """Generate the complete design document"""
    try:
        with app.app_context():
            if not template_id:
                return {'error': 'Missing template_id parameter'}
            
            # Check if all prompts are completed
            incomplete_prompts = Prompt.query.filter_by(
                template_id=template_id, 
                completed=False
            ).count()
            
            if incomplete_prompts > 0:
                return {
                    'error': 'Not all steps are completed',
                    'incomplete_steps': incomplete_prompts
                }
            
            # Get the template
            template = Template.query.get(template_id)
            if not template:
                return {'error': 'Template not found'}
            
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
            
            return {
                'message': 'Document generated successfully',
                'document_content': document_content
            }
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    # Check command line arguments for transport mode
    transport_mode = "stdio"  # default mode
    host = "127.0.0.1"
    port = 8000
    
    # Parse command line arguments
    if "--sse" in sys.argv:
        transport_mode = "sse"
    elif "--http" in sys.argv:
        transport_mode = "http"
    elif "--streamable-http" in sys.argv:
        transport_mode = "streamable-http"
    
    # Check for host and port arguments
    for i, arg in enumerate(sys.argv):
        if arg == "--host" and i + 1 < len(sys.argv):
            host = sys.argv[i + 1]
        elif arg == "--port" and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])
    
    # Run the MCP server with specified transport mode
    if transport_mode == "sse":
        print(f"Running MCP server with SSE transport on {host}:{port}")
        asyncio.run(mcp.run_sse_async(host=host, port=port))
    elif transport_mode == "http":
        print(f"Running MCP server with HTTP transport on {host}:{port}")
        asyncio.run(mcp.run_http_async(host=host, port=port))
    elif transport_mode == "streamable-http":
        print(f"Running MCP server with StreamableHTTP transport on {host}:{port}")
        asyncio.run(mcp.run_streamable_http_async(host=host, port=port))
    else:
        print("Running MCP server with STDIO transport")
        mcp.run()