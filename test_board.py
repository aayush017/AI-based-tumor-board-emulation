#!/usr/bin/env python3
"""
Test script for the Board Emulation System

This script tests the basic functionality without making API calls.
Run with: python test_board.py
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from board_emulation import (
            PatientCase, MedicalAgent, Oncologist, 
            Radiologist, Pathologist, TumorBoard
        )
        print("✅ All classes imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_patient_case():
    """Test PatientCase data structure"""
    print("\nTesting PatientCase...")
    
    try:
        from board_emulation import PatientCase
        case = PatientCase(
            patient_id="TEST-001",
            age=45,
            gender="male",
            tumor_size=2.5,
            tumor_stage="T1N0M0",
            biopsy_result="Test biopsy result",
            imaging_result="Test imaging result",
            symptoms=["test symptom"],
            medical_history=["test history"]
        )
        
        print(f"✅ PatientCase created: {case.patient_id}")
        print(f"   Age: {case.age}, Gender: {case.gender}")
        print(f"   Tumor: {case.tumor_size}cm, Stage: {case.tumor_stage}")
        return True
    except Exception as e:
        print(f"❌ PatientCase error: {e}")
        return False

def test_agent_creation():
    """Test agent creation (without LLM calls)"""
    print("\nTesting agent creation...")
    
    try:
        # Test that we can create agents (they won't work without API key)
        from board_emulation import Oncologist, Radiologist, Pathologist
        oncologist = Oncologist()
        radiologist = Radiologist()
        pathologist = Pathologist()
        
        print("✅ All agents created successfully")
        print(f"   Oncologist: {oncologist.name} ({oncologist.specialty})")
        print(f"   Radiologist: {radiologist.name} ({radiologist.specialty})")
        print(f"   Pathologist: {pathologist.name} ({pathologist.specialty})")
        return True
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False

def test_tumor_board():
    """Test tumor board creation"""
    print("\nTesting TumorBoard...")
    
    try:
        from board_emulation import TumorBoard
        board = TumorBoard()
        print(f"✅ TumorBoard created with {len(board.agents)} agents")
        
        for i, agent in enumerate(board.agents):
            print(f"   Agent {i+1}: {agent.specialty}")
        
        return True
    except Exception as e:
        print(f"❌ TumorBoard error: {e}")
        return False

def test_sample_case():
    """Test sample case creation"""
    print("\nTesting sample case creation...")
    
    try:
        from board_emulation import create_sample_case
        case = create_sample_case()
        
        print("✅ Sample case created successfully")
        print(f"   Patient ID: {case.patient_id}")
        print(f"   Case details: {case.age} year old {case.gender}")
        print(f"   Tumor: {case.tumor_size}cm, Stage: {case.tumor_stage}")
        return True
    except Exception as e:
        print(f"❌ Sample case error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Board Emulation System")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_patient_case,
        test_agent_creation,
        test_tumor_board,
        test_sample_case
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to run.")
        print("\nTo run the full simulation:")
        print("1. Set your GEMINI_API_KEY environment variable")
        print("2. Run: python board_emulation.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
