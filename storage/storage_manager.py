# Storage Module Implementation

import os
import json
from datetime import datetime

class StorageManager:
    """Manage user resources and data storage"""
    
    def __init__(self, storage_dir="storage"):
        self.storage_dir = storage_dir
        # Create storage directory if it doesn't exist
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
    
    def save_user_data(self, user_id, data):
        """Save user data to storage"""
        user_file = os.path.join(self.storage_dir, f"user_{user_id}.json")
        
        # Add timestamp
        data['last_updated'] = datetime.now().isoformat()
        
        # Load existing data if file exists
        if os.path.exists(user_file):
            with open(user_file, 'r') as f:
                existing_data = json.load(f)
            # Merge data
            existing_data.update(data)
            data = existing_data
        
        # Save data
        with open(user_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return user_file
    
    def load_user_data(self, user_id):
        """Load user data from storage"""
        user_file = os.path.join(self.storage_dir, f"user_{user_id}.json")
        
        if not os.path.exists(user_file):
            return {}
        
        with open(user_file, 'r') as f:
            return json.load(f)
    
    def save_template(self, user_id, template_id, template_data):
        """Save a template for a user"""
        user_data = self.load_user_data(user_id)
        if 'templates' not in user_data:
            user_data['templates'] = {}
        
        user_data['templates'][template_id] = template_data
        self.save_user_data(user_id, user_data)
    
    def get_template(self, user_id, template_id):
        """Get a template for a user"""
        user_data = self.load_user_data(user_id)
        if 'templates' not in user_data:
            return None
        
        return user_data['templates'].get(template_id)
    
    def list_user_templates(self, user_id):
        """List all templates for a user"""
        user_data = self.load_user_data(user_id)
        if 'templates' not in user_data:
            return []
        
        return list(user_data['templates'].values())