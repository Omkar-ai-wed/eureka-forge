"""
Demo Rehearsal and Reliability Audit Test Suite (Phase 5, Prompts 11 & 12).
Executes the exact 10-step demo rehearsal defined in Section 7 of the Master Spec.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_step_01_dashboard_and_health():
    """Step 1: Dashboard health check and service status."""
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["simulator_ready"] is True
    assert data["backend"] == "qiskit-aer"

def test_step_02_superposition_lesson_and_circuits():
    """Step 2: Superposition lesson - retrieve golden canonical circuits and trace."""
    res = client.get("/api/v1/circuits/golden")
    assert res.status_code == 200
    data = res.json()
    assert "h_circuit" in data
    assert "bell_circuit" in data
    assert data["h_circuit"]["qubits"] == 1
    assert data["bell_circuit"]["qubits"] == 2

    # Verify trace for superposition
    trace_res = client.get("/api/v1/trace?concept=superposition")
    assert trace_res.status_code == 200
    trace = trace_res.json()
    assert len(trace) >= 2
    assert "H gate" in trace[1]["event"]

def test_step_03_prediction_and_comparison_match():
    """Step 3 & 4 & 5: Predict, Simulate H|0>, and Compare deterministically."""
    # 1. Run simulation via Qiskit Aer
    sim_res = client.post("/api/v1/simulate", json={"concept": "superposition", "shots": 1024})
    assert sim_res.status_code == 200
    sim_data = sim_res.json()
    assert "0" in sim_data["probabilities"]
    assert "1" in sim_data["probabilities"]
    assert 0.35 <= sim_data["probabilities"]["0"] <= 0.65
    assert 0.35 <= sim_data["probabilities"]["1"] <= 0.65

    # 2. Compare with accurate prediction
    h_circuit = client.get("/api/v1/circuits/golden").json()["h_circuit"]
    pred_payload = {
        "prediction": {
            "circuit": h_circuit,
            "probabilities": {"0": 0.5, "1": 0.5},
            "concept": "superposition"
        },
        "simulation": sim_data
    }
    cmp_res = client.post("/api/v1/compare", json=pred_payload)
    assert cmp_res.status_code == 200
    cmp_data = cmp_res.json()
    assert cmp_data["overall_match"] is True
    assert cmp_data["accuracy_score"] >= 0.90

def test_step_05_misconception_m1_trigger():
    """Step 5: Compare with misconception prediction (M1: Hidden Classical Value -> 100% |0>)."""
    h_circuit = client.get("/api/v1/circuits/golden").json()["h_circuit"]
    sim_res = client.post("/api/v1/simulate", json={"concept": "superposition", "shots": 1024})
    sim_data = sim_res.json()

    pred_payload = {
        "prediction": {
            "circuit": h_circuit,
            "probabilities": {"0": 1.0, "1": 0.0},
            "concept": "superposition"
        },
        "simulation": sim_data
    }
    cmp_res = client.post("/api/v1/compare", json=pred_payload)
    cmp_data = cmp_res.json()
    assert cmp_data["overall_match"] is False

    # Diagnose trigger
    diag_res = client.post("/api/v1/diagnose", json={**pred_payload, "comparison": cmp_data})
    assert diag_res.status_code == 200
    triggers = diag_res.json()
    assert any(t["rule"] == "M1" for t in triggers)

def test_step_06_grounded_ai_tutor():
    """Step 6: AI Tutor explains the result using grounded simulator evidence."""
    tutor_res = client.post("/api/v1/tutor", json={
        "concept": "superposition",
        "user_question": "Why did my 100% |0> prediction not match the simulator?"
    })
    assert tutor_res.status_code == 200
    tutor_data = tutor_res.json()
    assert "explanation" in tutor_data or "response" in tutor_data
    assert "grounded_evidence" in tutor_data

def test_step_07_manim_show_me_why():
    """Step 7: Manim 'Show Me Why' selector retrieves the exact explanation clip."""
    clip_res = client.get("/api/v1/manim/select?concept=superposition&rule=M1")
    assert clip_res.status_code == 200
    clip = clip_res.json()
    assert clip["clip_id"] == "clip_superposition"
    assert len(clip["key_takeaways"]) >= 2
    assert len(clip["fallback_explanation"]) > 20

def test_step_08_bell_state_entanglement():
    """Step 8: Learner applies concept to Entanglement (Bell State H + CNOT)."""
    bell_circuit = client.get("/api/v1/circuits/golden").json()["bell_circuit"]
    sim_res = client.post("/api/v1/simulate", json={"circuit": bell_circuit, "shots": 1024})
    assert sim_res.status_code == 200
    sim_data = sim_res.json()

    # Bell state ideal: P(00) ≈ 0.5, P(11) ≈ 0.5, P(01) = 0, P(10) = 0
    p00 = sim_data["probabilities"].get("00", 0.0)
    p11 = sim_data["probabilities"].get("11", 0.0)
    p01 = sim_data["probabilities"].get("01", 0.0)
    p10 = sim_data["probabilities"].get("10", 0.0)

    assert 0.35 <= p00 <= 0.65
    assert 0.35 <= p11 <= 0.65
    assert p01 < 0.05
    assert p10 < 0.05

def test_step_09_adaptive_challenge():
    """Step 9: Challenge is selected and deterministically graded from performance."""
    challenges_res = client.get("/api/v1/challenges?concept=superposition")
    assert challenges_res.status_code == 200
    challenges = challenges_res.json()
    assert len(challenges) >= 1

    target_ch = challenges[0]
    sub_res = client.post("/api/v1/challenges/submit", json={
        "challenge_id": target_ch["id"],
        "selected_option_index": 0,
        "prediction": {"0": 0.5, "1": 0.5}
    })
    assert sub_res.status_code == 200
    sub_data = sub_res.json()
    assert "passed" in sub_data
    assert "score" in sub_data

def test_step_10_mastery_tracking():
    """Step 10: Mastery changes from actual performance and is measurable."""
    mastery_res = client.get("/api/v1/mastery")
    assert mastery_res.status_code == 200
    mastery = mastery_res.json()
    assert "overall_progress" in mastery
    assert "concepts" in mastery
    assert "superposition" in mastery["concepts"]
    assert "entanglement" in mastery["concepts"]
