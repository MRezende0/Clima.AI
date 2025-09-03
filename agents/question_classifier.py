"""
Agente responsável por classificar o tipo de pergunta
"""
from typing import Dict, Any, Tuple
from enum import Enum

class QuestionType(Enum):
    """Tipos de perguntas possíveis"""
    LIST_STATIONS = "list_stations"
    CURRENT_CLIMATE = "current_climate"
    TEMPERATURE_ONLY = "temperature_only"
    FORECAST = "forecast"
    HOURLY_DATA = "hourly_data"
    GENERAL_ANALYSIS = "general_analysis"

class QuestionClassifierAgent:
    """Agente para classificar o tipo de pergunta"""
    
    def __init__(self):
        self.keywords = {
            QuestionType.LIST_STATIONS: [
                'estação', 'estações', 'estacoes', 'estacao', 'listar', 'todas', 'quais são', 'disponiveis', 'disponíveis'
            ],
            QuestionType.TEMPERATURE_ONLY: [
                'temperatura', 'temp', 'quente', 'frio', 'calor'
            ],
            QuestionType.CURRENT_CLIMATE: [
                'clima', 'umidade', 'chuva', 'vento', 'radiação', 'agora', 'hoje', 'atual'
            ],
            QuestionType.FORECAST: [
                'previsão', 'previsao', 'previsões', 'previsoes', 'futuro', 'amanhã', 'amanha', 'proximos', 'próximos'
            ],
            QuestionType.HOURLY_DATA: [
                'hora', 'horário', 'horario', 'por hora'
            ]
        }
    
    def classify_question(self, question: str) -> QuestionType:
        """
        Classifica o tipo de pergunta
        
        Args:
            question: Pergunta do usuário
            
        Returns:
            QuestionType: Tipo da pergunta
        """
        question_lower = question.lower()
        
        # Verificar se é uma pergunta sobre listar estações
        if any(keyword in question_lower for keyword in self.keywords[QuestionType.LIST_STATIONS]):
            return QuestionType.LIST_STATIONS
        
        # Verificar se é apenas sobre temperatura
        if any(keyword in question_lower for keyword in self.keywords[QuestionType.TEMPERATURE_ONLY]):
            return QuestionType.TEMPERATURE_ONLY
        
        # Verificar outros tipos de pergunta
        for question_type, keywords in self.keywords.items():
            if question_type not in [QuestionType.LIST_STATIONS, QuestionType.TEMPERATURE_ONLY]:
                if any(keyword in question_lower for keyword in keywords):
                    return question_type
        
        return QuestionType.GENERAL_ANALYSIS
    
    def get_question_info(self, question: str) -> Dict[str, Any]:
        """
        Retorna informações sobre a pergunta
        
        Args:
            question: Pergunta do usuário
            
        Returns:
            Dict com informações da pergunta
        """
        question_type = self.classify_question(question)
        
        return {
            'type': question_type,
            'original_question': question,
            'requires_station': question_type != QuestionType.LIST_STATIONS and question_type != QuestionType.GENERAL_ANALYSIS
        }
