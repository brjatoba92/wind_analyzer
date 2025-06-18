# 🌬️ WindAnalyzer - Analisador Avançado de Padrões de Vento

O **WindAnalyzer** é uma ferramenta robusta desenvolvida em Python para análise estatística, visual e técnica de dados de vento. Permite desde o cálculo de estatísticas descritivas até a geração de rosas dos ventos, ajuste de distribuição de Weibull e estimativa de potencial eólico — sendo útil para estudos climáticos, energéticos e ambientais.

---

## 🚀 Funcionalidades

- ✅ Pré-processamento de dados de vento (limpeza e normalização)
- 📊 Estatísticas descritivas de direção e velocidade
- 🌪️ Cálculo da turbulência e calmaria
- 📈 Ajuste de distribuição Weibull por setores
- ⚡ Estimativa de potencial eólico teórico (em W/m²)
- 🌐 Geração de rosas dos ventos com codificação de cores por velocidade
- 📄 Geração automática de relatórios técnicos (texto)
- 🏙️ Análise de cisalhamento vertical do vento

---

## 🧠 Tecnologias Utilizadas

- Python
- pandas, numpy
- matplotlib, seaborn
- scipy.stats para ajuste de distribuições
- Estilo visual com colormap **viridis**

---

## 📁 Organização do Projeto

```
resultados/
├── graficos/         # Imagens geradas da rosa dos ventos
├── estatisticas/     # Arquivos .txt com estatísticas descritivas
├── relatorios/       # Relatórios técnicos completos por estação
└── cissalhamento/    # Resultados da análise de cisalhamento vertical
```

---

## 📌 Estrutura dos Dados Esperada

O DataFrame de entrada deve conter as seguintes colunas:

| Coluna     | Tipo      | Descrição                                         |
|------------|-----------|---------------------------------------------------|
| estacao    | str       | Nome da estação meteorológica                      |
| data       | datetime  | Data/hora da medição                               |
| direcao    | float     | Direção do vento em graus (0 a 360)                |
| velocidade | float     | Velocidade do vento em m/s                         |
| altura     | float     | (Opcional) Altura da medição para cisalhamento     |

## 📦 Como Usar

### Clone o repositório:

    git clone https://github.com/brjatoba92/wind_analyzer.git
    cd wind_analyzer

### Instale as dependências:

    pip install -r requirements.txt

### Execute o script principal:

    python3 windPattern_roseWind.py

## 📊 Exemplo de Saída

### Estatísticas:
    media_velocidade: 6.52
    max_velocidade: 17.93
    ...

### Rosa dos ventos:

Relatório Técnico:

    RELATÓRIO TÉCNICO - ANÁLISE EÓLICA
    Estação: Estacao_A
    Período: 2023-01-01 a 2023-02-11
    ...
    Potencial teórico: 342.89 W/m²
    Classificação de vento: Bom (Classe 5)


## 📈 Aplicações Possíveis

    Avaliação de locais para usinas eólicas

    Estudos climáticos e energéticos

    Pesquisa científica em meteorologia e física ambiental

## 🧪 Testes com Dados Sintéticos

    O script já contém um gerador de dados de exemplo baseado em distribuição Weibull e von Mises. 
    Isso permite testar a aplicação sem necessidade de dados reais iniciais.

## ✅ TODO Futuro

    Exportar gráficos diretamente em PDF para relatórios
    Interface web interativa com Dash ou Streamlit
    Integração com bancos de dados meteorológicos externos

## 👤 Autor

    Bruno Jatobá
    Email: brunojatobadev@gmail.com
    Meteorologista e Desenvolvedor Python

## 📄 Licença

    Este projeto está licenciado sob a Licença MIT.