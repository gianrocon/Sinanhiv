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

## Integrações externas

- `bookmarklet_vida/` — bookmarklet para importar dados do sistema VIDA; ver README interno.

## Shell
- Ambiente: Windows 11, PowerShell 5.1
- Operadores `&&` e `||` **não existem** no PS 5.1 — usar `; if ($?) { }` para encadear com verificação
- Usar `$env:VAR` para variáveis de ambiente (não `export`)
