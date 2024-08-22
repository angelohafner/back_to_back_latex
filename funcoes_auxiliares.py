







# ===================================================================================
def substituir_valores(arquivo_tex, valores):
    with open(arquivo_tex, 'r') as file:
        filedata = file.read()

    for chave, valor in valores.items():
        filedata = filedata.replace('{{' + chave + '}}', str(valor))

    with open(arquivo_tex, 'w') as file:
        file.write(filedata)


# ===================================================================================

import numpy as np
import pandas as pd
from matplotlib.ticker import EngFormatter


def calcular_back_to_back(C, L, R_EQ_PARA_AMORTECIMENTO, V_fn, FC, I_fn, w_isolado, i_pico_inicial_isolado, nr_bancos,
                          Q_3f, Q_1f, V_ff, X, L_reator):
    # Inicializando listas
    i_pico_inicial_list = []
    sigma_list = []
    omega_list = []

    # Cálculo das grandezas
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

    # Convertendo listas em arrays NumPy e adicionando valores iniciais
    i_pico_inicaL_todos_pu = np.array([i_pico_inicial_isolado] + i_pico_inicial_list) / (I_fn * np.sqrt(2))
    omega_list_todos = np.array([w_isolado] + omega_list)

    # Selecionando os valores finais
    i_pico_inicial = i_pico_inicial_list[-1]
    sigma = sigma_list[-1]
    omega = omega_list[-1]

    # Calculando o tempo e a corrente de curto-circuito
    t = np.linspace(0, 1 / 60, 1 * int(2 ** 12))
    i_curto = i_pico_inicial * np.exp(-sigma * t) * np.sin(omega * t)

    # Formatando os dados para o DataFrame
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

    # Criando o DataFrame
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

    # Retornando as saídas especificadas
    return df, i_curto, i_pico_inicial, sigma, omega, t, i_pico_inicial_list


# Exemplo de chamada da função










