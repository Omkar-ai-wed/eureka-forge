import React from 'react';
import { ConceptName } from '../types/quantum';
import { Atom, Info } from 'lucide-react';

interface Props {
  concept: ConceptName;
  circuitDiagram: string;
}

/* Static circuit descriptions per concept */
const CIRCUIT_INFO: Record<ConceptName, { gates: string[]; description: string }> = {
  superposition: {
    gates: ['H on q0', 'Measure q0'],
    description: 'The Hadamard gate creates an equal superposition: |0⟩ → (|0⟩+|1⟩)/√2, giving ~50% probability for each outcome.',
  },
  measurement: {
    gates: ['H on q0', 'H on q0', 'Measure q0'],
    description: 'Double Hadamard followed by measurement: H·H = Identity, so state returns to |0⟩ before collapse.',
  },
  entanglement: {
    gates: ['H on q0', 'CX q0→q1', 'Measure q0', 'Measure q1'],
    description: 'Bell state circuit: Hadamard creates superposition, CX (CNOT) entangles qubits into (|00⟩+|11⟩)/√2.',
  },
};

export const CircuitCanvas: React.FC<Props> = ({ concept, circuitDiagram }) => {
  const info = CIRCUIT_INFO[concept];

  return (
    <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5'>
      {/* Header */}
      <div className='flex items-center justify-between pb-4 border-b border-slate-800'>
        <div className='flex items-center gap-3'>
          <div className='w-8 h-8 rounded-lg bg-cyan-600/30 border border-cyan-500/40 flex items-center justify-center'>
            <Atom className='w-4 h-4 text-cyan-400' />
          </div>
          <div>
            <h3 className='text-sm font-bold text-white capitalize'>{concept} Circuit</h3>
            <p className='text-xs text-slate-400 font-mono'>Qiskit canonical circuit — ready for Aer simulation</p>
          </div>
        </div>
        <span className='text-xs px-2 py-1 rounded bg-slate-800 text-slate-400 font-mono border border-slate-700'>
          {info.gates.length} gates
        </span>
      </div>

      {/* Gate rail visualisation */}
      <div className='overflow-x-auto'>
        <div className='flex items-center gap-2 min-w-max py-4 px-2'>
          {/* Qubit wires */}
          <div className='flex flex-col gap-6'>
            {concept === 'entanglement' ? (
              <>
                <div className='text-xs font-mono text-slate-400'>q0:</div>
                <div className='text-xs font-mono text-slate-400'>q1:</div>
              </>
            ) : (
              <div className='text-xs font-mono text-slate-400'>q0:</div>
            )}
          </div>

          {/* Gates */}
          <div className='flex items-start gap-3 relative'>
            {concept === 'superposition' && (
              <div className='flex flex-col gap-6'>
                <GateBox label='H' color='cyan' tooltip='Hadamard: creates superposition' />
                <div className='h-8 border-l-2 border-dashed border-slate-700' />
              </div>
            )}
            {concept === 'measurement' && (
              <>
                <div className='flex flex-col gap-6'>
                  <GateBox label='H' color='cyan' tooltip='Hadamard #1' />
                </div>
                <div className='flex flex-col gap-6'>
                  <GateBox label='H' color='cyan' tooltip='Hadamard #2 — cancels first' />
                </div>
              </>
            )}
            {concept === 'entanglement' && (
              <>
                <div className='flex flex-col gap-4'>
                  <GateBox label='H' color='cyan' tooltip='Hadamard on q0' />
                  <div className='w-14 h-8' />
                </div>
                                <div className='flex flex-col gap-4 items-center relative'>
                  <GateBox label='●' color='violet' tooltip='Control qubit (q0)' small />
                  <GateBox label='⊕' color='violet' tooltip='Target qubit (q1)' />
                  <div className='absolute top-4 bottom-4 w-0.5 bg-violet-500/60 pointer-events-none' />
                </div>
              </>
            )}
            {/* Measurement gate */}
            <div className='flex flex-col gap-4'>
              <MeasureBox />
              {concept === 'entanglement' && <MeasureBox />}
            </div>
          </div>
        </div>
      </div>

      {/* Info callout */}
      <div className='flex items-start gap-3 p-4 bg-cyan-950/30 border border-cyan-900/40 rounded-xl'>
        <Info className='w-4 h-4 text-cyan-400 mt-0.5 shrink-0' />
        <div className='space-y-1'>
          <div className='text-xs font-mono text-slate-400'>
            Gates: {info.gates.join(' → ')}
          </div>
          <p className='text-xs text-slate-300 leading-relaxed'>{info.description}</p>
        </div>
      </div>

      {/* ASCII diagram from backend if available */}
      {circuitDiagram && (
        <div className='p-3 bg-slate-950 rounded-xl border border-slate-800 overflow-x-auto'>
          <pre className='text-[10px] font-mono text-slate-400 whitespace-pre'>{circuitDiagram}</pre>
        </div>
      )}
    </div>
  );
};

function GateBox({ label, color, tooltip, small }: { label: string; color: string; tooltip: string; small?: boolean }) {
  const colors: Record<string, string> = {
    cyan: 'bg-cyan-600/20 border-cyan-500/50 text-cyan-300',
    violet: 'bg-violet-600/20 border-violet-500/50 text-violet-300',
    indigo: 'bg-indigo-600/20 border-indigo-500/50 text-indigo-300',
  };
  return (
    <div
      title={tooltip}
      className={`${small ? 'w-8 h-8 text-xs' : 'w-14 h-10 text-sm'} rounded-lg border font-bold font-mono flex items-center justify-center cursor-help transition-all hover:scale-105`}
    >
      {label}
    </div>
  );
}

function MeasureBox() {
  return (
    <div
      title='Measure: collapses superposition to 0 or 1'
      className='w-14 h-10 rounded-lg border border-emerald-700/50 bg-emerald-950/30 text-emerald-300 font-bold font-mono text-sm flex items-center justify-center cursor-help hover:scale-105 transition-all'
    >
      M
    </div>
  );
}
