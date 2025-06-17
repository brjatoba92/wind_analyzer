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
