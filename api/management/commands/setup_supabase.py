from django.core.management.base import BaseCommand
from django.conf import settings
import os
from supabase import create_client, Client
from datetime import datetime

class Command(BaseCommand):
    help = 'Set up Supabase tables and initial data for CarbonThink'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of tables (will drop existing tables)',
        )

    def handle(self, *args, **options):
        # Check if environment variables are set
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')  # Use service role for admin operations
        
        if not supabase_url or not supabase_key:
            self.stdout.write(
                self.style.ERROR(
                    'SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in your .env file.\n'
                    'Please check the SUPABASE_SETUP.md file for instructions.'
                )
            )
            return

        if supabase_url == 'your_supabase_project_url_here' or supabase_key == 'your_supabase_service_role_key_here':
            self.stdout.write(
                self.style.ERROR(
                    'Please update your .env file with actual Supabase credentials.\n'
                    'Check the SUPABASE_SETUP.md file for instructions.'
                )
            )
            return

        try:
            # Create Supabase client with service role key
            supabase: Client = create_client(supabase_url, supabase_key)
            
            self.stdout.write('Setting up Supabase tables...')
            
            # Read and execute the SQL migration files
            self.execute_sql_file(supabase, 'supabase/migrations/001_create_tables.sql')
            self.execute_sql_file(supabase, 'supabase/migrations/002_grant_permissions.sql')
            
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully set up Supabase tables and permissions!\n'
                    'You can now test your API endpoints.'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error setting up Supabase: {str(e)}')
            )

    def execute_sql_file(self, supabase: Client, file_path: str):
        """Execute SQL commands from a file"""
        try:
            with open(file_path, 'r') as file:
                sql_content = file.read()
            
            # Split SQL content by semicolons and execute each statement
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement:
                    # Use the rpc method to execute raw SQL
                    result = supabase.rpc('exec_sql', {'sql': statement}).execute()
                    
            self.stdout.write(f'✓ Executed {file_path}')
            
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'SQL file not found: {file_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error executing {file_path}: {str(e)}')
            )
            # For SQL execution, we'll provide manual instructions instead
            self.stdout.write(
                self.style.WARNING(
                    f'Please manually execute the SQL in {file_path} using the Supabase SQL Editor.\n'
                    'See SUPABASE_SETUP.md for detailed instructions.'
                )
            )