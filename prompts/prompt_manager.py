# Prompts Module Implementation

class PromptManager:
    """Manage prompts for design document creation"""
    
    def __init__(self):
        self.prompts = {}
    
    def create_prompt_sequence(self, template_id, prompt_list):
        """Create a sequence of prompts for a template"""
        self.prompts[template_id] = []
        for i, prompt_content in enumerate(prompt_list):
            prompt = {
                'id': f"{template_id}_{i}",
                'order': i,
                'content': prompt_content,
                'completed': False
            }
            self.prompts[template_id].append(prompt)
    
    def get_next_prompt(self, template_id):
        """Get the next incomplete prompt for a template"""
        if template_id not in self.prompts:
            return None
        
        for prompt in self.prompts[template_id]:
            if not prompt['completed']:
                return prompt
        return None
    
    def mark_prompt_completed(self, prompt_id):
        """Mark a prompt as completed"""
        # Extract template_id and order from prompt_id
        parts = prompt_id.split('_')
        if len(parts) != 2:
            return False
        
        template_id = int(parts[0])
        order = int(parts[1])
        
        if template_id not in self.prompts:
            return False
        
        for prompt in self.prompts[template_id]:
            if prompt['order'] == order:
                prompt['completed'] = True
                return True
        return False
    
    def all_prompts_completed(self, template_id):
        """Check if all prompts for a template are completed"""
        if template_id not in self.prompts:
            return False
        
        for prompt in self.prompts[template_id]:
            if not prompt['completed']:
                return False
        return True