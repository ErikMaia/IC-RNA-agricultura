"""Metricas espaciais auxiliares para comparacao de modelos.

Este modulo implementa o calculo do Indice de Dependencia Espacial (IDE)
e do indicador complementar ISI, com funcoes de apoio para parametros
de variograma no formato comum do PyKrige.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Tuple

import numpy as np


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
        "ise": isi,
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

    try:
        values = list(params)
    except TypeError as exc:
        raise ValueError("Esperado dict ou sequencia com pelo menos 3 elementos.") from exc

    if len(values) < 3:
        raise ValueError("Esperado dict ou sequencia com pelo menos 3 elementos.")

    first = float(values[0])  # sill total ou psill
    nugget = float(values[2])

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


def ide_isi_from_prediction_points(
    points: Any,
    variogram_model: str = "exponential",
    max_points: int = 1000,
    random_state: int = 42,
) -> Dict[str, float | str]:
    """Estima IDE/ISI a partir de pontos previstos em colunas x, y, z.

    A funcao ajusta um variograma com OrdinaryKriging sobre uma amostra dos
    pontos previstos e calcula o ISI da superficie gerada pelo modelo.
    """

    from pykrige.ok import OrdinaryKriging

    if max_points <= 0:
        raise ValueError("max_points deve ser maior que zero.")

    x = np.asarray(points["x"], dtype=float)
    y = np.asarray(points["y"], dtype=float)
    z = np.asarray(points["z"], dtype=float)
    valid_mask = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    x, y, z = x[valid_mask], y[valid_mask], z[valid_mask]

    if len(z) < 3:
        raise ValueError("Sao necessarios pelo menos 3 pontos validos para estimar o variograma.")

    if len(z) > max_points:
        rng = np.random.default_rng(random_state)
        sample_index = rng.choice(len(z), size=max_points, replace=False)
        x, y, z = x[sample_index], y[sample_index], z[sample_index]

    ok = OrdinaryKriging(
        x=x,
        y=y,
        z=z,
        variogram_model=variogram_model,
        enable_plotting=False,
        verbose=False,
    )
    result = ide_isi_from_pykrige(ok.variogram_model_parameters)
    result["variogram_model"] = variogram_model
    result["n_points_variogram"] = int(len(z))
    return result


def kriging_mae(
    points: Any,
    variogram_model: str = "exponential",
    variogram_parameters: Mapping[str, Any] | Sequence[float] | None = None,
    n_splits: int = 5,
    random_state: int = 42,
) -> float:
    """Calcula o MAE da krigagem por validacao cruzada em *n_splits* partes.

    A validacao e feita separando os pontos de teste antes de executar o
    ``OrdinaryKriging``. Assim, o erro nao e medido nos mesmos pontos usados
    para ajustar o interpolador (o que produziria MAE artificialmente zero).
    ``points`` deve conter as colunas/chaves ``x``, ``y`` e ``z``.
    """

    from pykrige.ok import OrdinaryKriging

    if n_splits < 2:
        raise ValueError("n_splits deve ser maior ou igual a 2.")

    x = np.asarray(points["x"], dtype=float)
    y = np.asarray(points["y"], dtype=float)
    z = np.asarray(points["z"], dtype=float)
    valid_mask = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    x, y, z = x[valid_mask], y[valid_mask], z[valid_mask]

    if len(z) < n_splits or len(z) < 3:
        raise ValueError("Sao necessarios pontos validos suficientes para a validacao cruzada.")

    indices = np.arange(len(z))
    np.random.default_rng(random_state).shuffle(indices)
    fold_indices = np.array_split(indices, n_splits)
    absolute_errors = []

    for test_index in fold_indices:
        train_index = np.setdiff1d(indices, test_index, assume_unique=True)
        kwargs = {
            "x": x[train_index],
            "y": y[train_index],
            "z": z[train_index],
            "variogram_model": variogram_model,
            "enable_plotting": False,
            "verbose": False,
        }
        if variogram_parameters is not None:
            kwargs["variogram_parameters"] = variogram_parameters

        ok = OrdinaryKriging(**kwargs)
        predictions, _ = ok.execute("points", x[test_index], y[test_index])
        absolute_errors.extend(np.abs(z[test_index] - np.asarray(predictions, dtype=float)))

    return float(np.mean(absolute_errors))
