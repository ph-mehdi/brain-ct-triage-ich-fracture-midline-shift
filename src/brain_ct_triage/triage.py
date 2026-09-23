"""Series-level triage rule transcribed from Notebook 28.

This is an experimental decision rule, not a clinical implementation.
"""

from __future__ import annotations

import math


def _nonnegative_finite(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return max(0.0, result)


def triage_class(
    v_edh_ml: float,
    v_sdh_ml: float,
    v_iph_ml: float,
    v_sah_ml: float,
    v_ivh_ml: float,
    fracture_probability: float,
    mls_mm: float,
) -> int:
    """Return class 0, 1, or 2 from the fusion notebooks' feature values.

    Negative volumes and MLS values are clipped to zero, matching Notebook 28.
    Non-finite values are rejected to avoid silently assigning a class.
    """

    edh = _nonnegative_finite(v_edh_ml, "v_edh_ml")
    sdh = _nonnegative_finite(v_sdh_ml, "v_sdh_ml")
    iph = _nonnegative_finite(v_iph_ml, "v_iph_ml")
    sah = _nonnegative_finite(v_sah_ml, "v_sah_ml")
    ivh = _nonnegative_finite(v_ivh_ml, "v_ivh_ml")
    mls = _nonnegative_finite(mls_mm, "mls_mm")
    fracture = float(fracture_probability)
    if not math.isfinite(fracture):
        raise ValueError("fracture_probability must be finite")

    total = edh + sdh + iph + sah + ivh
    has_ich = total >= 0.1
    has_fracture = fracture >= 0.5

    if mls >= 5 and (has_ich or has_fracture):
        return 2
    if edh >= 30 or sdh >= 70 or iph >= 70 or total >= 60:
        return 2
    if has_ich and mls >= 3 and total >= 40:
        return 2
    if has_fracture and total >= 15:
        return 2
    if mls >= 5 or has_ich or 3 <= mls < 5 or has_fracture:
        return 1
    return 0
