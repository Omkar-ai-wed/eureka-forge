'''
Tests for full learning loop: AI Tutor, Manim selector, Challenges, and Mastery.
Principle: Simulator computes. Everything else reads.
'''
import pytest
from app.schemas.models import (
    CanonicalCircuit, Gate, GateType, PredictionInput, ExecutionContext,
    TutorRequest, TutorMode, MisconceptionRule, ChallengeSubmission
)
from app.services.simulator import run_simulation
from app.services.comparison import compare
from app.services.misconception import evaluate
from app.services.tutor import ask_tutor
from app.services.manim import select_clip_for_context, list_clips
from app.services.challenges import list_challenges, grade_challenge, get_mastery_profile

@pytest.fixture
def h_circuit():
    return CanonicalCircuit(
        qubits=1,
        gates=[Gate(gate=GateType.H, target=0)],
        label='H|0>',
        concept='superposition',
    )

@pytest.fixture
def bell_circuit():
    return CanonicalCircuit(
        qubits=2,
        gates=[
            Gate(gate=GateType.H, target=0),
            Gate(gate=GateType.CX, target=1, control=0),
        ],
        label='Bell State',
        concept='entanglement',
    )

def test_tutor_grounded_response_superposition(h_circuit):
    sim = run_simulation(h_circuit, shots=1024)
    pred = PredictionInput(circuit=h_circuit, probabilities={'0': 0.5, '1': 0.5}, concept='superposition')
    cmp = compare(pred, sim)
    ctx = ExecutionContext(circuit=h_circuit, simulation=sim, prediction=pred, comparison=cmp)

    req = TutorRequest(mode=TutorMode.EXPLAIN, context=ctx)
    res = ask_tutor(req)
    assert res.response is not None
    assert 'Superposition' in res.response
    assert res.grounded_evidence['match'] is True

def test_tutor_debug_mode_mismatch(h_circuit):
    sim = run_simulation(h_circuit, shots=1024)
    pred = PredictionInput(circuit=h_circuit, probabilities={'0': 1.0, '1': 0.0}, concept='superposition')
    cmp = compare(pred, sim)
    misc = evaluate(cmp)
    ctx = ExecutionContext(circuit=h_circuit, simulation=sim, prediction=pred, comparison=cmp, misconceptions=misc)

    req = TutorRequest(mode=TutorMode.DEBUG, context=ctx)
    res = ask_tutor(req)
    assert 'Mismatch detected' in res.response
    assert res.grounded_evidence['match'] is False

def test_manim_selector():
    clips = list_clips()
    assert len(clips) >= 3
    clip = select_clip_for_context(concept='superposition', rule=MisconceptionRule.M1)
    assert clip.clip_id == 'clip_superposition'
    assert 'Bloch' in clip.description or 'equatorial' in clip.title.lower()

def test_challenges_and_deterministic_grading(bell_circuit):
    challenges = list_challenges()
    assert len(challenges) >= 3

    # Challenge 1: Superposition prediction
    sub1 = ChallengeSubmission(challenge_id='challenge-superposition', prediction={'0': 0.5, '1': 0.5})
    res1 = grade_challenge(sub1)
    assert res1.passed is True
    assert res1.score >= 0.95

    # Challenge 2: Bell state construction
    sub2 = ChallengeSubmission(challenge_id='challenge-bell', circuit=bell_circuit)
    res2 = grade_challenge(sub2)
    assert res2.passed is True
    assert res2.score == 1.0

    # Challenge 3: Diagnosis
    sub3 = ChallengeSubmission(challenge_id='challenge-diagnosis', selected_option_index=0)
    res3 = grade_challenge(sub3)
    assert res3.passed is True
    assert res3.score == 1.0

def test_mastery_profile():
    prof = get_mastery_profile()
    assert prof.overall_progress > 0.0
    assert 'superposition' in prof.concepts
    assert 'entanglement' in prof.concepts
