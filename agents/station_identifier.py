"""
Agente responsável por identificar estações meteorológicas
"""
import re
from typing import Tuple, Optional, List, Dict, Any
from config import Config
import requests

class StationIdentifierAgent:
    """Agente para identificar estações meteorológicas"""
    
    def __init__(self):
        self.config = Config
    
    def get_all_stations(self) -> List[Dict[str, Any]]:
        """Busca todas as estações disponíveis"""
        try:
            response = requests.get(
                f"{self.config.ICROP_BASE_URL}/estacoes",
                headers={"Authorization": f"Bearer {self.config.ICROP_API_KEY}"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Erro ao buscar estações: {str(e)}")
    
    def identify_station(self, question: str) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Identifica qual estação o usuário quer consultar
        
        Returns:
            Tuple[Optional[Dict], str]: (estação_encontrada, mensagem_resposta)
        """
        question_lower = question.lower()
        
        # Se é uma pergunta sobre listar estações (mais específica)
        if any(word in question_lower for word in ['listar', 'todas', 'quais são', 'disponiveis', 'disponíveis']):
            try:
                estacoes = self.get_all_stations()
                return None, self._format_stations_list(estacoes)
            except Exception as e:
                return None, f"Erro ao buscar estações: {str(e)}"
        
        # Buscar estações para análise
        try:
            estacoes = self.get_all_stations()
        except Exception as e:
            return None, f"Erro ao buscar estações: {str(e)}"
        
        # Buscar por ID na pergunta
        station = self._find_by_id(question_lower, estacoes)
        if station:
            return station, f"✅ Identifiquei a estação: **{station['nome']}** (ID: {station['id']})"
        
        # Buscar por nome na pergunta (método melhorado)
        station = self._find_by_name_improved(question, estacoes)
        if station:
            return station, f"✅ Identifiquei a estação: **{station['nome']}** (ID: {station['id']})"
        
        # Se não encontrou nenhuma estação específica
        return None, "❌ Não consegui identificar qual estação você quer consultar. Por favor, especifique o nome ou ID da estação."
    
    def _find_by_id(self, question: str, estacoes: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Busca estação por ID"""
        id_match = re.search(r'id\s*(\d+)', question)
        if id_match:
            estacao_id = int(id_match.group(1))
            return next((e for e in estacoes if e['id'] == estacao_id), None)
        return None
    
    def _find_by_name_improved(self, question: str, estacoes: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Busca estação por nome com algoritmo melhorado"""
        question_lower = question.lower()
        palavras = question_lower.split()
        
        # Remover palavras comuns que não são nomes de estação
        stop_words = {'estação', 'estacao', 'da', 'de', 'em', 'na', 'no', 'temperatura', 'clima', 'atual', 'hoje', 'agora', 'quero', 'saber', 'qual', 'a', 'o', 'essa', 'essa', 'essa', 'com', 'id', 'usina', 'reg'}
        palavras_filtradas = [p for p in palavras if p not in stop_words and len(p) > 2]
        
        # Se não há palavras filtradas, tentar buscar por palavras únicas
        if not palavras_filtradas:
            # Buscar por palavras únicas que podem ser nomes de estação
            for palavra in palavras:
                if len(palavra) > 2 and palavra not in stop_words:
                    palavras_filtradas.append(palavra)
        
        # Buscar por palavras-chave nas estações
        for palavra in palavras_filtradas:
            for estacao in estacoes:
                nome_estacao_lower = estacao['nome'].lower()
                
                # Busca exata da palavra
                if palavra in nome_estacao_lower:
                    return estacao
                
                # Busca por similaridade (palavras que começam igual)
                if nome_estacao_lower.startswith(palavra) or palavra.startswith(nome_estacao_lower[:3]):
                    return estacao
        
        # Buscar por combinações de palavras
        for i in range(len(palavras_filtradas)):
            for j in range(i + 1, min(i + 3, len(palavras_filtradas) + 1)):
                combinacao = ' '.join(palavras_filtradas[i:j])
                for estacao in estacoes:
                    nome_estacao_lower = estacao['nome'].lower()
                    if combinacao in nome_estacao_lower:
                        return estacao
        
        # Buscar por palavras únicas que podem ser nomes de estação
        for palavra in palavras:
            if len(palavra) > 2:
                for estacao in estacoes:
                    nome_estacao_lower = estacao['nome'].lower()
                    # Busca mais flexível
                    if palavra in nome_estacao_lower or any(palavra in parte for parte in nome_estacao_lower.split()):
                        return estacao
        
        return None
    
    def _format_stations_list(self, estacoes: List[Dict[str, Any]]) -> str:
        """Formata lista de estações para exibição (simplificada)"""
        return f"Encontrei {len(estacoes)} estações meteorológicas:\n\n" + \
               "\n".join([f"• **{e['nome']}** (ID: {e['id']})" for e in estacoes])
