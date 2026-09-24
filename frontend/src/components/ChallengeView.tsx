import React, { useState } from 'react';
import { Challenge, SubmitAnswerResponse, SimulationResult } from '../types/quantum';
import { Award, CheckCircle2, XCircle, RefreshCw, Send } from 'lucide-react';

interface Props {
  challenges: Challenge[];
  loading: boolean;
  result: SubmitAnswerResponse | null;
  simResult: SimulationResult | null;
  onSubmit: (challengeId: string, answerId: string) => void;
  onReload: () => void;
}

export const ChallengeView: React.FC<Props> = ({
  challenges,
  loading,
  result,
  simResult,
  onSubmit,
  onReload,
}) => {
  const [selectedChallenge, setSelectedChallenge] = useState<string>('');
  const [selectedOption, setSelectedOption] = useState<string>('');

  const currentChallenge = challenges.find((c) => c.id === selectedChallenge) || challenges[0];

  const handleSubmit = () => {
    if (!currentChallenge || !selectedOption) return;
    onSubmit(currentChallenge.id, selectedOption);
  };

  if (loading) {
    return (
      <div className='flex items-center gap-3 p-6 bg-slate-900/80 border border-slate-800 rounded-2xl'>
        <RefreshCw className='w-5 h-5 text-amber-400 animate-spin' />
        <span className='text-slate-300 font-mono text-sm'>Loading challenges...</span>
      </div>
    );
  }

  if (!simResult) {
    return (
      <div className='bg-slate-900/80 border border-slate-800 rounded-2xl p-8 text-center space-y-3'>
        <Award className='w-8 h-8 text-slate-600 mx-auto' />
        <p className='text-slate-400 text-sm'>Run a simulation first to unlock challenges.</p>
      </div>
    );
  }

  return (
    <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6'>
      {/* Header */}
      <div className='flex items-center justify-between pb-4 border-b border-slate-800'>
        <div className='flex items-center gap-3'>
          <div className='w-8 h-8 rounded-lg bg-amber-600/30 border border-amber-500/40 flex items-center justify-center'>
            <Award className='w-4 h-4 text-amber-400' />
          </div>
          <div>
            <h3 className='text-sm font-bold text-white'>Graded Mastery Challenges</h3>
            <p className='text-xs text-slate-400 font-mono'>
              Deterministic grading. Simulator truth, not LLM guesses.
            </p>
          </div>
        </div>
        <button
          onClick={onReload}
          className='flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-slate-300 hover:text-white transition-all'
        >
          <RefreshCw className='w-3.5 h-3.5' />
          Reload
        </button>
      </div>

      {challenges.length === 0 ? (
        <div className='text-center py-8 text-slate-500 font-mono text-sm'>
          No challenges loaded.{' '}
          <button onClick={onReload} className='text-amber-400 underline'>Reload</button>
        </div>
      ) : (
        <div className='space-y-5'>
          {/* Challenge selector */}
          <div className='flex gap-2 flex-wrap'>
            {challenges.map((c) => (
              <button
                key={c.id}
                onClick={() => { setSelectedChallenge(c.id); setSelectedOption(''); }}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all border ${
                  (selectedChallenge === c.id || (!selectedChallenge && challenges[0]?.id === c.id))
                    ? 'bg-amber-600/20 border-amber-500/60 text-amber-300'
                    : 'bg-slate-900 border-slate-700 text-slate-400 hover:border-slate-600'
                }`}
              >
                {c.title}
              </button>
            ))}
          </div>

          {/* Current challenge */}
          {currentChallenge && (
            <div className='space-y-4'>
              <div className='p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2'>
                <div className='flex items-center justify-between text-xs font-mono'>
                  <span className='text-amber-400 font-bold'>{currentChallenge.title}</span>
                  <span className='px-2 py-0.5 rounded bg-slate-800 text-slate-400 capitalize'>
                    {currentChallenge.difficulty}
                  </span>
                </div>
                <p className='text-sm text-slate-200 leading-relaxed'>{currentChallenge.prompt}</p>
              </div>

              {/* Options */}
              <div className='space-y-2'>
                {currentChallenge.options.map((opt) => (
                  <label
                    key={opt.id}
                    className={`flex items-start gap-3 p-3.5 rounded-xl border text-sm cursor-pointer transition-all ${
                      selectedOption === opt.id
                        ? 'bg-amber-950/40 border-amber-500/50 text-white'
                        : 'bg-slate-950/60 border-slate-800 text-slate-300 hover:border-slate-700'
                    }`}
                  >
                    <input
                      type='radio'
                      name='challenge_option'
                      value={opt.id}
                      checked={selectedOption === opt.id}
                      onChange={() => setSelectedOption(opt.id)}
                      className='mt-0.5 accent-amber-500'
                    />
                    <span>{opt.text}</span>
                  </label>
                ))}
              </div>

              {/* Submit */}
              <button
                onClick={handleSubmit}
                disabled={!selectedOption}
                className='px-6 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-sm transition-all flex items-center gap-2 disabled:opacity-40'
              >
                <Send className='w-4 h-4' />
                Submit Answer
              </button>

              {/* Result card */}
              {result && (
                <div className={`p-5 rounded-xl border space-y-2 ${
                  result.correct
                    ? 'bg-emerald-950/30 border-emerald-700/50'
                    : 'bg-rose-950/30 border-rose-700/50'
                }`}>
                  <div className='flex items-center justify-between text-sm font-bold font-mono'>
                    <div className='flex items-center gap-2'>
                      {result.correct
                        ? <CheckCircle2 className='w-4 h-4 text-emerald-400' />
                        : <XCircle className='w-4 h-4 text-rose-400' />}
                      <span className={result.correct ? 'text-emerald-300' : 'text-rose-300'}>
                        {result.correct ? 'Correct!' : 'Not quite — try again'}
                      </span>
                    </div>
                    <span className='text-slate-400'>Score: {(result.score * 100).toFixed(0)}%</span>
                  </div>
                  <p className='text-sm text-slate-300 leading-relaxed'>{result.feedback}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
