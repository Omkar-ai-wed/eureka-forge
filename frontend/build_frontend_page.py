from pathlib import Path

app_dir = Path(r'C:\Users\Omkar Shedage\quantum-intelligence-lab\frontend\src\app')

# 1. globals.css
globals_css = '''@import " tailwindcss\;

:root {
 --background: #030712;
 --foreground: #f8fafc;
}

body {
 background-color: var(--background);
 color: var(--foreground);
 font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
 overflow-x: hidden;
}

/* Custom scrollbars */
::-webkit-scrollbar {
 width: 6px;
 height: 6px;
}
::-webkit-scrollbar-track {
 background: #020617;
}
::-webkit-scrollbar-thumb {
 background: #1e293b;
 border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
 background: #334155;
}
'''
(app_dir / 'globals.css').write_text(globals_css.strip() + '\n', encoding='utf-8')
print('1. globals.css written')

# 2. page.tsx
page_tsx = '''\use client\;

import React, { useState, useEffect } from 'react';
import { Navbar, ActiveTab } from '../components/Navbar';
import { BlochSphere } from '../components/BlochSphere';
import { Histogram } from '../components/Histogram';
import { CircuitCanvas } from '../components/CircuitCanvas';
import { AITutorPanel } from '../components/AITutorPanel';
import { ManimPlayer } from '../components/ManimPlayer';
import { TraceViewer } from '../components/TraceViewer';
import { ChallengeView } from '../components/ChallengeView';
import { MasteryView } from '../components/MasteryView';
import {
 CanonicalCircuit,
 GateType,
 PredictionInput,
 SimulationResult,
 ComparisonResult,
 ExecutionContext,
 MisconceptionResult,
} from '../types/quantum';
import {
 simulateCircuit,
 comparePrediction,
 getGoldenCircuits,
 getManimClips,
} from '../lib/api';
import {
 Sparkles,
 ArrowRight,
 BrainCircuit,
 Cpu,
 Lock,
 Unlock,
 Layers,
 Award,
 BookOpen,
 CheckCircle2,
 AlertTriangle,
 RotateCcw,
} from 'lucide-react';

export default function Home() {
 const [activeTab, setActiveTab] = useState<ActiveTab>('dashboard');
 const [simulatorReady, setSimulatorReady] = useState<boolean>(false);

 // Canonical Circuit state
 const [circuit, setCircuit] = useState<CanonicalCircuit>({
 schema_version: '1.0',
 qubits: 1,
 gates: [{ gate: 'H', target: 0, params: [] }],
 label: 'H|0>',
 concept: 'superposition',
 });

 // Prediction state
 const [predZero, setPredZero] = useState<number>(50);
 const [predictionLocked, setPredictionLocked] = useState<boolean>(false);

 // Execution state
 const [isSimulating, setIsSimulating] = useState<boolean>(false);
 const [simulationResult, setSimulationResult] = useState<SimulationResult | null>(null);
 const [comparisonResult, setComparisonResult] = useState<ComparisonResult | null>(null);
 const [misconceptions, setMisconceptions] = useState<MisconceptionResult[]>([]);

 // Verify backend connection on load
 useEffect(() => {
 async function init() {
 try {
 await getGoldenCircuits();
 setSimulatorReady(true);
 } catch (err) {
 console.error('Simulator backend ping error:', err);
 setSimulatorReady(false);
 }
 }
 init();
 }, []);

 // Preset loader
 const handleLoadPreset = (preset: 'h' | 'bell') => {
 if (preset === 'h') {
 setCircuit({
 schema_version: '1.0',
 qubits: 1,
 gates: [{ gate: 'H', target: 0, params: [] }],
 label: 'H|0>',
 concept: 'superposition',
 });
 setPredZero(50);
 } else {
 setCircuit({
 schema_version: '1.0',
 qubits: 2,
 gates: [
 { gate: 'H', target: 0, params: [] },
 { gate: 'CX', target: 1, control: 0, params: [] },
 ],
 label: 'Bell State',
 concept: 'entanglement',
 });
 setPredZero(50);
 }
 setPredictionLocked(false);
 setSimulationResult(null);
 setComparisonResult(null);
 };

 // Run Simulation flow
 const handleRunSimulation = async () => {
 setIsSimulating(true);
 try {
 const simRes = await simulateCircuit(circuit, 1024);
 setSimulationResult(simRes);

 // Deterministic comparison
 const predInput: PredictionInput = {
 circuit,
 probabilities:
 circuit.qubits === 1
 ? { '0': predZero / 100, '1': (100 - predZero) / 100 }
 : { '00': 0.5, '11': 0.5 },
 concept: circuit.concept ?? undefined,
 };

 const compRes = await comparePrediction(predInput, simRes);
 setComparisonResult(compRes);

 // Check M1-M4 heuristics
 const miscList: MisconceptionResult[] = [];
 if (circuit.qubits === 1 && (predZero >= 80 || predZero <= 20) && !compRes.overall_match) {
 miscList.push({
 rule: 'M1',
 triggered: true,
 confidence: 0.85,
 evidence: Learner predicted % definite outcome for H|0>,
 learner_explanation:
 'Superposition is not a hidden coin toss. The qubit is genuinely in both states simultaneously until measured.',
 remediation_concept: 'superposition',
 suggested_challenge: 'Predict H|0> five times to observe the balanced distribution.',
 manim_clip_id: 'clip_superposition',
 });
 }
 setMisconceptions(miscList);
 setActiveTab('results');
 } catch (err: any) {
 console.error('Simulation failed:', err);
 } finally {
 setIsSimulating(false);
 }
 };

 // Execution Context for AI Tutor
 const currentContext: ExecutionContext = {
 schema_version: '1.0',
 circuit,
 prediction: {
 circuit,
 probabilities:
 circuit.qubits === 1
 ? { '0': predZero / 100, '1': (100 - predZero) / 100 }
 : { '00': 0.5, '11': 0.5 },
 concept: circuit.concept ?? undefined,
 },
 simulation: simulationResult || {
 schema_version: '1.0',
 circuit,
 shots: 1024,
 counts: { '0': 512, '1': 512 },
 probabilities: { '0': 0.5, '1': 0.5 },
 trace: [],
 backend: 'qiskit-aer',
 },
 comparison: comparisonResult,
 misconceptions,
 };

 return (
 <div className='min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-slate-950'>
 <Navbar activeTab={activeTab} setActiveTab={setActiveTab} simulatorReady={simulatorReady} />

 <main className='flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-8'>
 {/* ================= SCREEN 1: DASHBOARD ================= */}
 {activeTab === 'dashboard' && (
 <div className='space-y-8'>
 {/* Hero banner */}
 <div className='relative overflow-hidden rounded-3xl bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-cyan-800/40 p-8 shadow-2xl'>
 <div className='max-w-2xl space-y-4'>
 <div className='inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/80 border border-cyan-700/60 text-cyan-300 text-xs font-mono font-semibold'>
 <Sparkles className='w-3.5 h-3.5 text-cyan-400' />
 Level-3 SIH26140 Learning Engine
 </div>
 <h1 className='text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight'>
 Students Predict. The Simulator Proves. <span className='text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-indigo-400'>AI Explains Why.</span>
 </h1>
 <p className='text-slate-300 text-sm leading-relaxed'>
 Experience the complete quantum algorithm learning loop grounded strictly in Qiskit Aer simulation truth. Predict before simulating, diagnose classical misconceptions, and achieve true quantum intuition.
 </p>
 <div className='flex items-center gap-3 pt-2'>
 <button
 onClick={() => setActiveTab('lesson')}
 className='px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-slate-950 font-bold text-xs shadow-lg shadow-cyan-500/25 flex items-center gap-2 transition-all'
 >
 <span>Continue Lesson: Superposition</span>
 <ArrowRight className='w-4 h-4' />
 </button>
 <button
 onClick={() => setActiveTab('circuit')}
 className='px-5 py-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 text-xs font-medium transition-all'
 >
 Open Circuit Lab
 </button>
 </div>
 </div>
 </div>

 {/* Core Learning Loop Steps */}
 <div className='space-y-3'>
 <h2 className='text-xs font-mono uppercase tracking-wider text-slate-400 font-semibold'>
 The Nine-Stage Mastery Loop:
 </h2>
 <div className='grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 text-xs font-mono'>
 {[
 { n: '1', name: 'Predict', desc: 'Lock hypothesis' },
 { n: '2', name: 'Build', desc: 'Assemble gates' },
 { n: '3', name: 'Simulate', desc: 'Aer ground truth' },
 { n: '4', name: 'Compare', desc: 'Delta breakdown' },
 { n: '5', name: 'Diagnose', desc: 'M1-M4 heuristics' },
 { n: '6', name: 'Explain', desc: 'Grounded AI tutor' },
 { n: '7', name: 'Show Me Why', desc: 'Manim animations' },
 { n: '8', name: 'Challenge', desc: 'Deterministic grade' },
 { n: '9', name: 'Mastery', desc: 'Concept progress' },
 ].map((s) => (
 <div key={s.n} className='p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1'>
 <div className='text-cyan-400 font-bold'>Stage {s.n}: {s.name}</div>
 <div className='text-[11px] text-slate-400'>{s.desc}</div>
 </div>
 ))}
 </div>
 </div>

 {/* Mastery Quick View */}
 <MasteryView />
 </div>
 )}

 {/* ================= SCREEN 2: LESSON ================= */}
 {activeTab === 'lesson' && (
 <div className='space-y-6'>
 <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-8 shadow-xl space-y-6'>
 <div className='flex items-center justify-between pb-4 border-b border-slate-800'>
 <div>
 <span className='text-xs font-mono uppercase tracking-wider text-cyan-400 font-semibold'>
 Curriculum Unit 2
 </span>
 <h2 className='text-2xl font-bold text-white'>Superposition & The Hadamard Gate</h2>
 </div>
 <span className='px-3 py-1 rounded-full bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-mono'>
 Concept MVP
 </span>
 </div>

 <div className='grid grid-cols-1 lg:grid-cols-2 gap-8 items-center'>
 <div className='space-y-4 text-xs text-slate-300 leading-relaxed font-sans'>
 <p className='text-sm text-slate-200 font-medium'>
 In classical computing, a bit is strictly 0 or 1. In quantum computing, a qubit begins in state |0&gt;, but quantum gates rotate its state vector continuously through complex Hilbert space.
 </p>
 <p>
 The <strong>Hadamard (H) gate</strong> is the fundamental quantum superposition creator. It takes the computational ground state |0&gt; and rotates it directly onto the equator of the Bloch sphere, forming the state:
 </p>
 <div className='p-4 bg-slate-950 rounded-xl border border-cyan-900/60 font-mono text-cyan-300 text-sm text-center shadow-inner'>
 |?&gt; = H|0&gt; = (|0&gt; + |1&gt;) / v2
 </div>
 <p>
 <strong>Key Intuition:</strong> This is <em>not</em> classical randomness or a hidden coin toss. The qubit genuinely possesses probability amplitudes for both outcomes simultaneously. Only when measured does the state project onto |0&gt; or |1&gt; with equal 50% probability.
 </p>
 </div>

 <div className='flex justify-center'>
 <BlochSphere theta={Math.PI / 2} phi={0} stateLabel='|+? = (|0? + |1?)/v2' size={240} />
 </div>
 </div>

 <div className='pt-6 border-t border-slate-800 flex items-center justify-between'>
 <span className='text-xs text-slate-400 font-mono'>Ready to test your intuition?</span>
 <button
 onClick={() => setActiveTab('predict')}
 className='px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-slate-950 font-bold text-xs transition-all shadow-md shadow-cyan-500/20 flex items-center gap-2'
 >
 <span>Step 2: Predict the Result</span>
 <ArrowRight className='w-4 h-4' />
 </button>
 </div>
 </div>
 </div>
 )}

 {/* ================= SCREEN 3: PREDICTION-BEFORE-RUN ================= */}
 {activeTab === 'predict' && (
 <div className='space-y-6'>
 <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-8 shadow-xl space-y-6 max-w-3xl mx-auto'>
 <div className='text-center space-y-2 pb-4 border-b border-slate-800'>
 <span className='text-xs font-mono uppercase tracking-wider text-cyan-400 font-semibold'>
 Predict-Before-Run Contract
 </span>
 <h2 className='text-xl font-bold text-white'>What do you think will happen?</h2>
 <p className='text-xs text-slate-400'>
 Before the quantum simulator computes, commit your hypothesis. The platform will compare your prediction against Qiskit Aer ground truth.
 </p>
 </div>

 <div className='p-6 bg-slate-950 rounded-xl border border-slate-800 space-y-6'>
 <div className='flex items-center justify-between text-xs font-mono'>
 <span className='text-slate-300'>Target Circuit:</span>
 <span className='text-cyan-400 font-bold'>{circuit.label || 'H|0> Single Qubit'}</span>
 </div>

 <div className='space-y-4'>
 <div className='flex items-center justify-between font-mono text-xs'>
 <span>Outcome |0&gt;: <strong className='text-cyan-400 text-sm'>{predZero}%</strong></span>
 <span>Outcome |1&gt;: <strong className='text-indigo-400 text-sm'>{100 - predZero}%</strong></span>
 </div>

 <input
 type='range'
 min='0'
 max='100'
 disabled={predictionLocked}
 value={predZero}
 onChange={(e) => setPredZero(Number(e.target.value))}
 className='w-full accent-cyan-400 cursor-pointer disabled:opacity-50'
 />

 <div className='flex items-center justify-between text-[11px] text-slate-500 font-mono'>
 <span>100% |0&gt; (Classical Ground)</span>
 <span>50% / 50% (Equal Superposition)</span>
 <span>100% |1&gt; (Inverted State)</span>
 </div>
 </div>

 <div className='pt-2 flex items-center justify-between'>
 <button
 onClick={() => setPredictionLocked(!predictionLocked)}
 className={px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all }
 >
 {predictionLocked ? <Lock className='w-3.5 h-3.5 text-amber-400' /> : <Unlock className='w-3.5 h-3.5' />}
 <span>{predictionLocked ? 'Prediction Locked' : 'Lock Prediction'}</span>
 </button>

 <button
 onClick={() => {
 setPredictionLocked(true);
 setActiveTab('circuit');
 }}
 className='px-6 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-slate-950 font-bold text-xs transition-all shadow-md shadow-cyan-500/20 flex items-center gap-2'
 >
 <span>Proceed to Circuit Lab</span>
 <ArrowRight className='w-4 h-4' />
 </button>
 </div>
 </div>
 </div>
 </div>
 )}

 {/* ================= SCREEN 4: CIRCUIT LAB ================= */}
 {activeTab === 'circuit' && (
 <div className='space-y-6'>
 <CircuitCanvas
 circuit={circuit}
 setCircuit={setCircuit}
 onSimulate={handleRunSimulation}
 isSimulating={isSimulating}
 onLoadPreset={handleLoadPreset}
 />
 </div>
 )}

 {/* ================= SCREEN 5 & 6: SIMULATION RESULT & COMPARE ================= */}
 {activeTab === 'results' && (
 <div className='space-y-6'>
 <div className='grid grid-cols-1 lg:grid-cols-3 gap-6'>
 {/* Histogram probability view */}
 <div className='lg:col-span-2 space-y-6'>
 <Histogram
 probabilities={simulationResult?.probabilities || { '0': 0.5, '1': 0.5 }}
 predicted={
 circuit.qubits === 1
 ? { '0': predZero / 100, '1': (100 - predZero) / 100 }
 : { '00': 0.5, '11': 0.5 }
 }
 outcomes={comparisonResult?.outcomes}
 overallMatch={comparisonResult?.overall_match}
 shots={simulationResult?.shots || 1024}
 />

 {/* Comparison Card */}
 {comparisonResult && (
 <div
 className={p-5 rounded-2xl border space-y-3 }
 >
 <div className='flex items-center justify-between text-xs font-mono font-bold'>
 <div className='flex items-center gap-2'>
 {comparisonResult.overall_match ? (
 <CheckCircle2 className='w-4 h-4 text-emerald-400' />
 ) : (
 <AlertTriangle className='w-4 h-4 text-rose-400' />
 )}
 <span>{comparisonResult.summary}</span>
 </div>
 <span className='px-2 py-0.5 rounded bg-slate-900 text-slate-300'>
 Accuracy: {(comparisonResult.accuracy_score * 100).toFixed(0)}%
 </span>
 </div>

 {!comparisonResult.overall_match && (
 <p className='text-xs text-slate-300 leading-relaxed font-sans'>
 Your prediction deviated from the quantum simulator result. Ask the AI Tutor to diagnose why or watch the Show Me Why animation.
 </p>
 )}
 </div>
 )}
 </div>

 {/* Bloch Sphere and Quick Actions */}
 <div className='space-y-6'>
 <BlochSphere
 theta={circuit.gates.some((g) => g.gate === 'H') ? Math.PI / 2 : 0}
 phi={0}
 stateLabel={circuit.gates.some((g) => g.gate === 'H') ? '|+? = (|0? + |1?)/v2' : '|0?'}
 size={220}
 />

 <div className='p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-3 text-xs'>
 <span className='font-mono text-slate-400 uppercase font-semibold block'>Next Step:</span>
 <button
 onClick={() => setActiveTab('trace')}
 className='w-full py-2 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition-all text-left flex items-center justify-between'
 >
 <span>Step 5: View Execution Trace</span>
 <ArrowRight className='w-3.5 h-3.5' />
 </button>
 <button
 onClick={() => setActiveTab('tutor')}
 className='w-full py-2 px-3 rounded-lg bg-indigo-950 hover:bg-indigo-900 text-indigo-300 border border-indigo-800 transition-all text-left flex items-center justify-between font-medium'
 >
 <span>Step 6: Consult Grounded AI Tutor</span>
 <ArrowRight className='w-3.5 h-3.5' />
 </button>
 <button
 onClick={() => setActiveTab('manim')}
 className='w-full py-2 px-3 rounded-lg bg-cyan-950 hover:bg-cyan-900 text-cyan-300 border border-cyan-800 transition-all text-left flex items-center justify-between font-medium'
 >
 <span>Step 7: Watch Show Me Why</span>
 <ArrowRight className='w-3.5 h-3.5' />
 </button>
 </div>
 </div>
 </div>
 </div>
 )}

 {/* ================= SCREEN 7: STEP-BY-STEP TRACE ================= */}
 {activeTab === 'trace' && (
 <div className='space-y-6'>
 <TraceViewer
 trace={
 simulationResult?.trace.length
 ? simulationResult.trace
 : [
 { step: 0, event: 'Initialize state |00...0>' },
 { step: 1, event: 'H on q0 -> (|0> + |1>)/sqrt(2)' },
 { step: 2, event: 'Measurement projection' },
 ]
 }
 />
 </div>
 )}

 {/* ================= SCREEN 8: AI TUTOR ================= */}
 {activeTab === 'tutor' && (
 <div className='space-y-6'>
 <AITutorPanel context={currentContext} />
 </div>
 )}

 {/* ================= SCREEN 9: SHOW ME WHY ================= */}
 {activeTab === 'manim' && (
 <div className='space-y-6'>
 <ManimPlayer
 currentConcept={circuit.concept ?? undefined}
 triggeredMisconception={misconceptions.length > 0 ? misconceptions[0].rule : null}
 />
 </div>
 )}

 {/* ================= SCREEN 10: CHALLENGES ================= */}
 {activeTab === 'challenges' && (
 <div className='space-y-6'>
 <ChallengeView currentCircuit={circuit} onRefreshMastery={() => {}} />
 </div>
 )}

 {/* ================= SCREEN 11: MASTERY ================= */}
 {activeTab === 'mastery' && (
 <div className='space-y-6'>
 <MasteryView onStartLesson={() => setActiveTab('lesson')} />
 </div>
 )}
 </main>

 {/* Footer */}
 <footer className='border-t border-slate-900 bg-slate-950 py-4 px-6 text-center text-xs text-slate-500 font-mono'>
 <span>Eureka Forge SIH26140 Prototype - Principle: Simulator computes. Everything else reads.</span>
 </footer>
 </div>
 );
}
'''
(app_dir / 'page.tsx').write_text(page_tsx.strip() + '\n', encoding='utf-8')
print('2. page.tsx written')
