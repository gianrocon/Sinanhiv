"""
SINAN — Sistema de Informação de Agravos de Notificação
Aplicação Streamlit para preenchimento e geração de fichas em PDF.

Para rodar:
    streamlit run app.py
"""

from __future__ import annotations

import tomllib
from pathlib import Path

import streamlit as st

from form_renderer import render_generic, get_fixed_fields
from pdf_filler import fill_pdf

_FICHAS_DIR = Path(__file__).parent / "fichas_sinan"

# ── Configuração da página ───────────────────────────────────────────────────

st.set_page_config(
    page_title="SINAN",
    page_icon=":hospital:",
    layout="wide",
)

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
/* Bordas visíveis — modo claro */
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] > div > div {
    border: 2px solid #555 !important;
    border-radius: 4px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #1565c0 !important;
    box-shadow: 0 0 0 2px rgba(21, 101, 192, 0.2) !important;
}
/* Bordas visíveis — modo escuro */
@media (prefers-color-scheme: dark) {
    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] > div > div {
        border: 2px solid #aaa !important;
    }
}
[data-theme="dark"] div[data-testid="stTextInput"] input,
[data-theme="dark"] div[data-testid="stSelectbox"] > div > div {
    border: 2px solid #aaa !important;
}
/* Rádios — substitui completamente o visual do Streamlit */
label[data-baseweb="radio"] > div:first-child {
    border: 3px solid #222 !important;
    background-color: #fff !important;
    box-shadow: none !important;
}
label[data-baseweb="radio"] > div:first-child > div {
    display: none !important;
}
label[data-baseweb="radio"]:has(input:checked) > div:first-child {
    box-shadow: inset 0 0 0 4px #1565c0 !important;
}
/* Rádios — modo escuro */
@media (prefers-color-scheme: dark) {
    label[data-baseweb="radio"] > div:first-child {
        border: 3px solid #ccc !important;
        background-color: #1e1e2e !important;
    }
    label[data-baseweb="radio"]:has(input:checked) > div:first-child {
        box-shadow: inset 0 0 0 4px #4d96ff !important;
    }
}
[data-theme="dark"] label[data-baseweb="radio"] > div:first-child {
    border: 3px solid #ccc !important;
    background-color: #1e1e2e !important;
}
[data-theme="dark"] label[data-baseweb="radio"]:has(input:checked) > div:first-child {
    box-shadow: inset 0 0 0 4px #4d96ff !important;
}
div[data-testid="stDownloadButton"] button {
    background-color: #28a745 !important;
    border-color: #28a745 !important;
    color: white !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background-color: #218838 !important;
    border-color: #1e7e34 !important;
}
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


# ── Descoberta de fichas disponíveis ────────────────────────────────────────

def _discover_forms() -> list[Path]:
    """Retorna pastas com field_coords.json (fichas mapeadas)."""
    if not _FICHAS_DIR.exists():
        return []
    return sorted(
        d for d in _FICHAS_DIR.iterdir()
        if d.is_dir() and (d / "field_coords.json").exists()
    )


def _load_form_meta(form_folder: Path) -> dict:
    cfg_path = form_folder / "config.toml"
    if cfg_path.exists():
        with open(cfg_path, "rb") as f:
            return tomllib.load(f).get("form", {})
    return {"name": form_folder.name}


def _form_is_ready(form_folder: Path) -> bool:
    """True se a ficha tem field_coords.json e config.toml com seção [form]."""
    if not (form_folder / "field_coords.json").exists():
        return False
    cfg_path = form_folder / "config.toml"
    if not cfg_path.exists():
        return False
    with open(cfg_path, "rb") as f:
        return "form" in tomllib.load(f)


# ── Telas ────────────────────────────────────────────────────────────────────

def _show_home() -> None:
    st.title("SINAN")
    st.markdown("#### Selecione a ficha de notificação")

    forms = _discover_forms()

    if not forms:
        st.info(
            "Nenhuma ficha disponível. "
            "Use a skill **sinan-coords-create** para mapear os campos de uma ficha PDF."
        )
        return

    # Grade de cards — até 3 por linha
    cols = st.columns(3)
    for i, form_folder in enumerate(forms):
        meta  = _load_form_meta(form_folder)
        name  = meta.get("name", form_folder.name)
        desc  = meta.get("description", "")
        ready = _form_is_ready(form_folder)

        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"**{name}**")
                if desc:
                    st.caption(desc)
                if ready:
                    if st.button("Abrir", key=f"open_{form_folder.name}",
                                 use_container_width=True):
                        st.session_state.current_form = str(form_folder)
                        st.rerun()
                else:
                    st.caption(":orange[Aguardando configuração — crie o config.toml]")
                    st.button("Abrir", key=f"open_{form_folder.name}",
                              use_container_width=True, disabled=True)


def _show_form(form_folder: Path) -> None:
    meta = _load_form_meta(form_folder)
    name = meta.get("name", form_folder.name)

    st.title(f"SINAN — {name}")

    if st.button("← Voltar à lista"):
        st.session_state.current_form = None
        st.rerun()

    gen_key = f"form_gen_{form_folder.name}"
    if gen_key not in st.session_state:
        st.session_state[gen_key] = 0

    form_data = render_generic(gen=st.session_state[gen_key], form_folder=form_folder)

    st.divider()

    _pdf_bytes = None
    _pdf_error = None
    try:
        all_data = {**form_data, **get_fixed_fields(form_folder)}
        # data_diagnostico = data do primeiro exame laboratorial disponível
        _data_diag = form_data.get("lab_triagem_data") or form_data.get("lab_rapidos_data")
        if _data_diag:
            all_data["data_diagnostico"] = _data_diag
        _pdf_bytes = fill_pdf(all_data, form_folder)
    except Exception as e:
        _pdf_error = e

    col1, col2 = st.columns(2)
    with col1:
        if _pdf_bytes is not None:
            file_name = f"notificacao_{form_folder.name.lower()}.pdf"
            st.download_button(
                label="Baixar PDF",
                data=_pdf_bytes,
                file_name=file_name,
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.error(f"Erro ao preparar PDF: {_pdf_error}")
    with col2:
        if st.button("Nova Notificação", use_container_width=True):
            st.session_state[gen_key] = st.session_state.get(gen_key, 0) + 1
            st.rerun()


# ── Roteamento ───────────────────────────────────────────────────────────────

if "current_form" not in st.session_state:
    st.session_state.current_form = None

if st.session_state.current_form is None:
    _show_home()
else:
    _show_form(Path(st.session_state.current_form))
