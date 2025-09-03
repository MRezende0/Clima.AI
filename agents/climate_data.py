"""
Agente responsável por buscar dados climáticos
"""
from typing import Dict, Any, List, Optional
from config import Config
import requests
from datetime import datetime

class ClimateDataAgent:
    """Agente para buscar dados climáticos"""
    
    def __init__(self):
        self.config = Config
    
    def get_daily_climate(self, station_id: int) -> List[Dict[str, Any]]:
        """Busca dados climáticos por dia"""
        try:
            response = requests.get(
                f"{self.config.ICROP_BASE_URL}/clima_por_dia/{station_id}",
                headers={"Authorization": f"Bearer {self.config.ICROP_API_KEY}"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Erro ao buscar clima por dia: {str(e)}")
    
    def get_hourly_climate(self, station_id: int) -> List[Dict[str, Any]]:
        """Busca dados climáticos por hora"""
        try:
            response = requests.get(
                f"{self.config.ICROP_BASE_URL}/clima_por_hora/{station_id}",
                headers={"Authorization": f"Bearer {self.config.ICROP_API_KEY}"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Erro ao buscar clima por hora: {str(e)}")
    
    def get_forecast(self, station_id: int) -> List[Dict[str, Any]]:
        """Busca previsões do tempo"""
        try:
            response = requests.get(
                f"{self.config.ICROP_BASE_URL}/previsao/{station_id}",
                headers={"Authorization": f"Bearer {self.config.ICROP_API_KEY}"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Erro ao buscar previsão: {str(e)}")
    
    def get_data_by_request(self, request_data: Dict[str, Any], station: Dict[str, Any]) -> str:
        """
        Busca dados baseado no JSON estruturado do pedido
        
        Args:
            request_data: JSON com dados do pedido
            station: Dados da estação encontrada
            
        Returns:
            str: Resposta formatada
        """
        try:
            data_type = request_data['data_type']['primary']
            
            if data_type == 'temperature':
                return self.get_current_temperature(station)
            elif data_type == 'climate':
                return self.get_current_climate_data(station)
            elif data_type == 'forecast':
                return self.get_forecast_data(station)
            elif data_type == 'hourly':
                return self.get_hourly_data(station)
            elif data_type == 'humidity':
                return self.get_specific_data(station, 'humidity')
            elif data_type == 'rain':
                return self.get_specific_data(station, 'rain')
            elif data_type == 'wind':
                return self.get_specific_data(station, 'wind')
            elif data_type == 'radiation':
                return self.get_specific_data(station, 'radiation')
            else:
                return self.get_current_climate_data(station)
                
        except Exception as e:
            return f"❌ Erro ao buscar dados: {str(e)}"
    
    def get_specific_data(self, station: Dict[str, Any], data_type: str) -> str:
        """Busca dados específicos (umidade, chuva, vento, radiação)"""
        try:
            # Primeiro tentar dados por hora (mais atuais)
            try:
                dados_hora = self.get_hourly_climate(station['id'])
                if dados_hora:
                    # Buscar a medição mais recente (não 00:00:00)
                    dados_ultimos = self._get_most_recent_data(dados_hora)
                    return self._format_specific_data(station, dados_ultimos, data_type)
            except:
                pass
            
            # Se não conseguiu dados por hora, usar dados diários
            dados_dia = self.get_daily_climate(station['id'])
            if not dados_dia:
                return f"❌ Nenhum dado de {data_type} disponível para esta estação."
            
            dados_ultimos = dados_dia[0]
            return self._format_specific_data(station, dados_ultimos, data_type)
            
        except Exception as e:
            return f"❌ Erro ao buscar {data_type}: {str(e)}"
    
    def _get_most_recent_data(self, dados_hora: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Busca a medição mais recente (não 00:00:00)"""
        # Filtrar dados que não são 00:00:00
        dados_filtrados = []
        for dado in dados_hora:
            if 'datahora' in dado:
                hora = dado['datahora'].split(' ')[1] if ' ' in dado['datahora'] else dado['datahora']
                if hora != '00:00:00':
                    dados_filtrados.append(dado)
        
        # Se encontrou dados filtrados, retornar o mais recente
        if dados_filtrados:
            return dados_filtrados[0]  # Primeiro item é o mais recente
        
        # Se não encontrou, retornar o primeiro dado original
        return dados_hora[0]
    
    def _format_specific_data(self, station: Dict[str, Any], dados: Dict[str, Any], data_type: str) -> str:
        """Formata dados específicos"""
        data_labels = {
            'humidity': ('Umidade', 'umidade', '%'),
            'rain': ('Chuva', 'chuva', 'mm'),
            'wind': ('Vento', 'vento', 'km/h'),
            'radiation': ('Radiação', 'radiacao', 'W/m²')
        }
        
        label, key, unit = data_labels.get(data_type, ('Dados', 'dados', ''))
        
        if 'datahora' in dados:
            return f"📊 **{label} atual em {station['nome']}:**\n\n" + \
                   f"📅 **{dados['datahora']}**\n" + \
                   f"📊 **{label}:** {dados[key]} {unit}"
        else:
            return f"📊 **{label} atual em {station['nome']}:**\n\n" + \
                   f"📅 **{dados['data']}**\n" + \
                   f"📊 **{label}:** {dados[key]} {unit}"
    
    def get_current_temperature(self, station: Dict[str, Any]) -> str:
        """Busca apenas a temperatura atual (formato limpo)"""
        try:
            # Primeiro tentar dados por hora (mais atuais)
            try:
                dados_hora = self.get_hourly_climate(station['id'])
                if dados_hora:
                    # Buscar a medição mais recente (não 00:00:00)
                    dados_ultimos = self._get_most_recent_data(dados_hora)
                    return f"🌡️ **Temperatura atual em {station['nome']}:**\n\n" + \
                           f"📅 **{dados_ultimos['datahora']}**\n" + \
                           f"🌡️ **{dados_ultimos['temp_min']}°C - {dados_ultimos['temp_max']}°C** (média: {dados_ultimos['temp_med']}°C)"
            except:
                pass
            
            # Se não conseguiu dados por hora, usar dados diários
            dados_dia = self.get_daily_climate(station['id'])
            if not dados_dia:
                return "❌ Nenhum dado de temperatura disponível para esta estação."
            
            dados_ultimos = dados_dia[0]  # Dados mais recentes
            return f"🌡️ **Temperatura atual em {station['nome']}:**\n\n" + \
                   f"📅 **{dados_ultimos['data']}**\n" + \
                   f"🌡️ **{dados_ultimos['temp_min']}°C - {dados_ultimos['temp_max']}°C** (média: {dados_ultimos['temp_med']}°C)"
        except Exception as e:
            return f"❌ Erro ao buscar temperatura: {str(e)}"
    
    def get_current_climate_data(self, station: Dict[str, Any]) -> str:
        """Busca e formata dados climáticos atuais (SEMPRE o mais recente)"""
        try:
            # Primeiro tentar dados por hora (mais atuais)
            try:
                dados_hora = self.get_hourly_climate(station['id'])
                if dados_hora:
                    # Buscar a medição mais recente (não 00:00:00)
                    dados_ultimos = self._get_most_recent_data(dados_hora)
                    return f"🌤️ **Dados climáticos de {station['nome']}:**\n\n" + \
                           f"📅 **{dados_ultimos['datahora']}**\n" + \
                           f"🌡️ **Temperatura:** {dados_ultimos['temp_min']}°C - {dados_ultimos['temp_max']}°C (média: {dados_ultimos['temp_med']}°C)\n" + \
                           f"💧 **Umidade:** {dados_ultimos['umidade']}%\n" + \
                           f"🌧️ **Chuva:** {dados_ultimos['chuva']}mm\n" + \
                           f"💨 **Vento:** {dados_ultimos['vento']} km/h\n" + \
                           f"☀️ **Radiação:** {dados_ultimos['radiacao']} W/m²"
            except:
                pass
            
            # Se não conseguiu dados por hora, usar dados diários
            dados_dia = self.get_daily_climate(station['id'])
            if not dados_dia:
                return "❌ Nenhum dado climático disponível para esta estação."
            
            dados_ultimos = dados_dia[0]  # Dados mais recentes
            return f"🌤️ **Dados climáticos de {station['nome']}:**\n\n" + \
                   f"📅 **{dados_ultimos['data']}**\n" + \
                   f"🌡️ **Temperatura:** {dados_ultimos['temp_min']}°C - {dados_ultimos['temp_max']}°C (média: {dados_ultimos['temp_med']}°C)\n" + \
                   f"💧 **Umidade:** {dados_ultimos['umidade']}%\n" + \
                   f"🌧️ **Chuva:** {dados_ultimos['chuva']}mm\n" + \
                   f"💨 **Vento:** {dados_ultimos['vento']} km/h\n" + \
                   f"☀️ **Radiação:** {dados_ultimos['radiacao']} W/m²"
        except Exception as e:
            return f"❌ Erro ao buscar dados climáticos: {str(e)}"
    
    def get_forecast_data(self, station: Dict[str, Any]) -> str:
        """Busca e formata previsões do tempo"""
        try:
            previsao = self.get_forecast(station['id'])
            if not previsao:
                return "❌ Nenhuma previsão disponível para esta estação."
            
            resposta = f"🔮 **Previsão do tempo para {station['nome']}:**\n\n"
            resposta += "📅 **Próximos dias:**\n"
            for p in previsao[:5]:  # Mostrar próximos 5 dias
                resposta += f"• **{p['data']}**: {p['temp_min']}°C - {p['temp_max']}°C\n"
                resposta += f"  🌧️ Chuva: {p['rain_prob']}% ({p['rain_total']}mm)\n"
                resposta += f"  💨 Vento: {p['wind_spd']} km/h\n"
                resposta += f"  ☁️ Observação: {p['obs']}\n\n"
            return resposta
        except Exception as e:
            return f"❌ Erro ao buscar previsão: {str(e)}"
    
    def get_hourly_data(self, station: Dict[str, Any]) -> str:
        """Busca e formata dados por hora"""
        try:
            dados_hora = self.get_hourly_climate(station['id'])
            if not dados_hora:
                return "❌ Nenhum dado por hora disponível para esta estação."
            
            resposta = f"⏰ **Dados climáticos por hora de {station['nome']}:**\n\n"
            for d in dados_hora[:5]:  # Mostrar últimas 5 medições
                resposta += f"• **{d['datahora']}**: {d['temp_med']}°C, {d['umidade']}% umidade, {d['vento']} km/h vento\n"
            return resposta
        except Exception as e:
            return f"❌ Erro ao buscar dados por hora: {str(e)}"
