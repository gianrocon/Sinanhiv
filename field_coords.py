"""
Mapa de coordenadas dos campos da ficha SINAN AIDS Adulto.

Formato: nome_campo -> (numero_pagina, x, y)
  - pagina: 1 ou 2
  - x, y: coordenadas em pontos PDF (0,0 = canto superior esquerdo, 595x841)

Coordenadas baseadas no dump real do PDF via PyMuPDF.
Use "python calibrate.py test" para gerar calibracao_output.pdf e verificar
o alinhamento. Ajuste os valores abaixo conforme necessario.

Dica de ajuste: aumente x para mover para direita, aumente y para mover para baixo.
"""

# Todos os campos indexados por nome logico
ALL_FIELDS = {

    # =========================================================================
    # PAGINA 1
    # =========================================================================

    # --- CABECALHO ---
    # "No" esta em (458.6, 41.2); campo fica a direita
    "numero_notificacao":           (1, 480.0,  41.0),

    # --- DADOS GERAIS ---
    # Campo 3: Data da Notificacao - delimitadores "|" em y=163.4 a partir de x=449
    "data_notificacao":             (1, 447.7, 161.2),

    # Campo 4: UF - delimitador "|" em (56.0, 191.8)
    "uf_notificacao":               (1,  60.0, 191.0),

    # Campo 5: Municipio de Notificacao - label em y=176.5, campo em y=191
    "municipio_notificacao":        (1, 100.0, 191.0),
    # IBGE - delimitadores em (488.4, 193.1) e seguintes
    "ibge_municipio_notif":         (1, 487.2, 189.7),

    # Campo 6: Unidade de Saude - label em y=205.9
    "unidade_saude":                (1,  80.0, 219.0),
    # Codigo CNES - delimitadores em (348.9, 221.5) e seguintes (6 digitos)
    "codigo_unidade_saude":         (1, 352.0, 219.0),

    # Campo 7: Data do Diagnostico - delimitadores em y=219.7 a partir de x=446
    "data_diagnostico":             (1, 455.2, 216.7),

    # --- NOTIFICACAO INDIVIDUAL ---
    # Campo 8: Nome do Paciente - label em y=233.9
    "nome_paciente":                (1,  80.0, 248.0),

    # Campo 9: Data de Nascimento - delimitadores em y=250.3 a partir de x=450
    "data_nascimento":              (1, 463.7, 248.1),

    # Campo 10: Idade (numero e unidade) - "|  |" em (66.0, 280.1)
    "idade_valor":                  (1,  68.0, 280.0),
    "idade_unidade":                (1, 110.0, 271.0),  # codigo 1-Hora,2-Dia,3-Mes,4-Ano

    # Campo 11: Sexo - label em (163.1, 263.2)
    "sexo":                         (1, 232.7, 265.9),  # M, F ou I

    # Campo 12: Gestante - label em (260.0, 260.6)
    "gestante":                     (1, 427.0, 264.0),  # codigos 1-6,9

    # Campo 13: Raca/Cor - label em (461.9, 262.2)
    "raca_cor":                     (1, 553.7, 266.4),  # codigos 1-5,9

    # Campo 14: Escolaridade - label em (65.6, 288.5), descricao ate y=308
    "escolaridade":                 (1, 552.7, 295.7),  # codigos 0-10,9

    # Campo 15: Cartao SUS - delimitadores "|" em (56.5, 340.8) — 15 digitos
    "cartao_sus":                   (1, 66.7, 339.7),

    # Campo 16: Nome da Mae - label em (245.4, 324.8)
    "nome_mae":                     (1, 250.0, 340.0),

    # --- DADOS DE RESIDENCIA ---
    # Campo 17: UF residencia - label em (66.3, 355.7), "|" em (56.9, 371.7)
    "uf_residencia":                (1, 60.7, 370.2),

    # Campo 18: Municipio - label em (95.4, 356.9)
    "municipio_residencia":         (1, 99.7, 369.3),
    # IBGE - delimitadores em y=372.3 a partir de x=337
    "ibge_municipio_resid":         (1, 337.7, 369.2),

    # Campo 19: Distrito - label em (426.9, 357.5)
    "distrito":                     (1, 436.2, 369.2),

    # Campo 20: Bairro - label em (67.5, 381.8)
    "bairro":                       (1, 72.2, 393.7),

    # Campo 21: Logradouro - label em (206.7, 382.6)
    "logradouro":                   (1, 209.2, 395.7),
    # Codigo logradouro - "Codigo" label em (480.6, 381.7), delimitadores em y=398.6
    "codigo_logradouro":            (1, 488.7, 393.7),

    # Campo 22: Numero - label em (68.1, 406.2)
    "numero_residencia":            (1, 67.7, 418.2),

    # Campo 23: Complemento - label em (122.0, 406.1)
    "complemento":                  (1, 135.7, 417.7),

    # Campo 24: Geo campo 1 - label em (423.0, 406.6)
    "geo_campo1":                   (1, 428.0, 420.0),

    # Campo 25: Geo campo 2 - label em (67.5, 429.2)
    "geo_campo2":                   (1,  70.0, 443.0),

    # Campo 26: Ponto de Referencia - label em (228.7, 432.9)
    "ponto_referencia":             (1, 232.0, 443.0),

    # Campo 27: CEP - delimitadores em (458.6, 449.2)
    "cep":                          (1, 464.2, 446.2),

    # Campo 28: DDD+Telefone - label em (68.9, 457.0)
    "ddd_telefone":                 (1, 77.2, 471.6),

    # Campo 29: Zona - label em (218.6, 456.2)
    "zona":                         (1, 333.7, 460.2),  # 1=Urbana,2=Rural,3=Periurbana,9=Ignorado

    # Campo 30: Pais exterior - label em (368.0, 457.8)
    "pais_exterior":                (1, 372.0, 467.0),

    # --- DADOS COMPLEMENTARES ---
    # Campo 31: Ocupacao - label em (73.4, 511.1)
    "ocupacao":                     (1,  78.0, 521.0),

    # --- PROVAVEL MODO DE TRANSMISSAO ---
    # Campo 32: Transmissao Vertical - label em (70.9, 546.6)
    # Caixa de codigo fica na margem direita da linha
    "transmissao_vertical":         (1, 235.2, 553.1),  # 1=Sim,2=NaoFoi,9=Ignorado

    # Campo 33: Sexual - label em (273.0, 545.5)
    # Caixa de codigo na margem direita
    "transmissao_sexual":           (1, 549.2, 549.1),  # 1-4,9

    # Campo 34: Sanguinea - 4 sub-campos
    # "Uso de drogas injetaveis" em (178.4, 590.8)
    "sanguinea_drogas":             (1, 284.2, 596.6),  # 1=Sim,2=Nao,9=Ignorado
    # "Tratamento/hemotransfusao para hemofilia" em (177.8, 605.9)
    "sanguinea_hemofilia":          (1, 283.7, 614.6),
    # "Transfusao sanguinea" em (341.9, 591.5)
    "sanguinea_transfusao":         (1, 483.7, 595.1),
    # "Acidente com material biologico" em (341.9, 605.3)
    "sanguinea_acidente":           (1, 483.2, 612.1),

    # Campo 35: Data da transfusao/acidente - delimitadores em y=655.1, x=78.8
    "data_transfusao_acidente":     (1, 75.7, 652.3),

    # Campo 36: UF transfusao - label em (197.6, 637.4), "|" em (186.8, 653.5)
    "uf_transfusao":                (1, 191.2, 650.9),

    # Campo 37: Municipio transfusao - label em (233.4, 636.2)
    "municipio_transfusao":         (1, 247.7, 651.4),
    # IBGE - delimitadores em (493.4, 655.1) e seguintes
    "ibge_municipio_transfusao":    (1, 489.7, 649.7),

    # Campo 38: Instituicao - label em (76.1, 666.0)
    "instituicao_transfusao":       (1, 103.2, 679.4),
    # Codigo - delimitadores em (480.2, 682.7) e seguintes
    "codigo_instituicao":           (1, 482.7, 678.4),

    # Campo 39: Foi causa do HIV? - opcoes em (278.3, 707.8)
    "transfusao_foi_causa":         (1, 543.0, 702.0),  # 1=Sim,2=Nao,3=NaoSeAplica

    # --- DADOS DO LABORATORIO (Campo 40) ---
    # Opcoes globais em (104.4, 738.7)
    # Teste de triagem - label em (126.0, 757.3)/(126.0, 766.2)
    "lab_triagem_resultado":        (1, 111.2, 765.7),
    # Data coleta triagem - delimitadores em y=772.4, x=176.9
    "lab_triagem_data":             (1, 171.7, 767.8),

    # Teste confirmatorio - label em (325.7, 757.3)/(325.7, 766.2)
    "lab_confirmatorio_resultado":  (1, 310.2, 765.2),
    # Data coleta confirmatorio - delimitadores em y=773.3, x=398.5
    "lab_confirmatorio_data":       (1, 395.7, 768.3),

    # Teste rapido 1 - label em (170.1, 793.3)/(170.1, 802.3)
    "lab_rapido1_resultado":        (1, 153.7, 796.2),

    # Teste rapido 2 - label em (250.3, 794.6)/(250.3, 803.6)
    "lab_rapido2_resultado":        (1, 234.7, 797.7),

    # Teste rapido 3 - label em (326.6, 794.6)/(326.6, 803.6)
    "lab_rapido3_resultado":        (1, 311.2, 795.7),

    # Data coleta dos rapidos (compartilhada) - delimitadores em y=808.0, x=379.6
    "lab_rapidos_data":             (1, 379.7, 803.3),


    # =========================================================================
    # PAGINA 2
    # =========================================================================

    # --- CRITERIO RIO DE JANEIRO/CARACAS (Campo 41) ---
    # Caixas de marcacao ficam a ESQUERDA de cada label
    # Coluna esquerda:
    "rj_sarcoma_kaposi":            (2,  67.0,  50.0),   # label em (80.0, 48.2)
    "rj_tb_disseminada":            (2,  67.0,  64.0),   # label em (80.7, 62.8)
    "rj_candidose_oral":            (2,  67.0,  79.0),   # label em (80.7, 77.4)
    "rj_tb_pulmonar":               (2,  67.0,  94.0),   # label em (80.7, 92.2)
    "rj_herpes_zoster":             (2,  67.0, 108.0),   # label em (80.8, 106.4)
    "rj_disfuncao_snc":             (2,  67.0, 123.0),   # label em (80.8, 121.0)
    "rj_diarreia":                  (2,  67.0, 137.0),   # label em (80.8, 135.5)
    "rj_febre":                     (2,  67.0, 150.0),   # label em (81.5, 148.7)
    # Coluna direita:
    "rj_caquexia":                  (2, 301.0,  50.0),   # label em (314.7, 48.5)
    "rj_astenia":                   (2, 301.0,  65.0),   # label em (314.7, 63.0)
    "rj_dermatite":                 (2, 301.0,  79.0),   # label em (314.7, 77.6)
    "rj_anemia":                    (2, 301.0,  94.0),   # label em (314.8, 92.2)
    "rj_tosse":                     (2, 301.0, 108.0),   # label em (316.2, 106.0)
    "rj_linfadenopatia":            (2, 301.0, 121.0),   # label em (314.8, 119.7)

    # --- CRITERIO CDC ADAPTADO (Campo 42) ---
    # Coluna esquerda:
    "cdc_cancer_cervical":          (2,  67.0, 183.0),   # label em (79.8, 181.1)
    "cdc_candidose_esofago":        (2,  67.0, 196.0),   # label em (79.3, 194.6)
    "cdc_candidose_traqueia":       (2,  67.0, 211.0),   # label em (79.3, 209.6)
    "cdc_citomegalovirose":         (2,  67.0, 226.0),   # label em (79.8, 224.8)
    "cdc_criptococose":             (2,  67.0, 240.0),   # label em (79.3, 238.9)
    "cdc_criptosporidiose":         (2,  67.0, 256.0),   # label em (79.4, 254.0)
    "cdc_herpes_simples":           (2,  67.0, 271.0),   # label em (79.3, 269.4)
    "cdc_histoplasmose":            (2,  67.0, 285.0),   # label em (79.8, 283.7)
    "cdc_isosporidiose":            (2,  67.0, 300.0),   # label em (80.3, 298.9)
    # Coluna direita:
    "cdc_leucoencefalopatia":       (2, 300.0, 182.0),   # label em (312.5, 180.1)
    "cdc_linfoma_hodgkin":          (2, 300.0, 198.0),   # label em (312.6, 196.9)
    "cdc_linfoma_cerebro":          (2, 300.0, 213.0),   # label em (312.6, 211.4)
    "cdc_micobacteriose":           (2, 300.0, 228.0),   # label em (312.6, 226.0)
    "cdc_pneumonia_pcp":            (2, 300.0, 242.0),   # label em (312.6, 240.5)
    "cdc_reativacao_chagas":        (2, 300.0, 257.0),   # label em (312.5, 255.1)
    "cdc_salmonelose":              (2, 300.0, 272.0),   # label em (313.4, 270.8)
    "cdc_toxoplasmose":             (2, 300.0, 287.0),   # label em (313.2, 285.0)
    "cdc_cd4_350":                  (2, 300.0, 301.0),   # label em (313.2, 299.8)

    # --- CRITERIO OBITO (Campo 43) ---
    # "Criterio Obito" em (68.0, 320.1), descricao ate y=338.6
    # Opcoes "1-Sim 2-Nao 9-Ignorado" em (370.5, 333.4)
    "criterio_obito":               (2, 504.7, 329.5),  # 1=Sim,2=Nao,9=Ignorado

    # --- TRATAMENTO ---
    # Campo 44: UF tratamento - "|" em (54.7, 379.0)
    "uf_tratamento":                (2,  58.0, 379.0),

    # Campo 45: Municipio tratamento - label em (94.3, 362.0)
    "municipio_tratamento":         (2,  98.0, 379.0),
    # IBGE - delimitadores em y=380.6, x=263.4
    "ibge_municipio_tratamento":    (2, 260.7, 377.9),

    # Campo 46: Unidade de saude tratamento - label em (354.3, 356.6)
    "unidade_tratamento":           (2, 357.0, 379.0),
    # Codigo - delimitadores em y=379.7, x=477.9
    "codigo_unidade_tratamento":    (2, 479.2, 373.4),

    # --- EVOLUCAO ---
    # Campo 47: Evolucao do caso - label em (66.5, 392.1)
    # Opcoes em (102.0, 403.7)
    "evolucao_caso":                (2, 426.2, 394.0),  # 1=Vivo,2=ObitoAids,3=ObitoOutras,9=Ignorado

    # Campo 48: Data do obito - label em (460.5, 389.6), delimitadores em y=413
    "data_obito":                   (2, 457.7, 409.0),

    # --- INVESTIGADOR ---
    # "Nome" em (59.1, 428.9)
    "investigador_nome":            (2,  80.0, 440.0),
    # "Funcao" em (353.1, 430.6)
    "investigador_funcao":          (2, 357.0, 440.0),
    # Assinatura nao é preenchida (manual)
}
