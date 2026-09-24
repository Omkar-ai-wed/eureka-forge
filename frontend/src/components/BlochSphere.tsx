import React, { useEffect, useRef } from 'react';
import { SimulationResult } from '../types/quantum';

interface Props {
  result: SimulationResult;
}

export const BlochSphere: React.FC<Props> = ({ result }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  /* Derive polar angles from probabilities */
  const p0 = result.probabilities['0'] ?? 0.5;
  const theta = Math.acos(2 * p0 - 1); // [0, pi]
  const phi = 0; // azimuthal angle (assume real amplitudes)

  /* Bloch coords */
  const bx = Math.sin(theta) * Math.cos(phi);
  const by = Math.sin(theta) * Math.sin(phi);
  const bz = Math.cos(theta);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const W = canvas.width;
    const H = canvas.height;
    const cx = W / 2;
    const cy = H / 2;
    const R = Math.min(W, H) * 0.38;

    ctx.clearRect(0, 0, W, H);

    /* Sphere outline */
    ctx.strokeStyle = 'rgba(100, 116, 139, 0.4)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.stroke();

    /* Equator ellipse */
    ctx.beginPath();
    ctx.ellipse(cx, cy, R, R * 0.3, 0, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(100, 116, 139, 0.25)';
    ctx.stroke();

    /* Axes */
    const axes = [
      { dx: 0, dy: -1, label: '|0⟩', color: '#06b6d4' },
      { dx: 0, dy: 1, label: '|1⟩', color: '#6366f1' },
      { dx: 1, dy: 0, label: '+x', color: 'rgba(100,116,139,0.5)' },
      { dx: -1, dy: 0, label: '-x', color: 'rgba(100,116,139,0.3)' },
    ];

    axes.forEach(({ dx, dy, label, color }) => {
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.lineWidth = 1;
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + dx * R * 1.15, cy + dy * R * 1.15);
      ctx.stroke();
      ctx.fillStyle = color;
      ctx.font = '11px monospace';
      ctx.fillText(label, cx + dx * R * 1.22, cy + dy * R * 1.22);
    });

    /* State vector */
    /* Project 3D Bloch onto 2D canvas: x→screen-x, z→screen-y (upward) */
    const svX = cx + bx * R;
    const svY = cy - bz * R;

    /* Glow */
    const grad = ctx.createRadialGradient(svX, svY, 0, svX, svY, 18);
    grad.addColorStop(0, 'rgba(6,182,212,0.5)');
    grad.addColorStop(1, 'rgba(6,182,212,0)');
    ctx.beginPath();
    ctx.arc(svX, svY, 18, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();

    /* Arrow shaft */
    ctx.beginPath();
    ctx.strokeStyle = '#06b6d4';
    ctx.lineWidth = 2.5;
    ctx.moveTo(cx, cy);
    ctx.lineTo(svX, svY);
    ctx.stroke();

    /* Arrowhead */
    const angle = Math.atan2(svY - cy, svX - cx);
    ctx.beginPath();
    ctx.fillStyle = '#06b6d4';
    ctx.moveTo(svX, svY);
    ctx.lineTo(svX - 10 * Math.cos(angle - 0.4), svY - 10 * Math.sin(angle - 0.4));
    ctx.lineTo(svX - 10 * Math.cos(angle + 0.4), svY - 10 * Math.sin(angle + 0.4));
    ctx.closePath();
    ctx.fill();

    /* Dot at tip */
    ctx.beginPath();
    ctx.arc(svX, svY, 5, 0, Math.PI * 2);
    ctx.fillStyle = '#e2e8f0';
    ctx.fill();
  }, [bx, bz]);

  return (
    <div className='bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4'>
      <div className='flex items-center justify-between'>
        <div>
          <h3 className='text-sm font-bold text-white'>Bloch Sphere</h3>
          <p className='text-xs text-slate-400 font-mono'>Statevector visualisation</p>
        </div>
        <div className='text-right text-xs font-mono space-y-0.5'>
          <div className='text-cyan-300'>|0⟩: {(p0 * 100).toFixed(1)}%</div>
          <div className='text-indigo-300'>|1⟩: {((1 - p0) * 100).toFixed(1)}%</div>
        </div>
      </div>

      <div className='flex justify-center'>
        <canvas
          ref={canvasRef}
          width={280}
          height={280}
          className='rounded-xl bg-slate-950/60'
        />
      </div>

      <div className='grid grid-cols-3 gap-2 text-xs font-mono'>
        {[
          { label: 'bx', val: bx },
          { label: 'by', val: by },
          { label: 'bz', val: bz },
        ].map(({ label, val }) => (
          <div key={label} className='p-2 rounded-lg bg-slate-950 border border-slate-800 text-center'>
            <div className='text-slate-500 text-[10px]'>{label}</div>
            <div className='text-slate-200 font-bold'>{val.toFixed(3)}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
