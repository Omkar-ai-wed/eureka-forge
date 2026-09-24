"""
Deterministic prediction vs. simulation comparison engine.
Numerical correctness is NEVER delegated to the LLM.
"""
from __future__ import annotations
from ..schemas.models import (
    PredictionInput, SimulationResult,
    ComparisonResult, OutcomeComparison,
)

DEFAULT_TOLERANCE = 0.10  # ±10 % per outcome


def compare(
    prediction: PredictionInput,
    simulation: SimulationResult,
    tolerance: float = DEFAULT_TOLERANCE,
) -> ComparisonResult:
    """
    Compare predicted vs. simulated probability distributions.
    Returns a ComparisonResult with per-outcome breakdown and overall match flag.
    """
    # Union of all outcome keys
    all_keys = set(prediction.probabilities) | set(simulation.probabilities)
    outcomes: list[OutcomeComparison] = []
    mae_sum = 0.0

    for outcome in sorted(all_keys):
        pred_p = prediction.probabilities.get(outcome, 0.0)
        sim_p  = simulation.probabilities.get(outcome, 0.0)
        delta  = sim_p - pred_p
        match  = abs(delta) <= tolerance
        outcomes.append(OutcomeComparison(
            outcome=outcome,
            predicted=round(pred_p, 4),
            simulated=round(sim_p,  4),
            delta=round(delta, 4),
            match=match,
        ))
        mae_sum += abs(delta)

    n = len(all_keys) if all_keys else 1
    mae = mae_sum / n
    accuracy_score = round(max(0.0, 1.0 - mae), 4)
    overall_match = all(o.match for o in outcomes)

    if overall_match:
        summary = (
            f"✓ MATCH — Your prediction matched the simulator result "
            f"(accuracy {accuracy_score:.0%})."
        )
    else:
        mismatched = [o.outcome for o in outcomes if not o.match]
        summary = (
            f"✕ MISMATCH — Outcomes differ for: {', '.join(mismatched)}. "
            f"Accuracy {accuracy_score:.0%}."
        )

    return ComparisonResult(
        prediction=prediction,
        simulation=simulation,
        tolerance=tolerance,
        overall_match=overall_match,
        outcomes=outcomes,
        accuracy_score=accuracy_score,
        summary=summary,
    )