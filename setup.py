#!/usr/bin/env python3
"""
Setup script for the Multi-Agent Board Emulation System

This script helps set up the environment and dependencies.
Run with: python setup.py
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"Python version: {sys.version}")
    return True

def install_requirements():
    """Install required packages"""
    print("\nInstalling required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False

def check_api_key():
    """Check if Gemini API key is set"""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"✅ Gemini API key is set: {api_key[:8]}...")
        return True
    else:
        print("⚠️  GEMINI_API_KEY environment variable not set")
        print("   To set it:")
        print("   Windows (PowerShell): $env:GEMINI_API_KEY='your_api_key_here'")
        print("   macOS/Linux: export GEMINI_API_KEY='your_api_key_here'")
        print("   Get your API key from: https://makersuite.google.com/app/apikey")
        return False

def test_imports():
    """Test if all modules can be imported"""
    print("\n🧪 Testing imports...")
    try:
        import board_emulation
        print("✅ Board emulation module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_demo():
    """Run the mock demo to verify functionality"""
    print("\n🎭 Running mock demo...")
    try:
        result = subprocess.run([sys.executable, "demo_mock.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Mock demo completed successfully")
            return True
        else:
            print(f"❌ Demo failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Demo timed out")
        return False
    except Exception as e:
        print(f"❌ Demo error: {e}")
        return False

def main():
    """Main setup function"""
    print("Setting up Multi-Agent Board Emulation System")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install requirements
    if not install_requirements():
        return 1
    
    # Test imports
    if not test_imports():
        return 1
    
    # Check API key
    api_key_available = check_api_key()
    
    # Run demo
    if not run_demo():
        return 1
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    
    if api_key_available:
        print("\nYou can now run the full simulation:")
        print("   python board_emulation.py")
    else:
        print("\nYou can run the mock demo anytime:")
        print("   python demo_mock.py")
    
    print("\nFor more information, see README.md")
    return 0

if __name__ == "__main__":
    exit(main())
