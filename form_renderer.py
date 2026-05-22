"""
Renderer genérico para qualquer ficha SINAN.

Lê field_coords.json e config.toml da pasta da ficha e gera widgets
automaticamente com base nos prefixos dos nomes dos campos (convenção SINAN):

  dt_*          → campo de data (dd/mm/aaaa)
  nm_*, no_*    → texto livre (nome)
  sg_uf_*, *_uf → texto curto (sigla UF, 2 chars)
  nu_*          → texto (número/código)
  co_*, id_*    → texto (código/ID)
  st_*          → Sim / Não / Ignorado (radio)
  cs_*, tp_*    → opções definidas em [fields.<campo>] ou texto livre

Campos em [fixed] e [hidden] são omitidos do formulário.
Valores padrão vêm de [defaults].
"""

from __future__ import annotations

import json
import tomllib
from datetime import date, datetime
from pathlib import Path

import streamlit as st

_GEN: int = 0


def _k(key: str) -> str:
    return f"{key}_{_GEN}"


def _load_cfg(form_folder: Path) -> dict:
    cfg_path = form_folder / "config.toml"
    if not cfg_path.exists():
        return {}
    with open(cfg_path, "rb") as f:
        return tomllib.load(f)


def _load_coords_raw(form_folder: Path) -> dict:
    with open(form_folder / "field_coords.json", encoding="utf-8") as f:
        return json.load(f)


def get_fixed_fields(form_folder: Path) -> dict:
    """
    Retorna campos ocultos: [fixed] com valores fixos + [hidden] como vazios.
    """
    cfg = _load_cfg(form_folder)
    fixed: dict = dict(cfg.get("fixed", {}))

    # data de notificação é sempre hoje
    if "data_notificacao" in _load_coords_raw(form_folder):
        fixed.setdefault("data_notificacao", date.today())

    for field in cfg.get("hidden", {}).get("campos", []):
        fixed.setdefault(field, "")

    return fixed


# ---------------------------------------------------------------------------
# Widgets auxiliares
# ---------------------------------------------------------------------------

def _date_input(label: str, key: str) -> date | None:
    raw = st.text_input(label, placeholder="dd/mm/aaaa", key=_k(key))
    if not raw:
        return None
    for fmt in ("%d/%m/%Y", "%d%m%Y"):
        try:
            return datetime.strptime(raw.strip(), fmt).date()
        except ValueError:
            continue
    st.error("Data inválida: use dd/mm/aaaa ou ddmmaaaa")
    return None


def _radio_sni(label: str, key: str) -> str:
    """Radio padrão Sim/Não/Ignorado."""
    opts = {"Sim (1)": "1", "Não (2)": "2", "Ignorado (9)": "9"}
    choice = st.radio(label, list(opts.keys()), index=1,
                      horizontal=True, key=_k(key))
    return opts[choice]


def _widget_for(field: str, label: str, default: str, cfg_field: dict) -> str | date | None:
    """Escolhe o widget adequado para o campo."""
    prefix = field.split("_")[0]

    # Opções customizadas em config.toml [fields.<campo>]
    if "options" in cfg_field:
        opts = cfg_field["options"]
        widget = cfg_field.get("widget", "selectbox")
        default_index = int(cfg_field.get("default_index", 0))
        if widget == "radio":
            choice = st.radio(label, opts, index=default_index,
                              horizontal=True, key=_k(field))
            return choice
        else:
            choice = st.selectbox(label, opts, index=default_index,
                                  key=_k(field))
            return choice

    # Data
    if prefix == "dt":
        return _date_input(label, field)

    # Booleano SINAN (st_*): Sim/Não/Ignorado
    if prefix == "st":
        return _radio_sni(label, field)

    # UF (2 chars)
    if "uf" in field and prefix in ("sg", "co", "id", ""):
        return st.text_input(label, value=default, max_chars=2, key=_k(field))

    # Texto livre para o restante
    return st.text_input(label, value=default, key=_k(field))


# ---------------------------------------------------------------------------
# Renderer principal
# ---------------------------------------------------------------------------

def render_generic(gen: int = 0, form_folder: Path | None = None) -> dict:
    """
    Renderiza o formulário genérico a partir do field_coords.json e config.toml.
    Retorna {campo: valor} com os dados preenchidos pelo usuário.
    """
    global _GEN
    _GEN = gen

    if form_folder is None:
        raise ValueError("form_folder é obrigatório para o renderer genérico")

    cfg = _load_cfg(form_folder)
    coords_raw = _load_coords_raw(form_folder)

    defaults     = cfg.get("defaults", {})
    fixed_keys   = set(cfg.get("fixed", {}).keys())
    hidden_keys  = set(cfg.get("hidden", {}).get("campos", []))
    fields_cfg   = cfg.get("fields", {})
    skip_keys    = fixed_keys | hidden_keys

    # Agrupa campos por página, na ordem y crescente (leitura natural da ficha)
    by_page: dict[int, list[tuple[float, str, dict]]] = {}
    for field, meta in coords_raw.items():
        if field in skip_keys:
            continue
        p = meta["page"]
        by_page.setdefault(p, []).append((meta["y"], field, meta))

    data: dict = {}

    for page_num in sorted(by_page.keys()):
        st.subheader(f"Página {page_num}")
        fields_on_page = sorted(by_page[page_num], key=lambda t: t[0])

        for _, field, meta in fields_on_page:
            label   = meta.get("label", field)
            default = str(defaults.get(field, ""))
            cfg_f   = fields_cfg.get(field, {})

            value = _widget_for(field, label, default, cfg_f)
            data[field] = value

    return data
