# SINAN — Preenchimento de Fichas em PDF

Aplicação Streamlit para preencher fichas do Sistema de Informação de Agravos de Notificação (SINAN) em PDF, com importação de dados cadastrais direto do sistema VIDA.

Disponível em: **[sinanhiv.streamlit.app](https://sinanhiv.streamlit.app)**

## Funcionalidades

- Preenchimento das fichas **SINAN AIDS Adulto** e **SINAN Tuberculose**
- Geração de PDFs preenchidos para download (ficha SINAN, SICLOM, Carga Viral, CD4)
- Importação de dados do paciente via bookmarklet do sistema VIDA (nome, cartão SUS, data de nascimento, nome da mãe, prontuário)
- Navegação cruzada entre fichas com transferência automática dos campos em comum

## Importação via bookmarklet VIDA

O link **(configurar)** no topo de qualquer ficha exibe o passo a passo para instalar o bookmarklet no navegador. Após instalado:

1. Abra o prontuário do paciente no sistema VIDA
2. Clique no favorito **"VIDA - Copiar dados"** na barra de favoritos
3. Volte para esta aba e cole o texto no campo de importação (Ctrl+V)

Os campos reconhecidos são preenchidos automaticamente no formulário.

## Rodando localmente

```bash
streamlit run app.py
```

Requer Python 3.14+ e as dependências em `requirements.txt`.

## Estrutura

```
fichas_sinan/
  Aids_adulto_v5/      # Ficha AIDS: PDF, config.toml, field_coords.json
  Tuberculose_v5/      # Ficha TB:   PDF, config.toml, field_coords.json
bookmarklet_vida/
  SCRIPT.js            # Código do bookmarklet (extrai dados do DOM do VIDA)
app.py                 # Roteamento e orquestração Streamlit
form_renderer.py       # Renderização genérica de formulários
pdf_filler.py          # Preenchimento de PDF com coordenadas
clipboard_import.py    # Parser do texto copiado pelo bookmarklet
```
