# SIH 2026 --- SIH26140

# PROTOTYPE MASTER SPEC + ANTIGRAVITY BUILD PROMPTS

## Eureka Forge --- Quantum Intelligence Learning Lab (working expansion)

> **Purpose:** Single source of truth for building the Level-3 SIH
> prototype. This file can be handed to Antigravity section-by-section.

# 0. PRODUCT CONTRACT

**Working expansion:** Quantum Intelligence Learning Lab

**Acronym/product name:** TBD after uniqueness check. Do not hard-code
"QuILL" as the final public brand until the team approves it.

**Promise:** \> **Students predict. The simulator proves. AI explains
why.**

**Core loop:** \> **Predict → Build → Simulate → Compare → Diagnose →
Explain → Show Me Why → Challenge → Mastery**

**Primary user:** Undergraduate / early-postgraduate learners learning
introductory gate-model quantum computing.

**Secondary user:** Instructors / educators.

**MVP curriculum:** 1. Qubit 2. Superposition 3. H gate 4. Measurement
5. CNOT 6. Entanglement 7. Bell state

**Prototype level:** Level 3 --- complete learning loop.

# 1. NON-NEGOTIABLE ARCHITECTURE

## Principle

> **Simulator computes. Everything else reads.**

``` text
Learner Action
     ↓
Canonical Circuit Representation
     ↓
Qiskit Aer
     ↓
Structured Execution Trace
     ↓
 ┌─────────────┬─────────────┬──────────────┬─────────────┐
 ↓             ↓             ↓              ↓
Visualizer   Assessment    AI Tutor       Manim Selector
 ↓             ↓             ↓              ↓
 UI         Mastery      Explanation    Show Me Why
```

The simulator is the source of quantum-result truth.

Do **not** let the LLM independently calculate the circuit result and
present that as ground truth.

The LLM should receive structured context such as:

``` json
{
  "circuit": {
    "qubits": 2,
    "gates": [
      {"gate": "H", "target": 0},
      {"gate": "CX", "control": 0, "target": 1}
    ]
  },
  "prediction": {
    "probabilities": {
      "00": 0.5,
      "11": 0.5
    }
  },
  "simulation": {
    "probabilities": {
      "00": 0.5,
      "11": 0.5
    },
    "shots": 1024
  },
  "trace": [
    {"step": 0, "state": "|00>"},
    {"step": 1, "event": "H on q0"},
    {"step": 2, "event": "CX q0→q1"}
  ],
  "assessment": {
    "prediction_correct": true,
    "misconception": null
  }
}
```

The exact schema may evolve, but the contract must remain.

# 2. TECH STACK

## MVP

**Frontend:** React / Next.js, TypeScript, Tailwind CSS, SVG/Canvas,
Three.js only where useful.

**Backend:** Python, FastAPI, Qiskit Aer.

**AI:** Ollama local-first + Gemini fallback, behind one provider
interface.

**Animation:** Manim Community Edition, pre-rendered MVP clips.

**Data:** SQLite MVP; PostgreSQL later.

## Backend strategy

MVP = Qiskit Aer actual simulator.

Architecture = canonical circuit representation / execution event schema
for future adapters.

Future = PennyLane, Cirq, qBraid/other environments, real QPU execution.

Do not claim future adapters are implemented unless they are.

# 3. REQUIRED SCREENS

## Screen 1 --- Dashboard

Show: - current learning path - progress - concept cards - Continue
Learning - mastery indicators

Cards: - Qubit - Superposition - Measurement - Entanglement

Primary CTA: \> Continue Lesson

## Screen 2 --- Lesson

Structure:

``` text
Concept
  ↓
Visual intuition
  ↓
Mini explanation
  ↓
Predict
  ↓
Experiment
  ↓
Challenge
```

MVP lesson = Superposition.

Show: - short explanation - simple state representation - H gate
visual - Predict the Result CTA

Avoid huge paragraphs.

## Screen 3 --- Prediction

Before simulation:

> **What do you think will happen?**

For H\|0\>: - \|0\> probability - \|1\> probability

Then: \> **Lock Prediction**

Only after prediction: \> **Run Simulation**

Store: - prediction - timestamp - circuit version - concept - actual
result later

## Screen 4 --- Circuit Lab

Required: - qubit rows - gate palette - H - X - Z - CNOT/CX -
Measurement - Clear - Run - Step Through

Optional: - code view - Qiskit code export

MVP circuits:

``` text
|0> — H — Measure
```

``` text
|00> — H — CX — Measure
```

## Screen 5 --- Simulation Result

Show: - probability histogram - shots - circuit summary -
state/probability view - Compare with Prediction

Bell ideal conceptual result:

``` text
|00> ≈ 50%
|11> ≈ 50%
|01> ≈ 0%
|10> ≈ 0%
```

Do not hard-code fake production output. Derive visuals from simulator
results.

## Screen 6 --- Compare

Correct:

``` text
YOUR PREDICTION          SIMULATOR RESULT
     50/50                    50/50
        ✓ MATCH
```

Mismatch:

``` text
YOUR PREDICTION          SIMULATOR RESULT
     80/20                    50/50
        ✕ MISMATCH
```

Then: \> **What did you misunderstand?**

## Screen 7 --- Step-by-Step Trace

``` text
Step 0     |00>
   ↓
Step 1     H on q0
   ↓
Step 2     CNOT q0 → q1
   ↓
Final      Bell state
```

Trace should be generated from the execution pipeline, not duplicated as
hand-written UI facts.

## Screen 8 --- AI Tutor

Modes: - Explain - Hint - Debug

Tutor receives: - learner question - circuit - simulator result -
execution trace - prediction - comparison - misconception rule - curated
lesson context

Tutor must: - explain supplied evidence - avoid inventing results -
never override grading - say when evidence is unavailable - keep
explanations beginner-friendly

## Screen 9 --- Misconception Engine

Use a small deterministic rule engine.

### M1 --- Superposition as hidden classical value

Trigger: learner repeatedly predicts a definite hidden value for H\|0\>.

### M2 --- Measurement does not change state

Trigger: learner expects post-measurement state to remain identical to
pre-measurement state.

### M3 --- Entanglement as communication

Trigger: learner describes CNOT/entanglement as faster-than-light
information transfer.

### M4 --- Phase = probability

Trigger: learner treats phase as identical to probability.

These are MVP teaching heuristics, not a claim of an exhaustive
scientific taxonomy.

## Screen 10 --- "Show Me Why" Manim

Manim is a supporting educational layer, not the novelty claim.

### Clip 1

**H gate → superposition** - \|0\> vector - H transformation -
Bloch-sphere movement - measurement probability

### Clip 2

**Measurement → observed outcome/state change** - pre-measurement
state - measurement event - outcome - post-measurement state

### Clip 3

**H + CNOT → Bell-state correlation** - H - CNOT - correlated outcomes -
no faster-than-light signalling claim

UX: \> **Want to see why?** \> \> ▶ Show Me Why

Use pre-rendered clips.

## Screen 11 --- Challenge

Three graded challenges: 1. Predict H\|0\> measurement distribution. 2.
Identify/build the Bell-state circuit. 3. Diagnose why a prediction is
inconsistent with a circuit.

Numerical grading is deterministic; LLM does not assign the score.

## Screen 12 --- Mastery

Show concept progress:

``` text
QUANTUM FOUNDATIONS

Qubit            ████████░░ 80%
Superposition    ██████████ 100%
Measurement      ██████░░░░ 60%
Entanglement     ████░░░░░░ 40%
```

States: - Learning - Practicing - Mastered

Next challenge should use deterministic mastery + misconception signals.

# 4. ANTIGRAVITY PROMPT PACK

## Prompt 01 --- Repository audit

``` text
You are the lead engineer for the Eureka Forge SIH26140 prototype.

Problem:
SIH26140 — AI-Based Interactive Quantum Algorithm Learning Platform.

Learning loop:
Predict → Build → Simulate → Compare → Diagnose → Explain → Show Me Why → Challenge → Mastery

Core principle:
“Simulator computes. Everything else reads.”

First inspect the entire repository before changing anything.

Report:
1. frontend architecture
2. backend architecture
3. simulator integration
4. current circuit representation
5. execution/result schema
6. visualization
7. AI/LLM integration
8. Manim assets
9. tests
10. broken/incomplete features

DO NOT rewrite the project yet.
DO NOT invent missing functionality.
DO NOT replace working code for style reasons.

End with:
- current architecture
- working features
- missing features
- highest-risk issues
- recommended implementation order
```

## Prompt 02 --- Canonical execution architecture

``` text
Implement/refactor toward:

Learner circuit
→ canonical circuit representation
→ Qiskit Aer
→ structured execution trace
→ visualizer / assessment / AI tutor / Manim selector / mastery

Requirements:
1. Aer is the MVP source of quantum-result truth.
2. Circuit representation is deterministic and serializable.
3. Execution result includes probabilities/counts, metadata, final result, and per-step information where implemented.
4. Create a stable internal execution-result schema.
5. Never let the LLM invent quantum results.
6. Add golden tests for H|0> and Bell-state circuits.
7. Keep future PennyLane/Cirq adapters possible.
8. Do not claim future adapters are implemented.

Inspect first. Make the smallest safe change. Run all tests. Report files changed and test results.
```

## Prompt 03 --- Prediction-before-run

``` text
Implement:

Predict → Run → Compare → Diagnose

Flow:
1. user opens lesson/circuit
2. user submits prediction
3. store prediction + circuit version + concept
4. run Qiskit Aer
5. compare prediction vs simulator output
6. create deterministic comparison object
7. display prediction, result, match/mismatch and difference
8. send structured evidence to misconception engine

Do not use the LLM to determine numerical correctness.

Support H|0> and Bell-state circuit first.

Test correct prediction, incorrect prediction, malformed prediction, repeated prediction, and circuit modification after prediction.
```

## Prompt 04 --- Misconception engine

``` text
Implement a deterministic MVP misconception engine.

Rules:
M1 superposition treated as hidden classical value
M2 measurement expected not to alter observed state
M3 entanglement interpreted as faster-than-light communication
M4 phase treated as identical to probability

Each rule should expose:
- id
- trigger
- evidence
- strength/confidence
- learner explanation
- remediation concept
- suggested challenge
- optional Manim clip id

Do not use an LLM to decide whether the rule fired.
Add unit tests.
Do not claim the taxonomy is exhaustive.
```

## Prompt 05 --- Grounded AI tutor

``` text
Implement the AI tutor as a grounded explanation layer.

Pass:
- learner question
- canonical circuit
- simulator result
- prediction
- comparison
- execution trace
- misconception result
- curated lesson context

Contract:
1. Never invent a simulator result.
2. Never override deterministic grading.
3. If evidence is missing, say so.
4. Explain using supplied execution evidence.
5. Hint mode must not reveal the answer.
6. Debug mode must identify the supplied mismatch.
7. Separate simulator facts from conceptual explanation.

Use Ollama locally when configured and Gemini as fallback.
Keep both behind one provider interface.
Mock the LLM in tests.
```

## Prompt 06 --- Manim "Show Me Why"

``` text
Implement three pre-rendered Manim explanation clips:

1. H → superposition
2. measurement → observed outcome/state change
3. H + CNOT → Bell-state correlation

Create metadata:
clip_id
concept
misconception_ids
title
description

Add deterministic frontend selection from concept/misconception context.

No live Manim generation is required.
Provide a static fallback explanation if the video cannot load.
```

## Prompt 07 --- Circuit lab

``` text
Build/refine the learning-focused circuit lab.

Required:
H, X, Z, CNOT/CX, Measurement
Add, remove, clear, run, step through, reset.

Required circuits:
A) H|0>
B) Bell state H + CNOT

The UI must feed the same canonical circuit representation used by the simulator.

Do not maintain a separate frontend-only circuit model.

Optional Qiskit code view.
Do not overbuild a full professional quantum IDE.
```

## Prompt 08 --- Visualization

``` text
Implement visualization from simulator output.

Required:
1. probability histogram
2. single-qubit Bloch visualization where applicable
3. circuit diagram
4. execution timeline
5. prediction vs actual comparison

No hard-coded fake production simulation output.
Handle empty/invalid results.
Keep visuals beginner-friendly.
```

## Prompt 09 --- Challenge + mastery

``` text
Implement deterministic assessment and mastery.

Challenges:
1. H|0> prediction
2. Bell-state construction/prediction
3. circuit misconception diagnosis

Track:
- attempts
- prediction accuracy
- challenge accuracy
- misconception occurrences
- concept mastery

States:
Learning / Practicing / Mastered

Do not let the LLM assign numerical scores or mastery.
```

## Prompt 10 --- Complete learner journey

``` text
Connect:

Dashboard
→ Lesson
→ Predict
→ Circuit Lab
→ Run
→ Compare
→ Step Through
→ AI Tutor
→ Show Me Why
→ Challenge
→ Mastery

No dead ends.
Clear CTA at every stage.
No placeholder lorem ipsum.
Consistent terminology and notation.
Do not add unrelated features until this journey is stable.
```

## Prompt 11 --- UI polish

``` text
Polish the SIH demo UI.

Visual direction:
Dark quantum lab + clean educational dashboard.

Professional, futuristic but restrained, accessible, responsive.

Use:
- strong hierarchy
- readable typography
- restrained glow
- clear cards
- consistent gates
- clear prediction/result states

Avoid:
- excessive neon
- excessive animation
- crowded dashboards
- generic chatbot look
- gaming-heavy UI

It should look like a serious learning platform.
```

## Prompt 12 --- Reliability audit

``` text
Audit the exact demo journey:

Dashboard
→ Superposition lesson
→ H prediction
→ simulation
→ comparison
→ AI explanation
→ Show Me Why
→ Bell circuit
→ challenge
→ mastery

Check:
- simulator correctness
- prediction persistence
- comparison correctness
- AI context
- misconception rules
- Manim loading
- routes
- error/loading/empty states
- responsive UI

Run all tests.

Fix root causes only.
Add regression tests where appropriate.
Finish with a PASS/FAIL table.
```

# 5. IMPLEMENTATION ORDER

### Phase 1 --- Foundation

1.  Audit
2.  Canonical circuit model
3.  Qiskit Aer
4.  Execution-result schema
5.  Golden-circuit tests

### Phase 2 --- Core learning loop

6.  Prediction
7.  Simulation
8.  Comparison
9.  Step trace
10. Visualizations

### Phase 3 --- Intelligence

11. Misconception engine
12. Grounded AI tutor
13. Mastery engine

### Phase 4 --- Experience

14. Manim clips
15. Dashboard
16. Lesson
17. Challenge flow

### Phase 5 --- SIH polish

18. UI polish
19. Reliability audit
20. Demo rehearsal

# 6. TEST CIRCUITS

## H\|0\>

Conceptual ideal result:

``` text
|0> ≈ 50%
|1> ≈ 50%
```

Because shot-based simulation is stochastic, use tolerance rather than
demanding exactly 50/50 counts on every run.

## Bell state

``` text
q0: ──H────■────M
           │
q1: ───────X────M
```

Conceptual ideal probabilities:

``` text
P(00) ≈ 50%
P(11) ≈ 50%
P(01) ≈ 0%
P(10) ≈ 0%
```

Use tolerance for finite-shot simulation.

# 7. DEMO SCRIPT

1.  Dashboard --- "Quantum concepts are easy to describe but difficult
    to see."
2.  Superposition lesson --- "The student does not immediately get the
    answer."
3.  Prediction --- "First, they predict."
4.  H circuit --- "The simulator computes the actual result."
5.  Comparison --- "The platform compares prediction with simulator
    ground truth."
6.  AI --- "The tutor explains the mismatch using circuit and execution
    evidence."
7.  Manim --- "Show Me Why provides a visual explanation."
8.  Bell state --- "The learner applies the concept to entanglement."
9.  Challenge --- "The next challenge is selected from actual
    performance."
10. Mastery --- "Learning becomes measurable, iterative and adaptive."

Close: \> **"Students predict. The simulator proves. AI explains why."**

# 8. DO NOT BUILD FOR MVP

Do not spend SIH time on: - Shor - QFT - QAOA - full curriculum - real
QPU integration - four fully working backends - instructor dashboard -
classroom collaboration - advanced gamification - dynamic AI-generated
Manim - 20+ qubit simulation - social features - unnecessary 3D worlds

# 9. PROTOTYPE ACCEPTANCE CRITERIA

-   [ ] Lesson starts
-   [ ] Prediction can be submitted
-   [ ] Prediction is stored
-   [ ] H\|0\> can run through Aer
-   [ ] Actual output is visualized
-   [ ] Prediction is compared deterministically
-   [ ] Step-through works
-   [ ] A mismatch can trigger a misconception rule
-   [ ] AI receives structured simulator evidence
-   [ ] AI explanation appears
-   [ ] Show Me Why opens the correct clip
-   [ ] Challenge can be completed
-   [ ] Mastery changes from actual performance
-   [ ] Bell-state journey works
-   [ ] No critical route errors
-   [ ] Tests pass
-   [ ] Demo works in local-first configuration

# 10. EVIDENCE / HONESTY CONTRACT

Distinguish:

### Built

Feature works in the submitted prototype.

### Architected

Data model/interface supports it, but it is not demonstrated.

### Future

Not implemented.

Never convert: - architecture → implementation - intention → result -
simulation → hardware execution - AI explanation → verified physics
reasoning - planned research → completed research

# 11. FUTURE ROADMAP

## Phase 2

-   PennyLane adapter
-   Cirq adapter
-   additional algorithms
-   noise-aware learning
-   code exercises
-   larger lesson library

## Phase 3

-   real QPU execution
-   hardware-aware visualization
-   instructor dashboards
-   classroom analytics
-   collaborative learning
-   richer adaptive curriculum

## Research directions

Evaluate, rather than assume, whether: - prediction-before-run improves
conceptual understanding - misconception-targeted remediation improves
later prediction accuracy - simulator-grounded tutoring reduces
unsupported explanations - visual "Show Me Why" improves retention

Do not claim these outcomes until measured.

# 12. MASTER ANTIGRAVITY PROMPT

``` text
You are the lead engineer building the Eureka Forge prototype for SIH26140.

PRODUCT:
Quantum Intelligence Learning Lab
(working expansion; final acronym may change)

PROBLEM:
AI-Based Interactive Quantum Algorithm Learning Platform.

PRIMARY USERS:
Undergraduate/early-postgraduate quantum-computing learners.

MVP:
Qubit → Superposition → H → Measurement → CNOT → Entanglement → Bell State.

CORE LOOP:
Predict → Build → Simulate → Compare → Diagnose → Explain → Show Me Why → Challenge → Mastery

CORE PRINCIPLE:
“Simulator computes. Everything else reads.”

TECH:
Frontend: React/Next.js + TypeScript + Tailwind
Backend: Python + FastAPI
Simulation: Qiskit Aer
AI: Ollama local-first + Gemini fallback
Animation: Manim CE
Storage: SQLite MVP
Future adapters: PennyLane/Cirq/qBraid

NON-NEGOTIABLE:
1. Never allow the LLM to invent quantum results.
2. Simulator output is the source of quantum-result truth.
3. Prediction comparison is deterministic.
4. Misconception detection is deterministic/rule-based in MVP.
5. LLM receives structured simulator context.
6. Numerical grading is never delegated to the LLM.
7. Manim is a supporting “Show Me Why” remediation layer.
8. Keep MVP small and polished.
9. Do not break existing working features.
10. Do not fabricate data, benchmarks, user numbers or research results.

IMPLEMENTATION ORDER:
Audit → canonical circuit model → Aer → execution trace → prediction → comparison → visualization → misconception rules → grounded AI → Manim → challenges → mastery → UI polish → reliability audit.

Before every major implementation step:
- inspect current code
- identify reusable components
- make the smallest safe change
- run tests
- report changed files
- report test status

The final demo must support:
Dashboard → Lesson → Predict → Build → Simulate → Compare → Step Through → AI Tutor → Show Me Why → Challenge → Mastery.

Do not add unrelated features until this journey is stable.
```

# 13. FINAL PROTOTYPE QUESTION

Before showing the PPT team anything, verify:

> **Can we actually demonstrate the exact story shown on the slides?**

If the PPT says prediction, demonstrate prediction. If it says
simulator-grounded AI, demonstrate the relationship between simulator
output and AI context. If it says misconception detection, trigger one.
If it says Manim remediation, open one. If it says mastery, show it
changing.

If a claim cannot be demonstrated, downgrade it to **architecture** or
**future scope**.
