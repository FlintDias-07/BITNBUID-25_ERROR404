import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Output: {e.output}")
        return False

def create_directory_structure():
    """Create the required directory structure"""
    directories = [
        'templates/users',
        'templates/projects', 
        'templates/payments',
        'templates/chat',
        'templates/portfolio',
        'static/css',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def main():
    print("🎓 GigCampus Project Setup")
    print("=" * 40)
    
    # Check if we're in a Django project directory
    if not os.path.exists('manage.py'):
        print("❌ This script must be run from the Django project root directory.")
        print("   Make sure you've created the Django project first:")
        print("   django-admin startproject gigcampus")
        sys.exit(1)
    
    # Create directory structure
    print("\n📁 Creating directory structure...")
    create_directory_structure()
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("⚠️  You may need to install requirements manually:")
        print("   pip install Django>=4.2.0 channels>=4.0.0 channels-redis>=4.1.0")
    
    # Create apps if they don't exist
    apps = ['users', 'projects', 'payments', 'chat', 'portfolio']
    for app in apps:
        if not os.path.exists(app):
            run_command(f"python manage.py startapp {app}", f"Creating {app} app")
    
    # Run migrations
    run_command("python manage.py makemigrations", "Creating migrations")
    run_command("python manage.py migrate", "Running migrations")
    
    # Create superuser prompt
    print("\n👑 Create superuser account")
    print("   Run: python manage.py createsuperuser")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Copy all the model, view, form, and template code to respective files")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Run the server: python manage.py runserver")
    print("4. Visit http://127.0.0.1:8000 to see your GigCampus platform!")
    
    print("\n📝 Don't forget to:")
    print("- Update your SECRET_KEY in settings.py for production")
    print("- Configure Redis for production chat functionality")
    print("- Set up proper static file serving for production")

if __name__ == "__main__":
    main()