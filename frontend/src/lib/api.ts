import {
  SimulationResult,
  TutorRequest,
  TutorResponse,
  ManimClip,
  TraceStep,
  Challenge,
  SubmitAnswerRequest,
  SubmitAnswerResponse,
  MasteryMap,
  HealthResponse,
  ConceptName,
} from '../types/quantum';

const BASE = 'http://127.0.0.1:8000/api/v1';

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(`API ${res.status}: ${msg}`);
  }
  return res.json() as Promise<T>;
}

/* Health */
export async function checkHealth(): Promise<HealthResponse> {
  return fetchJson<HealthResponse>(`${BASE}/health`);
}

/* Simulation */
export async function runSimulation(concept: ConceptName, shots = 1024): Promise<SimulationResult> {
  return fetchJson<SimulationResult>(`${BASE}/simulate`, {
    method: 'POST',
    body: JSON.stringify({ concept, shots }),
  });
}

/* Execution trace */
export async function getTrace(concept: ConceptName): Promise<TraceStep[]> {
  return fetchJson<TraceStep[]>(`${BASE}/trace?concept=${encodeURIComponent(concept)}`);
}

/* Tutor */
export async function getTutorExplanation(req: TutorRequest): Promise<TutorResponse> {
  return fetchJson<TutorResponse>(`${BASE}/tutor`, {
    method: 'POST',
    body: JSON.stringify(req),
  });
}

/* Manim */
export async function getManimClip(concept: ConceptName): Promise<ManimClip> {
  return fetchJson<ManimClip>(`${BASE}/manim/select?concept=${encodeURIComponent(concept)}`);
}

/* Challenges */
export async function listChallenges(concept: ConceptName): Promise<Challenge[]> {
  return fetchJson<Challenge[]>(`${BASE}/challenges?concept=${encodeURIComponent(concept)}`);
}

export async function submitAnswer(req: SubmitAnswerRequest): Promise<SubmitAnswerResponse> {
  return fetchJson<SubmitAnswerResponse>(`${BASE}/challenges/submit`, {
    method: 'POST',
    body: JSON.stringify(req),
  });
}

/* Mastery */
export async function getMastery(): Promise<MasteryMap> {
  return fetchJson<MasteryMap>(`${BASE}/mastery`);
}
