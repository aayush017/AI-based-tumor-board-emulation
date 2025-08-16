#!/usr/bin/env python3
"""
Demo script for the Board Emulation System with Mock Responses

This script demonstrates the system functionality without requiring an API key.
Run with: python demo_mock.py
"""

import os
from board_emulation import (
    PatientCase, MedicalAgent, Oncologist, 
    Radiologist, Pathologist, TumorBoard, create_sample_case
)

class MockLLM:
    """Mock LLM that returns predefined responses for demonstration"""
    
    def __init__(self, specialty: str):
        self.specialty = specialty
        self.responses = {
            "Oncologist": "Based on the case analysis, I recommend a combination approach: neoadjuvant chemotherapy followed by surgical resection. Given the T2N1M0 staging and positive lymph node, this patient would benefit from systemic therapy to address potential micrometastases before surgery. Consider 4-6 cycles of AC-T chemotherapy regimen.",
            "Radiologist": "The imaging reveals a 3.2 cm irregular mass with spiculated margins in the upper outer quadrant, highly suspicious for malignancy. The axillary lymph node appears enlarged and irregular, suggesting nodal involvement. Recommend additional imaging with breast MRI for better tissue characterization and to rule out multifocal disease.",
            "Pathologist": "The biopsy confirms invasive ductal carcinoma, grade 2, with ER+ and PR+ hormone receptor expression and HER2- status. This represents a luminal A subtype with favorable prognosis. The tumor shows moderate differentiation with clear margins. Recommend Oncotype DX testing to guide chemotherapy decisions."
        }
    
    def invoke(self, prompt: str):
        """Return a mock response"""
        from langchain_core.messages import AIMessage
        return AIMessage(content=self.responses.get(self.specialty, "No recommendation available"))

def create_mock_agents():
    """Create agents with mock LLMs for demonstration"""
    
    # Create mock agents by temporarily replacing their LLMs
    # We need to handle the case where agents can't be created due to missing API key
    try:
        oncologist = Oncologist()
        oncologist.llm = MockLLM("Oncologist")
    except:
        # Create a minimal agent if the real one fails
        oncologist = type('MockOncologist', (), {
            'name': 'Dr. Smith',
            'specialty': 'Oncologist',
            'llm': MockLLM("Oncologist"),
            'analyze_case': lambda self, case: MockLLM("Oncologist").invoke("").content,
            'get_specialty_context': lambda self: "You are an Oncologist with expertise in oncologist analysis."
        })()
    
    try:
        radiologist = Radiologist()
        radiologist.llm = MockLLM("Radiologist")
    except:
        radiologist = type('MockRadiologist', (), {
            'name': 'Dr. Johnson',
            'specialty': 'Radiologist',
            'llm': MockLLM("Radiologist"),
            'analyze_case': lambda self, case: MockLLM("Radiologist").invoke("").content,
            'get_specialty_context': lambda self: "You are a Radiologist with expertise in radiologist analysis."
        })()
    
    try:
        pathologist = Pathologist()
        pathologist.llm = MockLLM("Pathologist")
    except:
        pathologist = type('MockPathologist', (), {
            'name': 'Dr. Williams',
            'specialty': 'Pathologist',
            'llm': MockLLM("Pathologist"),
            'analyze_case': lambda self, case: MockLLM("Pathologist").invoke("").content,
            'get_specialty_context': lambda self: "You are a Pathologist with expertise in pathologist analysis."
        })()
    
    return [oncologist, radiologist, pathologist]

def demo_mock_board():
    """Demonstrate the tumor board with mock responses"""
    print("Multi-Agent Tumor Board Emulation System - MOCK DEMO")
    print("=" * 60)
    print("This demo shows the system functionality without API calls")
    print("=" * 60)
    
    # Create sample case
    case = create_sample_case()
    
    # Create tumor board with mock agents
    board = TumorBoard()
    board.agents = create_mock_agents()
    
    # Run tumor board review
    print(f"\n{'='*60}")
    print(f"TUMOR BOARD REVIEW - Patient {case.patient_id}")
    print(f"{'='*60}")
    
    recommendations = {}
    
    # Collect recommendations from each agent
    for agent in board.agents:
        print(f"\n{agent.specialty} Analysis:")
        print(f"{'-'*40}")
        recommendation = agent.analyze_case(case)
        recommendations[agent.specialty] = recommendation
        print(f"Recommendation: {recommendation}")
    
    # Generate mock board decision
    print(f"\n{'='*60}")
    print("FINAL BOARD DECISION")
    print(f"{'='*60}")
    
    board_decision = """
BOARD DECISION - Patient CASE-2024-001

CONSOLIDATED TREATMENT PLAN:
Based on the multidisciplinary review, this patient presents with T2N1M0 invasive ductal carcinoma, luminal A subtype. The board recommends a comprehensive treatment approach combining systemic therapy, surgery, and radiation.

PRIORITY ACTIONS:
1. Immediate: Schedule neoadjuvant chemotherapy (AC-T regimen, 4-6 cycles)
2. Surgical planning: Modified radical mastectomy with axillary lymph node dissection
3. Post-operative: Adjuvant radiation therapy to chest wall and regional nodes

FOLLOW-UP RECOMMENDATIONS:
- Monthly clinical assessments during chemotherapy
- Post-surgery pathology review for treatment response assessment
- Long-term endocrine therapy with aromatase inhibitor
- Regular surveillance imaging and clinical follow-up

This approach addresses both local and systemic disease control while optimizing long-term outcomes.
"""
    
    print(board_decision)
    
    print(f"{'='*60}")
    print("MOCK SIMULATION COMPLETE")
    print(f"{'='*60}")
    
    return recommendations

def main():
    """Main function to run the mock demo"""
    try:
        # Run mock tumor board
        results = demo_mock_board()
        
        print("\nSummary of Agent Recommendations:")
        for specialty, recommendation in results.items():
            print(f"\n{specialty}:")
            print(f"  {recommendation[:100]}...")
        
        print(f"\nTotal Recommendations Generated: {len(results)}")
        
    except Exception as e:
        print(f"❌ Error running mock demo: {str(e)}")

if __name__ == "__main__":
    main()
