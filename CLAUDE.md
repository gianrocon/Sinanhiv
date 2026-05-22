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

## Shell
- Ambiente: Windows 11, PowerShell 5.1
- Operadores `&&` e `||` **não existem** no PS 5.1 — usar `; if ($?) { }` para encadear com verificação
- Usar `$env:VAR` para variáveis de ambiente (não `export`)
