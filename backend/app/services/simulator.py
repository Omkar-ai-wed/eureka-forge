"""
Qiskit Aer simulator service.

Contract:
- This is the source of quantum-result truth.
- Never let the LLM compute or override these values.
- Future adapters (PennyLane, Cirq) are NOT implemented; only Aer MVP.
"""
from __future__ import annotations
import time
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from ..schemas.models import (
    CanonicalCircuit, Gate, GateType, SimulationResult, TraceStep,
)


def get_canonical_circuit(concept: str) -> CanonicalCircuit:
    """Helper to return golden canonical circuit for a concept."""
    concept_lower = (concept or "superposition").lower()
    if "entangle" in concept_lower or "bell" in concept_lower:
        return CanonicalCircuit(
            qubits=2,
            gates=[
                Gate(gate=GateType.H, target=0),
                Gate(gate=GateType.CX, target=1, control=0),
            ],
            label="Bell State",
            concept="entanglement",
        )
    elif "measure" in concept_lower:
        return CanonicalCircuit(
            qubits=1,
            gates=[
                Gate(gate=GateType.H, target=0),
                Gate(gate=GateType.M, target=0),
            ],
            label="H + Measurement",
            concept="measurement",
        )
    else:
        return CanonicalCircuit(
            qubits=1,
            gates=[Gate(gate=GateType.H, target=0)],
            label="H|0>",
            concept="superposition",
        )


def _build_qiskit_circuit(circuit: CanonicalCircuit) -> QuantumCircuit:
    """Convert CanonicalCircuit to a Qiskit QuantumCircuit."""
    qc = QuantumCircuit(circuit.qubits, circuit.qubits)
    for gate in circuit.gates:
        g = gate.gate
        t = gate.target
        c = gate.control
        if g == GateType.H:
            qc.h(t)
        elif g == GateType.X:
            qc.x(t)
        elif g == GateType.Y:
            qc.y(t)
        elif g == GateType.Z:
            qc.z(t)
        elif g == GateType.S:
            qc.s(t)
        elif g == GateType.T:
            qc.t(t)
        elif g == GateType.CX:
            qc.cx(c, t)
        elif g == GateType.M:
            qc.measure(t, t)
    # Auto-measure any unmeasured qubits
    measured = {gate.target for gate in circuit.gates if gate.gate == GateType.M}
    for q in range(circuit.qubits):
        if q not in measured:
            qc.measure(q, q)
    return qc


def _build_trace(circuit: CanonicalCircuit) -> list[TraceStep]:
    """
    Generate a human-readable execution trace from the circuit definition.
    The trace is derived from the circuit, not re-simulated.
    """
    steps: list[TraceStep] = [
        TraceStep(step=0, event=f"Initial state: |{'0' * circuit.qubits}⟩",
                  state_label=f"|{'0' * circuit.qubits}⟩")
    ]
    for i, gate in enumerate(circuit.gates, start=1):
        g = gate.gate
        t = gate.target
        c = gate.control
        if g == GateType.H:
            event = f"H gate on q{t} → superposition"
        elif g == GateType.X:
            event = f"X gate on q{t} → bit flip"
        elif g == GateType.Y:
            event = f"Y gate on q{t}"
        elif g == GateType.Z:
            event = f"Z gate on q{t} → phase flip"
        elif g == GateType.S:
            event = f"S gate on q{t} → π/2 phase"
        elif g == GateType.T:
            event = f"T gate on q{t} → π/4 phase"
        elif g == GateType.CX:
            event = f"CNOT: control q{c} → target q{t}"
        elif g == GateType.M:
            event = f"Measure q{t}"
        else:
            event = f"{g.value} on q{t}"
        steps.append(TraceStep(step=i, event=event, state_label=None))
    steps.append(TraceStep(step=len(steps), event="Measurement complete", state_label=None))
    return steps


def run_simulation(circuit: CanonicalCircuit, shots: int = 1024) -> SimulationResult:
    """
    Run circuit through Qiskit Aer and return a SimulationResult.

    Returns error field populated on failure; never raises to caller.
    """
    t0 = time.perf_counter()
    concept = circuit.concept or "superposition"
    gates_applied = [g.gate.value for g in circuit.gates]
    try:
        qc = _build_qiskit_circuit(circuit)
        backend = AerSimulator()
        job = backend.run(qc, shots=shots)
        result = job.result()
        raw_counts: dict[str, int] = result.get_counts()
        # Normalise bitstring order (Qiskit returns LSB first)
        counts = {k[::-1]: v for k, v in raw_counts.items()}
        total = sum(counts.values())
        probabilities = {k: v / total for k, v in counts.items()}
        elapsed_ms = (time.perf_counter() - t0) * 1000
        trace = _build_trace(circuit)
        
        # Build text diagram
        try:
            circuit_diagram = str(qc.draw(output="text"))
        except Exception:
            circuit_diagram = f"{circuit.label or 'Circuit'}: {gates_applied}"

        return SimulationResult(
            circuit=circuit,
            shots=shots,
            counts=counts,
            probabilities=probabilities,
            trace=trace,
            execution_time_ms=round(elapsed_ms, 2),
            num_qubits=circuit.qubits,
            num_shots=shots,
            circuit_diagram=circuit_diagram,
            gates_applied=gates_applied,
            concept=concept,
        )
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return SimulationResult(
            circuit=circuit,
            shots=shots,
            counts={},
            probabilities={},
            trace=[],
            execution_time_ms=round(elapsed_ms, 2),
            num_qubits=circuit.qubits,
            num_shots=shots,
            circuit_diagram="",
            gates_applied=gates_applied,
            concept=concept,
            error=str(exc),
        )
