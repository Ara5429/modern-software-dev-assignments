"""Script to reset the database"""
from app.database import reset_db

if __name__ == "__main__":
    print("⚠️  This will delete all data!")
    confirm = input("Are you sure? (yes/no): ")
    if confirm.lower() == "yes":
        reset_db()
    else:
        print("❌ Cancelled")
