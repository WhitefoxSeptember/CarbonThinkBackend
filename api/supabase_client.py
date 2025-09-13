import os
from supabase import create_client, Client
from django.conf import settings

class SupabaseClient:
    """
    Supabase client utility for handling REST API operations
    """
    
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")
        
        self.client: Client = create_client(self.url, self.key)
    
    def get_client(self) -> Client:
        """Get the Supabase client instance"""
        return self.client
    
    # User Account operations
    def create_user_account(self, data):
        """Create a new user account"""
        return self.client.table('user_accounts').insert(data).execute()
    
    def get_user_account(self, user_id):
        """Get user account by ID"""
        return self.client.table('user_accounts').select('*').eq('id', user_id).execute()
    
    def update_user_account(self, user_id, data):
        """Update user account"""
        return self.client.table('user_accounts').update(data).eq('id', user_id).execute()
    
    def delete_user_account(self, user_id):
        """Delete user account"""
        return self.client.table('user_accounts').delete().eq('id', user_id).execute()
    
    def list_user_accounts(self):
        """List all user accounts"""
        return self.client.table('user_accounts').select('*').execute()
    
    # Activity operations
    def create_activity(self, data):
        """Create a new activity"""
        return self.client.table('activities').insert(data).execute()
    
    def get_activity(self, activity_id):
        """Get activity by ID"""
        return self.client.table('activities').select('*').eq('id', activity_id).execute()
    
    def update_activity(self, activity_id, data):
        """Update activity"""
        return self.client.table('activities').update(data).eq('id', activity_id).execute()
    
    def delete_activity(self, activity_id):
        """Delete activity"""
        return self.client.table('activities').delete().eq('id', activity_id).execute()
    
    def list_activities(self, user_id=None):
        """List activities, optionally filtered by user_id"""
        query = self.client.table('activities').select('*')
        if user_id:
            query = query.eq('user_id', user_id)
        return query.execute()
    
    # Carbon Source operations
    def create_carbon_source(self, data):
        """Create a new carbon source"""
        return self.client.table('carbon_sources').insert(data).execute()
    
    def get_carbon_source(self, source_id):
        """Get a specific carbon source by UID"""
        return self.client.table('carbon_sources').select('*').eq('uid', source_id).execute()

    def update_carbon_source(self, source_id, data):
        """Update a carbon source"""
        return self.client.table('carbon_sources').update(data).eq('uid', source_id).execute()

    def delete_carbon_source(self, source_id):
        """Delete a carbon source"""
        return self.client.table('carbon_sources').delete().eq('uid', source_id).execute()
    
    def list_carbon_sources(self):
        """List all carbon sources"""
        return self.client.table('carbon_sources').select('*').execute()
    
    # Carbon consumption calculation
    def calculate_carbon_consumption(self, user_id, start_date=None, end_date=None):
        """Calculate carbon consumption for a user within a date range"""
        query = self.client.table('activities').select('*').eq('user_id', user_id)
        
        if start_date:
            query = query.gte('date', start_date)
        if end_date:
            query = query.lte('date', end_date)
            
        return query.execute()

# Global instance
supabase_client = SupabaseClient()