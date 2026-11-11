# Revisão manual — amostra do dataset

12 exemplos (3 por layout), semente 7. Para cada atividade, marque no `revisao.csv`: `ok` ou o tipo de erro.

Tipos de erro: `nome_regra` (nome com subtítulo/palestrante/tema), `descricao` (informação errada, faltando ou inventada), `campo` (local/horário não confere com o texto), `irreal` (atividade ou texto implausível), `outro`.

## sint-42-00338-1 — cartaz — evento de inovação no agronegócio

Ruídos: secoes, decorativo, quebra

### Texto

```text
Programação - AgroTech Nordeste 2023: Inovação e Sustentabilidade no Semiárido
Edição 2023

18 de outubro de 2023
08:00 – 09:00
RECEPÇÃO E BOAS-VINDAS
Acolhimento dos participantes e entrega de crachás institucionais.
PAINÉIS PRINCIPAIS
09:00 – 10:30
PALESTRA DE ABERTURA
Apresentação Conectividade no Campo e a Revolução das AgTechs no Nordeste conduzida por Dr. Marcelo Albuquerque (Embrapa Semiárido).
AUDITÓRIO POTIGUAR
MOSTRA DE INOVAÇÃO
14:00 – 16:00
CIRCUITO DE DEMONSTRAÇÃO TECNOLÓGICA
Apresentação prática de drones aplicadores de defensivos biológicos sob coordenação de Larissa Medeiros.
ESPAÇO AGROFUTURO

19 de outubro de 2023
Sessões Técnicas
09:00 – 11:00
SESSÃO TEMÁTICA 1
Apresentação dos trabalhos Manejo Hídrico Inteligente na Fruticultura Irrigada por Renata Vasconcelos e Sensoriamento Remoto Aplicado a Pastagens por Felipe Castelo Branco.
SALA MANDACARU
Apoio:
09:00 – 11:00
SESSÃO TEMÁTICA 2
Discussão do artigo Biotecnologia e Fermentação para Alimentação Animal pelo pesquisador Igor Mendonça e moderação de Dra. Simone Galvão.
SALA CAATINGA
14:00 – 17:00
RODADA DE NEGÓCIOS E INVESTIMENTOS
Encontro entre fundos de venture capital e startups rurais potiguares organizado por Carla Antunes.
MOSTRA DE INOVAÇÃO
15:00 – 17:30
CIRCUITO DE DEMONSTRAÇÃO TECNOLÓGICA
Demonstração de sensores IoT para análise de solo em tempo real pelo engenheiro agrônomo Thiago Paiva.
ÁREA EXTERNA - LOTE DEMONSTRATIVO

20 de outubro de 2023
08:30
CONSULTORIA ABERTA PARA STARTUPS
PAINÉIS PRINCIPAIS
10:00 – 12:00
PAINEL DE ENCERRAMENTO
Mesa com o tema O Futuro do Agronegócio Sustentável e Crédito de Carbono com os convidados Beatriz Fontes e Jorge Linhares.
AUDITÓRIO POTIGUAR
14:00 – 16:00
PREMIAÇÃO AGROINOVA RN
Anúncio das soluções vencedoras do hackathon rural sob condução de Rodrigo Farias.
AUDITÓRIO POTIGUAR

Apoio:
@aniss
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | RECEPÇÃO E BOAS-VINDAS |  | 2023-10-18T08:00 | 2023-10-18T09:00 | <p>Acolhimento dos participantes e entrega de crachás institucionais.</p> |
| 1 | PALESTRA DE ABERTURA | AUDITÓRIO POTIGUAR | 2023-10-18T09:00 | 2023-10-18T10:30 | <p>Apresentação <i>Conectividade no Campo e a Revolução das AgTechs no Nordeste</i> conduzida por <b>Dr. Marcelo Albuquerque</b> (Embrapa Semiárido).</p> |
| 2 | CIRCUITO DE DEMONSTRAÇÃO TECNOLÓGICA | ESPAÇO AGROFUTURO | 2023-10-18T14:00 | 2023-10-18T16:00 | <p>Apresentação prática de drones aplicadores de defensivos biológicos sob coordenação de <b>Larissa Medeiros</b>.</p> |
| 3 | SESSÃO TEMÁTICA 1 | SALA MANDACARU | 2023-10-19T09:00 | 2023-10-19T11:00 | <p>Apresentação dos trabalhos <i>Manejo Hídrico Inteligente na Fruticultura Irrigada</i> por <b>Renata Vasconcelos</b> e <i>Sensoriamento Remoto Aplicado a Pastagens</i> por <b>Felipe Castelo Branco</b>.</p> |
| 4 | SESSÃO TEMÁTICA 2 | SALA CAATINGA | 2023-10-19T09:00 | 2023-10-19T11:00 | <p>Discussão do artigo <i>Biotecnologia e Fermentação para Alimentação Animal</i> pelo pesquisador <b>Igor Mendonça</b> e moderação de <b>Dra. Simone Galvão</b>.</p> |
| 5 | RODADA DE NEGÓCIOS E INVESTIMENTOS |  | 2023-10-19T14:00 | 2023-10-19T17:00 | <p>Encontro entre fundos de venture capital e startups rurais potiguares organizado por <b>Carla Antunes</b>.</p> |
| 6 | CIRCUITO DE DEMONSTRAÇÃO TECNOLÓGICA | ÁREA EXTERNA - LOTE DEMONSTRATIVO | 2023-10-19T15:00 | 2023-10-19T17:30 | <p>Demonstração de sensores IoT para análise de solo em tempo real pelo engenheiro agrônomo <b>Thiago Paiva</b>.</p> |
| 7 | CONSULTORIA ABERTA PARA STARTUPS |  | 2023-10-20T08:30 |  |  |
| 8 | PAINEL DE ENCERRAMENTO | AUDITÓRIO POTIGUAR | 2023-10-20T10:00 | 2023-10-20T12:00 | <p>Mesa com o tema <i>O Futuro do Agronegócio Sustentável e Crédito de Carbono</i> com os convidados <b>Beatriz Fontes</b> e <b>Jorge Linhares</b>.</p> |
| 9 | PREMIAÇÃO AGROINOVA RN | AUDITÓRIO POTIGUAR | 2023-10-20T14:00 | 2023-10-20T16:00 | <p>Anúncio das soluções vencedoras do hackathon rural sob condução de <b>Rodrigo Farias</b>.</p> |

## sint-42-00178-1 — cartaz — simpósio de pós-graduação

Ruídos: secoes, decorativo

### Texto

```text
IX SIMPÓSIO DE PÓS-GRADUAÇÃO EM ECOLOGIA E SUSTENTABILIDADE AMAZÔNICA
Campus Universitário do Guamá - Belém - PA
PROGRAMAÇÃO

Quarta-feira (13/05/2026)
(08h00 - 09h00)
RECEPÇÃO DOS PARTICIPANTES E ENTREGA DE CRACHÁS
HALL DO PRÉDIO DE PÓS-GRADUAÇÃO
Apoio:
(09h00 - 10h00)
SESSÃO SOLENE DE ABERTURA
Boas-vindas com a presença do Pró-Reitor Dr. Raimundo Nonato Castro e da coordenadora geral do programa Dra. Simone Alencar.
AUDITÓRIO SETORIAL BÁSICO
(10h00 - 12h00)
PALESTRA INAUGURAL
Tema: Desafios contemporâneos para a conservação da biodiversidade aquática frente às mudanças climáticas globais e a expansão da infraestrutura na bacia amazônica.
Palestrante: Dra. Helena Guimarães Bittencourt.
AUDITÓRIO SETORIAL BÁSICO
Organização:
(12h00 - 14h00)
INTERVALO PARA ALMOÇO
MESAS TEMÁTICAS
(14h00 - 16h00)
MESA DE DEBATE 1
Tema: Valoração de Serviços Ecossistêmicos e Comunidades Tradicionais.
Debatedores: Prof. Carlos Eduardo Viana e Pesq. Marília Tavares. Mediação de Dr. Jorge Luis Miranda.
AUDITÓRIO SETORIAL BÁSICO
(16h00 - 16h30)
LANCHE DA TARDE
(16h30 - 18h30)
SESSÃO DE PÔSTERES - BLOCO A
Apresentação dos trabalhos de mestrandos da área de Ecologia Teórica. Coordenação: Dra. Fernanda Bentes.
ESPAÇO DE CONVIVÊNCIA DA REITORIA
Acesse o QR Code

Quinta-feira (14/05/2026)
OFICINAS METODOLÓGICAS
(08h30 - 12h00)
OFICINA TEMÁTICA A
Tema: Mapeamento e análise espacial aplicados ao monitoramento florestal por meio de linguagens de programação abertas e gratuitas.
Ministrante: Msc. Thiago Prado Silva.
LABORATÓRIO DE GEOPROCESSAMENTO 2
Vagas limitadas!
(08h30 - 12h00)
OFICINA TEMÁTICA B
Tema: Modelos Lineares Generalizados em R.
Instrutor: Dr. Paulo Roberto Antunes.
SALA MULTIUSO 104
Acesse o QR Code
(12h00 - 14h00)
PAUSA PARA ALMOÇO
Comunicações Orais
(14h00 - 15h30)
APRESENTAÇÃO ORAL DE TESES 1
Exposições dos doutorandos Lucas Barreto e Camila Nogueira, com avaliação da banca formada por Dr. Vicente Meireles e Dra. Cláudia Esteves.
MINIAUDITÓRIO DO ICB
Siga @spgesa nas redes sociais
(15h30 - 17h00)
APRESENTAÇÃO ORAL DE TESES 2
Apresentações orais de Renato Gusmão com o estudo Dinâmica de nutrientes em florestas de várzea e de Letícia Albuquerque.
MINIAUDITÓRIO DO ICB
Apoio:
MESAS TEMÁTICAS
(17h00 - 18h30)
MESA DE DEBATE 2
Tema: Políticas Públicas para a Conservação de Bacias Hidrográficas.
Palestrantes convidados: Dra. Juliana Vasconcelos e Dr. Marcos Vinícius Paiva.
18h30
MOSTRA DE FOTOGRAFIA CIENTÍFICA
Abertura da exposição de fotografias de campo registradas pelos discentes do programa. Curadoria: Prof. Marcelo Camargo.
ESPAÇO DE CONVIVÊNCIA DA REITORIA
Patrocínio

Sexta-feira (15/05/2026)
(09h00 - 10h30)
PALESTRA ESPECIAL
Tema: A importância da interdisciplinaridade nos programas de pós-graduação brasileiros para a mitigação dos impactos socioambientais regionais.
Conferencista: Prof. Dr. Samuel Figueiredo Mendonça.
AUDITÓRIO SETORIAL BÁSICO
Realização:
(10h30 - 12h00)
RODA DE CONVERSA DISCENTE
Discussão sobre saúde mental na pós-graduação e representatividade discente. Mediação feita por Patrícia Leão e Gabriel Furtado.
(12h00 - 14h00)
INTERVALO LIVRE
(14h00 - 16h00)
SESSÃO DE PÔSTERES - BLOCO B
Apresentação das pesquisas dos alunos de iniciação científica e mestrandos de Ecologia Aplicada. Avaliadores: Dr. Daniel Aragão e Dra. Sílvia Pantoja.
ESPAÇO DE CONVIVÊNCIA DA REITORIA
(16h30 - 17h30)
PREMIAÇÃO DE TRABALHOS DESTACADOS
Entrega do Prêmio Destaque Acadêmico aos melhores artigos apresentados. Comissão julgadora liderada por Dra. Simone Alencar.
AUDITÓRIO SETORIAL BÁSICO
17h30
CERIMÔNIA DE ENCERRAMENTO
Palavras finais da comissão organizadora composta por Dra. Simone Alencar e Prof. Dr. Samuel Figueiredo Mendonça.
AUDITÓRIO SETORIAL BÁSICO

Realização:
@spgesa
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | RECEPÇÃO DOS PARTICIPANTES E ENTREGA DE CRACHÁS | HALL DO PRÉDIO DE PÓS-GRADUAÇÃO | 2026-05-13T08:00 | 2026-05-13T09:00 |  |
| 1 | SESSÃO SOLENE DE ABERTURA | AUDITÓRIO SETORIAL BÁSICO | 2026-05-13T09:00 | 2026-05-13T10:00 | <p>Boas-vindas com a presença do Pró-Reitor <b>Dr. Raimundo Nonato Castro</b> e da coordenadora geral do programa <b>Dra. Simone Alencar</b>.</p> |
| 2 | PALESTRA INAUGURAL | AUDITÓRIO SETORIAL BÁSICO | 2026-05-13T10:00 | 2026-05-13T12:00 | <p>Tema: <i>Desafios contemporâneos para a conservação da biodiversidade aquática frente às mudanças climáticas globais e a expansão da infraestrutura na bacia amazônica</i>.</p><p>Palestrante: <b>Dra. Helena Guimarães Bittencourt</b>.</p> |
| 3 | INTERVALO PARA ALMOÇO |  | 2026-05-13T12:00 | 2026-05-13T14:00 |  |
| 4 | MESA DE DEBATE 1 | AUDITÓRIO SETORIAL BÁSICO | 2026-05-13T14:00 | 2026-05-13T16:00 | <p>Tema: <i>Valoração de Serviços Ecossistêmicos e Comunidades Tradicionais</i>.</p><p>Debatedores: <b>Prof. Carlos Eduardo Viana</b> e <b>Pesq. Marília Tavares</b>. Mediação de <b>Dr. Jorge Luis Miranda</b>.</p> |
| 5 | LANCHE DA TARDE |  | 2026-05-13T16:00 | 2026-05-13T16:30 |  |
| 6 | SESSÃO DE PÔSTERES - BLOCO A | ESPAÇO DE CONVIVÊNCIA DA REITORIA | 2026-05-13T16:30 | 2026-05-13T18:30 | <p>Apresentação dos trabalhos de mestrandos da área de Ecologia Teórica. Coordenação: <b>Dra. Fernanda Bentes</b>.</p> |
| 7 | OFICINA TEMÁTICA A | LABORATÓRIO DE GEOPROCESSAMENTO 2 | 2026-05-14T08:30 | 2026-05-14T12:00 | <p>Tema: <i>Mapeamento e análise espacial aplicados ao monitoramento florestal por meio de linguagens de programação abertas e gratuitas</i>.</p><p>Ministrante: <b>Msc. Thiago Prado Silva</b>.</p> |
| 8 | OFICINA TEMÁTICA B | SALA MULTIUSO 104 | 2026-05-14T08:30 | 2026-05-14T12:00 | <p>Tema: <i>Modelos Lineares Generalizados em R</i>.</p><p>Instrutor: <b>Dr. Paulo Roberto Antunes</b>.</p> |
| 9 | PAUSA PARA ALMOÇO |  | 2026-05-14T12:00 | 2026-05-14T14:00 |  |
| 10 | APRESENTAÇÃO ORAL DE TESES 1 | MINIAUDITÓRIO DO ICB | 2026-05-14T14:00 | 2026-05-14T15:30 | <p>Exposições dos doutorandos <b>Lucas Barreto</b> e <b>Camila Nogueira</b>, com avaliação da banca formada por <b>Dr. Vicente Meireles</b> e <b>Dra. Cláudia Esteves</b>.</p> |
| 11 | APRESENTAÇÃO ORAL DE TESES 2 | MINIAUDITÓRIO DO ICB | 2026-05-14T15:30 | 2026-05-14T17:00 | <p>Apresentações orais de <b>Renato Gusmão</b> com o estudo <i>Dinâmica de nutrientes em florestas de várzea</i> e de <b>Letícia Albuquerque</b>.</p> |
| 12 | MESA DE DEBATE 2 |  | 2026-05-14T17:00 | 2026-05-14T18:30 | <p>Tema: <i>Políticas Públicas para a Conservação de Bacias Hidrográficas</i>.</p><p>Palestrantes convidados: <b>Dra. Juliana Vasconcelos</b> e <b>Dr. Marcos Vinícius Paiva</b>.</p> |
| 13 | MOSTRA DE FOTOGRAFIA CIENTÍFICA | ESPAÇO DE CONVIVÊNCIA DA REITORIA | 2026-05-14T18:30 |  | <p>Abertura da exposição de fotografias de campo registradas pelos discentes do programa. Curadoria: <b>Prof. Marcelo Camargo</b>.</p> |
| 14 | PALESTRA ESPECIAL | AUDITÓRIO SETORIAL BÁSICO | 2026-05-15T09:00 | 2026-05-15T10:30 | <p>Tema: <i>A importância da interdisciplinaridade nos programas de pós-graduação brasileiros para a mitigação dos impactos socioambientais regionais</i>.</p><p>Conferencista: <b>Prof. Dr. Samuel Figueiredo Mendonça</b>.</p> |
| 15 | RODA DE CONVERSA DISCENTE |  | 2026-05-15T10:30 | 2026-05-15T12:00 | <p>Discussão sobre saúde mental na pós-graduação e representatividade discente. Mediação feita por <b>Patrícia Leão</b> e <b>Gabriel Furtado</b>.</p> |
| 16 | INTERVALO LIVRE |  | 2026-05-15T12:00 | 2026-05-15T14:00 |  |
| 17 | SESSÃO DE PÔSTERES - BLOCO B | ESPAÇO DE CONVIVÊNCIA DA REITORIA | 2026-05-15T14:00 | 2026-05-15T16:00 | <p>Apresentação das pesquisas dos alunos de iniciação científica e mestrandos de Ecologia Aplicada. Avaliadores: <b>Dr. Daniel Aragão</b> e <b>Dra. Sílvia Pantoja</b>.</p> |
| 18 | PREMIAÇÃO DE TRABALHOS DESTACADOS | AUDITÓRIO SETORIAL BÁSICO | 2026-05-15T16:30 | 2026-05-15T17:30 | <p>Entrega do Prêmio Destaque Acadêmico aos melhores artigos apresentados. Comissão julgadora liderada por <b>Dra. Simone Alencar</b>.</p> |
| 19 | CERIMÔNIA DE ENCERRAMENTO | AUDITÓRIO SETORIAL BÁSICO | 2026-05-15T17:30 |  | <p>Palavras finais da comissão organizadora composta por <b>Dra. Simone Alencar</b> e <b>Prof. Dr. Samuel Figueiredo Mendonça</b>.</p> |

## sint-42-00421-1 — cartaz — simpósio de pós-graduação

Ruídos: quebra

### Texto

```text
XII Simpósio de Pós-Graduação em Agroecologia e Sustentabilidade da UFV
Programação 2024

Dia 1 - 18/10
(08:00 - 09:00)
ABERTURA OFICIAL E
APRESENTAÇÃO DO PROGRAMA
Abertura do simpósio conduzida pela coordenadora-geral Profa. Dra. Helena Vasconcelos Prado e pelo vice-reitor Prof. Dr. Carlos Eduardo Guimarães.
AUDITÓRIO DO CEE
(09:00 - 10:30)
PALESTRA
Palestra intitulada Desafios contemporâneos para a transição agroecológica sustentável frente às mudanças climáticas globais e os impactos na agricultura familiar brasileira, ministrada pelo pesquisador Dr. Marcos Vinicius Rezende e mediada pela Profa. Dra. Juliana Meireles Fontes.
(10:45 - 12:30)
SESSÃO TÉCNICA DE COMUNICAÇÃO ORAL
Coordenação de Renata Albuquerque Neves. Trabalhos apresentados:
1. Dinâmica da matéria orgânica em solos sob manejo agroflorestal na Zona da Mata mineira, por Lucas Barreto Sampaio e Otávio Mendes Camargo.
2. Levantamento etnobotânico de plantas medicinais cultivadas por agricultores familiares, por Camila Duarte Ferreira e Aline Peixoto Silva.
(14:00 - 15:45)
SESSÃO TÉCNICA DE COMUNICAÇÃO ORAL
Coordenação de Prof. Dr. Fernando Pires Fagundes. Trabalhos apresentados:
1. Indicadores biológicos de qualidade do solo em sistemas de plantio direto de hortaliças, por Gabriela Ramos Costa e Bruno Toledo Antunes.
2. Avaliação de extratos botânicos alternativos no controle de pragas da cafeicultura orgânica, por Rodrigo Viana Borges e Mariana Castro Leão.
SALA DE SEMINÁRIOS B
(16:00 - 17:30)
PALESTRA
Apresentação do tema Metodologias participativas e cartografia social aplicadas ao planejamento territorial e à conservação de recursos hídricos em comunidades tradicionais, proferida pelo Prof. Dr. Tiago Benevides Moreira, com coordenação de debate por Profa. Dra. Clarissa Silveira Ramos.
(17:30 - 18:15)
PREMIAÇÃO E ENCERRAMENTO
Divulgação dos melhores trabalhos de pós-graduação e encerramento conduzidos pelos coordenadores Helena Vasconcelos Prado e Fernando Pires Fagundes.
AUDITÓRIO DO CEE
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | ABERTURA OFICIAL E APRESENTAÇÃO DO PROGRAMA | AUDITÓRIO DO CEE | 2024-10-18T08:00 | 2024-10-18T09:00 | <p>Abertura do simpósio conduzida pela coordenadora-geral Profa. Dra. <b>Helena Vasconcelos Prado</b> e pelo vice-reitor Prof. Dr. <b>Carlos Eduardo Guimarães</b>.</p> |
| 1 | PALESTRA |  | 2024-10-18T09:00 | 2024-10-18T10:30 | <p>Palestra intitulada <i>Desafios contemporâneos para a transição agroecológica sustentável frente às mudanças climáticas globais e os impactos na agricultura familiar brasileira</i>, ministrada pelo pesquisador Dr. <b>Marcos Vinicius Rezende</b> e mediada pela Profa. Dra. <b>Juliana Meireles Fontes</b>.</p> |
| 2 | SESSÃO TÉCNICA DE COMUNICAÇÃO ORAL |  | 2024-10-18T10:45 | 2024-10-18T12:30 | <p>Coordenação de <b>Renata Albuquerque Neves</b>. Trabalhos apresentados:</p><p><i>1. Dinâmica da matéria orgânica em solos sob manejo agroflorestal na Zona da Mata mineira</i>, por <b>Lucas Barreto Sampaio</b> e <b>Otávio Mendes Camargo</b>.</p><p><i>2. Levantamento etnobotânico de plantas medicinais cultivadas por agricultores familiares</i>, por <b>Camila Duarte Ferreira</b> e <b>Aline Peixoto Silva</b>.</p> |
| 3 | SESSÃO TÉCNICA DE COMUNICAÇÃO ORAL | SALA DE SEMINÁRIOS B | 2024-10-18T14:00 | 2024-10-18T15:45 | <p>Coordenação de Prof. Dr. <b>Fernando Pires Fagundes</b>. Trabalhos apresentados:</p><p><i>1. Indicadores biológicos de qualidade do solo em sistemas de plantio direto de hortaliças</i>, por <b>Gabriela Ramos Costa</b> e <b>Bruno Toledo Antunes</b>.</p><p><i>2. Avaliação de extratos botânicos alternativos no controle de pragas da cafeicultura orgânica</i>, por <b>Rodrigo Viana Borges</b> e <b>Mariana Castro Leão</b>.</p> |
| 4 | PALESTRA |  | 2024-10-18T16:00 | 2024-10-18T17:30 | <p>Apresentação do tema <i>Metodologias participativas e cartografia social aplicadas ao planejamento territorial e à conservação de recursos hídricos em comunidades tradicionais</i>, proferida pelo Prof. Dr. <b>Tiago Benevides Moreira</b>, com coordenação de debate por Profa. Dra. <b>Clarissa Silveira Ramos</b>.</p> |
| 5 | PREMIAÇÃO E ENCERRAMENTO | AUDITÓRIO DO CEE | 2024-10-18T17:30 | 2024-10-18T18:15 | <p>Divulgação dos melhores trabalhos de pós-graduação e encerramento conduzidos pelos coordenadores <b>Helena Vasconcelos Prado</b> e <b>Fernando Pires Fagundes</b>.</p> |

## sint-42-00456-0 — colunas — maratona de programação e game jam

Ruídos: secoes, quebra

### Texto

```text
HACKAGAME LONDRINA 2025
Parque Tecnológico de Londrina - Hub de Inovação, Londrina - PR
PROGRAMAÇÃO

15 de maio de 2025
Horário
Atividade
Local
ABERTURA E WARM-UP
18:00 – 19:30
Cerimônia de Abertura e
Revelação do Tema
Auditório Araucária
Abertura oficial do evento com o coordenador Rodrigo Hayashi e anúncio das restrições criativas da maratona.
19:30
Formação de Equipes e Brainstorming
Espaço Coworking
Facilitação para conexão de desenvolvedores solo e alinhamento inicial de escopo com mentoria de Juliana Meirelles.

16 de maio de 2025
Horário
Atividade
Local
Workshops Técnicos
09:00 – 11:00
Workshop de Godot Engine
Laboratório de Informática 1
Oficina prática ministrada por Carlos Eduardo Pires sobre Desenvolvimento Rápido em 2D com Godot 4.
09:00 – 11:00
Workshop de Prototipagem Ágil com Unity
Laboratório de Informática 2
O instrutor Marcos Vinícius Prado apresenta Técnicas de Prototipagem Veloz em Game Jams utilizando templates pré-configurados.
12:00 – 13:30
Almoço dos Desenvolvedores
Praça de Convivência
MENTORIAS ESPECIALIZADAS
14:30 – 18:00
Plantão de Mentoria de Game Design
Arena Maker
Sessões de mentoria com os veteranos Fernanda Bittencourt e Lucas Zanin com foco em balanceamento e mecânicas centrais.
14:30 – 18:00
Plantão de Mentoria de Áudio e SFX
Estúdio Multimídia
Apoio na composição musical e foley com o sound designer Danilo Sanches.
23:00
Madrugada de Code Sprint
Salão Principal de Desenvolvimento
Madrugada livre dedicada à programação intensiva e integração de assets nas builds.

17 de maio de 2025
Horário
Atividade
Local
10:00 – 12:00
Check-in de Builds Parciais
Salão Principal de Desenvolvimento
Verificação obrigatória do progresso dos protótipos coordenada por Bárbara Casagrande.
15:00 – 16:30
Painel com Publishers Independentes
Auditório Araucária
Debate sobre Como Levar seu Jogo da Jam para o Mercado Comercial com participação de Thiago Mendonça e Aline Fonseca.
19:00 – 21:30
Playtest Aberto entre Equipes
Espaço Coworking
Troca de experiências e testes cruzados de usabilidade entre os participantes para coleta de feedback.

18 de maio de 2025
Horário
Atividade
Local
FASE FINAL
12:00
Congelamento de Código e
Submissão Final
Plataforma Online
Prazo limite improrrogável para upload dos executáveis e código-fonte no repositório da maratona.
14:00 – 17:00
Apresentação de Pitches e Gameplay
Auditório Araucária
Demonstração pública de 3 minutos por equipe para a banca de jurados liderada por Vanessa Toledo.
17:30 – 19:00
Cerimônia de Premiação e Encerramento
Auditório Araucária
Divulgação dos vencedores de cada categoria e encerramento com Rodrigo Hayashi.
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | Cerimônia de Abertura e Revelação do Tema | Auditório Araucária | 2025-05-15T18:00 | 2025-05-15T19:30 | <p>Abertura oficial do evento com o coordenador <b>Rodrigo Hayashi</b> e anúncio das restrições criativas da maratona.</p> |
| 1 | Formação de Equipes e Brainstorming | Espaço Coworking | 2025-05-15T19:30 |  | <p>Facilitação para conexão de desenvolvedores solo e alinhamento inicial de escopo com mentoria de <b>Juliana Meirelles</b>.</p> |
| 2 | Workshop de Godot Engine | Laboratório de Informática 1 | 2025-05-16T09:00 | 2025-05-16T11:00 | <p>Oficina prática ministrada por <b>Carlos Eduardo Pires</b> sobre <i>Desenvolvimento Rápido em 2D com Godot 4</i>.</p> |
| 3 | Workshop de Prototipagem Ágil com Unity | Laboratório de Informática 2 | 2025-05-16T09:00 | 2025-05-16T11:00 | <p>O instrutor <b>Marcos Vinícius Prado</b> apresenta <i>Técnicas de Prototipagem Veloz em Game Jams</i> utilizando templates pré-configurados.</p> |
| 4 | Almoço dos Desenvolvedores | Praça de Convivência | 2025-05-16T12:00 | 2025-05-16T13:30 |  |
| 5 | Plantão de Mentoria de Game Design | Arena Maker | 2025-05-16T14:30 | 2025-05-16T18:00 | <p>Sessões de mentoria com os veteranos <b>Fernanda Bittencourt</b> e <b>Lucas Zanin</b> com foco em balanceamento e mecânicas centrais.</p> |
| 6 | Plantão de Mentoria de Áudio e SFX | Estúdio Multimídia | 2025-05-16T14:30 | 2025-05-16T18:00 | <p>Apoio na composição musical e foley com o sound designer <b>Danilo Sanches</b>.</p> |
| 7 | Madrugada de Code Sprint | Salão Principal de Desenvolvimento | 2025-05-16T23:00 |  | <p>Madrugada livre dedicada à programação intensiva e integração de assets nas builds.</p> |
| 8 | Check-in de Builds Parciais | Salão Principal de Desenvolvimento | 2025-05-17T10:00 | 2025-05-17T12:00 | <p>Verificação obrigatória do progresso dos protótipos coordenada por <b>Bárbara Casagrande</b>.</p> |
| 9 | Painel com Publishers Independentes | Auditório Araucária | 2025-05-17T15:00 | 2025-05-17T16:30 | <p>Debate sobre <i>Como Levar seu Jogo da Jam para o Mercado Comercial</i> com participação de <b>Thiago Mendonça</b> e <b>Aline Fonseca</b>.</p> |
| 10 | Playtest Aberto entre Equipes | Espaço Coworking | 2025-05-17T19:00 | 2025-05-17T21:30 | <p>Troca de experiências e testes cruzados de usabilidade entre os participantes para coleta de feedback.</p> |
| 11 | Congelamento de Código e Submissão Final | Plataforma Online | 2025-05-18T12:00 |  | <p>Prazo limite improrrogável para upload dos executáveis e código-fonte no repositório da maratona.</p> |
| 12 | Apresentação de Pitches e Gameplay | Auditório Araucária | 2025-05-18T14:00 | 2025-05-18T17:00 | <p>Demonstração pública de 3 minutos por equipe para a banca de jurados liderada por <b>Vanessa Toledo</b>.</p> |
| 13 | Cerimônia de Premiação e Encerramento | Auditório Araucária | 2025-05-18T17:30 | 2025-05-18T19:00 | <p>Divulgação dos vencedores de cada categoria e encerramento com <b>Rodrigo Hayashi</b>.</p> |

## sint-42-00033-1 — colunas — congresso jurídico com mesas-redondas

Ruídos: quebra

### Texto

```text
CONGRESSO AMAZÔNICO DE DIREITO AMBIENTAL E CONSTITUCIONAL
Centro de Convenções João Batista de Azevedo Picanço, Macapá - AP
PROGRAMAÇÃO

19 de maio de 2027
Horário
Atividade
Local
18h00 às 20h30
Sessão Solene de Abertura
Auditório Tucuju
Abertura oficial com a conferência inaugural O Constitucionalismo Ecológico e a Proteção das Florestas Equatoriais, ministrada pela Desa. Maria de Fátima Cabral (TJAP) e presidida pelo Dr. Raimundo Nonato Picanço.

20 de maio de 2027
Horário
Atividade
Local
09h00 às 11h30
Mesa Temática
Auditório Tucuju
Debate sobre Litigância Climática e Populações Tradicionais na Borda da Amazônia. Coordenação de Cláudio Roberto Silveira. Palestrantes convidados: Profa. Dra. Irene dos Santos Maciel, abordando Jurisdição Constitucional e Direitos Originários, e Dr. Felipe Castelo Branco, com Reparação Civil por Danos Transfronteiriços.
14h30 às 17h30
Apresentação de Comunicações Orais
Sala 102
Apresentação de pesquisas submetidas ao Grupo de Trabalho de Direito Socioambiental. Coordenador da sessão: Prof. Me. Thiago Alcolumbre Viana.
Trabalhos apresentados:
1. Zoneamento Ecológico-Econômico e Sustentabilidade no Amapá, por Larissa Mendonça Guedes;
2. O Papel da Defensoria Pública nos Conflitos Fundiários Fluviais, por Rodrigo Otávio Pinheiro e Sabrina Leão Costa.
14h30 às 17h30
Apresentação de Comunicações Orais
Sala 104
Apresentação de pesquisas do Grupo de Trabalho de Hermenêutica Constitucional e Garantismo. Avaliadora responsável: Dra. Helena Esteves Vasconcelos.
Trabalhos apresentados:
1. Ativismo Judicial e Proteção dos Mananciais Urbanos, por Carlos Eduardo Belfort;
2. Democracia Participativa e Licenciamento em Terras Devolutas, por Bruna Marinho Teles e Jorge Aníbal Picanço.

21 de maio de 2027
Horário
Atividade
Local
09h00 às 11h45
Mesa Temática
Auditório Tucuju
Discussão sobre Mineração, Transição Energética e Sustentabilidade no Escudo das Guianas, sob a moderação da Profa. Glória Maria Albuquerque. Participam como expositores o Dr. Arthur Nogueira Sobrinho com o tema Tributação Extrafiscal e Compensação Ambiental, e a Dra. Viviane Bastos Trindade abordando Responsabilidade Corporativa em Áreas Protegidas.
11h45 às 14h00
Intervalo
Foyer Principal
14h30 às 17h00
Painel de Encerramento
Auditório Tucuju
Conferência de encerramento com o tema Desafios da Governança Jurídica Transnacional no Século XXI, apresentada pelo Prof. Titular Waldir Pacheco Fontes e mediada pela Dra. Regina Coeli Barata.
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | Sessão Solene de Abertura | Auditório Tucuju | 2027-05-19T18:00 | 2027-05-19T20:30 | <p>Abertura oficial com a conferência inaugural <i>O Constitucionalismo Ecológico e a Proteção das Florestas Equatoriais</i>, ministrada pela Desa. <b>Maria de Fátima Cabral</b> (TJAP) e presidida pelo Dr. <b>Raimundo Nonato Picanço</b>.</p> |
| 1 | Mesa Temática | Auditório Tucuju | 2027-05-20T09:00 | 2027-05-20T11:30 | <p>Debate sobre <i>Litigância Climática e Populações Tradicionais na Borda da Amazônia</i>. Coordenação de <b>Cláudio Roberto Silveira</b>. Palestrantes convidados: Profa. Dra. <b>Irene dos Santos Maciel</b>, abordando <i>Jurisdição Constitucional e Direitos Originários</i>, e Dr. <b>Felipe Castelo Branco</b>, com <i>Reparação Civil por Danos Transfronteiriços</i>.</p> |
| 2 | Apresentação de Comunicações Orais | Sala 102 | 2027-05-20T14:30 | 2027-05-20T17:30 | <p>Apresentação de pesquisas submetidas ao Grupo de Trabalho de Direito Socioambiental. Coordenador da sessão: Prof. Me. <b>Thiago Alcolumbre Viana</b>.</p><p>Trabalhos apresentados:</p><p>1. <i>Zoneamento Ecológico-Econômico e Sustentabilidade no Amapá</i>, por <b>Larissa Mendonça Guedes</b>;</p><p>2. <i>O Papel da Defensoria Pública nos Conflitos Fundiários Fluviais</i>, por <b>Rodrigo Otávio Pinheiro</b> e <b>Sabrina Leão Costa</b>.</p> |
| 3 | Apresentação de Comunicações Orais | Sala 104 | 2027-05-20T14:30 | 2027-05-20T17:30 | <p>Apresentação de pesquisas do Grupo de Trabalho de Hermenêutica Constitucional e Garantismo. Avaliadora responsável: Dra. <b>Helena Esteves Vasconcelos</b>.</p><p>Trabalhos apresentados:</p><p>1. <i>Ativismo Judicial e Proteção dos Mananciais Urbanos</i>, por <b>Carlos Eduardo Belfort</b>;</p><p>2. <i>Democracia Participativa e Licenciamento em Terras Devolutas</i>, por <b>Bruna Marinho Teles</b> e <b>Jorge Aníbal Picanço</b>.</p> |
| 4 | Mesa Temática | Auditório Tucuju | 2027-05-21T09:00 | 2027-05-21T11:45 | <p>Discussão sobre <i>Mineração, Transição Energética e Sustentabilidade no Escudo das Guianas</i>, sob a moderação da Profa. <b>Glória Maria Albuquerque</b>. Participam como expositores o Dr. <b>Arthur Nogueira Sobrinho</b> com o tema <i>Tributação Extrafiscal e Compensação Ambiental</i>, e a Dra. <b>Viviane Bastos Trindade</b> abordando <i>Responsabilidade Corporativa em Áreas Protegidas</i>.</p> |
| 5 | Intervalo | Foyer Principal | 2027-05-21T11:45 | 2027-05-21T14:00 |  |
| 6 | Painel de Encerramento | Auditório Tucuju | 2027-05-21T14:30 | 2027-05-21T17:00 | <p>Conferência de encerramento com o tema <i>Desafios da Governança Jurídica Transnacional no Século XXI</i>, apresentada pelo Prof. Titular <b>Waldir Pacheco Fontes</b> e mediada pela Dra. <b>Regina Coeli Barata</b>.</p> |

## sint-42-00052-1 — colunas — evento esportivo universitário com torneios e cerimônias

Ruídos: secoes, decorativo, quebra

### Texto

```text
I Jogos Universitários Integrados da Fronteira Norte (JUIFN 2023)
Programação 2023

Sábado (18/11/2023)
Horário
Atividade
Local
CERIMÔNIAS OFICIAIS
7h30 – 8h15
Concentração das Delegações
Acolhimento das atléticas e conferência de documentos com a coordenação de Lucas Bezerra.
8h30 – 9h30
Cerimônia de Abertura
Ginásio Poliesportivo
Desfile das atléticas, acendimento da pira e juramento dos atletas liderado por Amanda Picanço.
#juifnj2023
TORNEIOS MATUTINOS
10h – 12h
Torneio de Futsal Masculino -
Fase Classificatória
Quadra Coberta 1
Disputas da primeira fase entre os cursos de Exatas, Saúde e Humanas. Arbitragem coordenada por Carlos Eduardo Ramos.
10h – 12h
Torneio de Voleibol
Feminino - Fase
Classificatória
Quadra Coberta 2
Rodadas eliminatórias das chaves A e B sob supervisão da professora Renata Vales.
10h30
Competição de Xadrez Rápido
Etapa única pelo sistema suíço de 5 rodadas com ritmo de 15 minutos, organizada pelo mestre local Sérgio Maciel.
12h – 13h30
Almoço dos Atletas
Restaurante Universitário
Programação sujeita a alterações
13h30 – 15h
Mesa-Redonda
Auditório de Educação Física
Tema: Esporte Universitário na Amazônia: Desafios Logísticos e Inclusão Social, com participação de Profa. Dra. Elaine Guedes, Marcos Vinícius Silva e mediação de Tatiana Paiva.
FINAIS E DECISÕES
15h30 – 17h30
Disputa de Finais do Futsal e Voleibol
Ginásio Poliesportivo
Jogos decisivos de medalha de ouro e prata com narração esportiva de Diego Farias.
15h30
Torneio Universitário de Queimada Mista
Quadra Aberta
Competição integrativa entre atléticas e centros acadêmicos sob coordenação de Juliana Nery.
16h – 18h
Desafio de E-Sports Universitário
Subtítulo: Finais da Copa Interatléticas de FIFA e League of Legends. Organização do técnico Rodrigo Alencar.
CERIMÔNIAS OFICIAIS
18h30
Cerimônia de Premiação
Entrega de troféus, medalhas de honra e premiação da atlética campeã geral conduzida por Profa. Dra. Elaine Guedes e o diretor esportivo Lucas Bezerra.
Certificado de participação
19h30 – 22h
Confraternização e Bateria Show
Praça Universitária de Convivência
Apresentação especial das baterias universitárias Furiosa e Tsunami, com coordenação do estudante Gabriel Matos.
Siga @juifnj nas redes sociais

Apoio:
@juifnj
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | Concentração das Delegações |  | 2023-11-18T07:30 | 2023-11-18T08:15 | <p>Acolhimento das atléticas e conferência de documentos com a coordenação de <b>Lucas Bezerra</b>.</p> |
| 1 | Cerimônia de Abertura | Ginásio Poliesportivo | 2023-11-18T08:30 | 2023-11-18T09:30 | <p>Desfile das atléticas, acendimento da pira e juramento dos atletas liderado por <b>Amanda Picanço</b>.</p> |
| 2 | Torneio de Futsal Masculino - Fase Classificatória | Quadra Coberta 1 | 2023-11-18T10:00 | 2023-11-18T12:00 | <p>Disputas da primeira fase entre os cursos de Exatas, Saúde e Humanas. Arbitragem coordenada por <b>Carlos Eduardo Ramos</b>.</p> |
| 3 | Torneio de Voleibol Feminino - Fase Classificatória | Quadra Coberta 2 | 2023-11-18T10:00 | 2023-11-18T12:00 | <p>Rodadas eliminatórias das chaves A e B sob supervisão da professora <b>Renata Vales</b>.</p> |
| 4 | Competição de Xadrez Rápido |  | 2023-11-18T10:30 |  | <p>Etapa única pelo sistema suíço de 5 rodadas com ritmo de 15 minutos, organizada pelo mestre local <b>Sérgio Maciel</b>.</p> |
| 5 | Almoço dos Atletas | Restaurante Universitário | 2023-11-18T12:00 | 2023-11-18T13:30 |  |
| 6 | Mesa-Redonda | Auditório de Educação Física | 2023-11-18T13:30 | 2023-11-18T15:00 | <p>Tema: <i>Esporte Universitário na Amazônia: Desafios Logísticos e Inclusão Social</i>, com participação de <b>Profa. Dra. Elaine Guedes</b>, <b>Marcos Vinícius Silva</b> e mediação de <b>Tatiana Paiva</b>.</p> |
| 7 | Disputa de Finais do Futsal e Voleibol | Ginásio Poliesportivo | 2023-11-18T15:30 | 2023-11-18T17:30 | <p>Jogos decisivos de medalha de ouro e prata com narração esportiva de <b>Diego Farias</b>.</p> |
| 8 | Torneio Universitário de Queimada Mista | Quadra Aberta | 2023-11-18T15:30 |  | <p>Competição integrativa entre atléticas e centros acadêmicos sob coordenação de <b>Juliana Nery</b>.</p> |
| 9 | Desafio de E-Sports Universitário |  | 2023-11-18T16:00 | 2023-11-18T18:00 | <p>Subtítulo: <i>Finais da Copa Interatléticas de FIFA e League of Legends</i>. Organização do técnico <b>Rodrigo Alencar</b>.</p> |
| 10 | Cerimônia de Premiação |  | 2023-11-18T18:30 |  | <p>Entrega de troféus, medalhas de honra e premiação da atlética campeã geral conduzida por <b>Profa. Dra. Elaine Guedes</b> e o diretor esportivo <b>Lucas Bezerra</b>.</p> |
| 11 | Confraternização e Bateria Show | Praça Universitária de Convivência | 2023-11-18T19:30 | 2023-11-18T22:00 | <p>Apresentação especial das baterias universitárias Furiosa e Tsunami, com coordenação do estudante <b>Gabriel Matos</b>.</p> |

## sint-42-00164-0 — lista — fórum institucional de avaliação (CPA)

Ruídos: nenhum

### Texto

```text
VII FÓRUM DE AUTOAVALIAÇÃO INSTITUCIONAL DA CPA/IFRN
Reitoria do IFRN, Natal - RN
PROGRAMAÇÃO
© 2026 VII Fórum de Autoavaliação Institucional da CPA/IFRN

Quinta-feira, 14/05
das 08:30 às 10:00 | Acolhida e Apresentação dos Indicadores de Desempenho
Apresentação dos resultados da autoavaliação 2025 pela coordenadora geral da CPA, Profa. Clarice Medeiros de Vasconcelos, com ênfase no tema Metodologias Participativas e Impacto na Gestão Universitária.
das 10:30 às 12:00  Painel Temático
Auditório Pedro Silveira e Sá Leitão
Discussão com a participação de Marcos Aurélio Guedes e Luciana Dantas Pinheiro, abordando o painel A Integração da Comunidade Externa na Avaliação dos Cursos Técnicos e Superiores.
das 14:00 às 17:00 | Plenária Deliberativa e Encaminhamentos
Sessão para consolidação do relatório de autoavaliação e diretrizes para o próximo triênio, mediada pelo Prof. Rodrigo Tavares Peixoto.
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | Acolhida e Apresentação dos Indicadores de Desempenho |  | 2026-05-14T08:30 | 2026-05-14T10:00 | <p>Apresentação dos resultados da autoavaliação 2025 pela coordenadora geral da CPA, Profa. <b>Clarice Medeiros de Vasconcelos</b>, com ênfase no tema <i>Metodologias Participativas e Impacto na Gestão Universitária</i>.</p> |
| 1 | Painel Temático | Auditório Pedro Silveira e Sá Leitão | 2026-05-14T10:30 | 2026-05-14T12:00 | <p>Discussão com a participação de <b>Marcos Aurélio Guedes</b> e <b>Luciana Dantas Pinheiro</b>, abordando o painel <i>A Integração da Comunidade Externa na Avaliação dos Cursos Técnicos e Superiores</i>.</p> |
| 2 | Plenária Deliberativa e Encaminhamentos |  | 2026-05-14T14:00 | 2026-05-14T17:00 | <p>Sessão para consolidação do relatório de autoavaliação e diretrizes para o próximo triênio, mediada pelo Prof. <b>Rodrigo Tavares Peixoto</b>.</p> |

## sint-42-00360-0 — lista — encontro de mulheres na computação

Ruídos: decorativo, quebra

### Texto

```text
IV ENCONTRO MINEIRO DE MULHERES NA COMPUTAÇÃO
Departamento de Informática - Universidade Federal de Viçosa (UFV), Viçosa - MG
PROGRAMAÇÃO
Edição 2025

Quinta-feira, 15/05
das 08h30 às 09h15 - Recepção e Boas-Vindas
📍 Hall do CCE
Abertura do credenciamento e entrega de kits com a coordenadora geral Dra. Simone Rezende.
das 09h30 às 11h00  Palestra de Abertura
Local: Auditório Arthur da Silva Bernardes
Apresentação da palestra Desafios e Conquistas das Mulheres na Inteligência Artificial Moderna, ministrada pela Dra. Helena Guimarães da UFMG.
#emmc2025
das 11h00 às 11h30 | Intervalo para Café
📍 Área de Convivência do DCO
11h30
Roda de Conversa
📍 Auditório Arthur da Silva Bernardes
Debate sobre Trajetórias Femininas na Academia e Indústria Tech com mediação de Camila Duarte e participação de Eng. Mariana Silveira e Beatriz Nogueira.
das 14h00 às 17h30
Minicurso 1
Laboratório de Redes e Sistemas
Oficina prática de Introdução à Ciência de Dados com Python e Pandas ministrada pela doutoranda Leticia Albuquerque.
das 14h00 às 17h30 - Minicurso 2
📍 Laboratório de Informática 3
Treinamento de Desenvolvimento Web Inclusivo e Acessibilidade Digital com a instrutora Renata Meireles.
Patrocínio

Sexta-feira, 16/05
das 09h00 às 10h30 - Sessão de Pôsteres
Espaço Multiuso
Apresentação de pesquisas de graduação e pós-graduação. Destaque para o trabalho Visão Computacional Aplicada ao Monitoramento de Lavouras de Carla Peixoto e orientação de Profa. Vanessa Antunes.
10h45 - Palestra Técnica
📍 Auditório Arthur da Silva Bernardes
Palestra Engenharia de Software em Larga Escala e Microsserviços apresentada pela arquiteta de software Juliana Fontes.
#emmc2025
das 12h00 às 13h30 - Almoço Livre
Inscrições gratuitas
das 13h30 às 15h30  Painel de Carreira
📍 Auditório Arthur da Silva Bernardes
Discussão temática sobre Transição de Carreira e Liderança Feminina em Tecnologia coordenada por Gabriela Esteves com relatos de Tatiane Rocha e Daniela Faria.
das 16h00 às 17h30 | Mentoria em Grupo
Local: Salas de Estudos Integradas
Rodadas de mentoria acadêmica e profissional conduzidas pelas pesquisadoras Fernanda Brant e Aline Cotta.
17h45 - Premiação e Encerramento
📍 Auditório Arthur da Silva Bernardes
Entrega das menções honrosas aos melhores trabalhos e considerações finais pela comissão organizadora presidida por Dra. Simone Rezende.

Realização:
@emmc
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | Recepção e Boas-Vindas | Hall do CCE | 2025-05-15T08:30 | 2025-05-15T09:15 | <p>Abertura do credenciamento e entrega de kits com a coordenadora geral <b>Dra. Simone Rezende</b>.</p> |
| 1 | Palestra de Abertura | Auditório Arthur da Silva Bernardes | 2025-05-15T09:30 | 2025-05-15T11:00 | <p>Apresentação da palestra <i>Desafios e Conquistas das Mulheres na Inteligência Artificial Moderna</i>, ministrada pela <b>Dra. Helena Guimarães</b> da UFMG.</p> |
| 2 | Intervalo para Café | Área de Convivência do DCO | 2025-05-15T11:00 | 2025-05-15T11:30 |  |
| 3 | Roda de Conversa | Auditório Arthur da Silva Bernardes | 2025-05-15T11:30 |  | <p>Debate sobre <i>Trajetórias Femininas na Academia e Indústria Tech</i> com mediação de <b>Camila Duarte</b> e participação de <b>Eng. Mariana Silveira</b> e <b>Beatriz Nogueira</b>.</p> |
| 4 | Minicurso 1 | Laboratório de Redes e Sistemas | 2025-05-15T14:00 | 2025-05-15T17:30 | <p>Oficina prática de <i>Introdução à Ciência de Dados com Python e Pandas</i> ministrada pela doutoranda <b>Leticia Albuquerque</b>.</p> |
| 5 | Minicurso 2 | Laboratório de Informática 3 | 2025-05-15T14:00 | 2025-05-15T17:30 | <p>Treinamento de <i>Desenvolvimento Web Inclusivo e Acessibilidade Digital</i> com a instrutora <b>Renata Meireles</b>.</p> |
| 6 | Sessão de Pôsteres | Espaço Multiuso | 2025-05-16T09:00 | 2025-05-16T10:30 | <p>Apresentação de pesquisas de graduação e pós-graduação. Destaque para o trabalho <i>Visão Computacional Aplicada ao Monitoramento de Lavouras</i> de <b>Carla Peixoto</b> e orientação de <b>Profa. Vanessa Antunes</b>.</p> |
| 7 | Palestra Técnica | Auditório Arthur da Silva Bernardes | 2025-05-16T10:45 |  | <p>Palestra <i>Engenharia de Software em Larga Escala e Microsserviços</i> apresentada pela arquiteta de software <b>Juliana Fontes</b>.</p> |
| 8 | Almoço Livre |  | 2025-05-16T12:00 | 2025-05-16T13:30 |  |
| 9 | Painel de Carreira | Auditório Arthur da Silva Bernardes | 2025-05-16T13:30 | 2025-05-16T15:30 | <p>Discussão temática sobre <i>Transição de Carreira e Liderança Feminina em Tecnologia</i> coordenada por <b>Gabriela Esteves</b> com relatos de <b>Tatiane Rocha</b> e <b>Daniela Faria</b>.</p> |
| 10 | Mentoria em Grupo | Salas de Estudos Integradas | 2025-05-16T16:00 | 2025-05-16T17:30 | <p>Rodadas de mentoria acadêmica e profissional conduzidas pelas pesquisadoras <b>Fernanda Brant</b> e <b>Aline Cotta</b>.</p> |
| 11 | Premiação e Encerramento | Auditório Arthur da Silva Bernardes | 2025-05-16T17:45 |  | <p>Entrega das menções honrosas aos melhores trabalhos e considerações finais pela comissão organizadora presidida por <b>Dra. Simone Rezende</b>.</p> |

## sint-42-00063-0 — lista — evento de tecnologia com palestras de empresas e hackathon

Ruídos: nenhum

### Texto

```text
TechCorredor Summit & Hackathon 2026 2026
Programação

Sexta-feira, 15/05
8h – 9h  Recepção e Check-in de Participantes
Hall Central
Retirada de crachás, kits do participante e orientações gerais com a coordenadora de recepção Mariana Dornelles.
9h – 9h30 | Solenidade de Abertura
📍 Auditório Imembuí
Abertura oficial com os diretores Carlos Eduardo Pippi e Clarissa Medeiros apresentando o panorama de inovação do centro do estado.
9h30 – 10h30 - Palestra de Abertura
Local: Auditório Imembuí
Apresentação de Fernando Rossi com o tema Como a Inteligência Artificial Generativa e a Automação Conectada Estão Redefinindo o Mercado Corporativo Global nos Últimos Anos.
10h30 – 11h | Pausa para Café e Networking
11h – 12h  Briefing e Lançamento dos Desafios do Hackathon
Local: Arena Hacker
Apresentação das regras e metas da maratona conduzida por Lucas Fontana e Letícia Albuquerque.
11h – 12h
Palestra Técnica 1
📍 Auditório Imembuí
Palestra de Juliana Bastos sobre Arquiteturas Resilientes para Computação em Nuvem.
12h – 13h30 - Almoço Livre
13h30  Início da Prototipagem e Codificação
Local: Arena Hacker
Liberação das bancadas e início oficial do desenvolvimento de software e hardware pelas equipes inscritas.
14h – 15h30 | Oficina Técnica 1
Laboratório de Redes
Prática ministrada por Roberto Guimarães intitulada Estratégias Avançadas para Construção e Implantação de Microsserviços Escaláveis Utilizando Kubernetes e Ferramentas Modernas de Observabilidade Contínua.
15h30 – 16h30
Palestra Técnica 2
Apresentação do engenheiro Thiago Sampaio abordando Modelagem Preditiva com Rust para o Agronegócio.
16h – 17h30 | Oficina Técnica 2
📍 Laboratório de Redes
Atividade prática com foco em front-end com a instrutora Renata Silveira sobre Design Systems Modernos no Figma.
17h – 19h
Primeira Rodada de Mentoria Técnica
📍 Arena Hacker
Atendimento aos grupos com os mentores Felipe Fagundes, Camila Zanella e Diego Morales para validação da arquitetura de soluções.
18h – 19h30 | Painel de Debates
Discussão mediada por Aline Pozzobon com a presença dos convidados Marcos Vinicius Viero e Beatriz Brandão sobre Cibersegurança e Proteção de Dados Críticos no Setor Financeiro.
20h – 21h30 | Pausa para Jantar dos Hackers

Sábado, 16/05
2h – 4h | Sessão Madrugada de Validação de Pitch
📍 Arena Hacker
Simulações rápidas de pitch com os consultores Rodrigo Mello e Vanessa Rios.
7h30 – 8h30 - Café da Manhã dos Hackers
9h30 – 10h45 | Palestra de Inovação
Auditório Imembuí
Palestra de Guilherme Trevisan sobre Desafios e Métodos para Captação de Recursos e Fomento à Inovação Tecnológica em Startups Regionais Emergentes no Sul.
11h30 - Encerramento do Código e Congelamento dos Repositórios
Arena Hacker
Prazo fatal para submissão final dos códigos-fonte e links de demonstração no repositório oficial da competição.
12h – 13h30
Almoço dos Jurados e Participantes
14h – 16h30 - Apresentação Final dos Projetos
Local: Auditório Imembuí
Apresentação das 8 equipes finalistas para a banca julgadora presidida por Helena Schmidt e composta por Paulo Ricardo Antunes e Cíntia Flores.
17h – 18h | Cerimônia de Premiação e Encerramento
Auditório Imembuí
Anúncio dos vencedores do hackathon e entrega de troféus com os coordenadores Carlos Eduardo Pippi e Letícia Albuquerque.
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | Recepção e Check-in de Participantes | Hall Central | 2026-05-15T08:00 | 2026-05-15T09:00 | <p>Retirada de crachás, kits do participante e orientações gerais com a coordenadora de recepção <b>Mariana Dornelles</b>.</p> |
| 1 | Solenidade de Abertura | Auditório Imembuí | 2026-05-15T09:00 | 2026-05-15T09:30 | <p>Abertura oficial com os diretores <b>Carlos Eduardo Pippi</b> e <b>Clarissa Medeiros</b> apresentando o panorama de inovação do centro do estado.</p> |
| 2 | Palestra de Abertura | Auditório Imembuí | 2026-05-15T09:30 | 2026-05-15T10:30 | <p>Apresentação de <b>Fernando Rossi</b> com o tema <i>Como a Inteligência Artificial Generativa e a Automação Conectada Estão Redefinindo o Mercado Corporativo Global nos Últimos Anos</i>.</p> |
| 3 | Pausa para Café e Networking |  | 2026-05-15T10:30 | 2026-05-15T11:00 |  |
| 4 | Briefing e Lançamento dos Desafios do Hackathon | Arena Hacker | 2026-05-15T11:00 | 2026-05-15T12:00 | <p>Apresentação das regras e metas da maratona conduzida por <b>Lucas Fontana</b> e <b>Letícia Albuquerque</b>.</p> |
| 5 | Palestra Técnica 1 | Auditório Imembuí | 2026-05-15T11:00 | 2026-05-15T12:00 | <p>Palestra de <b>Juliana Bastos</b> sobre <i>Arquiteturas Resilientes para Computação em Nuvem</i>.</p> |
| 6 | Almoço Livre |  | 2026-05-15T12:00 | 2026-05-15T13:30 |  |
| 7 | Início da Prototipagem e Codificação | Arena Hacker | 2026-05-15T13:30 |  | <p>Liberação das bancadas e início oficial do desenvolvimento de software e hardware pelas equipes inscritas.</p> |
| 8 | Oficina Técnica 1 | Laboratório de Redes | 2026-05-15T14:00 | 2026-05-15T15:30 | <p>Prática ministrada por <b>Roberto Guimarães</b> intitulada <i>Estratégias Avançadas para Construção e Implantação de Microsserviços Escaláveis Utilizando Kubernetes e Ferramentas Modernas de Observabilidade Contínua</i>.</p> |
| 9 | Palestra Técnica 2 |  | 2026-05-15T15:30 | 2026-05-15T16:30 | <p>Apresentação do engenheiro <b>Thiago Sampaio</b> abordando <i>Modelagem Preditiva com Rust para o Agronegócio</i>.</p> |
| 10 | Oficina Técnica 2 | Laboratório de Redes | 2026-05-15T16:00 | 2026-05-15T17:30 | <p>Atividade prática com foco em front-end com a instrutora <b>Renata Silveira</b> sobre <i>Design Systems Modernos no Figma</i>.</p> |
| 11 | Primeira Rodada de Mentoria Técnica | Arena Hacker | 2026-05-15T17:00 | 2026-05-15T19:00 | <p>Atendimento aos grupos com os mentores <b>Felipe Fagundes</b>, <b>Camila Zanella</b> e <b>Diego Morales</b> para validação da arquitetura de soluções.</p> |
| 12 | Painel de Debates |  | 2026-05-15T18:00 | 2026-05-15T19:30 | <p>Discussão mediada por <b>Aline Pozzobon</b> com a presença dos convidados <b>Marcos Vinicius Viero</b> e <b>Beatriz Brandão</b> sobre <i>Cibersegurança e Proteção de Dados Críticos no Setor Financeiro</i>.</p> |
| 13 | Pausa para Jantar dos Hackers |  | 2026-05-15T20:00 | 2026-05-15T21:30 |  |
| 14 | Sessão Madrugada de Validação de Pitch | Arena Hacker | 2026-05-16T02:00 | 2026-05-16T04:00 | <p>Simulações rápidas de pitch com os consultores <b>Rodrigo Mello</b> e <b>Vanessa Rios</b>.</p> |
| 15 | Café da Manhã dos Hackers |  | 2026-05-16T07:30 | 2026-05-16T08:30 |  |
| 16 | Palestra de Inovação | Auditório Imembuí | 2026-05-16T09:30 | 2026-05-16T10:45 | <p>Palestra de <b>Guilherme Trevisan</b> sobre <i>Desafios e Métodos para Captação de Recursos e Fomento à Inovação Tecnológica em Startups Regionais Emergentes no Sul</i>.</p> |
| 17 | Encerramento do Código e Congelamento dos Repositórios | Arena Hacker | 2026-05-16T11:30 |  | <p>Prazo fatal para submissão final dos códigos-fonte e links de demonstração no repositório oficial da competição.</p> |
| 18 | Almoço dos Jurados e Participantes |  | 2026-05-16T12:00 | 2026-05-16T13:30 |  |
| 19 | Apresentação Final dos Projetos | Auditório Imembuí | 2026-05-16T14:00 | 2026-05-16T16:30 | <p>Apresentação das 8 equipes finalistas para a banca julgadora presidida por <b>Helena Schmidt</b> e composta por <b>Paulo Ricardo Antunes</b> e <b>Cíntia Flores</b>.</p> |
| 20 | Cerimônia de Premiação e Encerramento | Auditório Imembuí | 2026-05-16T17:00 | 2026-05-16T18:00 | <p>Anúncio dos vencedores do hackathon e entrega de troféus com os coordenadores <b>Carlos Eduardo Pippi</b> e <b>Letícia Albuquerque</b>.</p> |

## sint-42-00202-0 — tabela — congresso científico nacional com sessões técnicas de artigos

Ruídos: decorativo

### Texto

```text
Programação - XXIV Congresso Brasileiro de Ciência da Computação e Engenharia de Software
Edição 2026

13/05
Horário | Atividade | Local | Descrição
(09:00 - 10:00) | Cerimônia de Abertura | Auditório Principal | Abertura oficial do evento com a presença da coordenadora geral Dra. Juliana Prado e representantes da comissão organizadora.
(10:30 - 12:00) | Sessão Técnica 1 |  | Apresentação de artigos selecionados na trilha de Sistemas Inteligentes. Coordenação por Prof. Roberto Meireles. Artigo em destaque: Otimização Heurística em Grafos Dinâmicos por Lucas Silveira.
Organização:
14:00 | Sessão Técnica 2 | Sala Araucária | Apresentação de trabalhos na área de Engenharia de Software. Apresentação do artigo Refatoração Contínua em Microsserviços por Camila Duarte e Rodrigo Vasconcelos.

14/05
Horário | Atividade | Local | Descrição
(09:00 - 10:45) | Painel de Especialistas | Auditório Principal | Debate sobre Desafios Regulatórios da Inteligência Artificial Generativa no Brasil com a participação de Dra. Mariana Fagundes e Carlos Eduardo Pires.
(11:00 - 12:30) | Sessão Técnica 1 |  | Continuação das apresentações da trilha de Inteligência Computacional. Apresentação do trabalho Modelos Preditivos para Séries Temporais Financeiras pelo autor Felipe Sanches.
Acesse o QR Code
14:30 | Sessão de Pôsteres | Foyer das Araucárias | Exibição e avaliação de projetos de iniciação científica. Trabalho em destaque: Arquiteturas Resilientes para IoT, apresentado por Beatriz Nogueira e orientado por Prof. Marcos Zanin.
Programação sujeita a alterações

15/05
Horário | Atividade | Local | Descrição
(09:30 - 11:00) | Palestra Convidada |  | Palestra intitulada Novas Fronteiras da Computação Quântica Aplicada ministrada pelo pesquisador Dr. Henrique Albuquerque.
Patrocínio
(11:15 - 12:45) | Sessão Técnica 3 | Sala Iguaçu | Apresentação dos artigos da trilha de Segurança da Informação e Privacidade, mediada por Profa. Vanessa Guimarães. Trabalho: Protocolos Criptográficos para Aplicações Médicas por Alexandre Motta.
16:00 | Sessão de Encerramento e Premiação |  | Premiação dos melhores artigos do congresso e considerações finais com a comissão organizadora liderada por Dra. Juliana Prado.

Realização:
@xcbcces
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | Cerimônia de Abertura | Auditório Principal | 2026-05-13T09:00 | 2026-05-13T10:00 | <p>Abertura oficial do evento com a presença da coordenadora geral <b>Dra. Juliana Prado</b> e representantes da comissão organizadora.</p> |
| 1 | Sessão Técnica 1 |  | 2026-05-13T10:30 | 2026-05-13T12:00 | <p>Apresentação de artigos selecionados na trilha de Sistemas Inteligentes. Coordenação por <b>Prof. Roberto Meireles</b>. Artigo em destaque: <i>Otimização Heurística em Grafos Dinâmicos</i> por <b>Lucas Silveira</b>.</p> |
| 2 | Sessão Técnica 2 | Sala Araucária | 2026-05-13T14:00 |  | <p>Apresentação de trabalhos na área de Engenharia de Software. Apresentação do artigo <i>Refatoração Contínua em Microsserviços</i> por <b>Camila Duarte</b> e <b>Rodrigo Vasconcelos</b>.</p> |
| 3 | Painel de Especialistas | Auditório Principal | 2026-05-14T09:00 | 2026-05-14T10:45 | <p>Debate sobre <i>Desafios Regulatórios da Inteligência Artificial Generativa no Brasil</i> com a participação de <b>Dra. Mariana Fagundes</b> e <b>Carlos Eduardo Pires</b>.</p> |
| 4 | Sessão Técnica 1 |  | 2026-05-14T11:00 | 2026-05-14T12:30 | <p>Continuação das apresentações da trilha de Inteligência Computacional. Apresentação do trabalho <i>Modelos Preditivos para Séries Temporais Financeiras</i> pelo autor <b>Felipe Sanches</b>.</p> |
| 5 | Sessão de Pôsteres | Foyer das Araucárias | 2026-05-14T14:30 |  | <p>Exibição e avaliação de projetos de iniciação científica. Trabalho em destaque: <i>Arquiteturas Resilientes para IoT</i>, apresentado por <b>Beatriz Nogueira</b> e orientado por <b>Prof. Marcos Zanin</b>.</p> |
| 6 | Palestra Convidada |  | 2026-05-15T09:30 | 2026-05-15T11:00 | <p>Palestra intitulada <i>Novas Fronteiras da Computação Quântica Aplicada</i> ministrada pelo pesquisador <b>Dr. Henrique Albuquerque</b>.</p> |
| 7 | Sessão Técnica 3 | Sala Iguaçu | 2026-05-15T11:15 | 2026-05-15T12:45 | <p>Apresentação dos artigos da trilha de Segurança da Informação e Privacidade, mediada por <b>Profa. Vanessa Guimarães</b>. Trabalho: <i>Protocolos Criptográficos para Aplicações Médicas</i> por <b>Alexandre Motta</b>.</p> |
| 8 | Sessão de Encerramento e Premiação |  | 2026-05-15T16:00 |  | <p>Premiação dos melhores artigos do congresso e considerações finais com a comissão organizadora liderada por <b>Dra. Juliana Prado</b>.</p> |

## sint-42-00334-0 — tabela — evento esportivo universitário com torneios e cerimônias

Ruídos: secoes, quebra

### Texto

```text
XIV Jogos Universitários Sul-Mato-Grossenses 2023
Programação

19 de outubro de 2023
Horário | Atividade | Local | Descrição
RECEPÇÃO E ADMINISTRATIVO
08h00 às 11h30 | Credenciamento das Delegações | Hall Principal do Ginásio Guanandizão | Recepção das atléticas e verificação de documentação esportiva sob coordenação de Mariana Siqueira Castro.
09h30 às 11h00 | Congresso Técnico | Auditório da Reitoria UFMS | Sorteio de chaves e deliberação das diretrizes disciplinares. Coordenação geral com Prof. Dr. Marcos Vinicius Alencar e os delegados Patrícia Rios e Carlos Eduardo Guimarães.
12h00 às 13h30 | Pausa para Almoço
Torneio de Quadra
13h30 às 15h00 | Futsal Masculino - Fase de Grupos | Quadra Poliesportiva 1 - Guanandizão | Partida inicial da chave A entre Atlética Engenharia UFMS e Atlética Medicina UCDB. Arbitragem de Ricardo Farias Mendes.
13h30 às 15h00 | Voleibol Feminino - Fase de Grupos | Ginásio Moreninho - UFMS | Confronto da chave B. Arbitragem com Juliana Dornelles.
15h15 às 16h45 | Futsal Masculino - Fase de Grupos | Quadra Poliesportiva 1 - Guanandizão | Segunda rodada da chave A entre Atlética Direito Uniderp e Atlética Exatas UFGD.
15h15 às 16h45 | Voleibol Feminino - Fase de Grupos | Ginásio Moreninho - UFMS | Disputa entre Atlética Saúde UEMS e Atlética Agronomia UCDB.
16h45 às 17h30 | Coffee Break | Espaço Atleta - Guanandizão
ATIVIDADES CIENTÍFICAS E FORMATIVAS
17h30 às 18h45 | Palestra | Auditório Central do Guanandizão | Tema: Prevenção de Lesões e Rendimento em Atletas Universitários. Palestrante: Dra. Simone Rezende Brandão (Fisioterapeuta Esportiva da Seleção Brasileira Universitária).
Cerimônias Oficiais
19h30 | Cerimônia de Abertura | Arena Principal do Guanandizão | Desfile oficial das delegações universitárias, juramento do atleta conduzido por Thiago Albuquerque e acendimento da pira com a atleta homenageada Bruna Calheiros.

20 de outubro de 2023
Horário | Atividade | Local | Descrição
Torneio de Quadra
08h00 às 09h30 | Basquetebol Masculino - Fase Preliminar | Ginásio Moreninho - UFMS | Partida de abertura do grupo A. Coordenação da mesa por Renan Batistote.
08h00 às 09h30 | Handebol Feminino - Fase Preliminar | Quadra Poliesportiva 2 - Guanandizão | Primeira partida entre Atlética Enfermagem UFMS e Atlética Humanas UFMS.
ESPORTES INDIVIDUAIS
08h30 às 11h30 | Eliminatórias de Atletismo | Pista de Atletismo da UFMS | Provas de 100m rasos, salto em distância e arremesso de peso. Coordenação técnica de Prof. Geraldo Matos Couto.
TORNEIO DE QUADRA
09h45 às 11h15 | Basquetebol Masculino - Fase Preliminar | Ginásio Moreninho - UFMS | Confronto entre Atlética Economia UCDB e Atlética Computação UFMS.
09h45 às 11h15 | Handebol Feminino - Fase Preliminar | Quadra Poliesportiva 2 - Guanandizão | Disputa de vaga para semifinal entre Atlética Comunicação Uniderp e Atlética Odontologia UCDB.
11h30 às 13h00 | Pausa para Almoço
Atividades Científicas e Formativas
13h00 às 14h30 | Sessão de Pôsteres | Saguão das Faculdades Integradas - UFMS | Apresentação de trabalhos científicos na área de Ciências do Esporte. Coordenação: Profa. Dra. Letícia Viana Paim. Trabalhos em exibição: Análise de Composição Corporal em Universitários Praticantes de Crossfit, autoria de Felipe Prado Sanches e Lucas NogueiraEstratégias de Hidratação sob o Calor Centro-Oestino, de Carla Mendonça NevesImpactos Psicológicos da Ansiedade Pré-Competição em Jogos Regionais, com Tatiane Bastos Ferraz
Esportes Individuais
13h30 às 17h00 | Torneio de Judô | Dojô Central do Guanandizão | Categorias Ligeiro, Meio-médio, Médio e Pesado masculino e feminino. Coordenação de arbitragem: Sensei Hélio Kenji Takahashi.
TORNEIO DE QUADRA
14h00 às 15h30 | Futsal Masculino - Quartas de Final | Quadra Poliesportiva 1 - Guanandizão | Primeiro confronto eliminatório direto. Apuração com o delegado Carlos Eduardo Guimarães.
Atividades Científicas e Formativas
14h45 às 16h15 | Mesa-Redonda | Auditório Central do Guanandizão | Debate sobre Gestão e Sustentabilidade Financeira das Atléticas Universitárias. Debatedores convidados: Leandro Martins Paes (Presidente da Liga das Atléticas de Campo Grande), Camila Duarte Ferreira (Consultora Esportiva) e mediação de Prof. André Teodoro Valente.
TORNEIO DE QUADRA
15h45 às 17h15 | Futsal Masculino - Quartas de Final | Quadra Poliesportiva 1 - Guanandizão | Segundo confronto eliminatório direto.
17h15 às 17h45 | Lanche da Tarde | Espaço Atleta - Guanandizão
Esportes Individuais
17h45 às 19h45 | Finais da Natação | Parque Aquático da UFMS | Finais dos 50m livre, 100m borboleta e revezamento 4x50m medley mista. Cronometragem eletrônica coordenada por Marcelo Antunes Bittencourt.
20h00 | Desafio de Cheerleading | Arena Principal do Guanandizão | Apresentação competitiva de líderes de torcida universitárias. Comissão julgadora formada por Valéria Rios, Diego Fontes e Kelly Silveira Santos.

21 de outubro de 2023
Horário | Atividade | Local | Descrição
ESPORTES INDIVIDUAIS
08h00 às 11h00 | Torneio de Xadrez Rápido | Salão Nobre da Reitoria UFMS | Disputa no sistema suíço em cinco rodadas. Direção do árbitro nacional Fabrício Fagundes de Melo.
Torneio de Quadra
08h30 às 10h00 | Voleibol Feminino - Semifinal | Ginásio Moreninho - UFMS | Semifinal 1 com árbitro principal Juliana Dornelles.
Esportes Individuais
09h00 às 11h30 | Finais de Atletismo | Pista de Atletismo da UFMS | Disputas das finais dos 400m, 1500m rasos e revezamento 4x100m. Supervisão da pista por Prof. Geraldo Matos Couto.
TORNEIO DE QUADRA
10h15 às 11h45 | Voleibol Feminino - Semifinal | Ginásio Moreninho - UFMS | Semifinal 2 definindo a segunda finalista do torneio.
12h00 às 13h30 | Pausa para Almoço
FINAIS DOS ESPORTES COLETIVOS
13h30 às 15h00 | Disputa de 3º Lugar - Basquete Masculino | Ginásio Moreninho - UFMS | Confronto pela medalha de bronze universitária. Coordenação da mesa por Renan Batistote.
14h30 às 16h00 | Grande Final do Voleibol Feminino | Arena Principal do Guanandizão | Decisão do título feminino de vôlei com transmissão ao vivo pelas redes da Federação.
16h30 às 18h00 | Grande Final do Futsal Masculino | Arena Principal do Guanandizão | Decisão do ouro universitário do torneio de futsal. Apresentação conduzida pelo locutor Wagner Barreto.
18h15 às 19h00 | Coffee Break de Confraternização | Hall Social do Guanandizão
CERIMÔNIAS OFICIAIS
19h00 às 21h00 | Cerimônia de Premiação e Encerramento | Arena Principal do Guanandizão | Entrega de troféus gerais para a atlética campeã geral e melhor torcida. Pronunciamento do presidente da comissão organizadora Prof. Dr. Marcos Vinicius Alencar e entrega das medalhas de honra ao mérito pelos coordenadores Mariana Siqueira Castro e Patrícia Rios.
21h30 | Festa Oficial de Encerramento | Estacionamento Coberto do Guanandizão | Confraternização final dos estudantes com apresentação de baterias universitárias e DJ convidado.
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | Credenciamento das Delegações | Hall Principal do Ginásio Guanandizão | 2023-10-19T08:00 | 2023-10-19T11:30 | <p>Recepção das atléticas e verificação de documentação esportiva sob coordenação de <b>Mariana Siqueira Castro</b>.</p> |
| 1 | Congresso Técnico | Auditório da Reitoria UFMS | 2023-10-19T09:30 | 2023-10-19T11:00 | <p>Sorteio de chaves e deliberação das diretrizes disciplinares. Coordenação geral com <b>Prof. Dr. Marcos Vinicius Alencar</b> e os delegados <b>Patrícia Rios</b> e <b>Carlos Eduardo Guimarães</b>.</p> |
| 2 | Pausa para Almoço |  | 2023-10-19T12:00 | 2023-10-19T13:30 |  |
| 3 | Futsal Masculino - Fase de Grupos | Quadra Poliesportiva 1 - Guanandizão | 2023-10-19T13:30 | 2023-10-19T15:00 | <p>Partida inicial da chave A entre Atlética Engenharia UFMS e Atlética Medicina UCDB. Arbitragem de <b>Ricardo Farias Mendes</b>.</p> |
| 4 | Voleibol Feminino - Fase de Grupos | Ginásio Moreninho - UFMS | 2023-10-19T13:30 | 2023-10-19T15:00 | <p>Confronto da chave B. Arbitragem com <b>Juliana Dornelles</b>.</p> |
| 5 | Futsal Masculino - Fase de Grupos | Quadra Poliesportiva 1 - Guanandizão | 2023-10-19T15:15 | 2023-10-19T16:45 | <p>Segunda rodada da chave A entre Atlética Direito Uniderp e Atlética Exatas UFGD.</p> |
| 6 | Voleibol Feminino - Fase de Grupos | Ginásio Moreninho - UFMS | 2023-10-19T15:15 | 2023-10-19T16:45 | <p>Disputa entre Atlética Saúde UEMS e Atlética Agronomia UCDB.</p> |
| 7 | Coffee Break | Espaço Atleta - Guanandizão | 2023-10-19T16:45 | 2023-10-19T17:30 |  |
| 8 | Palestra | Auditório Central do Guanandizão | 2023-10-19T17:30 | 2023-10-19T18:45 | <p>Tema: <i>Prevenção de Lesões e Rendimento em Atletas Universitários</i>. Palestrante: <b>Dra. Simone Rezende Brandão</b> (Fisioterapeuta Esportiva da Seleção Brasileira Universitária).</p> |
| 9 | Cerimônia de Abertura | Arena Principal do Guanandizão | 2023-10-19T19:30 |  | <p>Desfile oficial das delegações universitárias, juramento do atleta conduzido por <b>Thiago Albuquerque</b> e acendimento da pira com a atleta homenageada <b>Bruna Calheiros</b>.</p> |
| 10 | Basquetebol Masculino - Fase Preliminar | Ginásio Moreninho - UFMS | 2023-10-20T08:00 | 2023-10-20T09:30 | <p>Partida de abertura do grupo A. Coordenação da mesa por <b>Renan Batistote</b>.</p> |
| 11 | Handebol Feminino - Fase Preliminar | Quadra Poliesportiva 2 - Guanandizão | 2023-10-20T08:00 | 2023-10-20T09:30 | <p>Primeira partida entre Atlética Enfermagem UFMS e Atlética Humanas UFMS.</p> |
| 12 | Eliminatórias de Atletismo | Pista de Atletismo da UFMS | 2023-10-20T08:30 | 2023-10-20T11:30 | <p>Provas de 100m rasos, salto em distância e arremesso de peso. Coordenação técnica de <b>Prof. Geraldo Matos Couto</b>.</p> |
| 13 | Basquetebol Masculino - Fase Preliminar | Ginásio Moreninho - UFMS | 2023-10-20T09:45 | 2023-10-20T11:15 | <p>Confronto entre Atlética Economia UCDB e Atlética Computação UFMS.</p> |
| 14 | Handebol Feminino - Fase Preliminar | Quadra Poliesportiva 2 - Guanandizão | 2023-10-20T09:45 | 2023-10-20T11:15 | <p>Disputa de vaga para semifinal entre Atlética Comunicação Uniderp e Atlética Odontologia UCDB.</p> |
| 15 | Pausa para Almoço |  | 2023-10-20T11:30 | 2023-10-20T13:00 |  |
| 16 | Sessão de Pôsteres | Saguão das Faculdades Integradas - UFMS | 2023-10-20T13:00 | 2023-10-20T14:30 | <p>Apresentação de trabalhos científicos na área de Ciências do Esporte. Coordenação: <b>Profa. Dra. Letícia Viana Paim</b>.</p><p>Trabalhos em exibição:</p><i>Análise de Composição Corporal em Universitários Praticantes de Crossfit</i>, autoria de <b>Felipe Prado Sanches</b> e <b>Lucas Nogueira</b><i>Estratégias de Hidratação sob o Calor Centro-Oestino</i>, de <b>Carla Mendonça Neves</b><i>Impactos Psicológicos da Ansiedade Pré-Competição em Jogos Regionais</i>, com <b>Tatiane Bastos Ferraz</b> |
| 17 | Torneio de Judô | Dojô Central do Guanandizão | 2023-10-20T13:30 | 2023-10-20T17:00 | <p>Categorias Ligeiro, Meio-médio, Médio e Pesado masculino e feminino. Coordenação de arbitragem: <b>Sensei Hélio Kenji Takahashi</b>.</p> |
| 18 | Futsal Masculino - Quartas de Final | Quadra Poliesportiva 1 - Guanandizão | 2023-10-20T14:00 | 2023-10-20T15:30 | <p>Primeiro confronto eliminatório direto. Apuração com o delegado <b>Carlos Eduardo Guimarães</b>.</p> |
| 19 | Mesa-Redonda | Auditório Central do Guanandizão | 2023-10-20T14:45 | 2023-10-20T16:15 | <p>Debate sobre <i>Gestão e Sustentabilidade Financeira das Atléticas Universitárias</i>. Debatedores convidados: <b>Leandro Martins Paes</b> (Presidente da Liga das Atléticas de Campo Grande), <b>Camila Duarte Ferreira</b> (Consultora Esportiva) e mediação de <b>Prof. André Teodoro Valente</b>.</p> |
| 20 | Futsal Masculino - Quartas de Final | Quadra Poliesportiva 1 - Guanandizão | 2023-10-20T15:45 | 2023-10-20T17:15 | <p>Segundo confronto eliminatório direto.</p> |
| 21 | Lanche da Tarde | Espaço Atleta - Guanandizão | 2023-10-20T17:15 | 2023-10-20T17:45 |  |
| 22 | Finais da Natação | Parque Aquático da UFMS | 2023-10-20T17:45 | 2023-10-20T19:45 | <p>Finais dos 50m livre, 100m borboleta e revezamento 4x50m medley mista. Cronometragem eletrônica coordenada por <b>Marcelo Antunes Bittencourt</b>.</p> |
| 23 | Desafio de Cheerleading | Arena Principal do Guanandizão | 2023-10-20T20:00 |  | <p>Apresentação competitiva de líderes de torcida universitárias. Comissão julgadora formada por <b>Valéria Rios</b>, <b>Diego Fontes</b> e <b>Kelly Silveira Santos</b>.</p> |
| 24 | Torneio de Xadrez Rápido | Salão Nobre da Reitoria UFMS | 2023-10-21T08:00 | 2023-10-21T11:00 | <p>Disputa no sistema suíço em cinco rodadas. Direção do árbitro nacional <b>Fabrício Fagundes de Melo</b>.</p> |
| 25 | Voleibol Feminino - Semifinal | Ginásio Moreninho - UFMS | 2023-10-21T08:30 | 2023-10-21T10:00 | <p>Semifinal 1 com árbitro principal <b>Juliana Dornelles</b>.</p> |
| 26 | Finais de Atletismo | Pista de Atletismo da UFMS | 2023-10-21T09:00 | 2023-10-21T11:30 | <p>Disputas das finais dos 400m, 1500m rasos e revezamento 4x100m. Supervisão da pista por <b>Prof. Geraldo Matos Couto</b>.</p> |
| 27 | Voleibol Feminino - Semifinal | Ginásio Moreninho - UFMS | 2023-10-21T10:15 | 2023-10-21T11:45 | <p>Semifinal 2 definindo a segunda finalista do torneio.</p> |
| 28 | Pausa para Almoço |  | 2023-10-21T12:00 | 2023-10-21T13:30 |  |
| 29 | Disputa de 3º Lugar - Basquete Masculino | Ginásio Moreninho - UFMS | 2023-10-21T13:30 | 2023-10-21T15:00 | <p>Confronto pela medalha de bronze universitária. Coordenação da mesa por <b>Renan Batistote</b>.</p> |
| 30 | Grande Final do Voleibol Feminino | Arena Principal do Guanandizão | 2023-10-21T14:30 | 2023-10-21T16:00 | <p>Decisão do título feminino de vôlei com transmissão ao vivo pelas redes da Federação.</p> |
| 31 | Grande Final do Futsal Masculino | Arena Principal do Guanandizão | 2023-10-21T16:30 | 2023-10-21T18:00 | <p>Decisão do ouro universitário do torneio de futsal. Apresentação conduzida pelo locutor <b>Wagner Barreto</b>.</p> |
| 32 | Coffee Break de Confraternização | Hall Social do Guanandizão | 2023-10-21T18:15 | 2023-10-21T19:00 |  |
| 33 | Cerimônia de Premiação e Encerramento | Arena Principal do Guanandizão | 2023-10-21T19:00 | 2023-10-21T21:00 | <p>Entrega de troféus gerais para a atlética campeã geral e melhor torcida. Pronunciamento do presidente da comissão organizadora <b>Prof. Dr. Marcos Vinicius Alencar</b> e entrega das medalhas de honra ao mérito pelos coordenadores <b>Mariana Siqueira Castro</b> e <b>Patrícia Rios</b>.</p> |
| 34 | Festa Oficial de Encerramento | Estacionamento Coberto do Guanandizão | 2023-10-21T21:30 |  | <p>Confraternização final dos estudantes com apresentação de baterias universitárias e DJ convidado.</p> |

## sint-42-00026-1 — tabela — feira de negócios e empreendedorismo do Sebrae

Ruídos: secoes

### Texto

```text
Feira Sebrae de Inovação e Negócios da Zona da Mata 2026
Programação 2026

14 de maio de 2026
Horário | Atividade | Local | Descrição
(8h - 9h30) | Credenciamento e Retirada de Crachás | Hall de Entrada
(9h30 - 10h30) | Cerimônia de Abertura | Auditório Principal | Abertura oficial com a presença de Carlos Henrique Ribeiro e autoridades locais para dar início à semana de empreendedorismo regional.
Palestras Magna e Tendências
(10h30 - 11h45) | Palestra | Auditório Principal | Palestra Transformação Digital e o Futuro dos Pequenos Negócios ministrada por Mariana Castro Alvim.
(12h - 13h30) | Pausa para Almoço
Capacitações Empresariais
(14h - 16h) | Oficina Prática | Sala Multiuso A | Tema: Modelagem de Negócios Inovadores com Business Model Canvas, conduzido por Rodrigo Duarte Faria.
ATENDIMENTOS E CONSULTORIAS
(16h - 18h) | Consultoria Individual Sebrae | Espaço Conexões | Atendimento individualizado para diagnóstico financeiro e mercadológico da sua empresa com Patrícia Gomes Moreira.

15 de maio de 2026
Horário | Atividade | Local | Descrição
PALESTRAS MAGNA E TENDÊNCIAS
(9h - 10h15) | Palestra |  | Apresentação de Agritech: Conectando a Produção Rural à Tecnologia de Ponta por Fernando Peixoto Sampaio.
(10h15 - 10h45) | Coffee Break e Networking | Área de Convivência
Capacitações Empresariais
(10h45 - 12h30) | Oficina Prática | Sala Multiuso B | Tema: Estratégias de Tráfego Pago e Redes Sociais para o Varejo ministrado por Juliana Vasconcelos.
(12h30 - 14h) | Pausa para Almoço
(14h30 - 16h30) | Sessão de Negócios | Pavilhão de Exposição | Dinâmica rápida de aproximação comercial entre microempresas e grandes compradores da região, coordenada por Leandro Silveira.
Atendimentos e Consultorias
(16h30 - 18h) | Consultoria Individual Sebrae | Espaço Conexões | Atendimento focado em marketing digital e vendas online orientado por Lucas Medeiros.

16 de maio de 2026
Horário | Atividade | Local | Descrição
(9h - 10h30) | Painel de Debates | Auditório Principal | Debate sobre Acelerando Startups no Ecossistema Universitário de Viçosa com a participação de Beatriz Mendonça e Guilherme Tavares.
(10h30 - 11h) | Coffee Break e Networking
(11h - 12h30) | Demoday de Startups | Auditório Principal | Apresentação final de pitches das startups incubadas para a banca de investidores coordenada por Renata Queiroz.
(12h30 - 14h) | Pausa para Almoço
(14h - 16h) | Cerimônia de Encerramento e Premiação | Auditório Principal | Premiação dos destaques da feira e encerramento conduzido por Carlos Henrique Ribeiro.
```

### Rótulo

| # | nome | lugar | início | fim | descrição |
|---|---|---|---|---|---|
| 0 | Credenciamento e Retirada de Crachás | Hall de Entrada | 2026-05-14T08:00 | 2026-05-14T09:30 |  |
| 1 | Cerimônia de Abertura | Auditório Principal | 2026-05-14T09:30 | 2026-05-14T10:30 | <p>Abertura oficial com a presença de <b>Carlos Henrique Ribeiro</b> e autoridades locais para dar início à semana de empreendedorismo regional.</p> |
| 2 | Palestra | Auditório Principal | 2026-05-14T10:30 | 2026-05-14T11:45 | <p>Palestra <i>Transformação Digital e o Futuro dos Pequenos Negócios</i> ministrada por <b>Mariana Castro Alvim</b>.</p> |
| 3 | Pausa para Almoço |  | 2026-05-14T12:00 | 2026-05-14T13:30 |  |
| 4 | Oficina Prática | Sala Multiuso A | 2026-05-14T14:00 | 2026-05-14T16:00 | <p>Tema: <i>Modelagem de Negócios Inovadores com Business Model Canvas</i>, conduzido por <b>Rodrigo Duarte Faria</b>.</p> |
| 5 | Consultoria Individual Sebrae | Espaço Conexões | 2026-05-14T16:00 | 2026-05-14T18:00 | <p>Atendimento individualizado para diagnóstico financeiro e mercadológico da sua empresa com <b>Patrícia Gomes Moreira</b>.</p> |
| 6 | Palestra |  | 2026-05-15T09:00 | 2026-05-15T10:15 | <p>Apresentação de <i>Agritech: Conectando a Produção Rural à Tecnologia de Ponta</i> por <b>Fernando Peixoto Sampaio</b>.</p> |
| 7 | Coffee Break e Networking | Área de Convivência | 2026-05-15T10:15 | 2026-05-15T10:45 |  |
| 8 | Oficina Prática | Sala Multiuso B | 2026-05-15T10:45 | 2026-05-15T12:30 | <p>Tema: <i>Estratégias de Tráfego Pago e Redes Sociais para o Varejo</i> ministrado por <b>Juliana Vasconcelos</b>.</p> |
| 9 | Pausa para Almoço |  | 2026-05-15T12:30 | 2026-05-15T14:00 |  |
| 10 | Sessão de Negócios | Pavilhão de Exposição | 2026-05-15T14:30 | 2026-05-15T16:30 | <p>Dinâmica rápida de aproximação comercial entre microempresas e grandes compradores da região, coordenada por <b>Leandro Silveira</b>.</p> |
| 11 | Consultoria Individual Sebrae | Espaço Conexões | 2026-05-15T16:30 | 2026-05-15T18:00 | <p>Atendimento focado em marketing digital e vendas online orientado por <b>Lucas Medeiros</b>.</p> |
| 12 | Painel de Debates | Auditório Principal | 2026-05-16T09:00 | 2026-05-16T10:30 | <p>Debate sobre <i>Acelerando Startups no Ecossistema Universitário de Viçosa</i> com a participação de <b>Beatriz Mendonça</b> e <b>Guilherme Tavares</b>.</p> |
| 13 | Coffee Break e Networking |  | 2026-05-16T10:30 | 2026-05-16T11:00 |  |
| 14 | Demoday de Startups | Auditório Principal | 2026-05-16T11:00 | 2026-05-16T12:30 | <p>Apresentação final de pitches das startups incubadas para a banca de investidores coordenada por <b>Renata Queiroz</b>.</p> |
| 15 | Pausa para Almoço |  | 2026-05-16T12:30 | 2026-05-16T14:00 |  |
| 16 | Cerimônia de Encerramento e Premiação | Auditório Principal | 2026-05-16T14:00 | 2026-05-16T16:00 | <p>Premiação dos destaques da feira e encerramento conduzido por <b>Carlos Henrique Ribeiro</b>.</p> |
