from pathlib import Path

comp = Path(r'C:\Users\Omkar Shedage\quantum-intelligence-lab\frontend\src\components')
comp.mkdir(parents=True, exist_ok=True)

# 1. Navbar.tsx
navbar_code = '''import React from 'react';
import { Cpu, Atom, BookOpen, BrainCircuit, Activity, Award, PlayCircle } from 'lucide-react';

export type ActiveTab =
  | 'dashboard'
  | 'lesson'
  | 'predict'
  | 'circuit'
  | 'results'
  | 'trace'
  | 'tutor'
  | 'manim'
  | 'challenges'
  | 'mastery';

interface NavbarProps {
  activeTab: ActiveTab;
  setActiveTab: (tab: ActiveTab) => void;
  simulatorReady: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab, simulatorReady }) => {
  const navItems: { id: ActiveTab; label: string; icon: React.ReactNode }[] = [
    { id: 'dashboard', label: 'Dashboard', icon: <Activity className='w-4 h-4' /> },
    { id: 'lesson', label: '1. Lesson', icon: <BookOpen className='w-4 h-4' /> },
    { id: 'predict', label: '2. Predict', icon: <BrainCircuit className='w-4 h-4' /> },
    { id: 'circuit', label: '3. Circuit Lab', icon: <Atom className='w-4 h-4' /> },
    { id: 'results', label: '4. Compare', icon: <Cpu className='w-4 h-4' /> },
    { id: 'trace', label: '5. Trace', icon: <Activity className='w-4 h-4' /> },
    { id: 'tutor', label: '6. AI Tutor', icon: <BrainCircuit className='w-4 h-4' /> },
    { id: 'manim', label: '7. Show Me Why', icon: <PlayCircle className='w-4 h-4' /> },
    { id: 'challenges', label: '8. Challenge', icon: <Award className='w-4 h-4' /> },
    { id: 'mastery', label: 'Mastery', icon: <Award className='w-4 h-4' /> },
  ];

  return (
    <header className='border-b border-cyan-900/40 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50 px-4 py-3'>
      <div className='max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3'>
        <div className='flex items-center gap-3 cursor-pointer' onClick={() => setActiveTab('dashboard')}>
          <div className='w-9 h-9 rounded-lg bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20'>
            <Atom className='w-5 h-5 text-white animate-spin-slow' />
          </div>
          <div>
            <div className='flex items-center gap-2'>
              <span className='font-bold text-base tracking-wide text-white'>Eureka Forge</span>
              <span className='text-xs px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 font-mono'>
                SIH26140
              </span>
            </div>
            <p className='text-xs text-slate-400'>Quantum Intelligence Learning Lab</p>
          </div>
        </div>

        <nav className='flex items-center gap-1 overflow-x-auto max-w-full pb-1 md:pb-0 scrollbar-none'>
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={lex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg transition-all whitespace-nowrap }
              >
                {item.icon}
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className='hidden lg:flex items-center gap-2 text-xs font-mono'>
          <div className={w-2 h-2 rounded-full } />
          <span className='text-slate-400'>Aer Simulator:</span>
          <span className={simulatorReady ? 'text-emerald-400 font-semibold' : 'text-amber-400'}>
            {simulatorReady ? 'Online (v1.0)' : 'Offline'}
          </span>
        </div>
      </div>
    </header>
  );
};
'''
(comp / 'Navbar.tsx').write_text(navbar_code.strip() + '\n', encoding='utf-8')
print('1. Navbar.tsx written')

# 2. BlochSphere.tsx
bloch_code = '''import React from 'react';

interface BlochSphereProps {
  theta?: number;
  phi?: number;
  stateLabel?: string;
  size?: number;
}

export const BlochSphere: React.FC<BlochSphereProps> = ({
  theta = Math.PI / 2,
  phi = 0,
  stateLabel = '|psi> = (|0> + |1>)/sqrt(2)',
  size = 240,
}) => {
  const r = size * 0.42;
  const cx = size / 2;
  const cy = size / 2;

  const vx = r * Math.sin(theta) * Math.cos(phi);
  const vy = r * Math.cos(theta);
  const vz = r * Math.sin(theta) * Math.sin(phi);

  const endX = cx + vx * 0.9 - vz * 0.35;
  const endY = cy - vy * 0.85 - vz * 0.2;

  return (
    <div className='flex flex-col items-center bg-slate-900/70 border border-slate-800 rounded-xl p-4 shadow-inner'>
      <div className='text-xs font-mono uppercase tracking-wider text-cyan-400 mb-2 flex items-center justify-between w-full'>
        <span>Bloch Sphere Vector</span>
        <span className='text-slate-400'>theta: {(theta / Math.PI).toFixed(2)}pi, phi: {(phi / Math.PI).toFixed(2)}pi</span>
      </div>

      <svg width={size} height={size} className='overflow-visible select-none'>
        <defs>
          <radialGradient id='sphereGlow' cx='50%' cy='50%' r='50%'>
            <stop offset='0%' stopColor='#06b6d4' stopOpacity='0.12' />
            <stop offset='80%' stopColor='#06b6d4' stopOpacity='0.02' />
            <stop offset='100%' stopColor='#0f172a' stopOpacity='0.8' />
          </radialGradient>
          <linearGradient id='vectorGrad' x1='0%' y1='0%' x2='100%' y2='100%'>
            <stop offset='0%' stopColor='#22d3ee' />
            <stop offset='100%' stopColor='#a855f7' />
          </linearGradient>
        </defs>

        <circle cx={cx} cy={cy} r={r} fill='url(#sphereGlow)' stroke='#1e293b' strokeWidth='1.5' />

        <ellipse
          cx={cx}
          cy={cy}
          rx={r}
          ry={r * 0.28}
          fill='none'
          stroke='#334155'
          strokeWidth='1'
          strokeDasharray='3 3'
        />

        <line x1={cx} y1={cy - r - 12} x2={cx} y2={cy + r + 12} stroke='#475569' strokeWidth='1.2' />
        <line x1={cx - r - 12} y1={cy} x2={cx + r + 12} y2={cy} stroke='#334155' strokeWidth='1' strokeDasharray='2 2' />

        <text x={cx} y={cy - r - 16} textAnchor='middle' fill='#38bdf8' fontSize='11' fontFamily='monospace' fontWeight='bold'>
          |0&gt; (+Z)
        </text>
        <text x={cx} y={cy + r + 24} textAnchor='middle' fill='#cbd5e1' fontSize='11' fontFamily='monospace'>
          |1&gt; (-Z)
        </text>
        <text x={cx + r + 16} y={cy + 4} textAnchor='start' fill='#a855f7' fontSize='10' fontFamily='monospace'>
          |+&gt; (+X)
        </text>

        <line
          x1={cx}
          y1={cy}
          x2={endX}
          y2={endY}
          stroke='url(#vectorGrad)'
          strokeWidth='3'
          strokeLinecap='round'
        />
        <circle cx={endX} cy={endY} r='4' fill='#22d3ee' className='animate-pulse' />
        <circle cx={cx} cy={cy} r='2.5' fill='#94a3b8' />
      </svg>

      <div className='mt-3 text-center'>
        <span className='inline-block px-3 py-1 rounded-full bg-cyan-950/70 border border-cyan-800/80 text-cyan-300 text-xs font-mono font-medium'>
          {stateLabel}
        </span>
      </div>
    </div>
  );
};
'''
(comp / 'BlochSphere.tsx').write_text(bloch_code.strip() + '\n', encoding='utf-8')
print('2. BlochSphere.tsx written')

# 3. Histogram.tsx
hist_code = '''import React from 'react';
import { OutcomeComparison } from '../types/quantum';
import { CheckCircle2, XCircle } from 'lucide-react';

interface HistogramProps {
  probabilities: Record<string, number>;
  predicted?: Record<string, number> | null;
  outcomes?: OutcomeComparison[] | null;
  overallMatch?: boolean | null;
  shots?: number;
}

export const Histogram: React.FC<HistogramProps> = ({
  probabilities,
  predicted,
  outcomes,
  overallMatch,
  shots = 1024,
}) => {
  const allKeys = Array.from(new Set([...Object.keys(probabilities), ...(predicted ? Object.keys(predicted) : [])])).sort();

  return (
    <div className='bg-slate-900/80 border border-slate-800 rounded-xl p-5 shadow-lg'>
      <div className='flex items-center justify-between mb-4 pb-3 border-b border-slate-800'>
        <div>
          <h3 className='text-sm font-semibold text-slate-100 flex items-center gap-2'>
            Measurement Probability Distribution
          </h3>
          <p className='text-xs text-slate-400 font-mono'>Qiskit Aer Simulator ({shots} shots)</p>
        </div>

        {overallMatch !== undefined && overallMatch !== null && (
          <div
            className={lex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border }
          >
            {overallMatch ? <CheckCircle2 className='w-3.5 h-3.5 text-emerald-400' /> : <XCircle className='w-3.5 h-3.5 text-rose-400' />}
            <span>{overallMatch ? 'MATCH' : 'MISMATCH'}</span>
          </div>
        )}
      </div>

      <div className='flex items-center gap-4 text-xs mb-4 text-slate-400'>
        <div className='flex items-center gap-1.5'>
          <div className='w-3 h-3 rounded bg-cyan-500' />
          <span>Simulated Result</span>
        </div>
        {predicted && (
          <div className='flex items-center gap-1.5'>
            <div className='w-3 h-3 rounded bg-indigo-500 border border-indigo-300' />
            <span>Your Prediction</span>
          </div>
        )}
      </div>

      <div className='space-y-4'>
        {allKeys.length === 0 ? (
          <p className='text-xs text-slate-500 text-center py-6'>No simulation results yet. Run the circuit to inspect probabilities.</p>
        ) : (
          allKeys.map((key) => {
            const simP = probabilities[key] || 0.0;
            const predP = predicted ? predicted[key] || 0.0 : null;
            const outcomeData = outcomes?.find((o) => o.outcome === key);

            return (
              <div key={key} className='space-y-1.5'>
                <div className='flex items-center justify-between text-xs font-mono'>
                  <span className='font-bold text-slate-200 text-sm'>|{key}&gt;</span>
                  <div className='flex items-center gap-3'>
                    {predP !== null && (
                      <span className='text-indigo-300'>
                        Pred: {(predP * 100).toFixed(1)}%
                      </span>
                    )}
                    <span className='text-cyan-400 font-bold'>
                      Sim: {(simP * 100).toFixed(1)}%
                    </span>
                    {outcomeData && (
                      <span
                        className={	ext-[10px] px-1.5 py-0.5 rounded }
                      >
                        Delta {outcomeData.delta > 0 ? '+' : ''}{(outcomeData.delta * 100).toFixed(1)}%
                      </span>
                    )}
                  </div>
                </div>

                <div className='relative h-6 bg-slate-950 rounded-lg overflow-hidden border border-slate-800 flex items-center p-1'>
                  <div
                    className='h-full bg-gradient-to-r from-cyan-600 to-cyan-400 rounded transition-all duration-700'
                    style={{ width: ${Math.max(simP * 100, 2)}% }}
                  />
                  {predP !== null && (
                    <div
                      className='absolute top-0 bottom-0 w-1 bg-indigo-300 shadow-sm shadow-indigo-300 z-10'
                      style={{ left: ${Math.min(Math.max(predP * 100, 1), 99)}% }}
                      title={Predicted: %}
                    />
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
'''
(comp / 'Histogram.tsx').write_text(hist_code.strip() + '\n', encoding='utf-8')
print('3. Histogram.tsx written')
