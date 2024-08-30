import locale
import streamlit as st
from dicionarios import translations

# Dicionário de idiomas com bandeiras
language_options = {
    "en": "🇬🇧 English",
    "pt": "🇧🇷 Português",
    "zh": "🇨🇳 中文 (Chinese)",
    "es": "🇪🇸 Español (Spanish)",
    "fr": "🇫🇷 Français (French)",
    "de": "🇩🇪 Deutsch (German)"
}

def configure_language_and_locale():
    # Criação de uma lista de idiomas a partir do dicionário
    language_list = list(language_options.values())

    # Caixa de seleção para escolha de idioma
    selected_language = st.selectbox(
        "Choose Language / Escolha o idioma / 选择语言 / Sprache wählen",
        language_list
    )

    # Obtenção da chave do idioma selecionado a partir do valor escolhido
    language_key = list(language_options.keys())[language_list.index(selected_language)]

    # Acesso ao dicionário de traduções com a chave selecionada
    text = translations[language_key]

    # Função de formatação de números dependendo do idioma
    def format_number(value):
        if language_key == 'en':
            # Use dot as decimal separator
            return f"{value:,.2f}"
        else:
            # Use comma as decimal separator
            return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return text, language_key, format_number





def format_number(value, language_key):
    """
    Format a number based on the specified language.

    Parameters:
        value (float): The number to format.
        language_key (str): The language key ('en' for English, others for languages that use a comma as a separator).

    Returns:
        str: The formatted number as a string.
    """
    if language_key == 'en':
        # Use dot as decimal separator
        formatted_number = f"{value:,.2f}"
    else:
        # Use comma as decimal separator
        formatted_number = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return formatted_number


