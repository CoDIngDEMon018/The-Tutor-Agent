import google.generativeai as genai
from typing import List, Dict
import re
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class BiologyAgent:
    def __init__(self, api_key: str):
        """Initialize the Biology Agent with Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.terminology_db = TerminologyTool()
        self.diagram_generator = DiagramGenerator()

    def process_question(self, question: str) -> str:
        """Main method to process biology questions"""
        try:
            response_parts = []
            
            # Check for terminology queries
            terms = self._detect_terminology(question)
            if terms:
                for term in terms:
                    term_info = self.terminology_db.lookup(term)
                    if term_info:
                        response_parts.append(f"📚 **{term}**: {term_info}")
            
            # Check for diagram requests
            if self._needs_diagram(question):
                diagram = self.diagram_generator.generate(question)
                if diagram:
                    response_parts.append(diagram)
            
            # Generate explanation
            explanation = self._get_explanation(question)
            response_parts.append(explanation)
            
            return "\n\n".join(response_parts)
            
        except Exception as e:
            return f"Biology error: {str(e)}"

    def _detect_terminology(self, question: str) -> List[str]:
        """Identify biological terms in the question"""
        biology_keywords = {
            'cell', 'dna', 'rna', 'mitosis', 'meiosis', 'photosynthesis',
            'respiration', 'ecosystem', 'biome', 'enzyme', 'protein',
            'evolution', 'taxonomy', 'genetics', 'chromosome', 'mutation'
        }
        return [word for word in question.lower().split() 
                if word in biology_keywords]

    def _needs_diagram(self, question: str) -> bool:
        """Determine if the question requires a diagram"""
        diagram_triggers = {
            'diagram', 'illustrate', 'show', 'process', 'steps',
            'structure of', 'cycle', 'flow chart'
        }
        return any(trigger in question.lower() 
                  for trigger in diagram_triggers)

    def _get_explanation(self, question: str) -> str:
        """Get Gemini-generated explanation"""
        prompt = f"""As a biology tutor, explain this concept: {question}
        
        Include:
        - Key biological principles involved
        - Relevant scientific terminology
        - Real-world examples
        - Common misconceptions to avoid
        
        Keep explanations under 200 words."""
        
        response = self.model.generate_content(prompt)
        return response.text

class TerminologyTool:
    """Biology terminology database and lookup tool"""
    
    def __init__(self):
        self.terminology = {
            'photosynthesis': {
                'definition': 'Process by which plants convert light energy to chemical energy',
                'equation': '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂',
                'key_components': ['Chlorophyll', 'Chloroplast', 'Light reactions', 'Calvin cycle']
            },
            'mitosis': {
                'definition': 'Cell division process resulting in two genetically identical daughter cells',
                'stages': ['Prophase', 'Metaphase', 'Anaphase', 'Telophase'],
                'purpose': 'Growth and repair of organisms'
            }
            # Add more terms as needed
        }

    def lookup(self, term: str) -> str:
        """Look up biological terminology"""
        term_data = self.terminology.get(term.lower())
        if not term_data:
            return None
            
        info = [f"**{term.capitalize()}**"]
        info.append(f"Definition: {term_data['definition']}")
        
        if 'equation' in term_data:
            info.append(f"Chemical equation: {term_data['equation']}")
            
        if 'stages' in term_data:
            info.append("Stages: " + " → ".join(term_data['stages']))
            
        return "\n".join(info)

class DiagramGenerator:
    """Generates biological diagrams and processes"""
    
    def generate(self, concept: str) -> str:
        """Generate a diagram description or ASCII art"""
        concept = concept.lower()
        
        if 'photosynthesis' in concept:
            return self._photosynthesis_diagram()
        elif 'cell' in concept:
            return self._cell_structure_diagram()
        elif 'dna' in concept:
            return self._dna_structure_diagram()
            
        return "Diagram unavailable for this concept"

    def _photosynthesis_diagram(self) -> str:
        """Generate photosynthesis diagram description"""
        return """
        🌿 Photosynthesis Process:
        1. [Light Absorption] Chlorophyll in chloroplasts absorbs sunlight
        2. [Water Splitting] H₂O → 2H⁺ + ½O₂ + electrons
        3. [ATP Production] Light energy → ATP
        4. [Carbon Fixation] CO₂ + ATP → Glucose (C₆H₁₂O₆)
        """

    def _cell_structure_diagram(self) -> str:
        """Generate cell structure description"""
        return """
        🧫 Animal Cell Structure:
        - Cell Membrane: Semi-permeable boundary
        - Nucleus: Contains DNA
        - Mitochondria: Powerhouse of cell
        - Ribosomes: Protein synthesis
        - Endoplasmic Reticulum: Transport system
        """

    def _dna_structure_diagram(self) -> str:
        """Generate DNA structure description"""
        return """
        🧬 DNA Structure:
        - Double helix structure
        - Sugar-phosphate backbone
        - Base pairs: A-T, C-G
        - Nucleotide components:
          • Phosphate
          • Deoxyribose sugar
          • Nitrogenous base
        """ 