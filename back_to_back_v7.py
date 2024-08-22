"""
Angelo Alfredo Hafner
aah@dax.energy
"""
# cuidado
INDUTOR_DEFAULT = 15.0
REATIVOS_DEFAULT = 5.4
TENSAO_DEFAULT = 13.8
NUM_BANCOS_DEFAULT = 4
CORRENTE_CURTO_DEFAULT = 1000.0
R_EQ_PARA_AMORTECIMENTO = 0.1

from matplotlib.ticker import EngFormatter
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from engineering_notation import EngNumber
import shutil
import matplotlib as mpl
mpl.rcParams['font.family'] = 'serif'
import zipfile
import io
from funcoes_auxiliares import *
from zipfile import ZipFile


st.markdown('# Resposta transitória da corrente de energização de capacitores')

col0, col1, col2 = st.columns([2, 0.2, 8])
with col0:
    V_ff = st.number_input("Tensão 3𝝋 [kV]", min_value=0.1, max_value=750.0, value=TENSAO_DEFAULT, format="%.1f") * 1e3
    V_fn = V_ff / np.sqrt(3)
    f_fund = st.number_input("Frequência [Hz]", min_value=40.0, max_value=70.0, value=60.0, step=0.1, format="%.1f")
    w_fund = 2 * np.pi * f_fund
    I_curto_circuito = st.number_input("Corrente de curto-circuito na barra [kA]", min_value=0.0, max_value=99e99,
                                       value=CORRENTE_CURTO_DEFAULT, format="%.0f") * 1e3
    nr_bancos = st.slider("Número de Bancos", min_value=2, max_value=20, value=NUM_BANCOS_DEFAULT, step=1)
    FC = st.slider("Fator de Segurança", min_value=1.0, max_value=1.5, value=1.4, step=0.1, format="%.1f")

with col2:
    st.image(image='Sistema.png')

# ==============================================================================================

# ===============================================================================================
Q_3f = np.zeros(nr_bancos)
comp_cabo = np.zeros(nr_bancos)
comp_barra = np.zeros(nr_bancos)
L_unit_cabo = np.zeros(nr_bancos)
L_unit_barra = np.zeros(nr_bancos)
L_capacitor = np.zeros(nr_bancos)
L_reator = np.zeros(nr_bancos)

st.markdown(r"#### Banco a ser energizado $(\#0)$")
cols = st.columns(5)
ii = 0
k = 0
with cols[ii]:
    Q_3f[k] = st.number_input("$Q_{3\\varphi}$[MVAr] ",
                              value=REATIVOS_DEFAULT, step=0.01,
                              key="Q_3f_" + str(k), format="%.2f") * 1e6
ii = ii + 1
with cols[ii]:
    comp_cabo[k] = st.number_input("$\\ell_{\\rm cabo}{\\rm [m]}$",
                                   min_value=0.0, max_value=10e3, value=0.0, step=0.01,
                                   key="comp_cabo" + str(k))
# ii = ii + 1
# with cols[ii]:
#         comp_barra[k] =  st.number_input("$\\ell_{\\rm barra}{\\rm [m]}$",
#                                         min_value=0.0,  max_value=100.0, value=0.0, step=0.01,
#                                         key="comp_barra"+str(k))
ii = ii + 1
with cols[ii]:
    L_unit_cabo[k] = st.number_input("$L'_{\\rm cabo} {\\rm \\left[{\\mu H}/{m} \\right]}$",
                                     min_value=0.00, max_value=100.0, value=0.00, step=0.01,
                                     key="L_unit_cabo" + str(k), format="%.1f") * 1e-6
# ii = ii + 1
# with cols[ii]:
#         L_unit_barra[k] =  st.number_input("$L'_{\\rm barra} {\\rm \\left[{\\mu H}/{m} \\right]}$",
#                                         min_value=0.0,  max_value=100.0, value=0.00, step=0.01,
#                                         key="L_unit_barra"+str(k)) * 1e-6
ii = ii + 1
with cols[ii]:
    L_capacitor[k] = st.number_input("$L_{\\rm capacitor} {\\rm \\left[{\\mu H} \\right]}$",
                                     min_value=0.0, max_value=100.0, value=5.00, step=0.01,
                                     key="L_capacitor" + str(k), format="%.1f") * 1e-6
ii = ii + 1
with cols[ii]:
    L_reator[k] = st.number_input("$L_{\\rm reator} {\\rm \\left[{\\mu H} \\right]}$",
                                  min_value=0.0, max_value=10000.0, value=INDUTOR_DEFAULT, step=1.0,
                                  key="L_reator" + str(k), format="%.1f") * 1e-6

st.markdown(r"#### Bancos já energizados $(\#1$ ao $\#n)$")

cols = st.columns(5)
for k in range(1, nr_bancos):
    ii = 0
    with cols[ii]:
        if k == 1:
            Q_3f[k] = st.number_input("$Q_{3\\varphi}$[MVAr] ",
                                      value=REATIVOS_DEFAULT,
                                      key="Q_3f_" + str(k), format="%.2f", label_visibility="visible") * 1e6
        else:
            Q_3f[k] = st.number_input("$Q_{3\\varphi}$[MVAr] ",
                                      value=REATIVOS_DEFAULT,
                                      key="Q_3f_" + str(k), format="%.2f", label_visibility="collapsed") * 1e6
    ii = ii + 1
    with cols[ii]:
        if k == 1:
            comp_cabo[k] = st.number_input("$\\ell_{\\rm cabo}{\\rm [m]}$",
                                           min_value=0.0, max_value=10e3, value=0.0, step=0.01,
                                           key="comp_cabo" + str(k), label_visibility="visible")
        else:
            comp_cabo[k] = st.number_input("$\\ell_{\\rm cabo}{\\rm [m]}$",
                                           min_value=0.0, max_value=10e3, value=0.0, step=0.01,
                                           key="comp_cabo" + str(k), label_visibility="collapsed")

    # ii = ii + 1
    # with cols[ii]:
    #     comp_barra[k] = st.number_input("$\\ell_{\\rm barra}{\\rm [m]}$",
    #                                     min_value=0.0, max_value=100.0, value=0.0, step=0.01,
    #                                     key="comp_barra" + str(k))
    ii = ii + 1
    with cols[ii]:
        if k == 1:
            L_unit_cabo[k] = st.number_input("$L'_{\\rm cabo} {\\rm \\left[{\\mu H}/{m} \\right]}$",
                                             min_value=0.0, max_value=100.0, value=0.00, step=0.01,
                                             key="L_unit_cabo" + str(k), label_visibility="visible") * 1e-6
        else:
            L_unit_cabo[k] = st.number_input("$L'_{\\rm cabo} {\\rm \\left[{\\mu H}/{m} \\right]}$",
                                             min_value=0.0, max_value=100.0, value=0.00, step=0.01,
                                             key="L_unit_cabo" + str(k), label_visibility="collapsed") * 1e-6
    # ii = ii + 1
    # with cols[ii]:
    #     L_unit_barra[k] = st.number_input("$L'_{\\rm barra} {\\rm \\left[{\\mu H}/{m} \\right]}$",
    #                                       min_value=0.0, max_value=100.0, value=0.00, step=0.01,
    #                                       key="L_unit_barra" + str(k)) * 1e-6
    ii = ii + 1
    with cols[ii]:
        if k == 1:
            L_capacitor[k] = st.number_input("$L_{\\rm capacitor} {\\rm \\left[{\\mu H} \\right]}$",
                                             min_value=0.0, max_value=100.0, value=5.00, step=0.01,
                                             key="L_capacitor" + str(k), label_visibility="visible") * 1e-6
        else:
            L_capacitor[k] = st.number_input("$L_{\\rm capacitor} {\\rm \\left[{\\mu H} \\right]}$",
                                             min_value=0.0, max_value=100.0, value=5.00, step=0.01,
                                             key="L_capacitor" + str(k), label_visibility="collapsed") * 1e-6
    ii = ii + 1
    with cols[ii]:
        if k == 1:
            L_reator[k] = st.number_input("$L_{\\rm reator} {\\rm \\left[{\\mu H} \\right]}$",
                                          min_value=0.1, max_value=10000.0, value=INDUTOR_DEFAULT, step=1.0,
                                          key="L_reator" + str(k), label_visibility="visible") * 1e-6
        else:
            L_reator[k] = st.number_input("$L_{\\rm reator} {\\rm \\left[{\\mu H} \\right]}$",
                                          min_value=0.1, max_value=10000.0, value=INDUTOR_DEFAULT, step=1.0,
                                          key="L_reator" + str(k), label_visibility="collapsed") * 1e-6


nome_arquivo_saida = f'Relatorio_Inrush_DAX_{REATIVOS_DEFAULT}kVAr_{TENSAO_DEFAULT}kV_uH{INDUTOR_DEFAULT}'
# ===============================================================================================
# === serve para o isolado e o back-to-back
soma_Q_3f = sum(Q_3f)
Q_1f = Q_3f / 3
I_fn = Q_1f / V_fn
X = V_fn / I_fn
C = 1 / (w_fund * X)
L_barra_mais_cabo = comp_barra * L_unit_barra + comp_cabo * L_unit_cabo
L = L_barra_mais_cabo + L_capacitor + L_reator

# === isolado ===
X_curto_circuito = V_fn / I_curto_circuito
L_curto_circuito = X_curto_circuito / w_fund
L_eq_isolado = L_curto_circuito + L[0]
w_isolado = 1 / np.sqrt( L_eq_isolado * C[0] )
num_i = V_fn * np.sqrt(2)
den_i = L_eq_isolado * w_isolado
i_pico_inicial_isolado = FC * num_i / den_i

# === back-to-back ===
df, i_curto, i_pico_inicial, sigma, omega, t, i_pico_inicial_list = calcular_back_to_back(
    C, L, R_EQ_PARA_AMORTECIMENTO, V_fn, FC, I_fn, w_isolado, i_pico_inicial_isolado,
    nr_bancos, Q_3f, Q_1f, V_ff, X, L_reator
)


i_pico_inicial_todos_pu = np.array([i_pico_inicial_isolado] + i_pico_inicial_list) / (I_fn * np.sqrt(2))
# =====================================================================================================

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=t * 1e3,
    y=i_curto / 1e3,
    name="Instantânea",
    line=dict(shape='linear', color='rgb(0, 0, 255)', width=2)
))

fig.add_trace(go.Scatter(
    x=t * 1e3,
    y=i_pico_inicial * np.exp(-sigma * t) / 1e3,
    name="Envelope",
    line=dict(shape='linear', color='rgb(0, 0, 0)', width=1, dash='dot'),
    connectgaps=True)
)

fig.add_trace(go.Scatter(
    x=t * 1e3,
    y=-i_pico_inicial * np.exp(-sigma * t) / 1e3,
    name="Envelope",
    line=dict(shape='linear', color='rgb(0, 0, 0)', width=1, dash='dot'),
    connectgaps=True)
)

fig.add_trace(go.Scatter(
    x=t * 1e3,
    y=i_pico_inicial * np.sin(2 * np.pi * f_fund * t) / 1e3,
    name="Referência 60 Hz",
    line=dict(shape='linear', color='rgb(0.2, 0.2, 0.2)', width=0.5),
    connectgaps=True)
)

fig.update_layout(legend_title_text='Corrente:', title_text="Inrush Banco de Capacitores",
                  xaxis_title=r"Tempo [ms]", yaxis_title="Corrente [kA]")
st.plotly_chart(fig, use_container_width=True)

# coluna0, coluna1 = st.columns([1, 1])

# with coluna0:
st.markdown('#### Resultados')
st.write("Corrente nominal do banco $I_{\\rm nominal}=$", EngNumber(I_fn[0]), "A")
st.markdown('##### Para banco único')

corrente_pico_bancos_isolado = i_pico_inicial_isolado / (I_fn[0] * np.sqrt(2))

st.write("Corrente de pico na energização $I_{\\rm{inrsuh}}=$",
         EngNumber(i_pico_inicial_isolado), "${\\rm A}$,$~$que corresponde a", np.round(corrente_pico_bancos_isolado, 1), "$\\times I_{\\rm{nominal}}$")
st.write("Frequência de Oscilação = ", EngNumber(w_isolado / (2 * np.pi)), "${\\rm Hz}$, que corresponde a",
         np.round(w_isolado / w_fund, 1), "$\\times f_1$")#, com $\max \left( {\\frac{{di}}{{dt}}} \\right) = $", EngNumber((V_fn*np.sqrt(2)/L_eq_isolado)/1e6), "$\\frac{{\\rm{V}}}{{{\\rm{\\mu s}}}}$")
st.markdown('##### Para banco com os demais bancos energizados')
corrente_pico_bancos_back_to_back = i_pico_inicial / (I_fn * np.sqrt(2))
st.write("Corrente de pico na energização $I_{\\rm{inrsuh}}=$",
         EngNumber(i_pico_inicial), "${\\rm A}$, que corresponde a", np.round(corrente_pico_bancos_back_to_back.max(), 1), "$\\times I_{\\rm{nominal}}$")
freq_oscilacao = omega / (2 * np.pi)
st.write("Frequência de Oscilação = ", EngNumber(freq_oscilacao), "${\\rm Hz}$, que corresponde a",
         np.round(omega / w_fund, 1), "$\\times f_1$")
# st.write("Harmônico de Oscilação = ", EngNumber(omega / w_fund))

# with coluna1:
st.markdown('#### Conclusão')
st.markdown(
    'As amplitudes típicas das correntes de *inrush* para energização *back-to-back* de bancos de capacitores são de vários ${\\rm kA}$ com frequências de $2{\\rm~kHz}$ a $5{\\rm~kHz}$ [$^{[1]}$](https://ieeexplore.ieee.org/document/7035261).')
conclusao1 = "cuidado aqui"
temp = max(corrente_pico_bancos_isolado, corrente_pico_bancos_back_to_back.max())

if temp < 100 and freq_oscilacao < 4250:
    conclusao1 = ("Reator adequado, pois $\\dfrac{I_{\\rm inrush}}{I_{\\rm nominal}} = $" + str(EngNumber(temp)) +
                 "$\\le 100$ e $f_{osc} = $" + str(EngNumber(freq_oscilacao)) + "Hz < 4,25 kHz, " +
                 "conforme IEEE Std C37.012, p\\'{a}gina 16[$^{[2]}$](https://ieeexplore.ieee.org/document/7035261) e IEC 62271-100, Table 9 (Preferred values of rated capacitive switching currents), p\\'{a}gina 45[$^{[3]}$](https://webstore.iec.ch/publication/62785).")

    conclusao = ("Reator adequado, pois $\\dfrac{I_{\\rm inrush}}{I_{\\rm nominal}} = $" + str(EngNumber(temp)) +
                 "$\\le 100$ e $f_{osc} = $" + str(EngNumber(freq_oscilacao)) + "Hz < 4,25 kHz, " +
                 "conforme IEEE Std C37.012, página 16[$^{[2]}$](https://ieeexplore.ieee.org/document/7035261) e IEC 62271-100, Table 9 (Preferred values of rated capacitive switching currents), página 45[$^{[3]}$](https://webstore.iec.ch/publication/62785).")

else:
    conclusao1 = ("Reator n\\~{a}o adequado, pois $\\dfrac{I_{\\rm inrush}}{I_{\\rm nominal}} = $" + str(EngNumber(temp)) +
                  "$> 100$ ou $f_{osc} = $" + str(EngNumber(freq_oscilacao)) + "Hz > 4,25 kHz, " +
                  "conforme IEEE Std C37.012, p\\'{a}gina 16[$^{[2]}$](https://ieeexplore.ieee.org/document/7035261) e IEC 62271-100, Table 9 (Preferred values of rated capacitive switching currents), p\\'{a}gina 45[$^{[3]}$](https://webstore.iec.ch/publication/62785).")

    conclusao = ("Reator NÃO adequado, pois $\\dfrac{I_{\\rm inrush}}{I_{\\rm nominal}} = $" + str(EngNumber(temp)) +
                 "$> 100$ ou $f_{osc} = $" + str(EngNumber(freq_oscilacao)) + "Hz > 4,25 kHz, " +
                 "conforme IEEE Std C37.012, página 16[$^{[2]}$](https://ieeexplore.ieee.org/document/7035261) e IEC 62271-100, Table 9 (Preferred values of rated capacitive switching currents), página 45[$^{[3]}$](https://webstore.iec.ch/publication/62785).")

st.write(conclusao)
cem = temp

st.markdown('#### Bibliografia')
col_bib1, col_bib2 = st.columns([1, 25])
with col_bib1:
    """
    [[1]](https://ieeexplore.ieee.org/document/7035261)\\
    \\
    \\
    [[2]](https://ieeexplore.ieee.org/document/9574631)\\
    \\
    [[3]](https://webstore.iec.ch/publication/62785)\\
    \\
    [[4]](https://ieeexplore.ieee.org/document/5318709)\\
    \\
    [[4]](https://cdn.standards.iteh.ai/samples/101972/4e7e06bd66d2443da668b8e0c6c60512/IEC-62271-100-2021.pdf)\\
    \\
    [[5]](https://www.normas.com.br/autorizar/visualizacao-nbr/313/identificar/visitante)
    """
with col_bib2:
    """
    IEEE Application Guide for Capacitance Current Switching for AC High-Voltage Circuit Breakers Rated on a Symmetrical Current Basis, in ANSI/IEEE C37.012-1979 , vol., no., pp.1-54, 6 Feb. 1979, doi: 10.1109/IEEESTD.1979.7035261.\\
    IEEE Approved Draft Standard Requirements for Capacitor Switches for AC Systems (1 kV to 38 kV), in IEEE PC37.66/D10, October 2021 , vol., no., pp.1-35, 13 Dec. 2021.\\
    IEC 62271-100 High-voltage switchgear and controlgear - Part 100: Alternating-current circuit-breakers
    IEEE Standard for AC High-Voltage Circuit Breakers Rated on a Symmetrical Current Basis--Preferred Ratings and Related Required Capabilities for Voltages Above 1000 V, in IEEE Std C37.06-2009 , vol., no., pp.1-56, 6 Nov. 2009, doi: 10.1109/IEEESTD.2009.5318709.\\
    IEC 62271-100 High-voltage switchgear and controlgear – Part 100: Alternating-current circuit-breakers\\
    NBR 5282 Capacitores de potência em derivação para sistema de tensão nominal acima de 1000 V
    """

# ===============================================================================================================
# RELATORIO
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
# from docx2pdf import convert

t = np.asarray(t)
i_curto = i_pico_inicial * np.exp(-sigma * t) * np.sin(omega * t)
mpl.rcParams.update({'font.size': 8})
cm = 1 / 2.54
fig_mpl, ax_mpl = plt.subplots(figsize=(16 * cm, 7 * cm))
ax_mpl.plot(t * 1e3, i_curto / 1e3, label='$i(t)$', color='blue', lw=1.0)
ax_mpl.plot(t * 1e3, i_pico_inicial * np.exp(-sigma * t) / 1e3, color='gray', ls='--', lw=0.5)
ax_mpl.plot(t * 1e3, -i_pico_inicial * np.exp(-sigma * t) / 1e3, color='gray', ls='--', lw=0.5)
ax_mpl.plot(t * 1e3, i_pico_inicial * np.sin(2 * np.pi * f_fund * t) / 1e3, label='$60 {\\rm Hz}$', color='gray',
            alpha=0.5, lw=1.0)
ax_mpl.set_xlabel('Tempo [ms]')
ax_mpl.set_ylabel('Corrente [kA]')
ax_mpl.legend()
fig_mpl.savefig('Correntes.png', bbox_inches='tight', dpi=300)


if st.button('Gerar Relatório'):
    arquivo_original_tex = 'TEMPLATE_Relatorio_Inrush_DAX.tex'
    arquivo_copiado_tex = nome_arquivo_saida+'.tex'
    shutil.copy(arquivo_original_tex, arquivo_copiado_tex)

    # Valores a serem substituídos
    formatter_VAr = EngFormatter(places=1, unit='VAr')
    formatter_V = EngFormatter(places=1, unit='V')
    formatter_A = EngFormatter(places=1, unit='A')
    formatter_H = EngFormatter(places=1)
    formatter_Hz = EngFormatter(places=1)
    formatter_pu = EngFormatter(places=1)

    valores = {
        "potencia_reativa_do_banco": formatter_VAr.format_data(soma_Q_3f),
        "tensao_trifasica": formatter_V.format_data(V_ff),
        "tensao_monofasica": formatter_V.format_data(V_fn),
        "corrente_de_curto": formatter_A.format_data(I_curto_circuito),
        "indutancia_escolhida": formatter_H.format_data(1e6*L_reator[0]),
        "corrente_pico":        formatter_A.format_data(i_pico_inicial),
        "frequencia_oscilacao": formatter_Hz.format_data(omega / (2 * np.pi)),
        "inrush_inominal":      formatter_pu.format_data(i_pico_inicial_todos_pu.max()),####
        "conclusao1": conclusao1,
        "cem": formatter_pu.format_data(cem)
    }

    # Substituindo os valores no arquivo copiado
    substituir_valores(arquivo_copiado_tex, valores)
    # Adiconando tabela de dados
    latex_table = df.to_latex(header=True, index=True, float_format="%.2f")
    with open(arquivo_copiado_tex, 'r', encoding='utf-8') as file:
        content = file.read()
    updated_content = content.replace('% INSERT_TABLE_HERE', latex_table)
    with open(arquivo_copiado_tex, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    # Criando um arquivo ZIP em memória
    zip_buffer = io.BytesIO()

    # Lista de arquivos que você quer zipar
    lista_para_zipar = ["Correntes.png", "Sistema.png", "logo.png", "Picture1.png", nome_arquivo_saida + ".tex"]

    # Nome do arquivo ZIP de destino
    zip_filename = nome_arquivo_saida + ".zip"

    # Cria o arquivo ZIP em memória
    with ZipFile(zip_buffer, 'w') as z:
        for file in lista_para_zipar:
            # Adiciona cada arquivo especificado na lista ao ZIP
            with open(file, "rb") as f:
                z.writestr(file, f.read())

    # Move o ponteiro do buffer para o início
    zip_buffer.seek(0)

    # Criando o botão de download do arquivo ZIP
    st.download_button(
        label="Download ZIP",
        data=zip_buffer,
        file_name=zip_filename,
        mime="application/zip"
    )

st.markdown('#### Desenvolvimento')
colunas = st.columns(2)
with colunas[0]:
    """
    Angelo A. Hafner\\
    Engenheiro Eletricista\\
    CONFEA: 2.500.821.919\\
    CREA/SC: 045.776-5\\
    aah@dax.energy
    """
with colunas[1]:
    """
    Tiago Machado\\
    Business Manager\\
    Mobile: +55 41 99940-3744\\
    tm@dax.energy
    """

