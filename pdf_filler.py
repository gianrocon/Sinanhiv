"""
Motor de preenchimento do PDF SINAN via sobreposicao de texto (PyMuPDF).

O arquivo original nunca e modificado — esta funcao retorna bytes do novo PDF.
"""

from __future__ import annotations

import tomllib
from datetime import date
from pathlib import Path

import fitz  # PyMuPDF

from field_coords import ALL_FIELDS

_CFG_PATH = Path(__file__).parent / "config.toml"
_PDF_PATH = Path(__file__).parent / "fichas_sinan" / "Aids_adulto_v5" / "Aids_adulto_v5.pdf"


def _load_app_config() -> dict:
    with open(_CFG_PATH, "rb") as f:
        return tomllib.load(f).get("app", {})


# Fragmentos de nome de campo que requerem fundo branco sob o texto
_WHITE_BG_KEYWORDS = ("codigo", "ibge", "cep", "telefone", "cartao")

# Campos que devem ser convertidos para maiusculas antes de inserir no PDF
_UPPERCASE_FIELDS = {
    "nome_paciente", "nome_mae",
    "uf_residencia", "municipio_residencia",
    "bairro", "logradouro", "ocupacao",
}


def _needs_white_bg(field_name: str, raw_value) -> bool:
    """Retorna True se o campo deve ter fundo branco antes do texto."""
    if isinstance(raw_value, date):
        return True
    name = field_name.lower()
    return any(kw in name for kw in _WHITE_BG_KEYWORDS)


def _draw_white_bg(page, x: float, y: float, text: str,
                   fontname: str, fontsize: float) -> None:
    """Desenha retangulo branco cobrindo a area do texto a ser inserido."""
    text_w = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)
    pad_x, pad_top, pad_bot = 1.0, fontsize * 0.85, fontsize * 0.15
    rect = fitz.Rect(x - pad_x, y - pad_top, x + text_w + pad_x, y + pad_bot)
    page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)


def fill_pdf(form_data: dict) -> bytes:
    """
    Preenche o PDF com os dados do formulario e retorna os bytes do arquivo gerado.

    Args:
        form_data: dicionario {nome_campo: valor} com os dados a inserir.
                   Valores None, False e strings vazias sao ignorados.

    Returns:
        bytes do PDF preenchido, prontos para st.download_button.
    """
    cfg = _load_app_config()
    font_name = cfg.get("font_name", "helv")
    font_size = float(cfg.get("font_size", 7))
    font_size_date = float(cfg.get("font_size_date", font_size))
    font_size_number = float(cfg.get("font_size_number", round(font_size * 0.8, 1)))
    black = (0.0, 0.0, 0.0)

    doc = fitz.open(str(_PDF_PATH))

    for field_name, raw_value in form_data.items():
        # Ignorar campos vazios / nulos / False
        if raw_value is None or raw_value == "" or raw_value is False:
            continue
        if isinstance(raw_value, bool) and not raw_value:
            continue

        coords = ALL_FIELDS.get(field_name)
        if coords is None:
            continue  # campo nao mapeado

        page_num, x, y = coords
        page = doc[page_num - 1]  # PyMuPDF: paginas 0-indexadas

        # Formatar valor
        if isinstance(raw_value, date):
            value = raw_value.strftime("%d/%m/%Y")
            fs = font_size_date
        else:
            value = str(raw_value).strip()
            if field_name in _UPPERCASE_FIELDS:
                value = value.upper()
            fs = font_size_number if _needs_white_bg(field_name, raw_value) else font_size

        if not value:
            continue

        if _needs_white_bg(field_name, raw_value):
            _draw_white_bg(page, x, y, value, font_name, fs)

        page.insert_text(
            fitz.Point(x, y),
            value,
            fontname=font_name,
            fontsize=fs,
            color=black,
        )

    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


# ── Teste standalone ────────────────────────────────────────────────────────
if __name__ == "__main__":
    from paciente_teste import DADOS_TESTE

    out = fill_pdf(DADOS_TESTE)
    _out = Path(__file__).parent / "fichas_sinan" / "Aids_adulto_v5" / "teste_output.pdf"
    _out.write_bytes(out)
    print(f"Arquivo gerado: {_out}")
    print("Abra e verifique o alinhamento dos campos.")
    print("Se necessario, ajuste as coordenadas em field_coords.py")
