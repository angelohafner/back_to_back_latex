
# ===================================================================================
# Functions needed for substitute poit by comma in decimal separators
# ===================================================================================
# Função para converter o valor de string para float, dependendo do locale
def parse_input(value_str, language_key):
    try:
        if language_key == 'en':
            return float(value_str)
        else:
            return float(value_str.replace('.', '').replace(',', '.'))
    except ValueError:
        return None

# Função para formatar o valor para exibição no input, conforme o locale
def format_input(value, language_key):
    if value is None:
        return ""
    if language_key == 'en':
        return f"{value:.1f}"
    else:
        return f"{value:.1f}".replace('.', ',')


def custom_slider(label, min_value, max_value, value, step, language_key):
    import streamlit as st
    # Exibindo o slider com o valor original (ponto como separador decimal)
    raw_value = st.slider(label, min_value, max_value, value, step=step)

    # Convertendo o valor para a string formatada com vírgula se necessário
    if language_key == 'en':
        formatted_value = raw_value
    else:
        formatted_value = float(format_input(raw_value, language_key))

    return formatted_value
# ===================================================================================
# ===================================================================================
# ===================================================================================
# ===================================================================================
# ===================================================================================
def substituir_valores(arquivo_copiado_tex, valores):
    with open(arquivo_copiado_tex, 'r', encoding='utf-8') as file:
        filedata = file.read()

    # Substitua os valores no arquivo
    for chave, valor in valores.items():
        filedata = filedata.replace(chave, valor)

    # Salve o arquivo novamente
    with open(arquivo_copiado_tex, 'w', encoding='utf-8') as file:
        file.write(filedata)
# ===================================================================================
# ===================================================================================
from docx import Document

def substituir_valores_docx(arquivo_docx, valores):
    # Carrega o documento Word
    doc = Document(arquivo_docx)
    
    # Percorre cada parágrafo no documento
    for para in doc.paragraphs:
        for chave, valor in valores.items():
            # Substitui as chaves pelos valores
            if '{{' + chave + '}}' in para.text:
                para.text = para.text.replace('{{' + chave + '}}', str(valor))
    
    # Salva o documento com as mudanças
    doc.save(arquivo_docx)
# ===================================================================================
# ===================================================================================
import numpy as np
import pandas as pd
from matplotlib.ticker import EngFormatter

def calcular_back_to_back(C, L, R_EQ_PARA_AMORTECIMENTO, V_fn, FC, I_fn, w_isolado, i_pico_inicial_isolado, nr_bancos,
                          Q_3f, Q_1f, V_ff, X, L_reator):

    i_pico_inicial_list = []
    sigma_list = []
    omega_list = []

    # Calculating Quantities
    for nn in range(2, len(C) + 1):
        C_paralelos = np.sum(C[1:nn])
        C_eq = 1 / (1 / C[0] + 1 / C_paralelos)

        L_paralelos = 1 / np.sum(1 / L[1:nn])
        L_eq = L[0] + L_paralelos

        raiz = -(R_EQ_PARA_AMORTECIMENTO / L_eq) ** 2 + 4 / (C_eq * L_eq)
        omega = np.sqrt(raiz) / 2
        omega_list.append(omega)

        i_pico_inicial = FC * V_fn * np.sqrt(2) / (L_eq * omega)
        i_pico_inicial_list.append(i_pico_inicial)

        sigma_list.append(R_EQ_PARA_AMORTECIMENTO / (2 * L_eq))

    # Converting Lists to NumPy Arrays and Adding Initial Values
    i_pico_inicaL_todos_pu = np.array([i_pico_inicial_isolado] + i_pico_inicial_list) / (I_fn * np.sqrt(2))
    omega_list_todos = np.array([w_isolado] + omega_list)

    # Selecting the Final Values from the List
    i_pico_inicial = i_pico_inicial_list[-1]
    sigma = sigma_list[-1]
    omega = omega_list[-1]

    # Setting the Time and Calculating the Short-Circuit Current
    t = np.linspace(0, 1 / 60, 1 * int(2 ** 12))
    i_curto = i_pico_inicial * np.exp(-sigma * t) * np.sin(omega * t)

    # Formatting the Data for the DataFrame
    formatter = EngFormatter(unit='VAr', places=1)
    arrayQ3f_eng = [formatter.format_data(x) for x in Q_3f]
    arrayQ1f_eng = [formatter.format_data(x) for x in Q_1f]
    formatter = EngFormatter(unit='V', places=1)
    arrayV3f_eng = [formatter.format_data(x) for x in V_ff * np.ones(nr_bancos)]
    arrayV1f_eng = [formatter.format_data(x) for x in V_fn * np.ones(nr_bancos)]
    formatter = EngFormatter(unit='A', places=1)
    arrayI1f_eng = [formatter.format_data(x) for x in I_fn * np.ones(nr_bancos)]
    formatter = EngFormatter(unit=r'$\Omega$', places=1)
    arrayX1f_eng = [formatter.format_data(x) for x in X * np.ones(nr_bancos)]
    formatter = EngFormatter(unit='F', places=2)
    arrayC1f_eng = [formatter.format_data(x) for x in C * np.ones(nr_bancos)]
    formatter = EngFormatter(unit='H', places=1)
    arrayL1f_eng = [formatter.format_data(x) for x in L_reator]
    formatter = EngFormatter(places=1)
    array_i_pico_inicaL_todos_pu_eng = [formatter.format_data(x) for x in i_pico_inicaL_todos_pu]
    formatter = EngFormatter(unit='Hz', places=1)
    array_frequencia_Hz_list_todos_eng = [formatter.format_data(x) for x in omega_list_todos / (2 * np.pi)]

    # Creating DataFrame
    data = {
        r'$Q_{3\phi}$': arrayQ3f_eng,
        r'$Q_{1\phi}$': arrayQ1f_eng,
        r'$V_{3\phi}$': arrayV3f_eng,
        r'$V_{1\phi}$': arrayV1f_eng,
        r'$I_{1\phi}$': arrayI1f_eng,
        r'$X_{1\phi}$': arrayX1f_eng,
        r'$C_{1\phi}$': arrayC1f_eng,
        r'$L_{1\phi}$': arrayL1f_eng,
        '$I_{p}/I_{n}$': array_i_pico_inicaL_todos_pu_eng,
        '$f_{0}$': array_frequencia_Hz_list_todos_eng,
    }

    df = pd.DataFrame(data)

    return df, i_curto, i_pico_inicial, sigma, omega, t, i_pico_inicial_list

# ===================================================================================
# ===================================================================================

import plotly.graph_objects as go
import numpy as np

def plot_inrush(t, i_curto, i_pico_inicial, omega, sigma, f_fund, text, X_curto_circuito, X, I_fn):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t * 1e3,
        y=i_curto / I_fn.max() + np.cos(f_fund*t+np.pi/2),
        name=text["instantaneous"],
        line=dict(shape='linear', color='rgb(0, 0, 255)', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=t * 1e3,
        y=i_pico_inicial * np.exp(-sigma * t) / I_fn.max(),
        name=text["envelope"],
        line=dict(shape='linear', color='rgb(0, 0, 0)', width=1, dash='dot'),
        connectgaps=True)
    )

    fig.add_trace(go.Scatter(
        x=t * 1e3,
        y=-i_pico_inicial * np.exp(-sigma * t) / I_fn.max(),
        name=text["envelope"],
        line=dict(shape='linear', color='rgb(0, 0, 0)', width=1, dash='dot'),
        connectgaps=True)
    )

    fig.add_trace(go.Scatter(
        x=t * 1e3,
        y=(1 - X_curto_circuito.max() / X.max()) * i_curto/i_curto.max() + np.cos(2 * np.pi * f_fund * t),
        name=text["reference_60hz"],
        line=dict(shape='linear', color='rgb(0.2, 0.2, 0.2)', width=0.5),
        connectgaps=True,
        yaxis='y2'  # Especifica que esse traço está no eixo secundário
    ))

    fig.update_layout(
        legend_title_text=text["current_label"],
        title_text=text["title"],
        xaxis_title=text["time_label"],
        yaxis_title=text["current_axis_label"],
        yaxis2=dict(
            overlaying='y',  # Colocar o eixo secundário sobre o eixo primário
            side='right',  # Eixo secundário à direita
            showgrid=False,  # Opcional: remover a grade do eixo secundário
            range=[-1.5, 1.5]  # Definir o intervalo do eixo secundário entre -1.5 e 1.5
        )
    )

    return fig
