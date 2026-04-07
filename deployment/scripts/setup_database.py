"""
Complete database setup script
Cross-platform (Windows/Linux/Mac)
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run command and print output"""
    try:
        result = subprocess.run(
            cmd,
            shell=False,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("=" * 50)
    print("Churn Prediction System - Database Setup")
    print("=" * 50)
    print()
    
    base_dir = Path(__file__).parent
    backend_dir = base_dir / "backend"
    app_dir = backend_dir / "app"
    
    # Step 1: Install dependencies
    print("Step 1: Installing dependencies...")
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=backend_dir):
        print("Warning: Some dependencies may have failed to install")
    
    # Step 2: Load customer data
    print("\nStep 2: Creating database and loading customer data...")
    if not run_command([sys.executable, "-m", "database.load_data"], cwd=app_dir):
        print("Error loading data. Please check the CSV URL and try again.")
        return
    
    # Step 3: Generate predictions
    print("\nStep 3: Generating predictions for all customers...")
    if not run_command([sys.executable, "-m", "database.generate_predictions"], cwd=app_dir):
        print("Warning: Prediction generation had issues")
    
    print("\n" + "=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print()
    print("Database created: churn_prediction.db")
    print("Tables: customers, predictions, interventions, model_metrics")
    print()
    print("To start the server:")
    print(f"  cd {backend_dir}")
    print(f"  {sys.executable} -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print()
    print("Then open: http://localhost:8000")
    print("=" * 50)

if __name__ == "__main__":
    main()
