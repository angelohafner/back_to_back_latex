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


import config
import streamlit as st
import shutil
import matplotlib as mpl
mpl.rcParams['font.family'] = 'serif'
from funcoes_auxiliares import *


# Set the language and locale
text, language_key, format_number = config.configure_language_and_locale()

st.markdown(text["title"])

col0, col1, col2 = st.columns([2, 0.2, 8])
with col0:
    # Input widgets using `st.text_input` to respect locale decimal separator
    V_ff_input = st.text_input(text["voltage"], value=format_input(13.8, language_key))
    f_fund_input = st.text_input(text["frequency"], value=format_input(60.0, language_key))
    I_curto_circuito_input = st.text_input(text["short_circuit_current"], value=format_input(20.0, language_key))

    # Convert inputs to floats
    V_ff = parse_input(V_ff_input, language_key) * 1e3 if V_ff_input else None
    f_fund = parse_input(f_fund_input, language_key) if f_fund_input else None
    I_curto_circuito = parse_input(I_curto_circuito_input, language_key) * 1e3 if I_curto_circuito_input else None

    # Check if the inputs were converted correctly
    if V_ff is None or f_fund is None or I_curto_circuito is None:
        st.error("Por favor, insira valores válidos.")

    nr_bancos = st.slider(text["number_of_banks"], min_value=2, max_value=20, value=5)


    V_fn = V_ff / np.sqrt(3)
    w_fund = 2 * np.pi * f_fund
    FC = 1.4

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

st.markdown(text["energize_bank"])  # "#### Banco a ser energizado $(\#0)$"
cols = st.columns(5)
ii = 0
k = 0
# Substituindo st.number_input por st.text_input
with cols[ii]:
    Q_3f_input = st.text_input("$Q_{3\\varphi}$[MVAr] ",
                               value=format_input(REATIVOS_DEFAULT, language_key),
                               key="Q_3f_" + str(k))
    Q_3f[k] = parse_input(Q_3f_input, language_key) * 1e6 if Q_3f_input else None

ii = ii + 1
with cols[ii]:
    comp_cabo_input = st.text_input("$\\ell_{\\rm cable}{\\rm [m]}$",
                                    value=format_input(0.0, language_key),
                                    key="comp_cabo" + str(k))
    comp_cabo[k] = parse_input(comp_cabo_input, language_key) if comp_cabo_input else None

ii = ii + 1
with cols[ii]:
    L_unit_cabo_input = st.text_input("$L'_{\\rm cable} {\\rm \\left[{\\mu H}/{m} \\right]}$",
                                      value=format_input(0.00, language_key),
                                      key="L_unit_cabo" + str(k))
    L_unit_cabo[k] = parse_input(L_unit_cabo_input, language_key) * 1e-6 if L_unit_cabo_input else None

ii = ii + 1
with cols[ii]:
    L_capacitor_input = st.text_input("$L_{\\rm capacitor} {\\rm \\left[{\\mu H} \\right]}$",
                                      value=format_input(5.00, language_key),
                                      key="L_capacitor" + str(k))
    L_capacitor[k] = parse_input(L_capacitor_input, language_key) * 1e-6 if L_capacitor_input else None

ii = ii + 1
with cols[ii]:
    L_reator_input = st.text_input("$L_{\\rm reactor} {\\rm \\left[{\\mu H} \\right]}$",
                                   value=format_input(INDUTOR_DEFAULT, language_key),
                                   key="L_reator" + str(k))
    L_reator[k] = parse_input(L_reator_input, language_key) * 1e-6 if L_reator_input else None




# st.markdown(r"#### Bancos já energizados $(\#1$ ao $\#n)$")
st.markdown(text["already_energized_banks"])  # "#### Bancos já energizados $(\#1$ ao $\#n)$"
cols = st.columns(5)
for k in range(1, nr_bancos):
    ii = 0
    with cols[ii]:
        Q_3f_input = st.text_input(
            "$Q_{3\\varphi}$[MVAr]",
            value=format_input(REATIVOS_DEFAULT, language_key),
            key="Q_3f_" + str(k),
            label_visibility="visible" if k == 1 else "collapsed"
        )
        Q_3f[k] = parse_input(Q_3f_input, language_key) * 1e6 if Q_3f_input else None

    ii = ii + 1
    with cols[ii]:
        comp_cabo_input = st.text_input(
            "$\\ell_{\\rm cable}{\\rm [m]}$",
            value=format_input(0.0, language_key),
            key="comp_cabo" + str(k),
            label_visibility="visible" if k == 1 else "collapsed"
        )
        comp_cabo[k] = parse_input(comp_cabo_input, language_key) if comp_cabo_input else None

    ii = ii + 1
    with cols[ii]:
        L_unit_cabo_input = st.text_input(
            "$L'_{\\rm cable} {\\rm \\left[{\\mu H}/{m} \\right]}$",
            value=format_input(0.00, language_key),
            key="L_unit_cabo" + str(k),
            label_visibility="visible" if k == 1 else "collapsed"
        )
        L_unit_cabo[k] = parse_input(L_unit_cabo_input, language_key) * 1e-6 if L_unit_cabo_input else None

    ii = ii + 1
    with cols[ii]:
        L_capacitor_input = st.text_input(
            "$L_{\\rm capacitor} {\\rm \\left[{\\mu H} \\right]}$",
            value=format_input(5.00, language_key),
            key="L_capacitor" + str(k),
            label_visibility="visible" if k == 1 else "collapsed"
        )
        L_capacitor[k] = parse_input(L_capacitor_input, language_key) * 1e-6 if L_capacitor_input else None

    ii = ii + 1
    with cols[ii]:
        L_reator_input = st.text_input(
            "$L_{\\rm reactor} {\\rm \\left[{\\mu H} \\right]}$",
            value=format_input(INDUTOR_DEFAULT, language_key),
            key="L_reator" + str(k),
            label_visibility="visible" if k == 1 else "collapsed"
        )
        L_reator[k] = parse_input(L_reator_input, language_key) * 1e-6 if L_reator_input else None







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
df, i_curto, i_pico_inicial, sigma, omega, t, i_pico_inicial_list = \
    calcular_back_to_back(C, L, R_EQ_PARA_AMORTECIMENTO, \
                          V_fn, FC, I_fn, w_isolado, i_pico_inicial_isolado, \
                          nr_bancos, Q_3f, Q_1f, V_ff, X, L_reator
    )


i_pico_inicial_todos_pu = np.array([i_pico_inicial_isolado] + i_pico_inicial_list) / (I_fn * np.sqrt(2))


# Gera o gráfico
fig = plot_inrush(t, i_curto, i_pico_inicial, sigma, f_fund, text)
st.plotly_chart(fig, use_container_width=True)




st.markdown(text["results"])

st.write(text["nominal_current"], format_input(I_fn[0], language_key), "A")
st.markdown(text["for_single_bank"])
corrente_pico_bancos_isolado = i_pico_inicial_isolado / (I_fn[0] * np.sqrt(2))
st.write(text["peak_current_energization"], format_input(i_pico_inicial_isolado, language_key), "${\\rm A}$   (", format_input(np.round(corrente_pico_bancos_isolado, 1), language_key), "$\\times I_{\\rm{rated}}$)")
st.write(text["oscillation_frequency"], format_input(w_isolado / (2 * np.pi), language_key), "${\\rm Hz}$   (", format_input(np.round(w_isolado / w_fund, 1), language_key), "$\\times f_1$)")

st.markdown(text["for_bank_with_others_energized"])
corrente_pico_bancos_back_to_back = i_pico_inicial / (I_fn * np.sqrt(2))
st.write(text["peak_current_energization"], format_input(i_pico_inicial, language_key), "${\\rm A}$   (", format_input(np.round(corrente_pico_bancos_back_to_back.max(), 1), language_key), "$\\times I_{\\rm{rated}}$)")
freq_oscilacao = omega / (2 * np.pi)
st.write(text["oscillation_frequency"], str(int(freq_oscilacao)), "${\\rm Hz}$   (", format_input(np.round(omega / w_fund, 1), language_key), "$\\times f_1$)")





st.markdown(text["conclusion"])

st.markdown(text["conclusion_text"])

maxima_corrente_de_pico_dos_bancos = max(corrente_pico_bancos_isolado, corrente_pico_bancos_back_to_back.max())

maxima_corrente_str = config.format_number(maxima_corrente_de_pico_dos_bancos, language_key)
freq_oscilacao_str  = str(int(freq_oscilacao))

if maxima_corrente_de_pico_dos_bancos < 100 and freq_oscilacao < 4250:
    conclusao1 = (text["adequate_reactor"] + maxima_corrente_str + "$\\le 100$ e $f_{\\rm osc} = $" +
                  freq_oscilacao_str + "Hz < 4,25 kHz, " +
                  "IEEE Std C37.012, p. 16[$^{[2]}$](https://ieeexplore.ieee.org/document/7035261) e IEC 62271-100, Table 9 (Preferred values of rated capacitive switching currents), p. 45[$^{[3]}$](https://webstore.iec.ch/publication/62785).")
else:
    conclusao1 = (text["not_adequate_reactor"] + maxima_corrente_str + "$> 100$ ou $f_{\\rm osc} = $" +
                  freq_oscilacao_str + "Hz > 4,25 kHz, " +
                  "IEEE Std C37.012, p. 16[$^{[2]}$](https://ieeexplore.ieee.org/document/7035261) e IEC 62271-100, Table 9 (Preferred values of rated capacitive switching currents), p. 45[$^{[3]}$](https://webstore.iec.ch/publication/62785).")


st.write(conclusao1)


st.markdown(text["bibliography"])
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

st.markdown(text["development"])
colunas = st.columns(2)
with colunas[0]:
    """
    Angelo A. Hafner\\
    Electrical Engineer\\
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
# ===============================================================================================================
import relatorio
base_filename = 'TEMPLATE_Relatorio_Inrush_DAX'
arquivo_original_tex = f"{base_filename}_{language_key}.tex"
relatorio.gerar_figura(t, i_pico_inicial, sigma, omega, f_fund)
nome_arquivo_saida = f'Report_Inrush_DAX_{REATIVOS_DEFAULT}kVAr_{TENSAO_DEFAULT}kV_uH{INDUTOR_DEFAULT}'


if st.button(text["latex_report"]):
    arquivo_original_tex = f"{base_filename}_{language_key}.tex"
    arquivo_copiado_tex = nome_arquivo_saida+'.tex'
    shutil.copy(arquivo_original_tex, arquivo_copiado_tex)

    valores = relatorio.format_values(
        soma_Q_3f=soma_Q_3f,
        V_ff=V_ff,
        V_fn=V_fn,
        I_curto_circuito=I_curto_circuito,
        L_reator=L_reator,
        i_pico_inicial=i_pico_inicial,
        omega=omega,
        i_pico_inicial_todos_pu=i_pico_inicial_todos_pu,
        conclusao1=conclusao1,
        maxima_corrente_de_pico_dos_bancos=maxima_corrente_de_pico_dos_bancos
    )

    zip_buffer, zip_filename = relatorio.process_latex_and_create_zip(
        arquivo_copiado_tex=arquivo_copiado_tex,
        valores=valores,
        df=df,
        nome_arquivo_saida=nome_arquivo_saida
    )

    st.download_button(
        label="Download ZIP",
        data=zip_buffer,
        file_name=zip_filename,
        mime="application/zip"
    )

    st.write(text["use_xelatex_compiler"])

