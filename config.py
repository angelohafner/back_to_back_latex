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

    # Caixa de seleção mais sofisticada para escolha de idioma
    selected_language = st.selectbox(
        "Choose Language / Escolha o idioma / 选择语言 / Sprache wählen",
        language_list
    )

    # Obtenção da chave do idioma selecionado a partir do valor escolhido
    language_key = list(language_options.keys())[language_list.index(selected_language)]

    # Acesso ao dicionário de traduções com a chave selecionada
    text = translations[language_key]

    # Configuração do locale
    if language_key == 'en':
        # Inglês dos EUA - Ponto como separador decimal
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    elif language_key in ['de', 'fr', 'pt', 'it', 'es']:
        # Alemanha, França, Brasil, Itália, Espanha - Vírgula como separador decimal
        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    else:
        # Outros idiomas
        locale.setlocale(locale.LC_ALL, '')

    return text, language_key



import locale

def format_number(value, language_key):
    if language_key == 'en':
        # Use dot as decimal separator
        return locale.format_string("%.2f", value, grouping=True)
    else:
        # Use comma as decimal separator
        return locale.format_string("%.2f", value, grouping=True).replace('.', ',')

