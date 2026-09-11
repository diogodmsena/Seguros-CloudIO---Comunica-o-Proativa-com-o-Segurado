"""
Agente 1: Coletor de Dados Meteorológicos (Weather Collector Agent).
Responsável por consumir APIs externas públicas de meteorologia ou carregar cenários de teste.
"""

from typing import Optional, Dict, Any, List
from src.agents.base_agent import BaseAgent
from src.services.weather_service import WeatherService
from src.models import EventoClimatico


class WeatherCollectorAgent(BaseAgent):
    """Agente especialista em obtenção e normalização de dados meteorológicos."""

    def __init__(self, weather_service: Optional[WeatherService] = None):
        super().__init__(
            nome="Agente Coletor Meteorológico",
            papel="Engenheiro de Dados Climáticos",
            objetivo="Consultar fontes externas de dados meteorológicos e normalizar leituras em tempo real ou simuladas."
        )
        self.weather_service = weather_service or WeatherService()

    def coletar_por_cenario(self, cenario_id: str) -> EventoClimatico:
        """Obtém dados meteorológicos a partir de um cenário simulado didático."""
        self.registrar_passo(f"Coletando dados do cenário simulado ID: '{cenario_id}'...")
        evento = self.weather_service.obter_cenario_por_id(cenario_id)
        if not evento:
            raise ValueError(f"Cenário com ID '{cenario_id}' não encontrado.")
        self.registrar_passo(f"Dados obtidos para {evento.cidade} - {evento.estado}: Precipitação={evento.precipitacao_mm}mm, Rajadas={evento.rajada_vento_kmh}km/h, Granizo={evento.probabilidade_granizo_pct}%.")
        return evento

    def coletar_por_cidade(self, nome_cidade: str) -> EventoClimatico:
        """Busca a localização e consulta a API pública Open-Meteo em tempo real."""
        self.registrar_passo(f"Buscando coordenadas para a cidade: '{nome_cidade}'...")
        geo = self.weather_service.buscar_coordenadas_cidade(nome_cidade)
        if not geo:
            self.registrar_passo(f"Cidade '{nome_cidade}' não localizada no geocoding. Usando coordenadas padrão de São Paulo.")
            lat, lon, cid, est = -23.5505, -46.6333, nome_cidade, "SP"
        else:
            lat, lon, cid, est = geo["lat"], geo["lon"], geo["cidade"], geo.get("estado", "")

        self.registrar_passo(f"Consultando API pública Open-Meteo para {cid} ({lat:.4f}, {lon:.4f})...")
        evento = self.weather_service.consultar_clima_tempo_real(latitude=lat, longitude=lon, cidade=cid, estado=est)
        self.registrar_passo(f"Leitura em tempo real concluída: Temp={evento.temperatura_c}°C, Precipitação={evento.precipitacao_mm}mm, Vento={evento.velocidade_vento_kmh}km/h.")
        return evento

    def listar_cenarios_disponiveis(self) -> List[Dict[str, Any]]:
        """Lista todos os cenários simulados disponíveis para seleção rápida."""
        return self.weather_service.carregar_cenarios_simulados()

    def executar(self, modo: str = "cenario", identificador: str = "CENARIO-01") -> EventoClimatico:
        """Executa a coleta conforme o modo escolhido ('cenario' ou 'tempo_real')."""
        if modo == "tempo_real":
            return self.coletar_por_cidade(identificador)
        else:
            return self.coletar_por_cenario(identificador)
