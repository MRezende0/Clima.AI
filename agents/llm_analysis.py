"""
Agente responsável por análise e interpretação com LLM
"""
import json
from typing import Dict, Any, Optional
from config import Config
import requests

class LLMAnalysisAgent:
    """Agente para análise e interpretação com LLM"""
    
    def __init__(self):
        self.config = Config
    
    def analyze_with_context(self, question: str, climate_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Analisa a pergunta com contexto dos dados climáticos
        
        Args:
            question: Pergunta do usuário
            climate_data: Dados climáticos opcionais para contexto
        """
        headers = {
            "Authorization": f"Bearer {self.config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://clima.ai",
            "X-Title": "Clima.AI",
        }
        
        # Preparar o contexto
        system_prompt = self._build_system_prompt(climate_data)
        
        data = {
            "model": self.config.MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
        
        try:
            response = requests.post(
                self.config.OPENROUTER_URL, 
                headers=headers, 
                data=json.dumps(data)
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Erro na análise com LLM: {str(e)}"
    
    def _build_system_prompt(self, climate_data: Optional[Dict[str, Any]] = None) -> str:
        """Constrói o prompt do sistema"""
        base_prompt = """Você é um assistente especializado em análise climática. 
        Você tem acesso a dados meteorológicos da API iCrop e pode analisar informações sobre:
        - Estações meteorológicas
        - Dados climáticos por dia e hora
        - Previsões do tempo
        
        Sua função é:
        1. Analisar os dados climáticos fornecidos
        2. Interpretar tendências e padrões
        3. Fornecer insights úteis
        4. Responder de forma clara e informativa
        
        Sempre seja preciso e use os dados disponíveis para fundamentar suas respostas."""
        
        if climate_data:
            base_prompt += f"\n\nDados climáticos disponíveis: {json.dumps(climate_data, indent=2)}"
        
        return base_prompt
    
    def get_general_response(self, question: str) -> str:
        """Resposta geral para perguntas não específicas sobre clima"""
        return self.analyze_with_context(question)
