"""
Deterministic MVP misconception engine.
Rules M1–M4 fire based on evidence, not LLM inference.
This taxonomy is intentionally limited to the MVP teaching heuristics.
"""
from __future__ import annotations
from ..schemas.models import (
    ComparisonResult, MisconceptionResult, MisconceptionRule,
)

# Canonical Manim clip IDs for each rule (populated in Phase 4)
_CLIP_MAP = {
    MisconceptionRule.M1: "clip_superposition",
    MisconceptionRule.M2: "clip_measurement",
    MisconceptionRule.M3: "clip_bell",
    MisconceptionRule.M4: None,
}


def _check_m1(comparison: ComparisonResult) -> MisconceptionResult:
    """
    M1 — Superposition treated as a hidden classical value.
    Trigger: learner predicts a strongly definite outcome for H|0⟩
    (e.g. ≥80 % for either |0⟩ or |1⟩) and the simulator shows ~50/50.
    """
    concept = comparison.prediction.concept or ""
    is_superposition = "superposition" in concept.lower() or any(
        len(o.outcome) == 1 for o in comparison.outcomes
    )
    if not is_superposition:
        return MisconceptionResult(
            rule=MisconceptionRule.M1, triggered=False, confidence=0.0,
            evidence="Concept is not superposition — M1 not applicable.",
            learner_explanation="", remediation_concept="",
        )

    max_pred = max(comparison.prediction.probabilities.values(), default=0.0)
    triggered = max_pred >= 0.80 and not comparison.overall_match
    confidence = round((max_pred - 0.50) * 2, 2) if triggered else 0.0
    return MisconceptionResult(
        rule=MisconceptionRule.M1,
        triggered=triggered,
        confidence=min(confidence, 1.0),
        evidence=(
            f"Learner predicted {max_pred:.0%} for a definite outcome; "
            f"simulator shows ~50/50."
        ) if triggered else "Prediction was not strongly deterministic.",
        learner_explanation=(
            "Superposition is not a hidden coin toss. The qubit is genuinely "
            "in both states simultaneously until measured."
        ),
        remediation_concept="superposition",
        suggested_challenge="Predict H|0⟩ five times to see the distribution.",
        manim_clip_id=_CLIP_MAP[MisconceptionRule.M1],
    )


def _check_m2(comparison: ComparisonResult) -> MisconceptionResult:
    """
    M2 — Measurement expected not to alter the observed state.
    Trigger: prediction includes both pre- and post-measurement values
    that are identical (learner notes suggest measurement is passive).
    This is a heuristic; requires explicit evidence in notes.
    """
    notes = (comparison.prediction.notes or "").lower()
    keywords = ["same state", "unchanged", "doesn't change", "still superposition"]
    triggered = any(kw in notes for kw in keywords)
    return MisconceptionResult(
        rule=MisconceptionRule.M2,
        triggered=triggered,
        confidence=0.9 if triggered else 0.0,
        evidence=f"Learner notes suggest measurement is passive: '{notes[:80]}'" if triggered
                 else "No measurement-passivity language detected.",
        learner_explanation=(
            "Measurement collapses the superposition. After measuring |+⟩ you "
            "get |0⟩ or |1⟩ — not both. The act of measuring changes the state."
        ),
        remediation_concept="measurement",
        manim_clip_id=_CLIP_MAP[MisconceptionRule.M2],
    )


def _check_m3(comparison: ComparisonResult) -> MisconceptionResult:
    """
    M3 — Entanglement interpreted as faster-than-light communication.
    Trigger: learner notes include FTL / teleportation / communication language
    in the context of a Bell-state circuit.
    """
    concept = (comparison.prediction.concept or "").lower()
    notes   = (comparison.prediction.notes or "").lower()
    is_bell = "bell" in concept or "entanglement" in concept
    ftl_kw  = ["communicate", "instantly", "faster than light", "ftl", "signal", "teleport"]
    triggered = is_bell and any(kw in notes for kw in ftl_kw)
    return MisconceptionResult(
        rule=MisconceptionRule.M3,
        triggered=triggered,
        confidence=0.9 if triggered else 0.0,
        evidence=f"FTL language detected in Bell-state context: '{notes[:80]}'" if triggered
                 else "No FTL communication language detected.",
        learner_explanation=(
            "Entanglement creates correlated measurement outcomes, but no "
            "information travels between particles. No FTL communication is possible."
        ),
        remediation_concept="entanglement",
        manim_clip_id=_CLIP_MAP[MisconceptionRule.M3],
    )


def _check_m4(comparison: ComparisonResult) -> MisconceptionResult:
    """
    M4 — Phase treated as identical to probability.
    Trigger: learner predicts non-50/50 outcomes for a Z-gate circuit
    (Z flips phase, not probability).
    """
    gates = comparison.prediction.circuit.gates
    has_z = any(g.gate.value == "Z" for g in gates)
    if not has_z:
        return MisconceptionResult(
            rule=MisconceptionRule.M4, triggered=False, confidence=0.0,
            evidence="No Z gate in circuit — M4 not applicable.",
            learner_explanation="", remediation_concept="",
        )
    # After Z on |+⟩ the probabilities are still 50/50 but phase is flipped
    max_pred = max(comparison.prediction.probabilities.values(), default=0.0)
    triggered = max_pred >= 0.70 and not comparison.overall_match
    return MisconceptionResult(
        rule=MisconceptionRule.M4,
        triggered=triggered,
        confidence=0.8 if triggered else 0.0,
        evidence="Learner predicted unequal probabilities after a Z gate." if triggered
                 else "Prediction consistent with Z gate behaviour.",
        learner_explanation=(
            "The Z gate flips the relative phase (|+⟩ → |−⟩) but does not "
            "change measurement probabilities. Phase ≠ probability."
        ),
        remediation_concept="phase",
    )


_RULE_CHECKERS = [_check_m1, _check_m2, _check_m3, _check_m4]


def evaluate(comparison: ComparisonResult) -> list[MisconceptionResult]:
    """Run all misconception rules deterministically. Returns list of results."""
    return [checker(comparison) for checker in _RULE_CHECKERS]


def triggered_only(comparison: ComparisonResult) -> list[MisconceptionResult]:
    """Return only fired misconception rules."""
    return [r for r in evaluate(comparison) if r.triggered]