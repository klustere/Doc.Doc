#!/usr/bin/env python
"""
Database setup script for Django Confluence Clone.
This script helps diagnose and fix database connectivity issues.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confluence_clone.settings')

def test_db_connection():
    """Test database connectivity."""
    print("🔍 Testing database connection...")
    
    try:
        django.setup()
        from django.db import connection
        from django.core.management.color import no_style
        
        # Test basic connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            print("✅ Database connection successful!")
            return True
        else:
            print("❌ Database connection failed - unexpected result")
            return False
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Possible solutions:")
        print("   1. Start PostgreSQL service")
        print("   2. Create the database: CREATE DATABASE confluence_db;")
        print("   3. Check credentials in settings.py")
        print("   4. Or switch to SQLite for development (see below)")
        return False

def suggest_sqlite_config():
    """Suggest SQLite configuration for development."""
    print("\n" + "="*50)
    print("🔧 DEVELOPMENT ALTERNATIVE: Switch to SQLite")
    print("="*50)
    print("If PostgreSQL setup is complex, you can use SQLite for development.")
    print("Replace the DATABASES setting in confluence_clone/settings.py with:")
    print()
    print("DATABASES = {")
    print("    'default': {")
    print("        'ENGINE': 'django.db.backends.sqlite3',")
    print("        'NAME': BASE_DIR / 'db.sqlite3',")
    print("    }")
    print("}")
    print()
    print("Then run:")
    print("  python manage.py migrate")
    print("  python manage.py runserver")

def run_migrations():
    """Run Django migrations."""
    print("\n🔄 Running migrations...")
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_sample_data():
    """Create some sample pages for testing."""
    print("\n📄 Creating sample data...")
    try:
        from pages.models import Page, Chapter
        
        # Create a sample chapter
        chapter, created = Chapter.objects.get_or_create(
            title="Getting Started",
            defaults={'description': "Introduction and basic concepts"}
        )
        
        # Create sample pages
        sample_pages = [
            {
                'title': 'Welcome to Confluence Clone',
                'content': '''# Welcome!

This is your first page in the Confluence Clone system.

## Features
- Create and edit pages with Markdown
- Link pages together
- Organize with chapters
- Vector search with Chroma DB

Happy writing! 🚀''',
                'chapter': chapter
            },
            {
                'title': 'How to Create Pages',
                'content': '''# Creating Pages

To create a new page:

1. Click the "Create Page" button
2. Enter a title and content
3. Use Markdown for formatting
4. Save your changes

## Markdown Tips
- Use `#` for headers
- Use `**bold**` for emphasis
- Use `[link text](url)` for links''',
                'chapter': chapter
            },
            {
                'title': 'Linking Pages',
                'content': '''# Page Linking

Pages can link to each other to create a knowledge graph.

## How to Link
1. Edit a page
2. Use the link button in the toolbar
3. Select the target page
4. Save changes

This creates bidirectional relationships between pages.''',
                'chapter': chapter
            }
        ]
        
        for page_data in sample_pages:
            page, created = Page.objects.get_or_create(
                title=page_data['title'],
                defaults={
                    'content': page_data['content'],
                    'chapter': page_data['chapter']
                }
            )
            if created:
                print(f"  ✅ Created: {page.title}")
            else:
                print(f"  ℹ️  Already exists: {page.title}")
        
        total_pages = Page.objects.count()
        print(f"\n📊 Total pages in database: {total_pages}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
        return False

def main():
    """Run the complete database setup process."""
    print("🔧 Django Database Setup")
    print("=" * 40)
    
    # Test connection
    if not test_db_connection():
        suggest_sqlite_config()
        return
    
    # Run migrations
    if not run_migrations():
        return
    
    # Create sample data
    create_sample_data()
    
    print("\n" + "=" * 40)
    print("✅ Database setup complete!")
    print("💡 Now start the server with: python manage.py runserver")

if __name__ == '__main__':
    main()