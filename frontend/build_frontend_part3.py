from pathlib import Path

comp = Path(r'C:\Users\Omkar Shedage\quantum-intelligence-lab\frontend\src\components')

# 1. CircuitCanvas.tsx
circuit_code = '''import React, { useState } from 'react';
import { CanonicalCircuit, Gate, GateType } from '../types/quantum';
import { Play, RotateCcw, Plus, Trash2, Code2, Sparkles, ChevronRight } from 'lucide-react';

interface CircuitCanvasProps {
  circuit: CanonicalCircuit;
  setCircuit: (circuit: CanonicalCircuit) => void;
  onSimulate: () => void;
  isSimulating: boolean;
  onLoadPreset: (preset: 'h' | 'bell') => void;
}

export const CircuitCanvas: React.FC<CircuitCanvasProps> = ({
  circuit,
  setCircuit,
  onSimulate,
  isSimulating,
  onLoadPreset,
}) => {
  const [selectedGate, setSelectedGate] = useState<GateType>('H');
  const [selectedQubit, setSelectedQubit] = useState<number>(0);
  const [showCode, setShowCode] = useState<boolean>(false);

  const addGate = () => {
    const newGate: Gate = {
      gate: selectedGate,
      target: selectedQubit,
      control: selectedGate === 'CX' ? (selectedQubit === 0 ? 0 : 1) : null,
    };
    if (selectedGate === 'CX') {
      newGate.control = 0;
      newGate.target = 1;
    }
    setCircuit({
      ...circuit,
      gates: [...circuit.gates, newGate],
    });
  };

  const removeGate = (index: number) => {
    const updated = circuit.gates.filter((_, i) => i !== index);
    setCircuit({
      ...circuit,
      gates: updated,
    });
  };

  const clearCircuit = () => {
    setCircuit({
      ...circuit,
      gates: [],
    });
  };

  const generateQiskitCode = (): string => {
    let lines = [
      'from qiskit import QuantumCircuit',
      'from qiskit_aer import AerSimulator',
      '',
      qc = QuantumCircuit(, ),
    ];
    circuit.gates.forEach((g) => {
      if (g.gate === 'H') lines.push(qc.h());
      else if (g.gate === 'X') lines.push(qc.x());
      else if (g.gate === 'Z') lines.push(qc.z());
      else if (g.gate === 'CX') lines.push(qc.cx(, ));
      else if (g.gate === 'M') lines.push(qc.measure(, ));
    });
    lines.push('');
    lines.push('qc.measure_all()');
    lines.push('sim = AerSimulator()');
    lines.push('job = sim.run(qc, shots=1024)');
    lines.push('counts = job.result().get_counts()');
    lines.push('print(" Counts:\, counts)');
 return lines.join('\\n');
 };

 return (
 <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6'>
 <div className='flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-slate-800'>
 <div>
 <h2 className='text-base font-bold text-white flex items-center gap-2'>
 <span>Interactive Circuit Lab</span>
 <span className='text-xs px-2 py-0.5 rounded bg-slate-800 text-cyan-400 font-mono'>
 {circuit.qubits} Qubit{circuit.qubits > 1 ? 's' : ''}
 </span>
 </h2>
 <p className='text-xs text-slate-400'>
 Canonical representation executes deterministically on Qiskit Aer simulator.
 </p>
 </div>

 <div className='flex items-center gap-2 flex-wrap'>
 <button
 onClick={() => onLoadPreset('h')}
 className='px-2.5 py-1.5 rounded-lg bg-cyan-950/70 border border-cyan-800 text-cyan-300 text-xs hover:bg-cyan-900/60 transition-all flex items-center gap-1.5 font-medium'
 >
 <Sparkles className='w-3.5 h-3.5 text-cyan-400' />
 <span>Preset: H|0&gt;</span>
 </button>
 <button
 onClick={() => onLoadPreset('bell')}
 className='px-2.5 py-1.5 rounded-lg bg-indigo-950/70 border border-indigo-800 text-indigo-300 text-xs hover:bg-indigo-900/60 transition-all flex items-center gap-1.5 font-medium'
 >
 <Sparkles className='w-3.5 h-3.5 text-indigo-400' />
 <span>Preset: Bell State</span>
 </button>
 <button
 onClick={clearCircuit}
 className='p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-rose-400 hover:bg-slate-700 transition-all text-xs'
 title='Clear Circuit'
 >
 <RotateCcw className='w-4 h-4' />
 </button>
 <button
 onClick={() => setShowCode(!showCode)}
 className='px-2.5 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-200 text-xs hover:bg-slate-700 transition-all flex items-center gap-1.5'
 >
 <Code2 className='w-3.5 h-3.5 text-slate-400' />
 <span>{showCode ? 'Hide Qiskit' : 'Export Code'}</span>
 </button>
 <button
 onClick={onSimulate}
 disabled={isSimulating}
 className='px-4 py-1.5 rounded-lg bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-semibold text-xs transition-all shadow-md shadow-cyan-500/20 flex items-center gap-1.5 disabled:opacity-50'
 >
 <Play className='w-3.5 h-3.5 fill-current' />
 <span>{isSimulating ? 'Simulating Aer...' : 'Simulate'}</span>
 </button>
 </div>
 </div>

 <div className='flex items-center gap-3 p-3 bg-slate-950/60 border border-slate-800/80 rounded-xl flex-wrap text-xs'>
 <span className='text-slate-400 font-mono uppercase text-[11px] font-semibold'>Gate Palette:</span>
 <div className='flex items-center gap-1.5'>
 {(['H', 'X', 'Z', 'CX', 'M'] as GateType[]).map((g) => (
 <button
 key={g}
 onClick={() => setSelectedGate(g)}
 className={w-8 h-8 rounded-lg font-mono font-bold transition-all }
 >
 {g}
 </button>
 ))}
 </div>

 <div className='h-5 w-px bg-slate-800 mx-1' />

 <div className='flex items-center gap-2 text-slate-300'>
 <span>Target Qubit:</span>
 <select
 value={selectedQubit}
 onChange={(e) => setSelectedQubit(Number(e.target.value))}
 className='bg-slate-800 border border-slate-700 rounded px-2 py-1 text-xs text-slate-100 font-mono outline-none'
 >
 {Array.from({ length: circuit.qubits }).map((_, i) => (
 <option key={i} value={i}>
 q[{i}]
 </option>
 ))}
 </select>
 </div>

 <button
 onClick={addGate}
 className='ml-auto px-3 py-1 rounded-lg bg-cyan-950 text-cyan-300 border border-cyan-800 hover:bg-cyan-900 transition-all font-medium flex items-center gap-1'
 >
 <Plus className='w-3.5 h-3.5' />
 <span>Add Gate</span>
 </button>
 </div>

 <div className='p-6 bg-slate-950 rounded-xl border border-slate-800 space-y-6 overflow-x-auto'>
 {Array.from({ length: circuit.qubits }).map((_, qIndex) => {
 return (
 <div key={qIndex} className='flex items-center gap-4 relative min-w-[480px]'>
 <div className='w-16 flex items-center justify-between font-mono text-xs font-semibold text-slate-300'>
 <span>q[{qIndex}]</span>
 <span className='text-cyan-400'>|0&gt;</span>
 </div>

 <div className='flex-1 relative flex items-center h-12'>
 <div className='absolute left-0 right-0 h-0.5 bg-slate-700' />

 <div className='relative flex items-center gap-4 z-10 pl-4'>
 {circuit.gates.map((g, gIdx) => {
 const isTarget = g.target === qIndex;
 const isControl = g.control === qIndex;

 if (!isTarget && !isControl) {
 return <div key={gIdx} className='w-10 h-10' />;
 }

 if (isControl) {
 return (
 <div
 key={gIdx}
 className='w-10 h-10 flex items-center justify-center relative group cursor-pointer'
 onClick={() => removeGate(gIdx)}
 title='Click to remove CNOT gate'
 >
 <div className='w-3.5 h-3.5 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400' />
 <div className='absolute -top-6 hidden group-hover:block bg-slate-900 text-rose-400 text-[10px] px-1.5 py-0.5 rounded border border-rose-900'>
 Delete
 </div>
 </div>
 );
 }

 return (
 <div
 key={gIdx}
 className='w-10 h-10 rounded-lg bg-gradient-to-br from-slate-800 to-slate-900 border border-cyan-500/70 text-cyan-300 font-mono font-bold flex items-center justify-center text-sm shadow-md shadow-cyan-950 relative group cursor-pointer hover:border-rose-500 hover:text-rose-400 transition-all'
 onClick={() => removeGate(gIdx)}
 title='Click to remove gate'
 >
 {g.gate === 'CX' ? '+' : g.gate}
 <div className='absolute -top-6 hidden group-hover:block bg-slate-900 text-rose-400 text-[10px] px-1.5 py-0.5 rounded border border-rose-900 whitespace-nowrap'>
 Remove
 </div>
 </div>
 );
 })}
 </div>
 </div>
 </div>
 );
 })}
 </div>

 {showCode && (
 <div className='bg-slate-950 p-4 rounded-xl border border-slate-800 text-xs font-mono space-y-2'>
 <div className='flex items-center justify-between text-slate-400'>
 <span>Qiskit 1.0 Python Canonical Code:</span>
 <span className='text-emerald-400'>Ready for execution</span>
 </div>
 <pre className='text-cyan-300 overflow-x-auto p-3 bg-slate-900/60 rounded-lg border border-slate-800/80'>
 {generateQiskitCode()}
 </pre>
 </div>
 )}
 </div>
 );
};
'''
(comp / 'CircuitCanvas.tsx').write_text(circuit_code.strip() + '\n', encoding='utf-8')
print('4. CircuitCanvas.tsx written')

# 2. AITutorPanel.tsx
tutor_code = '''import React, { useState } from 'react';
import { TutorMode, TutorResponse, ExecutionContext } from '../types/quantum';
import { queryTutor } from '../lib/api';
import { BrainCircuit, Sparkles, AlertCircle, HelpCircle, Terminal, Send } from 'lucide-react';

interface AITutorPanelProps {
 context: ExecutionContext;
}

export const AITutorPanel: React.FC<AITutorPanelProps> = ({ context }) => {
 const [mode, setMode] = useState<TutorMode>('explain');
 const [question, setQuestion] = useState<string>('');
 const [loading, setLoading] = useState<boolean>(false);
 const [response, setResponse] = useState<TutorResponse | null>(null);

 const fetchTutor = async (customMode = mode, customQ = question) => {
 setLoading(true);
 try {
 const res = await queryTutor({
 mode: customMode,
 learner_question: customQ.trim() || undefined,
 context,
 });
 setResponse(res);
 } catch (err: any) {
 console.error('Tutor query error:', err);
 } finally {
 setLoading(false);
 }
 };

 const handleModeChange = (newMode: TutorMode) => {
 setMode(newMode);
 fetchTutor(newMode);
 };

 const handleSendCustom = (e: React.FormEvent) => {
 e.preventDefault();
 if (!question.trim()) return;
 fetchTutor(mode, question);
 };

 const quickQuestions = [
 'Why is the measurement distribution 50/50?',
 'What does the Hadamard gate do on the Bloch sphere?',
 'Does Bell state entanglement allow faster-than-light communication?',
 ];

 return (
 <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5'>
 <div className='flex items-center justify-between pb-4 border-b border-slate-800'>
 <div className='flex items-center gap-3'>
 <div className='w-8 h-8 rounded-lg bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center'>
 <BrainCircuit className='w-4 h-4 text-indigo-400' />
 </div>
 <div>
 <h3 className='text-sm font-bold text-white'>Grounded AI Tutor</h3>
 <p className='text-xs text-slate-400 font-mono'>
 Reads simulator ground truth; never invents quantum probabilities.
 </p>
 </div>
 </div>

 <div className='flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs font-medium'>
 {(['explain', 'hint', 'debug'] as TutorMode[]).map((m) => (
 <button
 key={m}
 onClick={() => handleModeChange(m)}
 className={px-3 py-1 rounded capitalize transition-all }
 >
 {m}
 </button>
 ))}
 </div>
 </div>

 <div className='p-3 bg-slate-950/70 border border-slate-800/80 rounded-xl flex items-center justify-between text-xs font-mono text-slate-400'>
 <div className='flex items-center gap-2'>
 <Terminal className='w-3.5 h-3.5 text-cyan-400' />
 <span>Grounded in: Aer ({context.simulation.shots} shots)</span>
 </div>
 <div className='text-cyan-300'>
 {Object.entries(context.simulation.probabilities)
 .map(([k, v]) => |>: %)
 .join(', ')}
 </div>
 </div>

 <div className='min-h-[140px] p-4 bg-slate-950 rounded-xl border border-indigo-950/60 relative'>
 {loading ? (
 <div className='flex items-center justify-center h-32 text-indigo-300 text-xs gap-2 font-mono'>
 <Sparkles className='w-4 h-4 animate-spin' />
 <span>Consulting grounded quantum execution trace...</span>
 </div>
 ) : response ? (
 <div className='space-y-4 text-xs text-slate-200 leading-relaxed'>
 <div className='whitespace-pre-line'>{response.response}</div>

 {response.suggested_actions?.length > 0 && (
 <div className='pt-3 border-t border-slate-800/60 flex items-center gap-2 flex-wrap'>
 <span className='text-slate-500 font-mono text-[11px]'>Recommended:</span>
 {response.suggested_actions.map((act, i) => (
 <span
 key={i}
 className='px-2 py-0.5 rounded bg-indigo-950/80 border border-indigo-800 text-indigo-300 text-[11px]'
 >
 {act}
 </span>
 ))}
 </div>
 )}
 </div>
 ) : (
 <div className='flex flex-col items-center justify-center h-32 text-slate-500 text-xs space-y-2'>
 <HelpCircle className='w-6 h-6 text-slate-600' />
 <span>Click Explain, Hint, or Debug above, or ask a question below.</span>
 </div>
 )}
 </div>

 <div className='flex items-center gap-2 flex-wrap'>
 {quickQuestions.map((q, i) => (
 <button
 key={i}
 onClick={() => {
 setQuestion(q);
 fetchTutor(mode, q);
 }}
 className='px-2.5 py-1 rounded-full bg-slate-950 hover:bg-slate-800 border border-slate-800 text-[11px] text-slate-400 hover:text-cyan-300 transition-all text-left'
 >
 {q}
 </button>
 ))}
 </div>

 <form onSubmit={handleSendCustom} className='flex items-center gap-2'>
 <input
 type='text'
 value={question}
 onChange={(e) => setQuestion(e.target.value)}
 placeholder='Ask the grounded quantum tutor a question...'
 className='flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500'
 />
 <button
 type='submit'
 disabled={loading || !question.trim()}
 className='px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5 transition-all disabled:opacity-50'
 >
 <Send className='w-3.5 h-3.5' />
 <span>Ask</span>
 </button>
 </form>
 </div>
 );
};
'''
(comp / 'AITutorPanel.tsx').write_text(tutor_code.strip() + '\n', encoding='utf-8')
print('5. AITutorPanel.tsx written')

# 3. ManimPlayer.tsx
manim_code = '''import React, { useState, useEffect } from 'react';
import { ManimClipMetadata, MisconceptionRule } from '../types/quantum';
import { getManimClips, selectManimClip } from '../lib/api';
import { PlayCircle, Video, BookOpen, Sparkles, CheckCircle2 } from 'lucide-react';

interface ManimPlayerProps {
 currentConcept?: string;
 triggeredMisconception?: MisconceptionRule | null;
}

export const ManimPlayer: React.FC<ManimPlayerProps> = ({
 currentConcept,
 triggeredMisconception,
}) => {
 const [clips, setClips] = useState<ManimClipMetadata[]>([]);
 const [selectedClip, setSelectedClip] = useState<ManimClipMetadata | null>(null);
 const [animProgress, setAnimProgress] = useState<number>(0);
 const [isPlaying, setIsPlaying] = useState<boolean>(true);

 useEffect(() => {
 async function load() {
 try {
 const allClips = await getManimClips();
 setClips(allClips);
 const best = await selectManimClip(currentConcept, triggeredMisconception ?? undefined);
 setSelectedClip(best);
 } catch (err) {
 console.error('Failed to load Manim clips:', err);
 }
 }
 load();
 }, [currentConcept, triggeredMisconception]);

 useEffect(() => {
 if (!isPlaying) return;
 const interval = setInterval(() => {
 setAnimProgress((prev) => (prev >= 100 ? 0 : prev + 2));
 }, 80);
 return () => clearInterval(interval);
 }, [isPlaying]);

 return (
 <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6'>
 <div className='flex items-center justify-between pb-4 border-b border-slate-800 flex-wrap gap-3'>
 <div className='flex items-center gap-3'>
 <div className='w-8 h-8 rounded-lg bg-cyan-600/30 border border-cyan-500/40 flex items-center justify-center'>
 <PlayCircle className='w-4 h-4 text-cyan-400' />
 </div>
 <div>
 <h3 className='text-sm font-bold text-white'>Show Me Why - Visual Quantum Intuition</h3>
 <p className='text-xs text-slate-400 font-mono'>
 Pre-rendered Manim educational sequences with interactive vector dynamics.
 </p>
 </div>
 </div>

 <div className='flex items-center gap-1.5 flex-wrap'>
 {clips.map((clip) => (
 <button
 key={clip.clip_id}
 onClick={() => {
 setSelectedClip(clip);
 setAnimProgress(0);
 }}
 className={px-3 py-1.5 rounded-lg text-xs font-medium transition-all }
 >
 {clip.title.split(':')[0]}
 </button>
 ))}
 </div>
 </div>

 {selectedClip && (
 <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
 <div className='bg-slate-950 rounded-xl border border-slate-800 p-6 flex flex-col items-center justify-center relative overflow-hidden'>
 <div className='text-xs font-mono text-cyan-400 mb-4 flex items-center justify-between w-full'>
 <span>SIMULATION RENDER: {selectedClip.title.split('->')[0]}</span>
 <span>{selectedClip.duration_sec}s Loop</span>
 </div>

 <svg width='320' height='220' className='overflow-visible'>
 <defs>
 <linearGradient id='waveGrad' x1='0%' y1='0%' x2='100%' y2='0%'>
 <stop offset='0%' stopColor='#06b6d4' />
 <stop offset='50%' stopColor='#6366f1' />
 <stop offset='100%' stopColor='#a855f7' />
 </linearGradient>
 </defs>

 <circle cx='160' cy='110' r='75' fill='none' stroke='#1e293b' strokeWidth='1.5' />
 <line x1='80' y1='110' x2='240' y2='110' stroke='#334155' strokeWidth='1' strokeDasharray='3 3' />
 <line x1='160' y1='30' x2='160' y2='190' stroke='#334155' strokeWidth='1' strokeDasharray='3 3' />

 {(() => {
 const angle = (animProgress / 100) * (Math.PI / 2);
 const vx = 160 + 70 * Math.sin(angle);
 const vy = 110 - 70 * Math.cos(angle);
 return (
 <>
 <line
 x1='160'
 y1='110'
 x2={vx}
 y2={vy}
 stroke='url(#waveGrad)'
 strokeWidth='3.5'
 strokeLinecap='round'
 />
 <circle cx={vx} cy={vy} r='5' fill='#22d3ee' className='animate-ping' />
 <circle cx={vx} cy={vy} r='4' fill='#22d3ee' />
 </>
 );
 })()}

 <text x='160' y='22' textAnchor='middle' fill='#38bdf8' fontSize='11' fontFamily='monospace'>
 |0&gt; (Ground State)
 </text>
 <text x='250' y='114' textAnchor='start' fill='#a855f7' fontSize='11' fontFamily='monospace'>
 |+&gt; (Superposition)
 </text>
 </svg>

 <div className='w-full mt-4 flex items-center gap-3'>
 <button
 onClick={() => setIsPlaying(!isPlaying)}
 className='text-xs font-mono text-cyan-400 hover:text-cyan-300'
 >
 {isPlaying ? 'Pause' : 'Play'}
 </button>
 <div className='flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden'>
 <div
 className='h-full bg-cyan-400 rounded-full transition-all duration-75'
 style={{ width: ${animProgress}% }}
 />
 </div>
 <span className='text-[10px] font-mono text-slate-500'>{animProgress}%</span>
 </div>
 </div>

 <div className='space-y-4 flex flex-col justify-between'>
 <div>
 <h4 className='text-sm font-bold text-white mb-2'>{selectedClip.title}</h4>
 <p className='text-xs text-slate-300 leading-relaxed mb-4'>
 {selectedClip.description}
 </p>

 <div className='space-y-2 mb-4'>
 <span className='text-xs font-semibold text-slate-400 font-mono uppercase tracking-wider'>
 Key Insights:
 </span>
 {selectedClip.key_takeaways.map((takeaway, i) => (
 <div key={i} className='flex items-start gap-2 text-xs text-slate-300'>
 <CheckCircle2 className='w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5' />
 <span>{takeaway}</span>
 </div>
 ))}
 </div>
 </div>

 <div className='p-3.5 bg-slate-950/80 rounded-xl border border-slate-800 text-xs text-slate-400 space-y-1'>
 <span className='text-cyan-400 font-semibold block text-[11px] uppercase font-mono'>
 Physics Fallback Explanation:
 </span>
 <p className='leading-relaxed'>{selectedClip.fallback_explanation}</p>
 </div>
 </div>
 </div>
 )}
 </div>
 );
};
'''
(comp / 'ManimPlayer.tsx').write_text(manim_code.strip() + '\n', encoding='utf-8')
print('6. ManimPlayer.tsx written')
