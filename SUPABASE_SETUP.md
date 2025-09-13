# Supabase Setup Guide for CarbonThink Backend

## Step 1: Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Choose your organization and enter project details
4. Wait for the project to be created (usually takes 1-2 minutes)

## Step 2: Get Your Project Credentials

1. In your Supabase dashboard, go to **Settings** → **API**
2. Copy the following values:
   - **Project URL** (looks like: `https://your-project-id.supabase.co`)
   - **anon public** key (starts with `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)
   - **service_role** key (also starts with `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)

## Step 3: Update Your .env File

1. Open the `.env` file in your project root
2. Replace the placeholder values with your actual Supabase credentials:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Step 4: Create Database Tables

1. In your Supabase dashboard, go to **SQL Editor**
2. Click "New Query"
3. Copy and paste the contents of `supabase/migrations/001_create_tables.sql`
4. Click "Run" to execute the SQL
5. Then copy and paste the contents of `supabase/migrations/002_grant_permissions.sql`
6. Click "Run" to execute the permissions and sample data

## Step 5: Verify Setup

1. Go to **Table Editor** in your Supabase dashboard
2. You should see the following tables:
   - `user_accounts`
   - `user_profiles`
   - `carbon_sources`
   - `carbon_records`
   - `user_profile_sources`

## Step 6: Test Your API

1. Restart your Django server: `python manage.py runserver`
2. Test the API endpoints:
   - GET `http://127.0.0.1:8000/api/accounts/users/` (should return empty list or sample user)
   - GET `http://127.0.0.1:8000/api/sources/` (should return sample carbon sources)

## Troubleshooting

### Common Issues:

1. **"Could not find the table 'public.user_accounts'"**
   - Make sure you ran both SQL migration files in the correct order
   - Check that the tables exist in your Supabase Table Editor

2. **"SUPABASE_URL and SUPABASE_ANON_KEY must be set"**
   - Verify your `.env` file has the correct values
   - Restart your Django server after updating `.env`

3. **Permission denied errors**
   - Make sure you ran the `002_grant_permissions.sql` file
   - Check that RLS policies are properly configured

### Testing Individual Endpoints:

```bash
# Test user list (PowerShell)
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/accounts/users/" -Method GET

# Test carbon sources
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/sources/" -Method GET

# Test carbon consumption calculation
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/activities/carbon-consumption/1/" -Method GET
```

## Next Steps

Once your setup is complete:
1. Your Django backend will use Supabase for all data operations
2. You can manage your data through the Supabase dashboard
3. All API endpoints should work correctly with the Supabase database