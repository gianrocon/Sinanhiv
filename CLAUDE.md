# CLAUDE.md — Projeto SINAN

## Idioma
Responda sempre em **português brasileiro**. Mensagens de commit, comentários de código e toda comunicação devem estar em pt-BR.

## Ambiente Python
- Interpretador: sempre usar `.venv\Scripts\python.exe` (nunca `python`, `python3` ou `py`)
- Versão: **Python 3.14.4**
- O venv já existe na raiz do projeto; não recriar sem motivo explícito

## Plataforma de deploy
- O app é servido via **Streamlit Community Cloud** em `sinanhiv.streamlit.app`
- Ao fazer alterações, considerar compatibilidade com o Streamlit Cloud:
  - Arquivos de configuração ficam em `fichas_sinan/<nome_ficha>/config.toml`
  - PDFs da ficha ficam em `fichas_sinan/<nome_ficha>/`
  - Dependências declaradas em `requirements.txt` na raiz
- Para testar localmente: `streamlit run app.py`

## Encoding — regras obrigatórias
- **PowerShell 5.1** (padrão no Windows) não suporta `-Encoding utf8NoBOM`; usar `.NET`:
  ```powershell
  [System.IO.File]::WriteAllText("caminho.json", $conteudo, [System.Text.UTF8Encoding]::new($false))
  ```
- Definir `$env:PYTHONIOENCODING = "utf-8"` antes de rodar scripts Python que imprimem JSON no terminal
- Scripts Python que imprimem para stdout devem incluir no topo quando necessário:
  ```python
  import sys, io
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
  ```
- Ler JSONs com `encoding="utf-8-sig"` para tolerar BOM acidental
- Salvar JSONs via Python com `open(path, "w", encoding="utf-8")`
- **Nunca** usar `Out-File` sem especificar encoding; preferir `[System.IO.File]::WriteAllText`

## Convenções de campo — field_coords.json

- Campos UI-only (aparecem no formulário Streamlit mas **não** devem ser escritos no PDF SINAN) recebem `"skip_pdf": true` no `field_coords.json`.
- `pdf_filler._load_coords` filtra automaticamente entradas com `skip_pdf: true`.
- Exemplo: campo `cpf` da ficha AIDS — presente no formulário e nos PDFs de CV/CD4, ausente no PDF SINAN.

## Formulários de exames laboratoriais

- `carga_viral_filler.py` e `cd4_filler.py` preenchem PDFs em `forms_externos/`.
- Ambos recebem o mesmo `form_data` da ficha AIDS (incluindo campos comuns como `cpf`).
- Novas versões desses formulários devem seguir o mesmo padrão: `_FIELDS` com `(chave, x, y, font_size_base)`, `_FS = 1.2` como multiplicador.

## Roteamento de páginas (app.py)

O app tem três telas controladas por `st.session_state`:

| Estado | Tela exibida |
|---|---|
| `current_form = None` | Home (lista de fichas) |
| `current_form = "<caminho>"` | Formulário da ficha |
| `show_config = True` | Página de configuração do bookmarklet |

O link `(configurar)` usa `<a href='?show_config=1'>` (HTML inline no `st.markdown`). O roteamento detecta o query param, limpa-o e seta `show_config = True` antes de qualquer render. Não usar `st.button` para esse link — o query param é necessário para ficar inline com o texto do label.

## Integrações externas

- `bookmarklet_vida/SCRIPT.js` — código do bookmarklet que extrai dados do DOM do sistema VIDA e copia no formato `Nome: X | SUS: Y | Prontuário: Z | Nascimento: W | Mãe: V`. A página de configuração (`_show_config()` em `app.py`) exibe esse código e as instruções de instalação.

## Shell
- Ambiente: Windows 11, PowerShell 5.1
- Operadores `&&` e `||` **não existem** no PS 5.1 — usar `; if ($?) { }` para encadear com verificação
- Usar `$env:VAR` para variáveis de ambiente (não `export`)
