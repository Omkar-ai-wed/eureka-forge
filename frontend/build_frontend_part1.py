from pathlib import Path

src = Path(r'C:\Users\Omkar Shedage\quantum-intelligence-lab\frontend\src')
types_dir = src / 'types'
types_dir.mkdir(parents=True, exist_ok=True)
lib_dir = src / 'lib'
lib_dir.mkdir(parents=True, exist_ok=True)
comp_dir = src / 'components'
comp_dir.mkdir(parents=True, exist_ok=True)

# 1. types/quantum.ts
quantum_ts = '''export type GateType = 'H' | 'X' | 'Y' | 'Z' | 'CX' | 'S' | 'T' | 'M';

export interface Gate {
  gate: GateType;
  target: number;
  control?: number | null;
  params?: number[];
}

export interface CanonicalCircuit {
  schema_version: string;
  qubits: number;
  gates: Gate[];
  label?: string | null;
  concept?: string | null;
}

export interface PredictionInput {
  circuit: CanonicalCircuit;
  probabilities: Record<string, number>;
  session_id?: string | null;
  concept?: string | null;
  notes?: string | null;
}

export interface TraceStep {
  step: number;
  event: string;
  state_label?: string | null;
  statevector?: number[][] | null;
}

export interface SimulationResult {
  schema_version: string;
  circuit: CanonicalCircuit;
  shots: number;
  counts: Record<string, number>;
  probabilities: Record<string, number>;
  final_statevector?: number[][] | null;
  trace: TraceStep[];
  backend: string;
  execution_time_ms?: number | null;
  error?: string | null;
}

export interface OutcomeComparison {
  outcome: string;
  predicted: number;
  simulated: number;
  delta: number;
  match: boolean;
}

export interface ComparisonResult {
  prediction: PredictionInput;
  simulation: SimulationResult;
  tolerance: number;
  overall_match: boolean;
  outcomes: OutcomeComparison[];
  accuracy_score: number;
  summary: string;
}

export type MisconceptionRule = 'M1' | 'M2' | 'M3' | 'M4';

export interface MisconceptionResult {
  rule: MisconceptionRule;
  triggered: boolean;
  confidence: number;
  evidence: string;
  learner_explanation: string;
  remediation_concept: string;
  suggested_challenge?: string | null;
  manim_clip_id?: string | null;
}

export interface ExecutionContext {
  schema_version: string;
  session_id?: string | null;
  concept?: string | null;
  circuit: CanonicalCircuit;
  prediction?: PredictionInput | null;
  simulation: SimulationResult;
  comparison?: ComparisonResult | null;
  misconceptions: MisconceptionResult[];
}

export type TutorMode = 'explain' | 'hint' | 'debug';

export interface TutorRequest {
  mode: TutorMode;
  learner_question?: string | null;
  context: ExecutionContext;
}

export interface TutorResponse {
  mode: TutorMode;
  response: string;
  grounded_evidence: Record<string, any>;
  provider: string;
  suggested_actions: string[];
}

export interface ManimClipMetadata {
  clip_id: string;
  title: string;
  concept: string;
  description: string;
  duration_sec: number;
  video_url?: string | null;
  misconception_ids: string[];
  key_takeaways: string[];
  fallback_explanation: string;
}

export type ChallengeType = 'prediction' | 'construction' | 'diagnosis';

export interface Challenge {
  id: string;
  title: string;
  type: ChallengeType;
  concept: string;
  difficulty: string;
  prompt: string;
  initial_circuit?: CanonicalCircuit | null;
  expected_outcomes?: Record<string, number> | null;
  options?: string[] | null;
  correct_option_index?: number | null;
  explanation: string;
}

export interface ChallengeSubmission {
  challenge_id: string;
  prediction?: Record<string, number> | null;
  circuit?: CanonicalCircuit | null;
  selected_option_index?: number | null;
}

export interface ChallengeResult {
  challenge_id: string;
  passed: boolean;
  score: number;
  feedback: string;
  concept: string;
  misconceptions_triggered: string[];
  next_recommendation: string;
}

export type MasteryLevel = 'Learning' | 'Practicing' | 'Mastered';

export interface ConceptMastery {
  concept: string;
  score: number;
  level: MasteryLevel;
  attempts: number;
  correct: number;
}

export interface UserMasteryProfile {
  overall_progress: number;
  concepts: Record<string, ConceptMastery>;
}
'''
(types_dir / 'quantum.ts').write_text(quantum_ts.strip() + '\n', encoding='utf-8')
print('1. types/quantum.ts created')

# 2. lib/api.ts
api_ts = '''import {
  CanonicalCircuit,
  PredictionInput,
  SimulationResult,
  ComparisonResult,
  ExecutionContext,
  TutorRequest,
  TutorResponse,
  ManimClipMetadata,
  Challenge,
  ChallengeSubmission,
  ChallengeResult,
  UserMasteryProfile,
} from '../types/quantum';

const API_BASE = 'http://127.0.0.1:8000/api/v1';

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });
  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(API Error : );
  }
  return res.json() as Promise<T>;
}

export async function simulateCircuit(circuit: CanonicalCircuit, shots = 1024): Promise<SimulationResult> {
  return fetchJson<SimulationResult>(${API_BASE}/simulate, {
    method: 'POST',
    body: JSON.stringify({ circuit, shots }),
  });
}

export async function comparePrediction(
  prediction: PredictionInput,
  simulation: SimulationResult
): Promise<ComparisonResult> {
  return fetchJson<ComparisonResult>(${API_BASE}/compare, {
    method: 'POST',
    body: JSON.stringify({ prediction, simulation }),
  });
}

export async function runAndCompare(
  prediction: PredictionInput,
  simulation: SimulationResult
): Promise<ExecutionContext> {
  return fetchJson<ExecutionContext>(${API_BASE}/run-and-compare, {
    method: 'POST',
    body: JSON.stringify({ prediction, simulation }),
  });
}

export async function queryTutor(req: TutorRequest): Promise<TutorResponse> {
  return fetchJson<TutorResponse>(${API_BASE}/tutor, {
    method: 'POST',
    body: JSON.stringify(req),
  });
}

export async function getManimClips(): Promise<ManimClipMetadata[]> {
  return fetchJson<ManimClipMetadata[]>(${API_BASE}/manim/clips);
}

export async function selectManimClip(concept?: string, rule?: string): Promise<ManimClipMetadata> {
  const params = new URLSearchParams();
  if (concept) params.set('concept', concept);
  if (rule) params.set('rule', rule);
  return fetchJson<ManimClipMetadata>(${API_BASE}/manim/select?);
}

export async function getChallenges(): Promise<Challenge[]> {
  return fetchJson<Challenge[]>(${API_BASE}/challenges);
}

export async function submitChallenge(sub: ChallengeSubmission): Promise<ChallengeResult> {
  return fetchJson<ChallengeResult>(${API_BASE}/challenges/submit, {
    method: 'POST',
    body: JSON.stringify(sub),
  });
}

export async function getMasteryProfile(): Promise<UserMasteryProfile> {
  return fetchJson<UserMasteryProfile>(${API_BASE}/mastery);
}

export async function getGoldenCircuits(): Promise<{ h_circuit: CanonicalCircuit; bell_circuit: CanonicalCircuit }> {
  return fetchJson<{ h_circuit: CanonicalCircuit; bell_circuit: CanonicalCircuit }>(${API_BASE}/circuits/golden);
}
'''
(lib_dir / 'api.ts').write_text(api_ts.strip() + '\n', encoding='utf-8')
print('2. lib/api.ts created')
