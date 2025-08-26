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
        self.last_prompt = ""  # Store the last prompt sent
        
    @abstractmethod
    def analyze_case(self, case: PatientCase) -> str:
        """Analyze the patient case and provide recommendations"""
        pass
    
    def get_specialty_context(self) -> str:
        """Get specialty-specific context for the agent"""
        return f"You are a {self.specialty} with expertise in {self.specialty.lower()} analysis."
    
    def get_last_prompt(self) -> str:
        """Get the last prompt sent to this agent (for debug purposes)"""
        return self.last_prompt


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
        
        # Store the prompt for debug purposes
        self.last_prompt = prompt
        
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
        
        # Store the prompt for debug purposes
        self.last_prompt = prompt
        
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
        
        # Store the prompt for debug purposes
        self.last_prompt = prompt
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error in pathologist analysis: {str(e)}"


class TumorBoard:
    """Tumor board that coordinates multiple medical agents"""
    
    def __init__(self, debug_mode=False):
        self.agents = [
            Oncologist(),
            Radiologist(),
            Pathologist()
        ]
        self.debug_mode = debug_mode
    
    def _display_case_summary(self, case: PatientCase):
        """Display a clear summary of the patient case being reviewed"""
        print(f"\n{'='*60}")
        print(f"PATIENT CASE SUMMARY - {case.patient_id}")
        print(f"{'='*60}")
        print(f"📋 Patient Demographics:")
        print(f"   • Age: {case.age} years old")
        print(f"   • Gender: {case.gender}")
        print(f"   • Tumor Size: {case.tumor_size} cm")
        print(f"   • Tumor Stage: {case.tumor_stage}")
        print(f"\n🔬 Clinical Findings:")
        print(f"   • Biopsy Result: {case.biopsy_result}")
        print(f"   • Imaging Result: {case.imaging_result}")
        print(f"\n💊 Symptoms: {', '.join(case.symptoms)}")
        print(f"📚 Medical History: {', '.join(case.medical_history)}")
        print(f"{'='*60}")
        
        print(f"\n🤔 QUESTIONS TO BE ANSWERED:")
        print(f"   • Oncologist: Treatment plan, chemotherapy/radiation, surgical options, prognosis")
        print(f"   • Radiologist: Imaging interpretation, tumor characteristics, metastasis assessment")
        print(f"   • Pathologist: Biopsy interpretation, tumor grading, molecular markers, staging")
        print(f"   • Board Chair: Consolidate all recommendations into final treatment decision")
        print(f"{'='*60}")
    
    def review_case(self, case: PatientCase) -> Dict[str, Any]:
        """Review a patient case with all agents"""
        # First display the case summary for clarity
        self._display_case_summary(case)
        
        print(f"\n{'='*60}")
        print(f"TUMOR BOARD REVIEW - Patient {case.patient_id}")
        print(f"{'='*60}")
        
        recommendations = {}
        
        # Collect recommendations from each agent
        for agent in self.agents:
            print(f"\n{agent.specialty} Analysis:")
            print(f"{'-'*40}")
            
            # Show what question is being asked to this agent
            print(f"🤔 Question for {agent.specialty}:")
            print(f"   Analyzing case and providing {agent.specialty.lower()} recommendations...")
            
            # If debug mode is enabled, show the actual prompt
            if self.debug_mode:
                print(f"\n🔍 DEBUG - Prompt sent to {agent.specialty}:")
                print(f"   {self._get_agent_prompt(agent, case)[:200]}...")
            
            recommendation = agent.analyze_case(case)
            recommendations[agent.specialty] = recommendation
            print(f"\n💡 Recommendation: {recommendation}")
        
        # Generate board decision
        print(f"\n{'='*40}")
        print("BOARD CHAIR DECISION")
        print(f"{'='*40}")
        print("🤔 Question for Board Chair:")
        print("   Consolidating all specialist recommendations into final treatment decision...")
        
        # If debug mode is enabled, show the actual prompt
        if self.debug_mode:
            print(f"\n🔍 DEBUG - Prompt sent to Board Chair:")
            print(f"   {self.get_last_board_prompt()[:200]}...")
        
        board_decision = self._generate_board_decision(recommendations)
        recommendations['board_decision'] = board_decision
        
        # If debug mode is enabled, show full prompts
        if self.debug_mode:
            self._display_full_prompts(case)
        
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
            
            # Store the prompt for debug purposes
            self.last_board_prompt = prompt
            
            # Use the first available agent's LLM for board decision
            llm = self.agents[0].llm
            response = llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            return f"Error generating board decision: {str(e)}"
    
    def get_last_board_prompt(self) -> str:
        """Get the last prompt sent to the board chair (for debug purposes)"""
        return getattr(self, 'last_board_prompt', 'No board prompt available')

    def _get_agent_prompt(self, agent: MedicalAgent, case: PatientCase) -> str:
        """Get the actual prompt being sent to an agent (for debug purposes)"""
        # This method extracts the prompt that would be sent to the agent
        # We'll need to modify the agent classes to expose their prompts
        if hasattr(agent, 'get_last_prompt'):
            return agent.get_last_prompt()
        else:
            return f"Prompt for {agent.specialty} analysis of case {case.patient_id}"

    def _display_full_prompts(self, case: PatientCase):
        """Display full prompts sent to each agent and the board chair (debug mode)"""
        print(f"\n{'='*60}")
        print("DEBUG MODE - FULL PROMPTS")
        print(f"{'='*60}")
        
        for agent in self.agents:
            print(f"\n📝 {agent.specialty} Full Prompt:")
            print(f"{'-'*50}")
            print(agent.get_last_prompt())
        
        print(f"\n📝 Board Chair Full Prompt:")
        print(f"{'-'*50}")
        print(self.get_last_board_prompt())


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
    
    # Check for debug mode argument
    import sys
    debug_mode = "--debug" in sys.argv or "-d" in sys.argv
    
    if debug_mode:
        print("🔍 Debug mode enabled - will show detailed prompts and analysis")
    
    try:
        # Initialize tumor board
        board = TumorBoard(debug_mode=debug_mode)
        
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
        print("SUMMARY OF QUESTIONS ANSWERED")
        print(f"{'='*60}")
        print(f"✅ Oncologist Question: Treatment recommendations provided")
        print(f"✅ Radiologist Question: Imaging insights provided")
        print(f"✅ Pathologist Question: Pathological analysis provided")
        print(f"✅ Board Chair Question: Final consolidated decision provided")
        
        print(f"\n{'='*60}")
        print("SIMULATION COMPLETE")
        print(f"{'='*60}")
        
        if not debug_mode:
            print("\n💡 Tip: Run with --debug flag to see detailed prompts:")
            print("   python board_emulation.py --debug")
        
    except Exception as e:
        print(f"❌ Error running simulation: {str(e)}")
        print("Please check your API key and internet connection")


if __name__ == "__main__":
    main()
