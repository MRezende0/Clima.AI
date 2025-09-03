"""
Orquestrador principal que coordena todos os agentes
"""
from typing import Dict, Any, Optional
from agents.question_classifier import QuestionClassifierAgent, QuestionType
from agents.station_identifier import StationIdentifierAgent
from agents.climate_data import ClimateDataAgent
from agents.llm_analysis import LLMAnalysisAgent
from agents.request_collector import RequestCollectorAgent

class ClimateChatOrchestrator:
    """Orquestrador principal do sistema de chat climático"""
    
    def __init__(self):
        self.question_classifier = QuestionClassifierAgent()
        self.station_identifier = StationIdentifierAgent()
        self.climate_data = ClimateDataAgent()
        self.llm_analysis = LLMAnalysisAgent()
        self.request_collector = RequestCollectorAgent()
        self.previous_context = None  # Manter contexto entre mensagens
    
    def process_question(self, question: str) -> str:
        """
        Processa uma pergunta do usuário usando todos os agentes
        
        Args:
            question: Pergunta do usuário
            
        Returns:
            str: Resposta formatada
        """
        try:
            # Passo 1: Coletar e estruturar o pedido em JSON com contexto
            request_data = self.request_collector.collect_request(question, self.previous_context)
            
            # Passo 2: Verificar se é uma pergunta para listar estações
            if any(word in question.lower() for word in ['listar', 'todas', 'quais são', 'disponiveis', 'disponíveis']):
                try:
                    estacoes = self.station_identifier.get_all_stations()
                    return self.station_identifier._format_stations_list(estacoes)
                except Exception as e:
                    return f"Erro ao buscar estações: {str(e)}"
            
            # Passo 3: Se precisa de mais informações, retornar mensagem amigável
            if request_data['needs_more_info']:
                return request_data['friendly_message']
            
            # Passo 4: Identificar estação se necessário
            station = None
            station_message = ""
            
            if request_data['station']['found']:
                # Buscar estação por ID ou nome
                if request_data['station']['id']:
                    station = self._find_station_by_id(request_data['station']['id'])
                else:
                    station = self._find_station_by_name(request_data['station']['name'])
                
                if station:
                    station_message = f"✅ Identifiquei a estação: **{station['nome']}** (ID: {station['id']})"
                else:
                    return "❌ Não consegui encontrar a estação especificada."
            else:
                return "❌ Não consegui identificar qual estação você quer consultar. Por favor, especifique o nome ou ID da estação."
            
            # Passo 5: Buscar dados baseado no JSON estruturado
            if station:
                # Salvar contexto para próxima mensagem
                self.previous_context = request_data.copy()
                
                return f"{station_message}\n\n{self.climate_data.get_data_by_request(request_data, station)}"
            else:
                return station_message
                
        except Exception as e:
            return f"❌ Erro no processamento: {str(e)}"
    
    def _find_station_by_id(self, station_id: int) -> Optional[Dict[str, Any]]:
        """Busca estação por ID"""
        try:
            estacoes = self.station_identifier.get_all_stations()
            return next((e for e in estacoes if e['id'] == station_id), None)
        except:
            return None
    
    def _find_station_by_name(self, station_name: str) -> Optional[Dict[str, Any]]:
        """Busca estação por nome"""
        try:
            estacoes = self.station_identifier.get_all_stations()
            station_name_lower = station_name.lower()
            
            for estacao in estacoes:
                if station_name_lower in estacao['nome'].lower():
                    return estacao
            
            return None
        except:
            return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retorna o status do sistema"""
        try:
            # Testar conexão com APIs
            stations = self.station_identifier.get_all_stations()
            
            return {
                'status': 'operational',
                'stations_count': len(stations),
                'agents': {
                    'question_classifier': 'active',
                    'station_identifier': 'active',
                    'climate_data': 'active',
                    'llm_analysis': 'active',
                    'request_collector': 'active'
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'agents': {
                    'question_classifier': 'active',
                    'station_identifier': 'error',
                    'climate_data': 'error',
                    'llm_analysis': 'active',
                    'request_collector': 'active'
                }
            }
