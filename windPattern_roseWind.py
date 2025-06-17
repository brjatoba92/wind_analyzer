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
    
    def ajuste_distribuicao_weibull(self, estacao: str, setores: int = 16) -> Dict:
        """
        Ajusta distribuição de Weibull para os dados de velocidade do vento.
        
        Args:
            estacao (str): Nome da estação para filtrar (None para todas)
            setores (int): Número de setores direcionais (default: 16)
            
        Returns:
            Dict: Parâmetros de Weibull (k, c) por setor direcional
        """
        dados = self.dados if estacao is None else self.dados[self.dados['estacao'] == estacao]
        
        # Calcular limites dos setores
        limites_setores = np.linspace(0, 360, setores + 1)

        parametros = ()
        for i in range(setores):
            limite_inf = limites_setores[i]
            limite_sup = limites_setores[i+1]
        
            # Filtrar dados do setor
            if i == setores - 1:
                mascara = (dados['direcao'] >= limite_inf) & (dados['direcao'] <= limite_sup)
            else:
                mascara = (dados['direcao'] >= limite_inf) & (dados['direcao'] < limite_sup)
        
            dados_setor = dados[mascara]['velocidade']

            # Ajustar Weibull se houver dados insuficientes
            if len(dados_setor) > 10:
                shape, loc, scale = weibull_min.fit(dados_setor, floc=0)
                parametros[f'setor_{i}'] =  {'k': shape, 'c': scale, 'frequencia': len(dados_setor)/len(dados)}
        
        # Armazenar parametros para uso posterior
        chave = estacao if estacao else 'global'
        self.parametros_weibull[chave] = parametros

        return parametros

    def calcular_potencial_eolico(self, estacao: str, densidade_ar: float = 1.225) -> float:
        """
        Calcula o potencial eólico teórico para uma estação.
        
        Args:
            estacao (str): Nome da estação
            densidade_ar (float): Densidade do ar em kg/m³ (default: 1.225)
            
        Returns:
            float: Potencial eólico em W/m²
        """
        if estacao not in self.parametros_weibull:
            self.ajustar_distribuicao_weibull(estacao)
        parametros = self.parametros_weibull[estacao]
        potencia_total = 0.0

        for setor, vals in parametros.items():
            k, c, freq = vals['k'], vals['c'], vals['frequencia']
            # Fator de correção para potência média
            potencia_media = 0.5 * densidade_ar * (c**3) * (1+3/k) * freq
            potencia_total += potencia_media
        
        return potencia_total

    def plotar_rosa_ventos(self, estacao: str = None, setores: int = 16, 
                        figsize: Tuple = (10,10), titulo: str = None) -> plt.Figure:
        """
        Gera uma rosa dos ventos polar para os dados.
        
        Args:
            estacao (str): Nome da estação para filtrar (None para todas)
            setores (int): Número de setores direcionais (default: 16)
            figsize (Tuple): Tamanho da figura (width, height)
            titulo (str): Título do gráfico
            
        Returns:
            plt.Figure: Figura matplotlib com a rosa dos ventos
        """
        dados = self.dados if estacao is None else self.dados[self.dados['estacao'] == estacao]

        #Calcular frequencias direcionais
        limites_setores = np.linspace(0, 360, setores + 1)
        direcoes_centro = (limites_setores[:,-1] + limites_setores[1:]) / 2
        frequencias, _ =  np.histogram(dados['direcao'], bins=limites_setores, density=True)

        # Calcular velocidades médias por setor
        velocidades_medias = []
        for i in range(setores):
            if i == setores - 1:
                mascara = (dados['direcao'] >= limites_setores[i]) & (dados['direcao'] <= limites_setores[i+1])
            else:
                mascara = (dados['direcao'] >= limites_setores[i]) & (dados['direcao'] < limites_setores[i+1])
            velocidades_medias.append(dados[mascara]['velocidade'].mean())
        
        # Configurar plot polar
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='polar')

        # Converter oara radianos
        theta = np.deg2rad(direcoes_centro)
        width = np.deg2rad(360 / setores)

        #Plotar barras com cores por velocidade
        bars = ax.bar(theta, frequencias * 100, width=width, bottom=0, 
                    color=plt.cm.viridis(np.array(velocidades_medias) / max(velocidades_medias)))

        # Personalizar gráficos
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_rlabel_position(0)
       
        # Adicionar titulo e legenda
        titulo = titulo or f"Rosa dos Ventos - {estacao if estacao else 'Todas Estações'}"
        plt.title(titulo, y=1.1)

        # Adicionar barra de cores para velocidade
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=min(velocidades_medias), vmax=max(velocidades_medias)))
        sm._A = []
        cbar = plt.colorbar(sm, ax=ax, pad=0.1)
        cbar.set_label("Velocidade (m/s)")

        return fig


    
