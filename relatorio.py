# relatorio.py

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np



def gerar_figura(t, i_pico_inicial, sigma, omega, f_fund):
    # Update Matplotlib font size configuration
    mpl.rcParams.update({'font.size': 8})

    # Convert time to a numpy array if necessary
    t = np.asarray(t)

    # Calculate short-circuit current
    i_curto = i_pico_inicial * np.exp(-sigma * t) * np.sin(omega * t)

    # Figure settings
    cm = 1 / 2.54
    fig_mpl, ax_mpl = plt.subplots(figsize=(16 * cm, 7 * cm))

    # Plot the graphs
    ax_mpl.plot(t * 1e3, i_curto / 1e3, label='$i(t)$', color='blue', lw=1.0)
    ax_mpl.plot(t * 1e3, i_pico_inicial * np.exp(-sigma * t) / 1e3, color='gray', ls='--', lw=0.5)
    ax_mpl.plot(t * 1e3, -i_pico_inicial * np.exp(-sigma * t) / 1e3, color='gray', ls='--', lw=0.5)
    ax_mpl.plot(t * 1e3, i_pico_inicial * np.sin(2 * np.pi * f_fund * t) / 1e3, label='$60 {\\rm Hz}$', color='gray',
                alpha=0.5, lw=1.0)

    # Set axis labels
    ax_mpl.set_xlabel('Tempo [ms]')
    ax_mpl.set_ylabel('Corrente [kA]')

    # Add legend
    ax_mpl.legend()

    # Save the figure as a PNG file
    fig_mpl.savefig('Correntes.png', bbox_inches='tight', dpi=300)

    # Close the figure to free up memory
    plt.close(fig_mpl)


from matplotlib.ticker import EngFormatter


def format_values(soma_Q_3f, V_ff, V_fn, I_curto_circuito, L_reator, i_pico_inicial, omega, i_pico_inicial_todos_pu,
                  conclusao1, maxima_corrente_de_pico_dos_bancos):
    # Create formatters
    formatter_VAr = EngFormatter(places=2, unit='VAr')
    formatter_V = EngFormatter(places=1, unit='V')
    formatter_A = EngFormatter(places=1, unit='A')
    formatter_H = EngFormatter(places=1)
    formatter_Hz = EngFormatter(places=1)
    formatter_pu = EngFormatter(places=1)

    # Format values
    valores = {
        "potencia_reativa_do_banco": formatter_VAr.format_data(soma_Q_3f),
        "tensao_trifasica": formatter_V.format_data(V_ff),
        "tensao_monofasica": formatter_V.format_data(V_fn),
        "corrente_de_curto": formatter_A.format_data(I_curto_circuito),
        "indutancia_escolhida": formatter_H.format_data(1e6 * L_reator[0]),
        "corrente_pico": formatter_A.format_data(i_pico_inicial),
        "frequencia_oscilacao": formatter_Hz.format_data(omega / (2 * np.pi)),
        "inrush_inominal": formatter_pu.format_data(i_pico_inicial_todos_pu.max()),
        "conclusao1": conclusao1,
        "maxima_corrente_de_pico_dos_bancos": formatter_pu.format_data(maxima_corrente_de_pico_dos_bancos)
    }

    return valores


import io
from zipfile import ZipFile
import funcoes_auxiliares

def process_latex_and_create_zip(arquivo_copiado_tex, valores, df, nome_arquivo_saida):
    # Replace values in the copied file
    funcoes_auxiliares.substituir_valores(arquivo_copiado_tex, valores)

    # Add data table
    latex_table = df.to_latex(header=True, index=True, float_format="%.2f")
    with open(arquivo_copiado_tex, 'r', encoding='utf-8') as file:
        content = file.read()
    updated_content = content.replace('% INSERT_TABLE_HERE', latex_table)
    with open(arquivo_copiado_tex, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    # Create a ZIP file in memory
    zip_buffer = io.BytesIO()

    # List of files to be zipped
    files_to_zip = ["Correntes.png", "Sistema.png", "logo.png", "Picture1.png", nome_arquivo_saida + ".tex"]

    # ZIP file name
    zip_filename = nome_arquivo_saida + ".zip"

    # Create the ZIP file in memory
    with ZipFile(zip_buffer, 'w') as z:
        for file in files_to_zip:
            # Add each specified file to the ZIP
            with open(file, "rb") as f:
                z.writestr(file, f.read())

    # Move the buffer pointer to the beginning
    zip_buffer.seek(0)

    return zip_buffer, zip_filename
