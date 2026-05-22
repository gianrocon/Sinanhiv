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
Campos em [form] sni_fields recebem radio Sim/Não/Ignorado automaticamente,
independente do prefixo.

Opções em [fields.<campo>]:
  options       → lista de rótulos exibidos
  values        → lista de valores retornados (1:1 com options); se ausente, retorna o rótulo
  widget        → "selectbox" (padrão) ou "radio"
  default_index → índice selecionado por padrão (padrão: 0)
  horizontal    → true (padrão) ou false; só para widget="radio"
  allow_none    → true para radio sem seleção padrão (retorna "" se nada selecionado)
"""

from __future__ import annotations

import json
import tomllib
from datetime import date, datetime
from pathlib import Path

import streamlit as st

_GEN: int = 0

_SNI_OPTIONS = ["Sim (1)", "Não (2)", "Ignorado (9)"]
_SNI_VALUES  = ["1", "2", "9"]


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
    """Retorna campos ocultos: [fixed] com valores fixos + [hidden] como vazios."""
    cfg = _load_cfg(form_folder)
    fixed: dict = dict(cfg.get("fixed", {}))

    if "data_notificacao" in _load_coords_raw(form_folder):
        fixed.setdefault("data_notificacao", date.today())

    for field in cfg.get("hidden", {}).get("campos", []):
        fixed.setdefault(field, "")

    return fixed


# ---------------------------------------------------------------------------
# Widgets auxiliares
# ---------------------------------------------------------------------------

def _date_input(label: str, key: str, default: str = "") -> date | None:
    raw = st.text_input(label, value=default, placeholder="dd/mm/aaaa", key=_k(key))
    if not raw:
        return None
    for fmt in ("%d/%m/%Y", "%d%m%Y"):
        try:
            return datetime.strptime(raw.strip(), fmt).date()
        except ValueError:
            continue
    st.error("Data inválida: use dd/mm/aaaa ou ddmmaaaa")
    return None


def _radio_sni(label: str, key: str, default_index: int = 1) -> str:
    """Radio padrão Sim/Não/Ignorado."""
    choice = st.radio(label, _SNI_OPTIONS, index=default_index,
                      horizontal=True, key=_k(key))
    return _SNI_VALUES[_SNI_OPTIONS.index(choice)]


def _resolve_value(choice, opts: list, values: list | None) -> str:
    """Retorna o código correspondente à opção selecionada."""
    if choice is None:
        return ""
    if values is None:
        return choice
    try:
        return values[opts.index(choice)]
    except (ValueError, IndexError):
        return choice


def _widget_for(field: str, label: str, default: str,
                cfg_field: dict, sni_set: set) -> str | date | None:
    """Escolhe o widget adequado para o campo."""
    prefix = field.split("_")[0]

    # Campos listados explicitamente em [form] sni_fields → Sim/Não/Ignorado
    if field in sni_set:
        sni_default = int(cfg_field.get("default_index", 1))
        return _radio_sni(label, field, default_index=sni_default)

    # Opções customizadas em [fields.<campo>]
    if "options" in cfg_field:
        opts          = cfg_field["options"]
        values        = cfg_field.get("values")
        widget        = cfg_field.get("widget", "selectbox")
        default_index = int(cfg_field.get("default_index", 0))
        horizontal    = bool(cfg_field.get("horizontal", True))
        allow_none    = bool(cfg_field.get("allow_none", False))

        if widget == "radio":
            idx    = None if allow_none else default_index
            choice = st.radio(label, opts, index=idx,
                              horizontal=horizontal, key=_k(field))
            return _resolve_value(choice, opts, values)
        else:
            choice = st.selectbox(label, opts, index=default_index,
                                  key=_k(field))
            return _resolve_value(choice, opts, values)

    # Data
    if prefix in ("dt", "data"):
        return _date_input(label, field, default=default)

    # Booleano SINAN por prefixo (st_*)
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
    Renderiza o formulário a partir do field_coords.json e config.toml da ficha.
    Retorna {campo: valor} com os dados preenchidos pelo usuário.
    """
    global _GEN
    _GEN = gen

    if form_folder is None:
        raise ValueError("form_folder é obrigatório para o renderer genérico")

    cfg        = _load_cfg(form_folder)
    coords_raw = _load_coords_raw(form_folder)

    defaults    = cfg.get("defaults", {})
    fixed_keys  = set(cfg.get("fixed", {}).keys())
    hidden_keys = set(cfg.get("hidden", {}).get("campos", []))
    fields_cfg  = cfg.get("fields", {})
    sni_fields  = set(cfg.get("form", {}).get("sni_fields", []))
    skip_keys   = fixed_keys | hidden_keys
    if "data_notificacao" in coords_raw:
        skip_keys.add("data_notificacao")

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
            if default == "today":
                default = date.today().strftime("%d/%m/%Y")
            cfg_f   = fields_cfg.get(field, {})

            value = _widget_for(field, label, default, cfg_f, sni_fields)
            data[field] = value

    return data
