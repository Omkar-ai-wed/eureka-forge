import React from 'react';
import { SimulationResult, TutorResponse } from '../types/quantum';
import { BrainCircuit, Sparkles, HelpCircle, Send } from 'lucide-react';

interface Props {
  simResult: SimulationResult | null;
  tutorResponse: TutorResponse | null;
  loading: boolean;
  onAsk: (question: string) => void;
  question: string;
  setQuestion: (q: string) => void;
}

export const AITutorPanel: React.FC<Props> = ({
  simResult,
  tutorResponse,
  loading,
  onAsk,
  question,
  setQuestion,
}) => {
  const quickQs = [
    'Why is the distribution 50/50?',
    'What does the Hadamard gate do?',
    'Can entanglement send information faster than light?',
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;
    onAsk(question);
  };

  if (!simResult) {
    return (
      <div className='bg-slate-900/80 border border-slate-800 rounded-2xl p-8 text-center space-y-3'>
        <HelpCircle className='w-8 h-8 text-slate-600 mx-auto' />
        <p className='text-slate-400 text-sm'>Run a simulation first to enable the AI Tutor.</p>
      </div>
    );
  }

  return (
    <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5'>
      {/* Header */}
      <div className='flex items-center gap-3 pb-4 border-b border-slate-800'>
        <div className='w-8 h-8 rounded-lg bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center'>
          <BrainCircuit className='w-4 h-4 text-indigo-400' />
        </div>
        <div>
          <h3 className='text-sm font-bold text-white'>Grounded AI Tutor</h3>
          <p className='text-xs text-slate-400 font-mono'>
            Reads simulator ground truth — never invents quantum probabilities.
          </p>
        </div>
      </div>

      {/* Ground truth strip */}
      <div className='p-3 bg-slate-950/70 border border-slate-800/80 rounded-xl flex items-center justify-between text-xs font-mono text-slate-400'>
        <span>Grounded in: Aer ({simResult.num_shots} shots) · concept: {simResult.concept}</span>
        <span className='text-cyan-300'>
          {Object.entries(simResult.probabilities)
            .map(([k, v]) => `|${k}⟩: ${(v * 100).toFixed(1)}%`)
            .join(', ')}
        </span>
      </div>

      {/* Response pane */}
      <div className='min-h-[140px] p-4 bg-slate-950 rounded-xl border border-indigo-950/60'>
        {loading ? (
          <div className='flex items-center justify-center h-32 text-indigo-300 text-xs gap-2 font-mono'>
            <Sparkles className='w-4 h-4 animate-spin' />
            <span>Consulting grounded execution trace...</span>
          </div>
        ) : tutorResponse ? (
          <div className='space-y-4 text-xs text-slate-200 leading-relaxed'>
            <p className='whitespace-pre-line'>{tutorResponse.explanation}</p>
            <div className='pt-2 border-t border-slate-800/60 space-y-1'>
              <p className='text-cyan-300 font-semibold font-mono'>{tutorResponse.key_insight}</p>
              <p className='text-slate-400'>{tutorResponse.next_step}</p>
            </div>
            {tutorResponse.suggested_actions && tutorResponse.suggested_actions.length > 0 && (
              <div className='flex items-center gap-2 flex-wrap pt-2 border-t border-slate-800/60'>
                <span className='text-slate-500 font-mono text-[11px]'>Recommended:</span>
                {tutorResponse.suggested_actions.map((act, i) => (
                  <span key={i} className='px-2 py-0.5 rounded bg-indigo-950/80 border border-indigo-800 text-indigo-300 text-[11px]'>
                    {act}
                  </span>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className='flex flex-col items-center justify-center h-32 text-slate-500 text-xs space-y-2'>
            <HelpCircle className='w-6 h-6 text-slate-600' />
            <span>Ask a question or click a quick question below.</span>
          </div>
        )}
      </div>

      {/* Quick questions */}
      <div className='flex items-center gap-2 flex-wrap'>
        {quickQs.map((q, i) => (
          <button
            key={i}
            onClick={() => { setQuestion(q); onAsk(q); }}
            className='px-2.5 py-1 rounded-full bg-slate-950 hover:bg-slate-800 border border-slate-800 text-[11px] text-slate-400 hover:text-cyan-300 transition-all text-left'
          >
            {q}
          </button>
        ))}
      </div>

      {/* Custom question form */}
      <form onSubmit={handleSubmit} className='flex items-center gap-2'>
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
