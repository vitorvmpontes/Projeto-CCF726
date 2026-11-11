"""Especificações de eventos sintéticos (fonte B).

Cada `EventoSpec` descreve o evento que o LLM professor deve inventar: tipo,
número de dias e de atividades, ano e quais "casos difíceis" devem aparecer.
O sorteio é determinístico (semente), para o dataset ser reproduzível.
"""

from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field

TIPOS_EVENTO = [
    "semana acadêmica de um curso de graduação",
    "congresso científico nacional com sessões técnicas de artigos",
    "simpósio de pós-graduação",
    "feira de negócios e empreendedorismo do Sebrae",
    "evento de tecnologia com palestras de empresas e hackathon",
    "jornada médica / congresso de saúde",
    "festival cultural com shows, oficinas e exposições",
    "mostra de extensão universitária",
    "encontro de professores da educação básica",
    "evento de inovação no agronegócio",
    "semana de calouros com atividades de integração",
    "workshop de inteligência artificial com minicursos",
    "fórum institucional de avaliação (CPA)",
    "encontro de mulheres na computação",
    "maratona de programação e game jam",
    "congresso jurídico com mesas-redondas",
    "festival gastronômico com aulas-show",
    "evento religioso/comunitário com celebrações e oficinas",
    "seminário de sustentabilidade e meio ambiente",
    "evento esportivo universitário com torneios e cerimônias",
]

CIDADES = [
    "Belo Horizonte - MG", "Viçosa - MG", "Florestal - MG", "São Paulo - SP", "Campinas - SP",
    "Rio de Janeiro - RJ", "Niterói - RJ", "Curitiba - PR", "Porto Alegre - RS", "Florianópolis - SC",
    "Salvador - BA", "Recife - PE", "Fortaleza - CE", "Natal - RN", "Manaus - AM", "Belém - PA",
    "Macapá - AP", "Goiânia - GO", "Brasília - DF", "Cuiabá - MT", "Campo Grande - MS", "Vitória - ES",
    "Uberlândia - MG", "Juiz de Fora - MG", "Londrina - PR", "Santa Maria - RS", "João Pessoa - PB",
]

# Casos difíceis observados no TCC (ver evaluation/results/ANALISE_BASELINE.md)
CASOS = {
    "nomes_repetidos": "a mesma atividade (mesmo nome) acontece mais de uma vez, em horários ou locais diferentes",
    "titulos_longos": "2 ou 3 palestras/oficinas têm títulos longos (12 a 20 palavras); as demais têm títulos de tamanho comum",
    "sem_horario_fim": "algumas atividades não têm horário de término (dataFim null)",
    "sem_local": "várias atividades não têm local (lugar null)",
    "descricoes_ricas": "várias descrições com palestrantes, coordenadores e lista de trabalhos apresentados",
    "subtitulo_separado": "atividades com tema/subtítulo que deve ir na descrição, não no nome",
    "intervalos": "inclui intervalos como coffee break, almoço e credenciamento",
    "atividades_paralelas": "atividades simultâneas em salas diferentes",
}


@dataclass
class EventoSpec:
    id: str
    tipo: str
    cidade: str
    ano: int
    n_dias: int
    n_atividades: int
    casos: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def sortear_specs(n: int, semente: int = 42, ano_min: int = 2023, ano_max: int = 2027) -> list[EventoSpec]:
    rng = random.Random(semente)
    specs = []
    for k in range(n):
        n_dias = rng.choices([1, 2, 3, 4, 5], weights=[25, 25, 30, 12, 8])[0]
        n_ativ = rng.randint(max(3, 2 * n_dias), min(45, 12 * n_dias))
        casos = rng.sample(list(CASOS), k=rng.randint(1, 4))
        specs.append(EventoSpec(
            id=f"sint-{semente}-{k:05d}",
            tipo=rng.choice(TIPOS_EVENTO),
            cidade=rng.choice(CIDADES),
            ano=rng.randint(ano_min, ano_max),
            n_dias=n_dias,
            n_atividades=n_ativ,
            casos=casos,
        ))
    return specs
