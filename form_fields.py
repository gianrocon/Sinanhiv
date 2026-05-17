"""
Widgets Streamlit para todos os campos da Ficha SINAN AIDS Adulto.

- render_all_fields(gen): campos visiveis ao usuario, retorna dict {campo: valor}
- get_fixed_fields():     campos ocultos injetados automaticamente no PDF
"""

from __future__ import annotations

import tomllib
from datetime import date, datetime
from pathlib import Path

import streamlit as st

_CFG_PATH = Path(__file__).parent / "config.toml"

# Sufixo de geracao — muda ao clicar em "Nova Notificacao", forcando reset dos widgets
_FORM_GEN: int = 0


def _k(key: str) -> str:
    """Retorna a key do widget com o sufixo de geracao atual."""
    return f"{key}_{_FORM_GEN}"


def _load_cfg() -> dict:
    try:
        with open(_CFG_PATH, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        return {}


def get_fixed_fields() -> dict:
    """
    Campos ocultos — nao aparecem no formulario.
    Injetados automaticamente em app.py antes de chamar fill_pdf().
    """
    cfg = _load_cfg()
    fixed: dict = dict(cfg.get("fixed", {}))

    # Data de notificacao = hoje (dinamico)
    fixed["data_notificacao"] = date.today()

    # Campos em branco (ignorados pelo pdf_filler)
    _blank = [
        "numero_notificacao",
        "data_diagnostico",           # preenchido em app.py com data do lab
        "idade_valor", "idade_unidade",
        "ibge_municipio_resid", "distrito", "codigo_logradouro", "pais_exterior",
        "geo_campo1", "geo_campo2", "ponto_referencia", "zona",
        "ibge_municipio_transfusao", "codigo_instituicao",
        "criterio_obito",
        "uf_tratamento", "municipio_tratamento", "ibge_municipio_tratamento",
        "unidade_tratamento", "codigo_unidade_tratamento",
        "evolucao_caso", "data_obito",
        "investigador_nome", "investigador_funcao",
    ]
    for f in _blank:
        fixed.setdefault(f, "")

    return fixed


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _date_input(label: str, key: str) -> date | None:
    """Campo de texto para data. Aceita dd/mm/yyyy ou ddmmyyyy."""
    raw = st.text_input(label, placeholder="dd/mm/aaaa", key=_k(key))
    if not raw:
        return None
    for fmt in ("%d/%m/%Y", "%d%m%Y"):
        try:
            return datetime.strptime(raw.strip(), fmt).date()
        except ValueError:
            continue
    st.error(f"Data invalida: use dd/mm/aaaa ou ddmmaaaa")
    return None


def _radio3(label: str, key: str, index: int = 1) -> str:
    """Radio Sim/Nao/Ignorado retornando '1', '2' ou '9'."""
    opts = {"Sim (1)": "1", "Nao (2)": "2", "Ignorado (9)": "9"}
    choice = st.radio(label, list(opts.keys()), index=index,
                      horizontal=True, key=_k(key))
    return opts[choice]


def _radio_rapido(label: str, key: str) -> str:
    """Radio Positivo/Negativo/Inconclusivo sem selecao padrao."""
    opts = {"1 - Positivo": "1", "2 - Negativo": "2", "3 - Inconclusivo": "3"}
    choice = st.radio(label, list(opts.keys()), index=None,
                      horizontal=True, key=_k(key))
    return opts[choice] if choice else ""


# ---------------------------------------------------------------------------
# Formulario principal
# ---------------------------------------------------------------------------

def render_all_fields(gen: int = 0) -> dict:
    """Renderiza os campos visiveis e retorna o dicionario de dados."""
    global _FORM_GEN
    _FORM_GEN = gen

    d = _load_cfg().get("defaults", {})
    data: dict = {}

    # numero_notificacao e data_notificacao: OCULTOS

    st.subheader("Unidade de Saude")
    c1, c2 = st.columns([4, 2])
    with c1:
        data["unidade_saude"] = st.text_input(
            "Unidade Notificadora",
            value=d.get("unidade_saude", ""),
            key=_k("unidade_saude"))
    with c2:
        data["codigo_unidade_saude"] = st.text_input(
            "CNES",
            value=d.get("codigo_unidade_saude", ""),
            max_chars=8,
            key=_k("codigo_unidade_saude"))

    st.divider()
    st.subheader("Paciente")

    # Nome + Nascimento + Sexo na mesma linha
    c1, c2, c3 = st.columns([5, 1.4, 1])
    with c1:
        data["nome_paciente"] = st.text_input(
            "Nome Completo",
            placeholder="NOME COMPLETO EM MAIUSCULO",
            key=_k("nome_paciente"))
    with c2:
        data["data_nascimento"] = _date_input("Nascimento", "dt_nasc")
    with c3:
        sexo_opts = ["M - Masculino", "F - Feminino", "I - Ignorado"]
        data["sexo"] = st.selectbox("Sexo", sexo_opts, index=0, key=_k("sexo"))[0]

    # Gestante + Raca + Escolaridade
    c1, c2, c3 = st.columns([1.8, 1.5, 2])
    with c1:
        gestante_opts = [
            "1 - 1o Trimestre", "2 - 2o Trimestre", "3 - 3o Trimestre",
            "4 - IG Ignorada", "5 - Nao", "6 - Nao se aplica", "9 - Ignorado"]
        data["gestante"] = st.selectbox(
            "Gestante", gestante_opts, index=5, key=_k("gestante"))[0]
    with c2:
        raca_opts = [
            "1 - Branca", "2 - Preta", "3 - Amarela",
            "4 - Parda", "5 - Indigena", "9 - Ignorado"]
        data["raca_cor"] = st.selectbox(
            "Raca/Cor", raca_opts, index=3, key=_k("raca_cor"))[0]
    with c3:
        esc_opts = [
            "0 - Analfabeto",
            "1 - 1a a 4a serie incompleta EF",
            "2 - 4a serie completa EF",
            "3 - 5a a 8a serie incompleta EF",
            "4 - EF completo",
            "5 - EM incompleto",
            "6 - EM completo",
            "7 - Superior incompleto",
            "8 - Superior completo",
            "9 - Ignorado",
            "10 - Nao se aplica"]
        data["escolaridade"] = st.selectbox(
            "Escolaridade", esc_opts, index=9, key=_k("escolaridade"))[0:2].strip()

    # idade_valor e idade_unidade: OCULTOS e em branco

    # Cartao SUS + Nome da Mae
    c1, c2 = st.columns([1.2, 2.8])
    with c1:
        data["cartao_sus"] = st.text_input(
            "Cartao SUS", max_chars=15, placeholder="15 digitos",
            key=_k("cartao_sus"))
    with c2:
        data["nome_mae"] = st.text_input("Nome da Mae", key=_k("nome_mae"))

    st.divider()
    st.subheader("Residencia")

    # UF (estreito) + Municipio + Bairro na mesma linha
    c1, c2, c3 = st.columns([0.5, 2.5, 2])
    with c1:
        data["uf_residencia"] = st.text_input(
            "UF", value=d.get("uf_residencia", ""), max_chars=2,
            key=_k("uf_res"))
    with c2:
        data["municipio_residencia"] = st.text_input(
            "Municipio", value=d.get("municipio_residencia", ""),
            key=_k("municipio_res"))
    with c3:
        data["bairro"] = st.text_input("Bairro", key=_k("bairro"))

    # Logradouro + Numero (estreito) + Complemento
    c1, c2, c3 = st.columns([4, 0.8, 2])
    with c1:
        data["logradouro"] = st.text_input("Logradouro", key=_k("logradouro"))
    with c2:
        data["numero_residencia"] = st.text_input("No", key=_k("numero_res"))
    with c3:
        data["complemento"] = st.text_input("Complemento", key=_k("complemento"))

    # CEP + Telefone (estreitos, resto vazio)
    c1, c2, c3 = st.columns([1.2, 1.5, 3.3])
    with c1:
        data["cep"] = st.text_input(
            "CEP", max_chars=9, placeholder="XXXXX-XXX", key=_k("cep"))
    with c2:
        data["ddd_telefone"] = st.text_input("Telefone", key=_k("telefone"))

    st.divider()
    st.subheader("Complementar")
    data["ocupacao"] = st.text_input(
        "Ocupacao / Ramo de Atividade", key=_k("ocupacao"))

    st.divider()
    st.subheader("Transmissao")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Vertical**")
        tv_opts = {
            "1 - Sim": "1",
            "2 - Nao foi transmissao vertical": "2",
            "9 - Ignorado": "9"}
        tv = st.radio("Vertical", list(tv_opts.keys()),
                      index=1, horizontal=False, key=_k("tv"),
                      label_visibility="collapsed")
        data["transmissao_vertical"] = tv_opts[tv]
    with c2:
        st.markdown("**Sexual**")
        sx_opts = {
            "1 - Relacoes sexuais com homens": "1",
            "2 - Relacoes sexuais com mulheres": "2",
            "3 - Relacoes sexuais com homens e mulheres": "3",
            "4 - Nao foi transmissao sexual": "4",
            "9 - Ignorado": "9"}
        sx = st.radio("Sexual", list(sx_opts.keys()),
                      index=0, horizontal=False, key=_k("sx"),
                      label_visibility="collapsed")
        data["transmissao_sexual"] = sx_opts[sx]

    st.markdown("**Sanguinea**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        data["sanguinea_drogas"] = _radio3("Drogas injetaveis", "drg")
    with c2:
        data["sanguinea_hemofilia"] = _radio3("Hemotransfusao / hemofilia", "hmf")
    with c3:
        data["sanguinea_transfusao"] = _radio3("Transfusao sanguinea", "tfs")
    with c4:
        data["sanguinea_acidente"] = _radio3("Acidente c/ material biologico", "acm")

    # Campos 35-39 condicionais (transfusao ou acidente = Sim)
    if data.get("sanguinea_transfusao") == "1" or data.get("sanguinea_acidente") == "1":
        st.markdown("**Transfusao / Acidente**")
        c1, c2, c3 = st.columns([1, 1, 3])
        with c1:
            data["data_transfusao_acidente"] = _date_input("Data", "dt_tfs")
        with c2:
            data["uf_transfusao"] = st.text_input(
                "UF", max_chars=2, key=_k("uf_tfs"))
        with c3:
            data["municipio_transfusao"] = st.text_input(
                "Municipio", key=_k("mun_tfs"))

        data["instituicao_transfusao"] = st.text_input(
            "Instituicao", key=_k("instituicao_tfs"))

        causa_opts = ["", "1 - Sim", "2 - Nao", "3 - Nao se aplica"]
        causa_sel = st.selectbox(
            "A transfusao/acidente foi causa da infeccao pelo HIV?",
            causa_opts, key=_k("causa"))
        data["transfusao_foi_causa"] = causa_sel[0] if causa_sel else ""

    st.divider()
    # Laboratorio — sem titulo, separadores entre secoes
    st.markdown("**Triagem com IE 3ª/4ª G**")
    c1, c2 = st.columns(2)
    with c1:
        data["lab_triagem_resultado"] = _radio_rapido("Resultado", "tr1")
    with c2:
        data["lab_triagem_data"] = _date_input("Data da coleta", "dt_tr1")

    st.divider()
    st.markdown("**Triagem com Testes Rápidos**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        data["lab_rapido1_resultado"] = _radio_rapido("Rapido 1", "rp1")
    with c2:
        data["lab_rapido2_resultado"] = _radio_rapido("Rapido 2", "rp2")
    with c3:
        data["lab_rapido3_resultado"] = _radio_rapido("Rapido 3", "rp3")
    with c4:
        data["lab_rapidos_data"] = _date_input("Data da coleta", "dt_rp")

    st.divider()
    resultado_opts_conf = [
        "",
        "1 - Positivo/reagente",
        "2 - Negativo/nao reagente",
        "3 - Inconclusivo",
        "4 - Nao realizado",
        "9 - Ignorado"]

    def _res(sel: str) -> str:
        return sel[0] if sel else ""

    st.markdown("**Confirmatorio**")
    c1, c2 = st.columns(2)
    with c1:
        data["lab_confirmatorio_resultado"] = _res(st.selectbox(
            "Resultado", resultado_opts_conf, index=4, key=_k("tr2")))
    with c2:
        data["lab_confirmatorio_data"] = _date_input("Data da coleta", "dt_tr2")

    st.divider()
    st.subheader("Criterio Rio de Janeiro/Caracas")
    itens_rj_esq = [
        ("rj_sarcoma_kaposi",  "Sarcoma de Kaposi (10 pts)"),
        ("rj_tb_disseminada",  "Tuberculose disseminada/extra-pulmonar/nao cavitaria (10)"),
        ("rj_candidose_oral",  "Candidose oral ou leucoplasia pilosa (5)"),
        ("rj_tb_pulmonar",     "Tuberculose pulmonar cavitaria ou nao especificada (5)"),
        ("rj_herpes_zoster",   "Herpes zoster em individuo <= 60 anos (5)"),
        ("rj_disfuncao_snc",   "Disfuncao do sistema nervoso central (5)"),
        ("rj_diarreia",        "Diarreia >= 1 mes (2)"),
        ("rj_febre",           "Febre >= 38oC por >= 1 mes (2)*"),
    ]
    itens_rj_dir = [
        ("rj_caquexia",       "Caquexia ou perda de peso > 10% (2)*"),
        ("rj_astenia",        "Astenia >= 1 mes (2)*"),
        ("rj_dermatite",      "Dermatite persistente (2)"),
        ("rj_anemia",         "Anemia e/ou linfopenia e/ou trombocitopenia (2)"),
        ("rj_tosse",          "Tosse persistente ou qualquer pneumonia (2)*"),
        ("rj_linfadenopatia", "Linfadenopatia >= 1cm, >= 2 sitios extra-inguinais >= 1 mes (2)"),
    ]
    st.caption("*Excluida a tuberculose como causa")
    c1, c2 = st.columns(2)
    with c1:
        for key, label in itens_rj_esq:
            data[key] = _radio3(label, key)
    with c2:
        for key, label in itens_rj_dir:
            data[key] = _radio3(label, key)

    st.divider()
    st.subheader("Criterio CDC")
    itens_cdc_esq = [
        ("cdc_cancer_cervical",    "Cancer cervical invasivo"),
        ("cdc_candidose_esofago",  "Candidose de esofago"),
        ("cdc_candidose_traqueia", "Candidose de traqueia, bronquios ou pulmao"),
        ("cdc_citomegalovirose",   "Citomegalovirose (exceto figado, baco ou linfonodos)"),
        ("cdc_criptococose",       "Criptococose extrapulmonar"),
        ("cdc_criptosporidiose",   "Criptosporidiose intestinal cronica > 1 mes"),
        ("cdc_herpes_simples",     "Herpes simples mucocutaneo > 1 mes"),
        ("cdc_histoplasmose",      "Histoplasmose disseminada"),
        ("cdc_isosporidiose",      "Isosporidiose intestinal cronica > 1 mes"),
    ]
    itens_cdc_dir = [
        ("cdc_leucoencefalopatia", "Leucoencefalopatia multifocal progressiva"),
        ("cdc_linfoma_hodgkin",    "Linfoma nao Hodgkin e outros linfomas"),
        ("cdc_linfoma_cerebro",    "Linfoma primario do cerebro"),
        ("cdc_micobacteriose",     "Micobacteriose disseminada (exceto TB e hanseniase)"),
        ("cdc_pneumonia_pcp",      "Pneumonia por Pneumocystis carinii"),
        ("cdc_reativacao_chagas",  "Reativacao de doenca de Chagas (meningoencefalite/miocardite)"),
        ("cdc_salmonelose",        "Salmonelose (sepse recorrente nao-tifoide)"),
        ("cdc_toxoplasmose",       "Toxoplasmose cerebral"),
    ]
    c1, c2 = st.columns(2)
    with c1:
        for key, label in itens_cdc_esq:
            data[key] = _radio3(label, key)
    with c2:
        for key, label in itens_cdc_dir:
            data[key] = _radio3(label, key)
        # cdc_cd4_350: padrao 9 (Ignorado)
        data["cdc_cd4_350"] = _radio3(
            "Contagem de linfocitos T CD4+ menor que 350 cel/mm3",
            "cdc_cd4_350", index=2)

    # Campos 43-48 e Investigador: OCULTOS — injetados por get_fixed_fields()

    return data
