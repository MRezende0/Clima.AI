"""
Configurações do sistema
"""
import os

class Config:
    """Configurações do sistema"""
    
    # API iCrop
    ICROP_API_KEY = "f64ca436be34ea5a7c621facf63733b947260af56d3a3ab85c8ea3278a617225"
    ICROP_BASE_URL = "https://performance.icrop.online/homologacao/rest/v1/data"
    
    # API OpenRouter
    OPENROUTER_API_KEY = "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"
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    # Configurações do modelo
    MODEL_NAME = "deepseek/deepseek-chat-v3.1:free"
    
    @classmethod
    def validate(cls):
        """Valida se todas as configurações necessárias estão presentes"""
        required_vars = [
            'ICROP_API_KEY',
            'ICROP_BASE_URL', 
            'OPENROUTER_API_KEY',
            'OPENROUTER_URL'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            raise ValueError(f"Variáveis de ambiente ausentes: {missing_vars}")
        
        return True
