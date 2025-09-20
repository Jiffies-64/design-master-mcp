# Template Module Implementation

class TemplateManager:
    """Manage design document templates"""
    
    def __init__(self):
        self.templates = {}
    
    def create_template(self, name, content, description=""):
        """Create a new template"""
        template_id = len(self.templates) + 1
        self.templates[template_id] = {
            'id': template_id,
            'name': name,
            'content': content,
            'description': description,
            'placeholders': []
        }
        return template_id
    
    def add_placeholder(self, template_id, name, description="", example=""):
        """Add a placeholder to a template"""
        if template_id not in self.templates:
            raise ValueError("Template not found")
        
        placeholder = {
            'name': name,
            'description': description,
            'example': example
        }
        self.templates[template_id]['placeholders'].append(placeholder)
    
    def get_template(self, template_id):
        """Get a template by ID"""
        return self.templates.get(template_id)
    
    def list_templates(self):
        """List all templates"""
        return list(self.templates.values())