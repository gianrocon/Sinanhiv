"""
SINAN AIDS - Ficha de Notificacao/Investigacao
Aplicacao Streamlit para preenchimento e geracao do PDF.

Para rodar:
    streamlit run app.py
"""

import streamlit as st

from form_fields import get_fixed_fields, render_all_fields
from pdf_filler import fill_pdf

st.set_page_config(
    page_title="SINAN AIDS adulto",
    page_icon=":hospital:",
    layout="wide",
)

# Layout compacto + contraste nos campos
st.markdown("""
<style>
.block-container { padding-top: 0.8rem; padding-bottom: 0.5rem; }
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] { gap: 0rem; }
h3 { margin-top: 0.6rem !important; margin-bottom: 0.1rem !important; font-size: 1rem !important; }
hr { margin: 0.4rem 0 !important; }
div[data-testid="stRadio"] > label { font-size: 0.85rem; }
div[data-testid="stRadio"] { margin-bottom: 0rem; }
div[data-testid="stTextInput"] { margin-bottom: 0rem; }
div[data-testid="stSelectbox"] { margin-bottom: 0rem; }

/* Borda visivel nos inputs e selects (funciona em light e dark) */
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div > div {
    border: 1.5px solid rgba(150, 150, 150, 0.7) !important;
}
/* Circulos dos radio buttons — light mode */
div[data-testid="stRadio"] label > div:first-child {
    border: 2px solid #777 !important;
    box-shadow: 0 0 0 1px rgba(0,0,0,0.25) !important;
}
/* Circulos dos radio buttons — dark mode (preferencia do sistema) */
@media (prefers-color-scheme: dark) {
    div[data-testid="stRadio"] label > div:first-child {
        border: 2px solid #bbb !important;
        box-shadow: 0 0 0 1px rgba(255,255,255,0.2) !important;
    }
}
/* Circulos dos radio buttons — dark mode (toggle do Streamlit) */
[data-theme="dark"] div[data-testid="stRadio"] label > div:first-child {
    border: 2px solid #bbb !important;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.2) !important;
}
/* Botao Baixar PDF — verde */
div[data-testid="stDownloadButton"] button {
    background-color: #28a745 !important;
    border-color: #28a745 !important;
    color: white !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background-color: #218838 !important;
    border-color: #1e7e34 !important;
}
/* Botao Nova Notificacao — azul */
div[data-testid="stButton"] button {
    background-color: #1565c0 !important;
    border-color: #1565c0 !important;
    color: white !important;
}
div[data-testid="stButton"] button:hover {
    background-color: #0d47a1 !important;
    border-color: #0d47a1 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("SINAN AIDS adulto")

# Contador de geracao do formulario — incrementar forca reset para os defaults
if "form_gen" not in st.session_state:
    st.session_state["form_gen"] = 0

form_data = render_all_fields(gen=st.session_state["form_gen"])

st.divider()

# Pre-gera o PDF com os dados atuais do formulario
_pdf_bytes = None
_pdf_error = None
try:
    _all_data = {**form_data, **get_fixed_fields()}
    _data_diag = form_data.get("lab_triagem_data") or form_data.get("lab_rapidos_data")
    if _data_diag:
        _all_data["data_diagnostico"] = _data_diag
    _pdf_bytes = fill_pdf(_all_data)
except Exception as e:
    _pdf_error = e

col1, col2 = st.columns(2)

with col1:
    if _pdf_bytes is not None:
        st.download_button(
            label="Baixar PDF",
            data=_pdf_bytes,
            file_name="notificacao_aids.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.error(f"Erro ao preparar PDF: {_pdf_error}")

with col2:
    if st.button("Nova Notificacao", use_container_width=True):
        # Incrementa o contador — forca recriacao dos widgets com seus defaults
        st.session_state["form_gen"] = st.session_state.get("form_gen", 0) + 1
        st.rerun()
