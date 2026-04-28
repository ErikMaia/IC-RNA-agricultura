"""Metricas espaciais auxiliares para comparacao de modelos.

Este modulo implementa o calculo do Indice de Dependencia Espacial (IDE)
e do indicador complementar ISI, com funcoes de apoio para parametros
de variograma no formato comum do PyKrige.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Tuple


def ide_isi_from_variances(nugget: float, structured_variance: float) -> Dict[str, float | str]:
    """Calcula IDE/ISI a partir de C0 (nugget) e C1 (variancia estruturada).

    Definicoes usadas:
    - IDE (%) = 100 * C1 / (C0 + C1)
    - ISI (%) = 100 * C0 / (C0 + C1)

    Onde:
    - C0: efeito pepita (nugget)
    - C1: componente estrutural
    """

    if nugget < 0 or structured_variance < 0:
        raise ValueError("nugget e variancia estruturada devem ser >= 0.")

    total = nugget + structured_variance
    if total == 0:
        raise ValueError("C0 + C1 nao pode ser zero.")

    ide = 100.0 * structured_variance / total
    isi = 100.0 * nugget / total

    return {
        "ide": ide,
        "isi": isi,
        "classe_ide": classify_ide(ide),
        "classe_isi": classify_isi(isi),
    }


def classify_ide(ide: float) -> str:
    """Classificacao de dependencia espacial com base no IDE."""
    if ide >= 75.0:
        return "forte"
    if ide >= 25.0:
        return "moderada"
    return "fraca"


def classify_isi(isi: float) -> str:
    """Classificacao equivalente com base no ISI (inverso do IDE)."""
    if isi <= 25.0:
        return "forte"
    if isi <= 75.0:
        return "moderada"
    return "fraca"


def extract_nugget_structured_from_pykrige(params: Mapping[str, Any] | Sequence[float]) -> Tuple[float, float]:
    """Extrai C0 e C1 de parametros de variograma no formato PyKrige.

    Suporta:
    - dict com chaves `nugget` e `psill`
    - dict com chaves `nugget` e `sill`
    - sequencia [sill, range, nugget] (mais comum)
    - sequencia [psill, range, nugget] (fallback automatico)
    """

    if isinstance(params, Mapping):
        nugget = float(params.get("nugget", 0.0))
        if "psill" in params:
            structured = float(params["psill"])
            return nugget, structured
        if "sill" in params:
            sill_total = float(params["sill"])
            structured = sill_total - nugget
            if structured < 0:
                raise ValueError("`sill` menor que `nugget`; parametros invalidos.")
            return nugget, structured
        raise ValueError("Dict de variograma sem `psill` ou `sill`.")

    if not isinstance(params, Sequence) or len(params) < 3:
        raise ValueError("Esperado dict ou sequencia com pelo menos 3 elementos.")

    first = float(params[0])  # sill total ou psill
    nugget = float(params[2])

    structured = first - nugget
    if structured < 0:
        # Fallback: primeiro elemento ja era psill.
        structured = first

    if nugget < 0 or structured < 0:
        raise ValueError("Parametros invalidos: nugget/variancia estruturada negativos.")

    return nugget, structured


def ide_isi_from_pykrige(params: Mapping[str, Any] | Sequence[float]) -> Dict[str, float | str]:
    """Calcula IDE/ISI diretamente dos parametros de variograma do PyKrige."""

    nugget, structured = extract_nugget_structured_from_pykrige(params)
    result = ide_isi_from_variances(nugget=nugget, structured_variance=structured)
    result["nugget"] = nugget
    result["structured_variance"] = structured
    return result
