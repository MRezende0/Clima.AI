"""
Agente responsável por coletar e estruturar pedidos do usuário
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import re
from enum import Enum

class DataType(Enum):
    """Tipos de dados que podem ser solicitados"""
    TEMPERATURE = "temperature"
    CLIMATE = "climate"
    FORECAST = "forecast"
    HOURLY = "hourly"
    HUMIDITY = "humidity"
    RAIN = "rain"
    WIND = "wind"
    RADIATION = "radiation"

class RequestCollectorAgent:
    """Agente para coletar e estruturar pedidos do usuário"""
    
    def __init__(self):
        self.data_keywords = {
            DataType.TEMPERATURE: ['temperatura', 'temp', 'quente', 'frio', 'calor'],
            DataType.CLIMATE: ['clima', 'dados', 'condições', 'condicoes'],
            DataType.FORECAST: ['previsão', 'previsao', 'previsões', 'previsoes', 'futuro', 'amanhã', 'amanha'],
            DataType.HOURLY: ['hora', 'horário', 'horario', 'por hora'],
            DataType.HUMIDITY: ['umidade', 'úmido', 'umido'],
            DataType.RAIN: ['chuva', 'precipitação', 'precipitacao'],
            DataType.WIND: ['vento', 'ventoso'],
            DataType.RADIATION: ['radiação', 'radiacao', 'sol', 'solar']
        }
        
        self.station_keywords = [
            'estrela', 'narandiba', 'bradesco', 'são paulo', 'sao paulo', 'califórnia', 'california', 
            'porecatu', 'são cipriano', 'sao cipriano', 'miquelina', 'paraguaçu', 'paraguacu',
            'nadir', 'jubran', 'mosquito', 'mutum', 'tapirus', 'igrejinha', 'primavera', 'bartira',
            'retirinho', 'formosa', 'guarani', 'itaverá', 'itavera', 'são geraldo', 'sao geraldo',
            'lageado', 'rui terra', 'andreotti', 'lucinha', 'lagoa', 'lineu', 'edson borges'
        ]
    
    def collect_request(self, user_input: str, previous_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Coleta e estrutura o pedido do usuário em JSON com contexto
        
        Args:
            user_input: Entrada do usuário
            previous_context: Contexto da mensagem anterior
            
        Returns:
            Dict com dados estruturados do pedido
        """
        input_lower = user_input.lower()
        
        # Estrutura base do JSON
        request_data = {
            'station': {
                'name': None,
                'id': None,
                'found': False
            },
            'data_type': {
                'primary': None,
                'secondary': [],
                'specific': []
            },
            'datetime': {
                'date': None,
                'time': None,
                'is_specific': False,
                'is_current': True
            },
            'original_input': user_input,
            'processed': True,
            'needs_more_info': False,
            'friendly_message': ""
        }
        
        # 1. Identificar estação (com contexto)
        station_info = self._extract_station_with_context(input_lower, previous_context)
        request_data['station'] = station_info
        
        # 2. Identificar tipo de dados (com contexto)
        data_types = self._extract_data_types_with_context(input_lower, previous_context)
        request_data['data_type'] = data_types
        
        # 3. Identificar data e hora
        datetime_info = self._extract_datetime(input_lower)
        request_data['datetime'] = datetime_info
        
        # 4. Verificar se precisa de mais informações
        if not station_info['found'] and data_types['primary']:
            request_data['needs_more_info'] = True
            request_data['friendly_message'] = f"Perfeito! Você quer saber sobre **{data_types['primary']}**. De qual estação você gostaria de ver esses dados?"
        elif station_info['found'] and not data_types['primary']:
            request_data['needs_more_info'] = True
            station_display = station_info['name'] if station_info['name'] else f"ID {station_info['id']}"
            request_data['friendly_message'] = f"Ótimo! Você quer dados da estação **{station_display}**. Que tipo de informação você gostaria? (temperatura, clima, umidade, etc.)"
        elif not station_info['found'] and not data_types['primary']:
            request_data['needs_more_info'] = True
            request_data['friendly_message'] = "Claro! Posso ajudar você com dados climáticos. Que tipo de informação você gostaria e de qual estação?"
        
        return request_data
    
    def _extract_station_with_context(self, input_lower: str, previous_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extrai informações da estação com contexto"""
        station_info = {
            'name': None,
            'id': None,
            'found': False
        }
        
        # Buscar por ID
        id_match = re.search(r'id\s*(\d+)', input_lower)
        if id_match:
            station_info['id'] = int(id_match.group(1))
            station_info['found'] = True
            return station_info
        
        # Buscar por nome
        for keyword in self.station_keywords:
            if keyword in input_lower:
                station_info['name'] = keyword
                station_info['found'] = True
                return station_info
        
        # Se não encontrou e há contexto anterior, usar estação do contexto
        if previous_context and previous_context.get('station', {}).get('found'):
            station_info = previous_context['station'].copy()
        
        return station_info
    
    def _extract_data_types_with_context(self, input_lower: str, previous_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extrai tipos de dados com contexto"""
        data_types = {
            'primary': None,
            'secondary': [],
            'specific': []
        }
        
        # Identificar tipo primário
        for data_type, keywords in self.data_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                if data_types['primary'] is None:
                    data_types['primary'] = data_type.value
                else:
                    data_types['secondary'].append(data_type.value)
        
        # Se não encontrou e há contexto anterior, usar tipo do contexto
        if not data_types['primary'] and previous_context and previous_context.get('data_type', {}).get('primary'):
            data_types['primary'] = previous_context['data_type']['primary']
        
        # Se não encontrou tipo específico, assumir clima geral
        if data_types['primary'] is None:
            data_types['primary'] = DataType.CLIMATE.value
        
        # Identificar dados específicos
        if 'temperatura' in input_lower or 'temp' in input_lower:
            data_types['specific'].append('temperature')
        if 'umidade' in input_lower:
            data_types['specific'].append('humidity')
        if 'chuva' in input_lower:
            data_types['specific'].append('rain')
        if 'vento' in input_lower:
            data_types['specific'].append('wind')
        if 'radiação' in input_lower or 'radiacao' in input_lower:
            data_types['specific'].append('radiation')
        
        return data_types
    
    def _extract_datetime(self, input_lower: str) -> Dict[str, Any]:
        """Extrai informações de data e hora"""
        datetime_info = {
            'date': None,
            'time': None,
            'is_specific': False,
            'is_current': True
        }
        
        # Verificar se é uma data específica
        date_patterns = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # DD/MM/YYYY
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
            r'(\d{1,2})-(\d{1,2})-(\d{4})',  # DD-MM-YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, input_lower)
            if match:
                datetime_info['date'] = match.group(0)
                datetime_info['is_specific'] = True
                datetime_info['is_current'] = False
                break
        
        # Verificar se é um horário específico
        time_patterns = [
            r'(\d{1,2}):(\d{2})',  # HH:MM
            r'(\d{1,2})h',  # HHh
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, input_lower)
            if match:
                datetime_info['time'] = match.group(0)
                datetime_info['is_specific'] = True
                datetime_info['is_current'] = False
                break
        
        # Verificar palavras que indicam data específica
        specific_date_words = ['ontem', 'hoje', 'amanhã', 'amanha', 'semana', 'mês', 'mes']
        if any(word in input_lower for word in specific_date_words):
            datetime_info['is_specific'] = True
            datetime_info['is_current'] = False
        
        return datetime_info
    
    def get_request_summary(self, request_data: Dict[str, Any]) -> str:
        """Retorna um resumo legível do pedido coletado"""
        summary = "📋 **Resumo do Pedido:**\n\n"
        
        # Estação
        if request_data['station']['found']:
            if request_data['station']['id']:
                summary += f"📍 **Estação:** ID {request_data['station']['id']}\n"
            else:
                summary += f"📍 **Estação:** {request_data['station']['name']}\n"
        else:
            summary += f"📍 **Estação:** Não identificada\n"
        
        # Tipo de dados
        summary += f"📊 **Dados:** {request_data['data_type']['primary']}\n"
        if request_data['data_type']['secondary']:
            summary += f"📊 **Dados secundários:** {', '.join(request_data['data_type']['secondary'])}\n"
        if request_data['data_type']['specific']:
            summary += f"📊 **Específicos:** {', '.join(request_data['data_type']['specific'])}\n"
        
        # Data/Hora
        if request_data['datetime']['is_current']:
            summary += f"⏰ **Período:** Mais recente disponível\n"
        else:
            summary += f"⏰ **Período:** Específico\n"
            if request_data['datetime']['date']:
                summary += f"📅 **Data:** {request_data['datetime']['date']}\n"
            if request_data['datetime']['time']:
                summary += f"🕐 **Hora:** {request_data['datetime']['time']}\n"
        
        return summary
