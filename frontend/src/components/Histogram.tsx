import React from 'react';
import { SimulationResult } from '../types/quantum';

interface Props {
  result: SimulationResult;
  prediction?: { zero: number; one: number };
}

export const Histogram: React.FC<Props> = ({ result, prediction }) => {
  const outcomes = Object.keys(result.probabilities).sort();
  const maxProb = Math.max(...Object.values(result.probabilities), 0.01);

  return (
    <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5'>
      {/* Header */}
      <div className='flex items-center justify-between'>
        <div>
          <h3 className='text-sm font-bold text-white'>Measurement Histogram</h3>
          <p className='text-xs text-slate-400 font-mono'>
            {result.num_shots.toLocaleString()} shots · Qiskit Aer ({result.concept})
          </p>
        </div>
        <div className='text-xs font-mono text-slate-500'>
          {result.execution_time_ms.toFixed(1)} ms
        </div>
      </div>

      {/* Bars */}
      <div className='flex items-end gap-4 h-48 pt-4'>
        {outcomes.map((outcome) => {
          const prob = result.probabilities[outcome] ?? 0;
          const count = result.counts[outcome] ?? 0;
          const heightPct = (prob / maxProb) * 100;

          /* Prediction bar for this outcome */
          const predProb = outcome === '0'
            ? (prediction?.zero ?? 0) / 100
            : (prediction?.one ?? 0) / 100;
          const predHeight = (predProb / maxProb) * 100;

          return (
            <div key={outcome} className='flex-1 flex flex-col items-center gap-2'>
              {/* Bars side by side */}
              <div className='w-full flex items-end gap-1 h-36'>
                {/* Simulator bar */}
                <div className='flex-1 flex flex-col justify-end'>
                  <div
                    className='rounded-t-lg bg-gradient-to-t from-cyan-700 to-cyan-400 transition-all duration-700 relative group'
                    style={{ height:  `${heightPct}%`, minHeight: '4px' }}
                  >
                    <div className='absolute -top-6 left-1/2 -translate-x-1/2 text-[10px] font-mono text-cyan-300 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity'>
                      {(prob * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>
                {/* Prediction bar */}
                {prediction && (
                  <div className='flex-1 flex flex-col justify-end'>
                    <div
                      className='rounded-t-lg bg-gradient-to-t from-indigo-800 to-indigo-500 opacity-60 transition-all duration-700 border border-dashed border-indigo-400/60'
                      style={{ height:  `${predHeight}%`, minHeight: '4px' }}
                    />
                  </div>
                )}
              </div>

              {/* Outcome label */}
              <div className='text-center space-y-0.5'>
                <div className='text-xs font-mono font-bold text-slate-200'>|{outcome}⟩</div>
                <div className='text-[10px] font-mono text-cyan-300'>{(prob * 100).toFixed(1)}%</div>
                <div className='text-[10px] font-mono text-slate-500'>{count} counts</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Legend */}
      {prediction && (
        <div className='flex items-center gap-4 text-[11px] font-mono text-slate-400 pt-2 border-t border-slate-800'>
          <div className='flex items-center gap-1.5'>
            <div className='w-3 h-3 rounded-sm bg-cyan-500' />
            Simulator (Aer)
          </div>
          <div className='flex items-center gap-1.5'>
            <div className='w-3 h-3 rounded-sm bg-indigo-500 opacity-60 border border-dashed border-indigo-400/60' />
            Your Prediction
          </div>
        </div>
      )}
    </div>
  );
};
