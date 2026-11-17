# Revisão do juiz — 20 vereditos

O juiz (Claude) julgou **923 atividades de 80 exemplos** (40 de cada professor). Resultado: 921 `ok`, 1 `campo`, 1 `irreal`.
Abaixo, 20 desses vereditos em 10 exemplos. Para cada um, leia o texto e diga no `juiz_revisao.csv` se **concorda** (`sim`/`nao`) com o veredito do juiz. Se discordar, escreva o veredito certo em `observacao`.

Vereditos possíveis: `ok`, `nome_regra` (palestrante/local/horário/descrição no nome), `descricao` (conteúdo inventado, faltando ou de outra atividade; tags não contam), `campo` (local/data/hora não confere), `irreal` (implausível), `outro`.
Nomes com tema após ":" ou " - " são aceitos (decisão de 2026-11-16). A descrição é a versão limpa do texto (sem o ruído de OCR).

> Os 2 exemplos com erro (`sint-43-00064-1` e `sint-43-00133-0`) mostram o texto **antigo**: os dois problemas vinham do renderizador e já foram corrigidos (ver o fim deste arquivo).

## sint-43-00133-0

Layout `cartaz` · perfil `enxuto` · encontro de professores da educação básica

```text
Jornada Pedagógica da Rede Estadual do Amapá 2023
Programação 2023

QUARTA-FEIRA - 08/02/23
14h
FORMAÇÃO POR ÁREA
14h
FORMAÇÃO POR ÁREA
```

| # | atividade | nome | lugar | início | fim | descrição | veredito do juiz | justificativa |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | FORMAÇÃO POR ÁREA |  | 2023-02-08T14:00 |  |  | **irreal** | Duplicata exata de i=0 (mesmo nome e horário, sem nada que distinga); exemplo degenerado/incoerente. |
| 2 | 0 | FORMAÇÃO POR ÁREA |  | 2023-02-08T14:00 |  |  | **ok** |  |

## sint-42-00193-0

Layout `lista` · perfil `completo` · mostra de extensão universitária

```text
XIV Mostra de Extensão e Cultura do Centro-Oeste 2024
Programação

24/10
(8h - 9h)  Credenciamento e Entrega de Materiais
Local: Hall do Centro de Eventos Ricardo Freua Bufáiçal
(9h - 10h30)
Sessão Solene de Abertura
Auditório Nobre
Tema: Universidade pública e saberes tradicionais do Cerrado.
Abertura oficial conduzida pela coordenadora-geral Profa. Dra. Elaine Cristina Peixoto, com participação do conferencista convidado Mestre Aílton Krenak e da vice-reitora Profa. Camila Guimarães Rocha.
(10h30 - 11h) - Pausa para Café e Convivência
Comunicações Orais
(11h - 12h30)  Sessão Temática 1
Bloco Humanidades - Sala 104
Eixo: Educação Popular e Cidadania.
Coordenação de Prof. Marcos Aurélio Silveira.
Trabalhos apresentados:
- Alfabetização de Jovens e Adultos na Periferia de Goiânia por Juliana Dias de Souza e Carlos Mendes Faria;
- Cineclube Comunitário como Instrumento Pedagógico por Amanda Ribeiro Teles.
(12h30 - 14h) - Intervalo de Almoço
(14h - 16h) | Sessão Temática 2
📍 Bloco Humanidades - Sala 106
Eixo: Saúde Coletiva e Extensão Rural.
Coordenação de Dra. Simone Paiva Castro.
Apresentações:
- Promotores Comunitários de Saúde em Assentamentos Rurais de Goiás por Renato Cavalcanti e Dra. Simone Paiva Castro;
- Vigilância em Saúde Bucal para Populações Ribeirinhas por Tatiane Ferreira Lopes.
(16h30 - 18h) - Roda de Conversa Intercultural
Tema: Patrimônio Imaterial e Memória Kalunga.
Facilitadores: Seu Jorge Kalunga e Profa. Lúcia Tavares Batista.

25/10
(8h30 - 11h)
Mostra de Banners Extensionistas
Local: Tenda Expositiva Central
Exposição de pôsteres de projetos de extensão das áreas de Ciências Ambientais, Agrárias e Sociais Aplicadas. Avaliação com a presença dos relatores Prof. Danilo Albuquerque e Profa. Vanessa Meireles.
Oficinas Formativas
(11h - 12h30)  Oficina Prática 1
Laboratório de Informática 3
Tema: Mapeamento Colaborativo de Territórios Vulneráveis com Software Livre.
Ministrante: Igor Resende Vilela.
(14h - 16h)
Oficina Prática 2
Tema: Hortas Urbanas Agroecológicas em Espaços Escolares.
Ministrantes: Carla Beatriz Nogueira e Prof. Roberto Antunes da Mata.
(16h30 - 18h)
Plenária de Encerramento e Premiação
Auditório Nobre
Apresentação dos resultados da mostra e entrega do Prêmio Mérito Extensionista Paulo Freire aos melhores projetos de 2024, presidida por Profa. Dra. Elaine Cristina Peixoto.
```

| # | atividade | nome | lugar | início | fim | descrição | veredito do juiz | justificativa |
|---|---|---|---|---|---|---|---|---|
| 3 | 1 | Sessão Solene de Abertura | Auditório Nobre | 2024-10-24T09:00 | 2024-10-24T10:30 | <p>Tema: <i>Universidade pública e saberes tradicionais do Cerrado</i>.</p><p>Abertura oficial conduzida pela coordenadora-geral <b>Profa. Dra. Elaine Cristina Peixoto</b>, com participação do conferencista convidado <b>Mestre Aílton Krenak</b> e da vice-reitora <b>Profa. Camila Guimarães Rocha</b>.</p> | **ok** |  |
| 4 | 4 | Intervalo de Almoço |  | 2024-10-24T12:30 | 2024-10-24T14:00 |  | **ok** |  |

## sint-42-00062-0

Layout `cartaz` · perfil `completo` · mostra de extensão universitária

```text
XIV Mostra Intercampi de Extensão e Cultura da UFRJ 2027
Programação

Quarta-feira (19/05/2027)
08h30 - 10h00
CREDENCIAMENTO E ENTREGA DE MATERIAIS
HALL DO BLOCO A
10h00 - 12h00
RODA DE CONVERSA
Debate sobre A Curricularização da Extensão e os Impactos nas Comunidades Tradicionais da Baía de Guanabara, mediado pela Profa. Dra. Clarice Peixoto e com participação de lideranças comunitárias convidadas, incluindo o mestre pescador Severino dos Santos.
AUDITÓRIO HÉLIO FRAGA
12h00 - 13h30
ALMOÇO LIVRE

Quinta-feira (20/05/2027)
14h00 - 16h00
SESSÃO ORAL 1
Apresentação do projeto Alfabetização Ecológica nas Escolas da Maré coordenado por Felipe Fagundes e apresentado pela bolsista Juliana Meireles. Avaliação da banca presidida pelo Prof. Henrique Vianna.
SALA A-102
16h00 - 16h40
CAFÉ COMPARTILHADO
PÁTIO DAS ESCULTURAS

Sexta-feira (21/05/2027)
09h30 - 11h30
SESSÃO ORAL 2
Exposição do relato de experiência Promoção da Saúde Integral em Abrigos Institucionais pelo estudante de enfermagem Lucas Barreto sob supervisão da Profa. Márcia Guimarães.
SALA A-102
```

| # | atividade | nome | lugar | início | fim | descrição | veredito do juiz | justificativa |
|---|---|---|---|---|---|---|---|---|
| 5 | 1 | RODA DE CONVERSA | AUDITÓRIO HÉLIO FRAGA | 2027-05-19T10:00 | 2027-05-19T12:00 | <p>Debate sobre <i>A Curricularização da Extensão e os Impactos nas Comunidades Tradicionais da Baía de Guanabara</i>, mediado pela Profa. Dra. <b>Clarice Peixoto</b> e com participação de lideranças comunitárias convidadas, incluindo o mestre pescador <b>Severino dos Santos</b>.</p> | **ok** |  |
| 6 | 2 | ALMOÇO LIVRE |  | 2027-05-19T12:00 | 2027-05-19T13:30 |  | **ok** |  |

## sint-43-00064-1

Layout `colunas` · perfil `completo` · evento de tecnologia com palestras de empresas e hackathon

```text
Pantanal Dev Summit 2024
Programação 2024

19/09
Horário
Atividade
Local
19h00 – 19h30
Abertura
19h30 – 20h30
Arquitetura de Microsserviços na
Prática
Auditório A
19h30 – 20h30
Dados Abertos no Agro
Auditório B

20/09
Horário
Atividade
Local
08h00 – 12h00
Hackathon
#pds2024

21/09
Horário
Atividade
Local
14h00 – 17h00
Pitch dos Times
Siga @pds nas redes sociais

Apoio:
@pds
```

| # | atividade | nome | lugar | início | fim | descrição | veredito do juiz | justificativa |
|---|---|---|---|---|---|---|---|---|
| 7 | 3 | Hackathon |  | 2024-09-20T08:00 | 2024-09-21T12:00 |  | **campo** | Texto: 20/09 08h00–12h00; dataFim rotulada 2024-09-21T12:00 (dia errado, deveria ser 2024-09-20T12:00). |
| 8 | 4 | Pitch dos Times |  | 2024-09-21T14:00 | 2024-09-21T17:00 |  | **ok** |  |

## sint-43-00212-0

Layout `tabela` · perfil `sem_lugar` · evento religioso/comunitário com celebrações e oficinas

```text
Festa de São Sebastião 2027 - Comunidade do Alto da Boa Vista
Programação 2027

20/01
Horário | Atividade | Descrição
07:00 – 08:00 | Missa Solene
19:00 – 20:30 | Missa Solene | Presidida por Dom Ricardo Albuquerque, seguida de procissão.
```

| # | atividade | nome | lugar | início | fim | descrição | veredito do juiz | justificativa |
|---|---|---|---|---|---|---|---|---|
| 9 | 1 | Missa Solene |  | 2027-01-20T19:00 | 2027-01-20T20:30 | <p>Presidida por <b>Dom Ricardo Albuquerque</b>, seguida de procissão.</p> | **ok** |  |
| 10 | 0 | Missa Solene |  | 2027-01-20T07:00 | 2027-01-20T08:00 |  | **ok** |  |

## sint-42-00251-1

Layout `cartaz` · perfil `completo` · seminário de sustentabilidade e meio ambiente

```text
I SEMINÁRIO TRIANGULINO DE SUSTENTABILIDADE E GESTÃO AMBIENTAL
Centro de Convenções Center Minas, Uberlândia - MG
PROGRAMAÇÃO

17 de maio de 2023
08:00 - 09:00
RECEPÇÃO E ENTREGA DE CRACHÁS
HALL DE ENTRADA
09:00 - 10:30
SESSÃO DE ABERTURA
Boas-vindas institucionais e lançamento do fórum de debates com a participação da c0ordenadora Dra. Mariana Vasconcellos e do secretário Roberto Silveira Mendes.
AUDITÓRIO PAU-BRASIL
Ciclo de Debates
10:45 - 12:15
ESPAÇO DE DIÁLOGOS AMBIENTAIS
Apresentação e reflexão obre Transição Encrgética e Biocombstíveis no Cerrado Mineiro, com a presença do engenheiro Lucas Bernardes Fagundes.
Inscrições gratuitas
Capacitações Técnicas
14:00 - 16:30
OFICINA PRÁTICA
Módulo temático Recuperação| de Nascentes e Técnicas de Bioengenharia, ministrado pl|o especialista Carlos Edardo Pires.
LABORATÓRIO 3 - BLOCO VERDE
14:00 - 16:30
OFICINA PRÁTICA
Módulo temático Mapeamento de Áreas de Preservação Permanente com QGIS, conduzido pela geógrafa Patrícia Nogueira Campos.
SALA DE CAPACITAÇÃO 1
16:45 - 18:00
MOSTRA DE BANNERS ACADÊMICOS
Apresentação dos pôsteres selecionados. Avaliação do trabalho Indicadores de Ecoeficincia na Bacia do Rio Araguari pelo relator Prof. Fernando Guima'rães.
www.stsga.co m.br

18 de maio de 2023
CICLO DE DEBATES
08:30 - 10:00
PAINEL TEMÁTICO
Dis|cussão sobre Manejo Sustentável do So1o e Agricultura de Baixo C*arbono com os palestrante|s* Sérgio Antunes Lima e Cláudia Meireles Rocha.
AUDITÓRIO PAU-BRASIL
Vagas limitadas!
10:15 - 12:00
ESPAÇO DE DIÁLOGOS AMBIENTAIS
Paine1 com foco 'no te|ma Gestão Coletiva de Recursos Hídricos cm Bacias Hidográficas, contando com mediação da pesquisadora Juliana Prado Alencar.
AUDITÓRIO IPÊ-AMARELO
Comunicações Orais
14:00 - 16:00
COMUNICAÇÃO ORAL
Ses são com leitura do estudo Estratégias de Logística Reversa de Em|balagens de Defensivos pelo pesquisador Henr|ique Vilela Moreira.
Capacitações Técnicas
14:00 - 16:30
OFICINA PRÁTICA
Módulo temático Compostagem Termofílicae Ap roveitament|o de Resíduos Agroindustriais, conduzido pelo engenheiro  agrônomo Marcelo Diniz Esteves.
LABORATÓRIO 3 - BLOCO VERDE
Comunicações Orais
16:15 - 18:00
COMUNICAÇÃO ORAL
Apresentação do trabalho Análise da Pegada Hídrica d a Suinocultura Regional pela doutoranda Beatriz Fontes Cunha.
18:30
RODA DE SABERES TRADICIONAIS
Encon'tro focado no projeto Fi|toterapia Popular e Uso Consciente da Flora Nativa com mediação de Dona Sebastiana de Carvalho.
TENDA EXTERNA
Vagas limitadas!

19 de maio de 2023
Ciclo de Debates
08:30 - 10:00
PAINEL TEMÁTICO
Exposição sobre Cidades Inteligentes e* Drenagem Urbana Sustentável apresentada pela urbanista Aline Cordciro omes.
AUDITÓRIO PAU-BRASIL
10:00 - 10:30
PAUSA PARA CAFÉ E CONEXÕES
10:30 - 12:00
COLÓQUIO DE POLÍTICAS PÚBLICAS
Debate sobre Licenciamento  Ambiental Municipal: Avanços e Gargalos com a promotora Vanessa Miranda Toledo e o consultor Tiago Ramos Peixoto.
14:30 - 16:30
PAINEL DE ENCERRAMENTO
Apresentação magna intitulada O Papel do Cerrao na Segurança Climática Global, ministrada pelo ambientalista Dr. Vald emar Rabelo Sobrinho.
AUDITÓRIO PAU-BRASIL
16:30 - 17:30
PREMIAÇÃO DE MÉRITO ECOLÓGICO
Entrega das menções honrosas conduzia por Mariana Vasconcellos e pelo patrono Gilberto Siquei|ra Leite.
AUDITÓRIO PAU-BRASIL
17:30
APRESENTAÇÃO CULTURAL
Espetáculo de encerramento do violeiro Tarcísio Manhães tocando temas tradicionais mineiros.

Realização:
@stsga
```

| # | atividade | nome | lugar | início | fim | descrição | veredito do juiz | justificativa |
|---|---|---|---|---|---|---|---|---|
| 11 | 1 | SESSÃO DE ABERTURA | AUDITÓRIO PAU-BRASIL | 2023-05-17T09:00 | 2023-05-17T10:30 | <p>Boas-vindas institucionais e lançamento do fórum de debates com a participação da coordenadora <b>Dra. Mariana Vasconcellos</b> e do secretário <b>Roberto Silveira Mendes</b>.</p> | **ok** |  |
| 12 | 10 | COMUNICAÇÃO ORAL |  | 2023-05-18T16:15 | 2023-05-18T18:00 | <p>Apresentação do trabalho <i>Análise da Pegada Hídrica da Suinocultura Regional</i> pela doutoranda <b>Beatriz Fontes Cunha</b>.</p> | **ok** |  |

## sint-42-00093-0

Layout `tabela` · perfil `completo` · evento de inovação no agronegócio

```text
AgroTech Amazônia 2026: Inovação e Bioeconomia Sustentável
Programação 2026

18 • Agosto
Horário	Atividade	Local	Descrição
das 08:00 às 09:30	Credenciamento e Retirada de Crachás	Foyer Central
das 09:30 às 11:00	Painel de Abertura	Auditório Castanheira	Abertura oficial dos trabalhos sobre o futuro das cadeias produtivas amazônicas. Coordenação: Dra. Simone Alencar. Palestra magna: O papel estratégico das tecnologias disruptivas aplicadas à bioeconomia e conservação florestal na nova fronteira agroecológica mundial, ministrada por Dr. Marcos Vinícius Guimarães.
das 14:00 às 16:00	Rodada de Demonstrações Tecnológicas	Arena Inovação Norte	Apresentação prática de maquinários e protótipos em campo reduzido. Condução de Eng. Thiago Furtado e Profa. Camila Nogueira.
das 16:00 às 16:30	Pausa para Café e Networking	Espaço Samaúma

19 • Agosto
Horário	Atividade	Local	Descrição
das 09:00 às 12:00	Oficina Prática 1	Laboratório de Solos e Imagens	Tema: Desenvolvimento e implementação de algoritmos para monitoramento autônomo da saúde hídrica de plantios de açaí com sensoriamento remoto avançado. Instrutores: Dr. Raimundo Nonato Castro e MSc. Beatriz Vasconcelos.
das 12:00 às 14:00	Almoço Livre
das 14:00 às 17:00	Oficina Prática 2	Sala de Capacitação 3	Tema: Integração lavoura-pecuária-floresta em pequenas propriedades do norte brasileiro utilizando plataformas digitais colaborativas e agricultura de precisão acessível. Instrutor: Dr. Marcelo Tavares com assistência de Helena Rocha.

20 • Agosto
Horário	Atividade	Local	Descrição
das 09:00 às 11:30	Sessão de Pôsteres Científicos	Hall do Pavilhão B	Coordenação: Dra. Vanessa Meireles. Trabalhos em exposição: Bioinsumos derivados de sementes amazônicas para controle biológico de pragas, apresentado por Lucas Barreto. Rastreabilidade de cadeias da castanha-do-pará via tecnologia blockchain descentralizada, apresentado por Juliana Pantoja e Fernando Braga.
das 14:00 às 16:00	Rodada de Demonstrações Tecnológicas	Estande Demo AgroTech	Segunda rodada dedicada a sensores de umidade de baixo custo e telemetria para dendê. Coordenador: Eng. Thiago Furtado com os pesquisadores convidados Dra. Clarice Cunha e Renato Souza.
das 16:30 às 18:00	Solenidade de Premiação e Encerramento	Auditório Castanheira	Entrega do Prêmio Amazônia Inovadora 2026 conduzida por Dra. Simone Alencar e Carlos Eduardo Pinheiro.
```

| # | atividade | nome | lugar | início | fim | descrição | veredito do juiz | justificativa |
|---|---|---|---|---|---|---|---|---|
| 13 | 1 | Painel de Abertura | Auditório Castanheira | 2026-08-18T09:30 | 2026-08-18T11:00 | <p>Abertura oficial dos trabalhos sobre o futuro das cadeias produtivas amazônicas.</p><p>Coordenação: <b>Dra. Simone Alencar</b>.</p><p>Palestra magna: <i>O papel estratégico das tecnologias disruptivas aplicadas à bioeconomia e conservação florestal na nova fronteira agroecológica mundial</i>, ministrada por <b>Dr. Marcos Vinícius Guimarães</b>.</p> | **ok** |  |
| 14 | 6 | Oficina Prática 2 | Sala de Capacitação 3 | 2026-08-19T14:00 | 2026-08-19T17:00 | <p>Tema: <i>Integração lavoura-pecuária-floresta em pequenas propriedades do norte brasileiro utilizando plataformas digitais colaborativas e agricultura de precisão acessível</i>.</p><p>Instrutor: <b>Dr. Marcelo Tavares</b> com assistência de <b>Helena Rocha</b>.</p> | **ok** |  |

## sint-43-00073-0

Layout `lista` · perfil `completo` · mostra de extensão universitária

```text
Expo Extensão UFMS 2024
Programação

Quarta-feira (25/09/2024)
07h30 | Credenciamento
(08h00 - 09h00) - Abertura
Local: Auditório
(09h00 - 11h00) | Roda de Conversa com Comunidades
📍 Sala 3
Com lideranças da aldeia urbana Marçal de Souza.
(09h00 - 11h30)  Sessão de Pôsteres
Hall Central
Organização:
(11h30 - 13h00)
Almoço
13h00
Apresentações Culturais
Auditório

Realização:
@eeu
```

| # | atividade | nome | lugar | início | fim | descrição | veredito do juiz | justificativa |
|---|---|---|---|---|---|---|---|---|
| 15 | 2 | Roda de Conversa com Comunidades | Sala 3 | 2024-09-25T09:00 | 2024-09-25T11:00 | <p>Com lideranças da aldeia urbana <b>Marçal de Souza</b>.</p> | **ok** |  |
| 16 | 5 | Apresentações Culturais | Auditório | 2024-09-25T13:00 |  |  | **ok** |  |

## sint-42-00423-0

Layout `colunas` · perfil `completo` · evento de tecnologia com palestras de empresas e hackathon

```text
BSB Tech Summit & Hackathon 2024
Programação 2024

Quarta-feira, 15/05
Horário
Atividade
Local
(8h - 9h30)
Recepção e Check-in
Foyer Principal
(9h30 - 10h30)
Cerimônia de Abertura
Auditório Master
Abertura oficiál do evento com a presença de autoridades e organizadores, incluindo Maríana Siqueira e Carlos Eduardo Prao.
Palestras de Empresas
(10h45 - 12h)
Palestra Empresarial
Auditório Master
Apresentação da empresa Cloud*Scale Tech conduzida por Roberto Albuquerque com o tema Arquiteturas Resilientes n a Nuvem Pública.
(12h - 13h30)
Intervalo para Almoço
(13h30 - 14h45)
Palestra Empresarial
Auditório Master
P|ainel corporativo da FinTech Brasil com Beatriz Mendonça abordando A Evolução dos Pagamentos Instantâneos e Inteligência Artificial.
Maratona Hackathon
(15h - 16h30)
Lançamento dos Desafios do Hackathon
Arena Hacker
Apresentação  d|os desafios de inovação cívica e governamental pelos mentores Gu|ilherme Dorneles e Patrícia Ramos.
(16h30 - 18h)
Mentoria Técnica
Espaço Co-working
Atendimento às equipes iniciantes com o instrutor Fabano Neves para validação da stack tecnológica.
PALESTRAS DE EMPRESAS
(18h30 - 19h45)
Palestra Noturna
Auditório Master
Palestra de encerramento |do primeiro dia com Daniele Vasc|oncelos aresentando Cibersegurança e Proteç ão de Dados no Setor Público.

Quinta-feira, 16/05
Horário
Atividade
Local
TRILHA CORPORATIVA
(9h - 10h30)
Painel de Discussão
Auditório Master
Debate sobre tendências com* mediaço de Lucas Fontes e debatedores Aline Guimarães e Marcos Vinícius Terr a discutindo Desafios da Adoção de Inteligê'ncia Artificial Generativa em Grandes Corporações.
Maratona Hackathon
(10h30 - 12h)
Mentoria Técnica
Arena Hacker
Sssão de alinhamento e suporte de dados com Vanessa Botelho e Henrique Santana para squads competidores.
(12h - 13h30)
Intervalo para Almoço
TRILHA PRÁTICA
(13h30 - 15h30)
Oficina Prática
Laboratório 1
Oficiná ha nds-on conduzida por Juliana Meireles focada no treinamento Desenvolvimento de APIs Modernas com GraphQL e Node.js.
PALESTRAS DE EMPRESAS
(15h45 - 17h)
Palestra Empresarial
Auditório Master
Palestra técnica oferecida pel*a DataInsights com Thiago Faria discutindo Big Data e Tomada de Decisão em Tempo Real.
Maratona Hackathon
(17h15 - 18h30)
Sessão de Checkpoint
Arena Hacker
Primeira rodada de validação de prresso e entregáveis preliminares com os avaliadores Renata Silveira e Paulo Castr.
22h
Corujão de Codificação
Arena Hacker
Virada de noite para os times do hackathon, acompanhados pelo monitor técnico Diego Barbosa.

Sexta-feira, 17/05
Horário
Atividade
Local
Palestras de Empresas
(9h - 10h15)
Palestra Empresarial
Auditório Master
Apresentação da empresa GovTech Inovações por Camil Duarte sobre Transformação Digital dos Serviços Públicos.
TRILHA PRÁTICA
(10h30 - 12h)
Oficina Prática
Laboratório 2
Workshop ministrado por Leonardo Freitas demonstrando Estratégias de Deplo Contínu0 com Kubernetes e GitOps.
(12h - 13h30)
Intervalo para Almoço
TRILHA CORPORATIVA
(13h30 - 15h)
Painel de Discussão
Auditório Master
Debate sobre capital de risco com Rodrigo Assis, Fernanda Tavares e Sérgio Nogueira explorando Investimentos em Startups e o Ecossistemá do Centro-Oeste.*
MARATONA HACKATHON
(15h15 - 17h)
Mentoria Técnica
Espaço Co-working
Última rodada de consultoria técnica e refinameno de arquitetura antes daentrega final, com Patrícia Ramos.
(17h15 - 18h45)
Oficina de Pitch
Sala de Treinamento
Treinamento intensivode orató|ria e apresentaão para investidores conduzido por Lorena Magalhães.

Sábado, 18/05
Horário
Atividade
Local
Maratona Hackathon
(9h - 9h30)
Encerramento do Código
Arena Hacker
Congelamento dos repositórios e encerramento oficial da programação do hackathon sob supervisão de Guilherme Dorneles.
Palestras de Empresas
(9h30 - 10h45)
Palestra Empresarial
Auditório Master
Keynote da empresa CyberDefense liderado por André Queiroz trazendo O Futuro do Trabalho e Carreira em Engenharia de Software.
Maratona Hackathon
(11h - 12h30)
Rodada de Pitches
Auditório Master
Apresentação dos projetos finalistas para a comissã o julgadora composta por Mariana Siqueira, Robert Albuquerque e Carlos Eduardo Prado.
(12h30 - 14h)
Intervalo para Almoço
(14h - 15h30)
Deliberação da Banca
Sala VIP
(16h - 17h30)
Premiação do Hackathon
Auditório Master
Cerimônia de anúncio das equipes vencedora's e entrega de prêmios  com mediação de Carlos Eduardo Prado.
17h30
Encerramento e Happy Hour
Foyer Principal
Confraternizaão final e networking entr'e empresas participantes, mentores e participantes do congresso.
```

| # | atividade | nome | lugar | início | fim | descrição | veredito do juiz | justificativa |
|---|---|---|---|---|---|---|---|---|
| 17 | 1 | Cerimônia de Abertura | Auditório Master | 2024-05-15T09:30 | 2024-05-15T10:30 | <p>Abertura oficial do evento com a presença de autoridades e organizadores, incluindo <b>Mariana Siqueira</b> e <b>Carlos Eduardo Prado</b>.</p> | **ok** |  |
| 18 | 19 | Mentoria Técnica | Espaço Co-working | 2024-05-17T15:15 | 2024-05-17T17:00 | <p>Última rodada de consultoria técnica e refinamento de arquitetura antes da entrega final, com <b>Patrícia Ramos</b>.</p> | **ok** |  |

## sint-43-00111-1

Layout `colunas` · perfil `completo` · evento de inovação no agronegócio

```text
AGROINOVA VIÇOSA 2027
Centro de Ensino e Extensão - UFV
PROGRAMAÇÃO

17 de março de 2027
Horário
Atividade
Local
08h00 – 08h30
Café de Boas-Vindas
08h30 – 10h00
Painel Agricultura Digital
Auditório
10h30 – 12h00
Pitch de Startups
Auditório
10h30 – 12h00
Vitrine de Tecnologias
Hall de Exposições
```

| # | atividade | nome | lugar | início | fim | descrição | veredito do juiz | justificativa |
|---|---|---|---|---|---|---|---|---|
| 19 | 1 | Painel Agricultura Digital | Auditório | 2027-03-17T08:30 | 2027-03-17T10:00 |  | **ok** |  |
| 20 | 3 | Vitrine de Tecnologias | Hall de Exposições | 2027-03-17T10:30 | 2027-03-17T12:00 |  | **ok** |  |

## Problemas encontrados e corrigidos

1. **Fim em outro dia (`campo`)**: uma atividade das 8h de um dia às 12h do dia seguinte aparecia no texto como "08h00 - 12h00", sem a data do fim. Afetava 10 exemplos. Agora o texto mostra a data do fim ("08h00 - 21/09 12h00") quando ela não dá para deduzir pelos horários; viradas de noite ("21h - 6h") continuam sem data.
2. **Duplicata idêntica (`irreal`)**: a mesma oficina em duas salas, no mesmo horário; o perfil `enxuto` apagava o local e deixava duas atividades iguais no rótulo. Afetava 39 exemplos. Agora o perfil recua (`enxuto` → `sem_descricao` → `completo`; `sem_lugar` → `completo`) quando apagar o local criaria duplicatas.

Total de atividades para revisar: 20.