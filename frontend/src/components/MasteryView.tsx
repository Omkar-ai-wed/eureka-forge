import React from 'react';
import { MasteryMap, ConceptName, ConceptMastery } from '../types/quantum';
import { Award, Layers } from 'lucide-react';

interface Props {
  mastery: MasteryMap | null;
}

const CONCEPTS: ConceptName[] = ['superposition', 'measurement', 'entanglement'];

const levelColor = (level: string) => {
  if (level === 'Mastered') return 'text-emerald-400 border-emerald-700/50 bg-emerald-950/30';
  if (level === 'Practicing') return 'text-cyan-400 border-cyan-700/50 bg-cyan-950/30';
  return 'text-slate-400 border-slate-700 bg-slate-900/30';
};

export const MasteryView: React.FC<Props> = ({ mastery }) => {
  const overallScore = mastery
    ? Object.values(mastery).reduce((s, m) => s + m.score, 0) / Math.max(Object.values(mastery).length, 1)
    : 0;

  return (
    <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6'>
      {/* Header */}
      <div className='flex items-center justify-between pb-4 border-b border-slate-800'>
        <div className='flex items-center gap-3'>
          <div className='w-8 h-8 rounded-lg bg-violet-600/30 border border-violet-500/40 flex items-center justify-center'>
            <Award className='w-4 h-4 text-violet-400' />
          </div>
          <div>
            <h3 className='text-sm font-bold text-white'>Mastery Map</h3>
            <p className='text-xs text-slate-400 font-mono'>
              Computed from deterministic challenge grades.
            </p>
          </div>
        </div>
        <div className='text-right'>
          <div className='text-xs text-slate-500 font-mono'>Overall Progress</div>
          <div className='text-xl font-bold text-white font-mono'>{(overallScore * 100).toFixed(0)}%</div>
        </div>
      </div>

      {/* Overall bar */}
      <div className='space-y-2'>
        <div className='h-3 bg-slate-900 rounded-full overflow-hidden border border-slate-800'>
          <div
            className='h-full bg-gradient-to-r from-violet-600 to-cyan-500 rounded-full transition-all duration-700'
            style={{ width:  `${overallScore * 100}%` }}
          />
        </div>
      </div>

      {/* Per-concept cards */}
      {!mastery ? (
        <div className='text-center py-8 text-slate-500 font-mono text-sm flex flex-col items-center gap-3'>
          <Layers className='w-8 h-8 text-slate-700' />
          Complete challenges to populate your mastery map.
        </div>
      ) : (
        <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
          {CONCEPTS.map((conceptName) => {
            const cm: ConceptMastery = mastery[conceptName] || {
              concept: conceptName,
              score: 0,
              level: 'Learning',
              attempts: 0,
              correct: 0,
            };
            return (
              <div key={conceptName} className={`p-5 rounded-2xl border space-y-3 ${levelColor(cm.level)}`}>
                <div className='flex items-center justify-between'>
                  <span className='capitalize font-bold text-slate-200 text-sm font-mono'>
                    {conceptName}
                  </span>
                  <span className="text-[10px] px-2 py-0.5 rounded border font-mono">
                    {cm.level}
                  </span>
                </div>

                <div className='space-y-1.5'>
                  <div className='flex items-center justify-between text-[11px] font-mono text-slate-400'>
                    <span>Score</span>
                    <span className='text-cyan-300 font-bold'>{(cm.score * 100).toFixed(0)}%</span>
                  </div>
                  <div className='h-2 bg-slate-900 rounded-full overflow-hidden border border-slate-800'>
                    <div
                      className='h-full bg-gradient-to-r from-cyan-500 to-indigo-500 rounded-full transition-all duration-700'
                      style={{ width:  `${cm.score * 100}%` }}
                    />
                  </div>
                </div>

                <div className='flex items-center justify-between text-[10px] font-mono text-slate-500 pt-1'>
                  <span>Attempts: {cm.attempts}</span>
                  <span>
                    Accuracy: {cm.attempts > 0 ? ((cm.correct / cm.attempts) * 100).toFixed(0) : 0}%
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
