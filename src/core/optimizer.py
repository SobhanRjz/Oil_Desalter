"""
Core optimization engine for the Desalter Optimization Suite.
"""

from __future__ import annotations

import numpy as np
from typing import Dict, List, Tuple, Optional


class DesalterOptimizer:
    """Multi-objective optimizer using lexicographic ordering."""

    @staticmethod
    def bsw_response(flow_bpd: float, T: float, V: float, ppm: float, wash_pct: float, design_flow: float = 30000.0) -> float:
        x = ppm
        bsw = 2.8 * np.exp(-0.035 * x) + 0.10 * np.sin(0.18 * x)
        bsw *= (1.0 - 0.0020 * (T - 115.0))
        bsw *= (1.0 - 0.012 * (V - 26.0) / 10.0)
        wash_eff = 1.0 - 0.06 * (np.tanh((wash_pct - 1.0)/1.5) + 0.6)
        bsw *= wash_eff
        flow_ratio = flow_bpd / max(design_flow, 1.0)
        bsw *= (1.0 + 0.35 * (flow_ratio - 1.0))
        return float(np.clip(bsw, 0.05, 5.0))

    @staticmethod
    def sample_parameter_space(n: int, ranges: Dict[str, Tuple[float, float]], rng=None) -> Dict[str, np.ndarray]:
        rng = np.random.default_rng(rng)
        return {k: rng.uniform(v[0], v[1], size=n) for k, v in ranges.items()}

    @classmethod
    def optimize_multiobjective(
        cls,
        n_samples: int,
        ranges: Dict[str, Tuple[float, float]],
        spec_bsw: float,
        priorities: List[str],
        design_flow: float = 30000.0,
        rng=None,
    ) -> Tuple[Dict[str, np.ndarray], List[str]]:
        pts = cls.sample_parameter_space(n_samples, ranges, rng=rng)
        flow = np.round(pts["flow_bpd"] / 100.0) * 100.0
        T = np.round(pts["T"] / 1.0) * 1.0
        V = np.round(pts["V"] / 1.0) * 1.0
        ppm = np.round(pts["ppm"] / 1.0) * 1.0
        wash = np.round(pts["wash_pct"] / 0.1) * 0.1

        bsw = np.array([
            cls.bsw_response(f, t, v, p, w, design_flow=design_flow)
            for f, t, v, p, w in zip(flow, T, V, ppm, wash)
        ])

        feasible = bsw <= spec_bsw

        arr = np.vstack([flow, T, V, ppm, wash, bsw, feasible]).T
        cols = ["flow_bpd", "T", "V", "ppm", "wash_pct", "BSW", "feasible"]
        df = {c: arr[:, i] for i, c in enumerate(cols)}
        return df, cols

    @staticmethod
    def select_optimal_lexicographic(df: Dict[str, np.ndarray], priorities: List[str]) -> Tuple[Optional[int], Optional[np.ndarray]]:
        mask = df["feasible"] > 0.5
        if not mask.any():
            return None, None
        import numpy as _np
        idx = _np.where(mask)[0]
        order = idx
        for key in priorities[::-1]:
            arr = df[key][order]
            if key == "flow_bpd":
                sort_idx = _np.argsort(-arr, kind="mergesort")
            else:
                sort_idx = _np.argsort(arr, kind="mergesort")
            order = order[sort_idx]
        return int(order[0]), mask


