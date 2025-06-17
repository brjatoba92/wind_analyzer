# Dependencias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.projections import PolarAxes
import mpl_toolkits.axisartist.grid_finder as gf
import mpl_toolkits.axisartist.floating_axes as fa
from scipy.stats import weibull_min
from typing import Dict, List, Optional, Tuple

class WindAnalyzer:
    """
    Classe para análise avançada de padrões de vento e geração de rosas dos ventos.
    
    Atributos:
        dados (pd.DataFrame): DataFrame contendo os dados de vento
        estacoes (List[str]): Lista de estações disponíveis nos dados
        parametros_weibull (Dict): Dicionário com parâmetros de Weibull calculados
    """
    def __init__(self, dados: pd.DataFrame):
        """
        Inicializa o analisador com os dados de vento.
        
        Args:
            dados (pd.DataFrame): DataFrame com colunas:
                - 'estacao': nome da estação
                - 'data': timestamp da medição
                - 'direcao': direção do vento em graus (0-360)
                - 'velocidade': velocidade do vento em m/s
        """
        self.dados = dados.copy()
        self.estacoes = self.dados['estacao'].unique().tolist()
        self.parametros_weibull = {}

        # Pré-processamento
        self._preprocess_data()
    
    def _preprocess_data(self) -> None:
        """Realiza pré-processamento dos dados (limpeza, normalização)."""
        # Remover valores nulos
        self.dados.dropna(subset=['direcao', 'velocidade'], inplace=True)

        # Garantir que a direção está entre 0-360
        self.dados['direcao'] = self.dados['direcao'] % 360

        # Garantir que a velocidade seja maior ou igual a zero
        self.dados = self.dados[self.dados['velocidade'] >= 0]
    
    def calcular_estatisticas(self, estacao: str = None) -> Dict:
        """
        Calcula estatísticas descritivas para os dados de vento.
        
        Args:
            estacao (str): Nome da estação para filtrar (None para todas)
            
        Returns:
            Dict: Dicionário com estatísticas calculadas
        """
        dados = self.dados if estacao is None else self.dados[self.dados['estacao'] == estacao]

        estatisticas = {
            'media_velocidade': dados['velocidade'].mean(),
            'max_velocidade': dados['velocidade'].max(),
            'min_velocidade': dados['velocidade'].min(),
            'desvio_velocidade': dados['velocidade'].std(),
            'media_direcao': self._calcular_direcao_media(dados['direcao']),
            'frequencia_calmar': (dados['velocidade'] < 0.5).mean(),
            'turbulencia': dados['velocidade'].std() /  dados['velocidade'].mean()
        }

        return estatisticas
    
    def _calcular_direcao_media(self, direcoes: pd.Series) -> float:
        """
        Calcula a direção média considerando a circularidade dos dados.
        
        Args:
            direcoes (pd.Series): Série com direções em graus
            
        Returns:
            float: Direção média em graus (0-360)
        """
        radianos = np.deg2rad(direcoes)
        media_sen = np.sin(radianos).mean()
        media_cos = np.cos(radianos).mean()
        media_rad = np.arctan2(media_sen, media_cos)
        return (np.rad2deg(media_rad) + 360) % 360
