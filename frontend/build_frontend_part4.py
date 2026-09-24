from pathlib import Path

comp = Path(r'C:\Users\Omkar Shedage\quantum-intelligence-lab\frontend\src\components')

# 1. TraceViewer.tsx
trace_code = '''import React from 'react';
import { TraceStep } from '../types/quantum';
import { Activity, ArrowDown, ChevronRight, Layers } from 'lucide-react';

interface TraceViewerProps {
  trace: TraceStep[];
}

export const TraceViewer: React.FC<TraceViewerProps> = ({ trace }) => {
  return (
    <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6'>
      <div className='flex items-center justify-between pb-4 border-b border-slate-800'>
        <div className='flex items-center gap-3'>
          <div className='w-8 h-8 rounded-lg bg-emerald-600/30 border border-emerald-500/40 flex items-center justify-center'>
            <Layers className='w-4 h-4 text-emerald-400' />
          </div>
          <div>
            <h3 className='text-sm font-bold text-white'>Step-by-Step Quantum Execution Trace</h3>
            <p className='text-xs text-slate-400 font-mono'>
              Structured statevector evolution generated directly by Qiskit Aer.
            </p>
          </div>
        </div>
        <span className='text-xs px-2.5 py-1 rounded bg-slate-800 text-emerald-400 font-mono'>
          {trace.length} Execution Steps
        </span>
      </div>

      <div className='space-y-3 relative'>
        {trace.length === 0 ? (
          <p className='text-xs text-slate-500 py-6 text-center'>
            Run a simulation to generate the deterministic step-by-step state trace.
          </p>
        ) : (
          trace.map((step, idx) => (
            <div key={idx} className='flex items-start gap-4 group'>
              {/* Step indicator */}
              <div className='flex flex-col items-center'>
                <div className='w-7 h-7 rounded-full bg-slate-950 border border-cyan-500/60 text-cyan-300 font-mono text-xs flex items-center justify-center font-bold shadow-sm shadow-cyan-950'>
                  {step.step}
                </div>
                {idx < trace.length - 1 && <div className='w-0.5 h-10 bg-slate-800 my-1' />}
              </div>

              {/* Event card */}
              <div className='flex-1 p-3.5 bg-slate-950/80 rounded-xl border border-slate-800 group-hover:border-cyan-900/80 transition-all flex items-center justify-between'>
                <div>
                  <div className='flex items-center gap-2'>
                    <span className='font-mono font-semibold text-xs text-slate-200'>{step.event}</span>
                  </div>
                  {step.state_label && (
                    <div className='mt-1 text-xs font-mono text-cyan-400'>
                      State: <span className='text-cyan-300 font-bold'>{step.state_label}</span>
                    </div>
                  )}
                </div>

                <div className='text-[10px] font-mono text-slate-500 bg-slate-900 px-2 py-1 rounded border border-slate-800'>
                  Step {step.step + 1} of {trace.length}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
'''
(comp / 'TraceViewer.tsx').write_text(trace_code.strip() + '\n', encoding='utf-8')
print('7. TraceViewer.tsx written')

# 2. ChallengeView.tsx
chal_code = '''import React, { useState, useEffect } from 'react';
import { Challenge, ChallengeResult, CanonicalCircuit } from '../types/quantum';
import { getChallenges, submitChallenge } from '../lib/api';
import { Award, CheckCircle2, XCircle, Sparkles, Send, RefreshCw } from 'lucide-react';

interface ChallengeViewProps {
  currentCircuit: CanonicalCircuit;
  onRefreshMastery?: () => void;
}

export const ChallengeView: React.FC<ChallengeViewProps> = ({ currentCircuit, onRefreshMastery }) => {
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [selectedId, setSelectedId] = useState<string>('challenge-superposition');
  const [pred0, setPred0] = useState<number>(50);
  const [selectedOpt, setSelectedOpt] = useState<number>(0);
  const [result, setResult] = useState<ChallengeResult | null>(null);
  const [submitting, setSubmitting] = useState<boolean>(false);

  useEffect(() => {
    async function load() {
      try {
        const list = await getChallenges();
        setChallenges(list);
      } catch (err) {
        console.error('Failed to load challenges:', err);
      }
    }
    load();
  }, []);

  const currentChallenge = challenges.find((c) => c.id === selectedId) || challenges[0];

  const handleSubmit = async () => {
    if (!currentChallenge) return;
    setSubmitting(true);
    try {
      let submission: any = { challenge_id: currentChallenge.id };
      if (currentChallenge.type === 'prediction') {
        submission.prediction = {
          '0': pred0 / 100,
          '1': (100 - pred0) / 100,
        };
      } else if (currentChallenge.type === 'construction') {
        submission.circuit = currentCircuit;
      } else if (currentChallenge.type === 'diagnosis') {
        submission.selected_option_index = selectedOpt;
      }

      const res = await submitChallenge(submission);
      setResult(res);
      if (onRefreshMastery) onRefreshMastery();
    } catch (err) {
      console.error('Challenge submission error:', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6'>
      <div className='flex items-center justify-between pb-4 border-b border-slate-800 flex-wrap gap-3'>
        <div className='flex items-center gap-3'>
          <div className='w-8 h-8 rounded-lg bg-amber-600/30 border border-amber-500/40 flex items-center justify-center'>
            <Award className='w-4 h-4 text-amber-400' />
          </div>
          <div>
            <h3 className='text-sm font-bold text-white'>Graded Mastery Challenges</h3>
            <p className='text-xs text-slate-400 font-mono'>
              Deterministic grading engine. Simulator calculates results; LLM does not assign scores.
            </p>
          </div>
        </div>

        {/* Challenge selector tabs */}
        <div className='flex items-center gap-1.5 flex-wrap'>
          {challenges.map((c) => (
            <button
              key={c.id}
              onClick={() => {
                setSelectedId(c.id);
                setResult(null);
              }}
              className={px-3 py-1.5 rounded-lg text-xs font-medium transition-all }
            >
              {c.title.split(':')[0]}
            </button>
          ))}
        </div>
      </div>

      {currentChallenge && (
        <div className='space-y-6'>
          <div className='p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-3'>
            <div className='flex items-center justify-between text-xs font-mono text-slate-400'>
              <span className='text-amber-400 font-bold'>{currentChallenge.title}</span>
              <span className='px-2 py-0.5 rounded bg-slate-800 text-slate-300'>
                {currentChallenge.difficulty} - {currentChallenge.concept}
              </span>
            </div>
            <p className='text-xs text-slate-200 leading-relaxed font-sans'>
              {currentChallenge.prompt}
            </p>
          </div>

          {/* Interactive input based on challenge type */}
          {currentChallenge.type === 'prediction' && (
            <div className='p-5 bg-slate-950/70 border border-slate-800 rounded-xl space-y-4'>
              <div className='flex items-center justify-between text-xs font-mono'>
                <span>|0&gt; Probability: <strong className='text-cyan-400'>{pred0}%</strong></span>
                <span>|1&gt; Probability: <strong className='text-indigo-400'>{100 - pred0}%</strong></span>
              </div>
              <input
                type='range'
                min='0'
                max='100'
                value={pred0}
                onChange={(e) => setPred0(Number(e.target.value))}
                className='w-full accent-cyan-400 cursor-pointer'
              />
            </div>
          )}

          {currentChallenge.type === 'construction' && (
            <div className='p-4 bg-slate-950/70 border border-slate-800 rounded-xl text-xs space-y-2'>
              <div className='flex items-center justify-between text-slate-400'>
                <span>Current Circuit in Lab:</span>
                <span className='font-mono text-cyan-400'>{currentCircuit.gates.length} Gate(s)</span>
              </div>
              <p className='text-slate-300'>
                Switch to the <strong>Circuit Lab</strong> tab to assemble your circuit (e.g. H on q0, CX q0-&gt;q1), then click <strong>Submit Circuit for Evaluation</strong> below.
              </p>
            </div>
          )}

          {currentChallenge.type === 'diagnosis' && (
            <div className='space-y-2'>
              {currentChallenge.options?.map((opt, i) => (
                <label
                  key={i}
                  className={lex items-start gap-3 p-3.5 rounded-xl border text-xs cursor-pointer transition-all }
                >
                  <input
                    type='radio'
                    name='diagnosis_option'
                    checked={selectedOpt === i}
                    onChange={() => setSelectedOpt(i)}
                    className='mt-0.5 accent-amber-500'
                  />
                  <span>{opt}</span>
                </label>
              ))}
            </div>
          )}

          {/* Submit CTA */}
          <div className='flex items-center justify-between'>
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className='px-6 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-xs transition-all shadow-md shadow-amber-500/20 flex items-center gap-2 disabled:opacity-50'
            >
              {submitting ? <RefreshCw className='w-4 h-4 animate-spin' /> : <Send className='w-4 h-4' />}
              <span>{submitting ? 'Grading on Aer Simulator...' : 'Submit Challenge Solution'}</span>
            </button>
          </div>

          {/* Graded Result Card */}
          {result && (
            <div
              className={p-5 rounded-xl border space-y-2 }
            >
              <div className='flex items-center justify-between text-xs font-bold font-mono'>
                <div className='flex items-center gap-2'>
                  {result.passed ? <CheckCircle2 className='w-4 h-4 text-emerald-400' /> : <XCircle className='w-4 h-4 text-rose-400' />}
                  <span>{result.passed ? 'CHALLENGE PASSED!' : 'TRY AGAIN'}</span>
                </div>
                <span>Deterministic Score: {(result.score * 100).toFixed(0)}%</span>
              </div>
              <p className='text-xs leading-relaxed'>{result.feedback}</p>
              <div className='pt-2 text-[11px] text-slate-400 border-t border-slate-800/60'>
                Next Step: <span className='text-slate-200 font-semibold'>{result.next_recommendation}</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
'''
(comp / 'ChallengeView.tsx').write_text(chal_code.strip() + '\n', encoding='utf-8')
print('8. ChallengeView.tsx written')

# 3. MasteryView.tsx
mast_code = '''import React, { useState, useEffect } from 'react';
import { UserMasteryProfile } from '../types/quantum';
import { getMasteryProfile } from '../lib/api';
import { Award, CheckCircle, Flame, Target } from 'lucide-react';

interface MasteryViewProps {
  onStartLesson?: () => void;
}

export const MasteryView: React.FC<MasteryViewProps> = ({ onStartLesson }) => {
  const [profile, setProfile] = useState<UserMasteryProfile | null>(null);

  const load = async () => {
    try {
      const data = await getMasteryProfile();
      setProfile(data);
    } catch (err) {
      console.error('Failed to load mastery profile:', err);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6'>
      <div className='flex items-center justify-between pb-4 border-b border-slate-800 flex-wrap gap-3'>
        <div className='flex items-center gap-3'>
          <div className='w-8 h-8 rounded-lg bg-cyan-600/30 border border-cyan-500/40 flex items-center justify-center'>
            <Award className='w-4 h-4 text-cyan-400' />
          </div>
          <div>
            <h3 className='text-sm font-bold text-white'>Quantum Foundations Mastery</h3>
            <p className='text-xs text-slate-400 font-mono'>
              Deterministic skill accumulation across core gate-model concepts.
            </p>
          </div>
        </div>

        {profile && (
          <div className='flex items-center gap-3'>
            <div className='text-right'>
              <span className='text-[10px] text-slate-400 block font-mono'>OVERALL COMPLETION</span>
              <span className='text-sm font-bold text-cyan-400 font-mono'>
                {(profile.overall_progress * 100).toFixed(0)}%
              </span>
            </div>
            <div className='w-16 h-2 bg-slate-800 rounded-full overflow-hidden'>
              <div
                className='h-full bg-cyan-400 rounded-full'
                style={{ width: ${profile.overall_progress * 100}% }}
              />
            </div>
          </div>
        )}
      </div>

      {profile && (
        <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
          {Object.entries(profile.concepts).map(([conceptName, cm]) => {
            const badgeColor =
              cm.level === 'Mastered'
                ? 'bg-emerald-950 text-emerald-400 border-emerald-800'
                : cm.level === 'Practicing'
                ? 'bg-amber-950 text-amber-400 border-amber-800'
                : 'bg-cyan-950 text-cyan-400 border-cyan-800';

            return (
              <div
                key={conceptName}
                className='p-4 bg-slate-950/70 border border-slate-800 rounded-xl space-y-3'
              >
                <div className='flex items-center justify-between'>
                  <span className='capitalize font-bold text-slate-200 text-xs font-mono'>
                    {conceptName}
                  </span>
                  <span className={	ext-[10px] px-2 py-0.5 rounded border font-mono }>
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
                      className='h-full bg-gradient-to-r from-cyan-500 to-indigo-500 rounded-full'
                      style={{ width: ${cm.score * 100}% }}
                    />
                  </div>
                </div>

                <div className='flex items-center justify-between text-[10px] font-mono text-slate-500 pt-1'>
                  <span>Attempts: {cm.attempts}</span>
                  <span>Accuracy: {cm.attempts > 0 ? ((cm.correct / cm.attempts) * 100).toFixed(0) : 0}%</span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
'''
(comp / 'MasteryView.tsx').write_text(mast_code.strip() + '\n', encoding='utf-8')
print('9. MasteryView.tsx written')
