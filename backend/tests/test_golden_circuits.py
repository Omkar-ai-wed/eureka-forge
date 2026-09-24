"""
Golden-circuit tests — Phase 1 Foundation.

Tests H|0> and Bell-state circuits against Qiskit Aer.
Uses tolerance (±15%) rather than exact counts because shot-based
simulation is stochastic.
"""
import pytest
from app.schemas.models import CanonicalCircuit, Gate, GateType, PredictionInput
from app.services.simulator import run_simulation
from app.services.comparison import compare
from app.services.misconception import evaluate, triggered_only

TOLERANCE = 0.15  # 15 % tolerance for stochastic simulation


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def h_circuit():
    return CanonicalCircuit(
        qubits=1,
        gates=[Gate(gate=GateType.H, target=0)],
        label="H|0>",
        concept="superposition",
    )


@pytest.fixture
def bell_circuit():
    return CanonicalCircuit(
        qubits=2,
        gates=[
            Gate(gate=GateType.H, target=0),
            Gate(gate=GateType.CX, target=1, control=0),
        ],
        label="Bell State",
        concept="entanglement",
    )


# ── Simulator golden tests ────────────────────────────────────────────────────

def test_h_circuit_returns_result(h_circuit):
    result = run_simulation(h_circuit, shots=1024)
    assert result.error is None, f"Simulation error: {result.error}"
    assert result.shots == 1024
    assert result.circuit == h_circuit
    assert result.backend == "qiskit-aer"


def test_h_circuit_probabilities_near_fifty_fifty(h_circuit):
    """H|0> should produce ~50% |0> and ~50% |1>."""
    result = run_simulation(h_circuit, shots=4096)
    assert result.error is None
    p0 = result.probabilities.get("0", 0.0)
    p1 = result.probabilities.get("1", 0.0)
    assert abs(p0 - 0.5) <= TOLERANCE, f"|0> probability {p0:.3f} outside tolerance"
    assert abs(p1 - 0.5) <= TOLERANCE, f"|1> probability {p1:.3f} outside tolerance"
    assert abs(p0 + p1 - 1.0) < 0.001, "Probabilities do not sum to 1"


def test_h_circuit_trace_generated(h_circuit):
    """Trace must be non-empty and start from the initial state."""
    result = run_simulation(h_circuit, shots=1024)
    assert len(result.trace) >= 2
    assert "0" in result.trace[0].state_label  # initial |0>
    assert any("H gate" in step.event for step in result.trace)


def test_bell_circuit_probabilities(bell_circuit):
    """Bell state: ~50% |00>, ~50% |11>, ~0% |01>, ~0% |10>."""
    result = run_simulation(bell_circuit, shots=4096)
    assert result.error is None
    p00 = result.probabilities.get("00", 0.0)
    p11 = result.probabilities.get("11", 0.0)
    p01 = result.probabilities.get("01", 0.0)
    p10 = result.probabilities.get("10", 0.0)
    assert abs(p00 - 0.5) <= TOLERANCE, f"P(00)={p00:.3f} outside tolerance"
    assert abs(p11 - 0.5) <= TOLERANCE, f"P(11)={p11:.3f} outside tolerance"
    assert p01 <= TOLERANCE, f"P(01)={p01:.3f} should be ~0"
    assert p10 <= TOLERANCE, f"P(10)={p10:.3f} should be ~0"


def test_bell_circuit_no_error(bell_circuit):
    result = run_simulation(bell_circuit, shots=1024)
    assert result.error is None


def test_simulation_result_schema_version(h_circuit):
    result = run_simulation(h_circuit, shots=100)
    assert result.schema_version == "1.0"


# ── Comparison tests ──────────────────────────────────────────────────────────

def test_correct_prediction_matches(h_circuit):
    simulation = run_simulation(h_circuit, shots=2048)
    prediction = PredictionInput(
        circuit=h_circuit,
        probabilities={"0": 0.5, "1": 0.5},
        concept="superposition",
    )
    result = compare(prediction, simulation, tolerance=TOLERANCE)
    assert result.overall_match is True
    assert result.accuracy_score > 0.8


def test_wrong_prediction_mismatches(h_circuit):
    simulation = run_simulation(h_circuit, shots=2048)
    prediction = PredictionInput(
        circuit=h_circuit,
        probabilities={"0": 1.0, "1": 0.0},   # deterministic — wrong
        concept="superposition",
    )
    result = compare(prediction, simulation)
    assert result.overall_match is False
    assert result.accuracy_score < 0.6


def test_comparison_summary_contains_match_word(h_circuit):
    simulation = run_simulation(h_circuit, shots=1024)
    prediction = PredictionInput(
        circuit=h_circuit, probabilities={"0": 0.5, "1": 0.5}
    )
    result = compare(prediction, simulation, tolerance=TOLERANCE)
    assert "MATCH" in result.summary or "MISMATCH" in result.summary


# ── Misconception engine tests ────────────────────────────────────────────────

def test_m1_fires_on_deterministic_prediction(h_circuit):
    simulation = run_simulation(h_circuit, shots=2048)
    prediction = PredictionInput(
        circuit=h_circuit,
        probabilities={"0": 1.0, "1": 0.0},
        concept="superposition",
    )
    comparison_result = compare(prediction, simulation)
    results = evaluate(comparison_result)
    m1 = next(r for r in results if r.rule.value == "M1")
    assert m1.triggered is True, "M1 should fire for deterministic prediction on H|0>"


def test_m1_does_not_fire_on_correct_prediction(h_circuit):
    simulation = run_simulation(h_circuit, shots=2048)
    prediction = PredictionInput(
        circuit=h_circuit,
        probabilities={"0": 0.5, "1": 0.5},
        concept="superposition",
    )
    comparison_result = compare(prediction, simulation, tolerance=TOLERANCE)
    results = evaluate(comparison_result)
    m1 = next(r for r in results if r.rule.value == "M1")
    assert m1.triggered is False, "M1 should not fire when prediction is correct"


def test_m2_fires_on_measurement_passivity_notes(h_circuit):
    simulation = run_simulation(h_circuit, shots=1024)
    prediction = PredictionInput(
        circuit=h_circuit,
        probabilities={"0": 0.5, "1": 0.5},
        notes="The qubit stays the same state after measurement",
    )
    comparison_result = compare(prediction, simulation)
    results = evaluate(comparison_result)
    m2 = next(r for r in results if r.rule.value == "M2")
    assert m2.triggered is True


def test_misconception_results_have_explanations(h_circuit):
    simulation = run_simulation(h_circuit, shots=1024)
    prediction = PredictionInput(
        circuit=h_circuit,
        probabilities={"0": 1.0, "1": 0.0},
        concept="superposition",
    )
    comparison_result = compare(prediction, simulation)
    results = triggered_only(comparison_result)
    for r in results:
        assert r.learner_explanation, f"Rule {r.rule} has no explanation"
        assert r.remediation_concept, f"Rule {r.rule} has no remediation concept"


# ── Schema validation tests ───────────────────────────────────────────────────

def test_cx_gate_requires_control():
    import pytest
    with pytest.raises(Exception):
        Gate(gate=GateType.CX, target=1)  # missing control


def test_prediction_probabilities_must_sum_to_one():
    with pytest.raises(Exception):
        PredictionInput(
            circuit=CanonicalCircuit(qubits=1, gates=[]),
            probabilities={"0": 0.3, "1": 0.3},  # sums to 0.6
        )