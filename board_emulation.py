#!/usr/bin/env python3
"""
Multi-Agent Board Emulation System for Cancer Case Collaboration

This script demonstrates a primitive simulation where 3 medical agents collaborate
on a cancer case board using Biomni framework and Gemini LLM.

How to run:
    python board_emulation.py

Requirements:
    - Set GEMINI_API_KEY environment variable with your Gemini API key
    - Install required packages: pip install langchain-openai google-generativeai

"""

import os
from typing import Dict, List, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Try to import Biomni components, fall back to simplified versions if not available
try:
    from biomni.llm import get_llm
    BIOMNI_AVAILABLE = True
except ImportError:
    BIOMNI_AVAILABLE = False
    print("Warning: Biomni not available, using simplified LLM wrapper")

# Fallback LLM wrapper if Biomni is not available
if not BIOMNI_AVAILABLE:
    try:
        import google.generativeai as genai
        from langchain_core.language_models.chat_models import BaseChatModel
        from langchain_core.messages import HumanMessage, AIMessage
        
        class SimpleGeminiWrapper:
            """Simple wrapper for Gemini if Biomni is not available"""
            
            def __init__(self, model_name="gemini-2.0-flash", temperature=0.7):
                self.model_name = model_name
                self.temperature = temperature
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("GEMINI_API_KEY environment variable not set")
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(model_name)
            
            def invoke(self, prompt: str) -> AIMessage:
                """Simple invoke method that returns AIMessage"""
                try:
                    response = self.model.generate_content(prompt)
                    return AIMessage(content=response.text)
                except Exception as e:
                    return AIMessage(content=f"Error: {str(e)}")
        
        def get_llm(model="gemini-1.5-flash", temperature=0.7, **kwargs):
            """Fallback get_llm function"""
            return SimpleGeminiWrapper(model, temperature)
            
    except ImportError:
        print("Error: Neither Biomni nor google-generativeai available")
        print("Please install required packages: pip install langchain-openai google-generativeai")
        exit(1)


@dataclass
class PatientCase:
    """Data structure for patient case information"""
    patient_id: str
    age: int
    gender: str
    tumor_size: float  # in cm
    tumor_stage: str   # e.g., "T2N0M0"
    biopsy_result: str
    imaging_result: str
    symptoms: List[str]
    medical_history: List[str]


class MedicalAgent(ABC):
    """Abstract base class for medical agents"""
    
    def __init__(self, name: str, specialty: str, llm_model: str = "gemini-1.5-flash"):
        self.name = name
        self.specialty = specialty
        self.llm = get_llm(llm_model, temperature=0.7, source="Gemini")
        
    @abstractmethod
    def analyze_case(self, case: PatientCase) -> str:
        """Analyze the patient case and provide recommendations"""
        pass
    
    def get_specialty_context(self) -> str:
        """Get specialty-specific context for the agent"""
        return f"You are a {self.specialty} with expertise in {self.specialty.lower()} analysis."


class Oncologist(MedicalAgent):
    """Oncologist agent specializing in tumor treatment plans"""
    
    def __init__(self):
        super().__init__("Dr. Smith", "Oncologist")
    
    def analyze_case(self, case: PatientCase) -> str:
        context = self.get_specialty_context()
        prompt = f"""
{context}

You are analyzing a cancer case for tumor board discussion. Please provide your treatment recommendations based on the following case:

Patient: {case.age} year old {case.gender}
Tumor Size: {case.tumor_size} cm
Stage: {case.tumor_stage}
Biopsy: {case.biopsy_result}
Imaging: {case.imaging_result}
Symptoms: {', '.join(case.symptoms)}
Medical History: {', '.join(case.medical_history)}

As an oncologist, focus on:
1. Treatment plan recommendations
2. Chemotherapy/radiation considerations
3. Surgical options
4. Prognosis assessment

Provide a concise, professional recommendation (2-3 sentences):
"""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error in oncologist analysis: {str(e)}"


class Radiologist(MedicalAgent):
    """Radiologist agent specializing in imaging insights"""
    
    def __init__(self):
        super().__init__("Dr. Johnson", "Radiologist")
    
    def analyze_case(self, case: PatientCase) -> str:
        context = self.get_specialty_context()
        prompt = f"""
{context}

You are analyzing a cancer case for tumor board discussion. Please provide your imaging insights based on the following case:

Patient: {case.age} year old {case.gender}
Tumor Size: {case.tumor_size} cm
Stage: {case.tumor_stage}
Biopsy: {case.biopsy_result}
Imaging: {case.imaging_result}
Symptoms: {', '.join(case.symptoms)}
Medical History: {', '.join(case.medical_history)}

As a radiologist, focus on:
1. Imaging interpretation
2. Tumor characteristics on imaging
3. Metastasis assessment
4. Additional imaging recommendations

Provide a concise, professional recommendation (2-3 sentences):
"""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error in radiologist analysis: {str(e)}"


class Pathologist(MedicalAgent):
    """Pathologist agent specializing in biopsy and tissue analysis"""
    
    def __init__(self):
        super().__init__("Dr. Williams", "Pathologist")
    
    def analyze_case(self, case: PatientCase) -> str:
        context = self.get_specialty_context()
        prompt = f"""
{context}

You are analyzing a cancer case for tumor board discussion. Please provide your pathological insights based on the following case:

Patient: {case.age} year old {case.gender}
Tumor Size: {case.tumor_size} cm
Stage: {case.tumor_stage}
Biopsy: {case.biopsy_result}
Imaging: {case.imaging_result}
Symptoms: {', '.join(case.symptoms)}
Medical History: {', '.join(case.medical_history)}

As a pathologist, focus on:
1. Biopsy interpretation
2. Tumor grading and classification
3. Molecular markers if available
4. Pathological staging confirmation

Provide a concise, professional recommendation (2-3 sentences):
"""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error in pathologist analysis: {str(e)}"


class TumorBoard:
    """Tumor board that coordinates multiple medical agents"""
    
    def __init__(self):
        self.agents = [
            Oncologist(),
            Radiologist(),
            Pathologist()
        ]
    
    def review_case(self, case: PatientCase) -> Dict[str, Any]:
        """Review a patient case with all agents"""
        print(f"\n{'='*60}")
        print(f"TUMOR BOARD REVIEW - Patient {case.patient_id}")
        print(f"{'='*60}")
        
        recommendations = {}
        
        # Collect recommendations from each agent
        for agent in self.agents:
            print(f"\n{agent.specialty} Analysis:")
            print(f"{'-'*40}")
            recommendation = agent.analyze_case(case)
            recommendations[agent.specialty] = recommendation
            print(f"Recommendation: {recommendation}")
        
        # Generate board decision
        board_decision = self._generate_board_decision(recommendations)
        recommendations['board_decision'] = board_decision
        
        return recommendations
    
    def _generate_board_decision(self, recommendations: Dict[str, str]) -> str:
        """Generate final board decision based on all recommendations"""
        try:
            prompt = f"""
You are the tumor board chairperson. Review the following specialist recommendations and provide a final, consolidated treatment decision.

Oncologist: {recommendations.get('Oncologist', 'No recommendation')}
Radiologist: {recommendations.get('Radiologist', 'No recommendation')}
Pathologist: {recommendations.get('Pathologist', 'No recommendation')}

As the board chair, provide:
1. A consolidated treatment plan (2-3 sentences)
2. Priority actions to take
3. Follow-up recommendations

Provide a concise, actionable final decision:
"""
            
            # Use the first available agent's LLM for board decision
            llm = self.agents[0].llm
            response = llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            return f"Error generating board decision: {str(e)}"


def create_sample_case() -> PatientCase:
    """Create a sample patient case for demonstration"""
    return PatientCase(
        patient_id="CASE-2024-001",
        age=58,
        gender="female",
        tumor_size=3.2,
        tumor_stage="T2N1M0",
        biopsy_result="Invasive ductal carcinoma, grade 2, ER+, PR+, HER2-",
        imaging_result="3.2 cm irregular mass in upper outer quadrant, suspicious lymph node in axilla",
        symptoms=["palpable breast mass", "mild discomfort", "no pain"],
        medical_history=["hypertension", "mild obesity", "no family history of breast cancer"]
    )


def main():
    """Main function to run the tumor board simulation"""
    print("🏥 Multi-Agent Tumor Board Emulation System")
    print("=" * 50)
    
    # Check API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("Please set your Gemini API key:")
        print("export GEMINI_API_KEY='your_api_key_here'")
        return
    
    try:
        # Initialize tumor board
        board = TumorBoard()
        
        # Create sample case
        case = create_sample_case()
        
        # Run tumor board review
        results = board.review_case(case)
        
        # Display final board decision
        print(f"\n{'='*60}")
        print("FINAL BOARD DECISION")
        print(f"{'='*60}")
        print(results['board_decision'])
        
        print(f"\n{'='*60}")
        print("SIMULATION COMPLETE")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"❌ Error running simulation: {str(e)}")
        print("Please check your API key and internet connection")


if __name__ == "__main__":
    main()
