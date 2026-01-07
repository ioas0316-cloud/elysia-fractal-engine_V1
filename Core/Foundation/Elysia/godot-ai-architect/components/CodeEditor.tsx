
import React, { useState, useMemo, useEffect, useRef } from 'react';

interface CodeEditorProps {
  fileName: string;
  content: string;
}

// --- ICONS ---
const BrainIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 0 14.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>
);
const MapIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>
);
const CodeIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
);
const MaximizeIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
);
const MinimizeIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="4 14 10 14 10 20"/><polyline points="20 10 14 10 14 4"/><line x1="14" y1="10" x2="21" y2="3"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
);

// --- CUTE ASSETS (West Continent Theme) ---
// Enhanced with animations and expression support
const ChibiBase = ({ color, hairColor, accessory, faceType = 'happy', hat = null, scale = 1, beard = false, gender = 'neutral' }: any) => {
  const [breath, setBreath] = useState(0);
  
  useEffect(() => {
    const delay = Math.random() * 1000;
    const timer = setTimeout(() => {
      const interval = setInterval(() => {
        setBreath(prev => (prev === 0 ? 1 : 0));
      }, 1500);
      return () => clearInterval(interval);
    }, delay);
    return () => clearTimeout(timer);
  }, []);

  const isFemale = gender === 'female';

  return (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-md hover:drop-shadow-xl transition-all duration-1000 ease-in-out"
         style={{ transform: `scale(${scale}) translateY(${breath * 2}px)` }}>
      
      {/* Rear Hair (Behind Head) */}
      {isFemale && (
         <path d="M20 40 Q50 5 80 40 Q95 60 85 85 Q50 95 15 85 Q5 60 20 40" fill={hairColor} />
      )}

      {/* Body Shape - Gender Distinct */}
      {isFemale ? (
        // Dress / Female shape - More defined waist and skirt
        <path d="M35 85 Q50 95 65 85 L70 60 Q50 55 30 60 Z" fill={color} />
      ) : (
        // Tunic / Male shape
        <path d="M30 90 Q50 95 70 90 L70 55 Q50 50 30 55 Z" fill={color} />
      )}
      
      {/* Head */}
      <circle cx="50" cy="40" r="28" fill="#ffe0bd" />
      
      {/* Front Hair (Bangs) */}
      {isFemale ? (
         // Female Bangs
         <path d="M22 40 Q25 15 50 15 Q75 15 78 40 Q78 55 75 45 Q65 35 50 35 Q35 35 25 45 Q22 55 22 40" fill={hairColor} />
      ) : (
         // Male Short Hair
         <path d="M20 40 Q50 0 80 40 Q85 50 80 55 Q50 10 20 55 Q15 50 20 40" fill={hairColor} />
      )}
      
      {/* Face Types */}
      <g opacity="0.9" className="transition-all duration-300">
        {faceType === 'happy' && (
          <>
            <circle cx="38" cy="40" r="3" fill="#333" />
            <circle cx="62" cy="40" r="3" fill="#333" />
            <path d="M45 52 Q50 56 55 52" stroke="#333" strokeWidth="2" fill="none" />
            <circle cx="32" cy="48" r="3" fill="#ffaaa5" opacity="0.5" />
            <circle cx="68" cy="48" r="3" fill="#ffaaa5" opacity="0.5" />
          </>
        )}
        {faceType === 'sad' && (
          <>
            <circle cx="38" cy="42" r="3" fill="#333" />
            <circle cx="62" cy="42" r="3" fill="#333" />
            <path d="M45 58 Q50 54 55 58" stroke="#333" strokeWidth="2" fill="none" />
            <path d="M35 37 Q38 34 42 37" stroke="#333" strokeWidth="1" fill="none" opacity="0.5" />
            <path d="M58 37 Q62 34 65 37" stroke="#333" strokeWidth="1" fill="none" opacity="0.5" />
          </>
        )}
        {faceType === 'angry' && (
          <>
            <line x1="35" y1="35" x2="45" y2="38" stroke="#333" strokeWidth="2" />
            <line x1="55" y1="38" x2="65" y2="35" stroke="#333" strokeWidth="2" />
            <circle cx="40" cy="42" r="2" fill="#333" />
            <circle cx="60" cy="42" r="2" fill="#333" />
            <line x1="45" y1="54" x2="55" y2="54" stroke="#333" strokeWidth="2" />
            <circle cx="35" cy="48" r="3" fill="#ef4444" opacity="0.3" />
            <circle cx="65" cy="48" r="3" fill="#ef4444" opacity="0.3" />
          </>
        )}
        {(faceType === 'shocked' || faceType === 'surprised') && (
          <>
            <circle cx="38" cy="40" r="2" fill="#333" />
            <circle cx="62" cy="40" r="2" fill="#333" />
            <circle cx="50" cy="54" r="5" fill="#333" />
            <line x1="35" y1="32" x2="40" y2="30" stroke="#333" strokeWidth="1" />
            <line x1="65" y1="32" x2="60" y2="30" stroke="#333" strokeWidth="1" />
          </>
        )}
        {faceType === 'mystic' && (
          <>
            <circle cx="38" cy="40" r="3" fill="#6d28d9" />
            <circle cx="62" cy="40" r="3" fill="#6d28d9" />
            <path d="M48 52 Q50 54 52 52" stroke="#333" strokeWidth="2" fill="none" />
          </>
        )}
        {faceType === 'mask' && (
          <>
            <rect x="25" y="38" width="50" height="20" rx="5" fill="#374151" />
            <circle cx="40" cy="44" r="3" fill="#fff" />
            <circle cx="60" cy="44" r="3" fill="#fff" />
          </>
        )}
        {faceType === 'thinking' && (
          <>
            <circle cx="38" cy="38" r="3" fill="#333" />
            <circle cx="62" cy="38" r="3" fill="#333" />
            <path d="M46 54 L54 54" stroke="#333" strokeWidth="2" />
            <text x="70" y="30" fontSize="16" fill="#fbbf24" className="animate-pulse" style={{animationDuration: '2s'}}>?</text>
          </>
        )}
        {faceType === 'working' && (
          <>
             <path d="M35 42 L45 42" stroke="#333" strokeWidth="2" />
             <path d="M55 42 L65 42" stroke="#333" strokeWidth="2" />
             <path d="M45 52 Q50 54 55 52" stroke="#333" strokeWidth="2" fill="none" />
             <path d="M72 35 Q78 40 72 48 Q66 40 72 35" fill="#60a5fa" className="animate-bounce" style={{animationDuration: '1s'}} />
          </>
        )}
        {faceType === 'idle' && (
          <>
            <circle cx="38" cy="40" r="2.5" fill="#333" />
            <circle cx="62" cy="40" r="2.5" fill="#333" />
            <path d="M45 52 Q50 53 55 52" stroke="#333" strokeWidth="1.5" fill="none" />
          </>
        )}
      </g>
      
      {beard && (
         <path d="M35 55 Q50 70 65 55 L65 60 Q50 80 35 60 Z" fill="#e5e7eb" />
      )}

      {hat}
      {accessory}
    </svg>
  );
};

type DayPhase = 'dawn' | 'day' | 'dusk' | 'night';

const DAY_PHASES: DayPhase[] = ['dawn', 'day', 'dusk', 'night'];

type Point = {
  x: number;
  y: number;
};

const phaseNarrative: Record<DayPhase, string> = {
  dawn: "새벽 기운이 Silvercrest 성채 위에 번지고 있습니다.",
  day: "남쪽 광장이 낮의 생명으로 가득합니다.",
  dusk: "해질녘, 황금 해협이 노랗게 물들고 있습니다.",
  night: "별빛 아래 방어선이 조용히 경계를 서고 있습니다."
};

const phaseIcon: Record<DayPhase, string> = {
  dawn: '🌅',
  day: '☀️',
  dusk: '🌇',
  night: '🌙'
};

const phaseTint: Record<DayPhase, { top: string; bottom: string; accent: string }> = {
  dawn: { top: 'rgba(251, 191, 36, 0.45)', bottom: 'rgba(249, 115, 22, 0.25)', accent: '#f97316' },
  day: { top: 'rgba(59, 130, 246, 0.25)', bottom: 'rgba(14, 165, 233, 0.15)', accent: '#38bdf8' },
  dusk: { top: 'rgba(236, 72, 153, 0.4)', bottom: 'rgba(107, 33, 168, 0.35)', accent: '#f472b6' },
  night: { top: 'rgba(15, 23, 42, 0.65)', bottom: 'rgba(2, 6, 23, 0.8)', accent: '#a855f7' }
};

const overlayIntensityMap: Record<DayPhase, number> = {
  dawn: 0.35,
  day: 0.15,
  dusk: 0.65,
  night: 0.9
};

const overlayPalette: Record<DayPhase, { color: string; accent: string }> = {
  dawn: { color: 'linear-gradient(180deg, rgba(255,180,80,0.65), rgba(20,20,60,0.95))', accent: '#f97316' },
  day: { color: 'linear-gradient(180deg, rgba(78, 116, 255, 0.3), rgba(15, 23, 42, 0.8))', accent: '#38bdf8' },
  dusk: { color: 'linear-gradient(180deg, rgba(255, 128, 64, 0.75), rgba(5, 7, 35, 0.95))', accent: '#f472b6' },
  night: { color: 'linear-gradient(180deg, rgba(7, 11, 32, 0.95), rgba(1, 2, 15, 0.98))', accent: '#a855f7' }
};

const celestialPalette: Record<DayPhase, { color: string; label: string }> = {
  dawn: { color: 'radial-gradient(circle at 20% 20%, #ffe58a, #f97316)', label: 'Sunrise' },
  day: { color: 'radial-gradient(circle at 30% 30%, #fff1c2, #facc15)', label: 'Sun' },
  dusk: { color: 'radial-gradient(circle at 30% 30%, #ffdfba, #f472b6)', label: 'Sunset' },
  night: { color: 'radial-gradient(circle at 30% 30%, #dbeafe, #6366f1)', label: 'Moon' }
};

const MOVE_TRAIL_MS = 1400;

const Assets = {
  // --- HUMANOIDS ---
  King: ({face}: any) => (
    <ChibiBase color="#4f46e5" hairColor="#fbbf24" faceType={face || "happy"} gender="male"
      hat={<polygon points="30,20 40,10 50,20 60,10 70,20 70,25 30,25" fill="#fbbf24" stroke="#b45309" strokeWidth="1" />} 
    />
  ),
  Queen: ({face}: any) => (
    <ChibiBase color="#db2777" hairColor="#fcd34d" faceType={face || "happy"} gender="female"
      hat={<circle cx="50" cy="15" r="5" fill="#fbbf24" />} 
    />
  ),
  Knight: ({face}: any) => (
    <ChibiBase color="#9ca3af" hairColor="#4b5563" faceType={face || "angry"} gender="male"
      hat={
        <g>
          <path d="M25 33 Q50 10 75 33 L75 40 L25 40 Z" fill="#d1d5db" stroke="#6b7280" strokeWidth="1.5"/>
          <path d="M25 40 L25 60 L35 50 L35 40 Z" fill="#d1d5db" stroke="#6b7280" />
          <path d="M75 40 L75 60 L65 50 L65 40 Z" fill="#d1d5db" stroke="#6b7280" />
          <path d="M50 10 Q60 -5 70 5" stroke="#ef4444" strokeWidth="3" fill="none" />
        </g>
      }
      accessory={<line x1="80" y1="30" x2="80" y2="80" stroke="#9ca3af" strokeWidth="4" />}
    />
  ),
  Mage: ({face}: any) => (
    <ChibiBase color="#7c3aed" hairColor="#c084fc" faceType={face || "mystic"} gender="female"
      hat={<path d="M20 30 L50 5 L80 30 Z" fill="#5b21b6" />}
      accessory={<circle cx="80" cy="50" r="5" fill="#38bdf8" className="animate-pulse" />}
    />
  ),
  Cleric: ({face}: any) => (
    <ChibiBase color="#e2e8f0" hairColor="#fde047" faceType={face || "happy"} gender="male"
      hat={<path d="M30 30 Q50 20 70 30" fill="none" stroke="#fcd34d" strokeWidth="3"/>}
      accessory={<path d="M75 40 L85 40 M80 35 L80 45" stroke="#fbbf24" strokeWidth="3" />}
    />
  ),
  Ranger: ({face}: any) => (
    <ChibiBase color="#15803d" hairColor="#78350f" faceType={face || "angry"} gender="female"
      hat={<path d="M25 35 Q50 25 75 35 L70 45 L30 45 Z" fill="#166534" />}
    />
  ),
  Merchant: ({face}: any) => (
    <ChibiBase color="#b45309" hairColor="#1f2937" faceType={face || "happy"} gender="male"
      accessory={<circle cx="25" cy="60" r="8" fill="#fbbf24" stroke="#b45309" />}
    />
  ),
  Artisan: ({face}: any) => (
    <ChibiBase color="#92400e" hairColor="#57534e" faceType={face || "sad"} gender="male"
      accessory={<rect x="70" y="50" width="10" height="20" fill="#a8a29e" transform="rotate(-20 75 60)" />}
    />
  ),
  Bandit: ({face}: any) => (
    <ChibiBase color="#374151" hairColor="#111827" faceType={face || "mask"} gender="male"
      accessory={<path d="M75 50 L85 40 L80 60" fill="#9ca3af" />}
    />
  ),
  Man: ({face}: any) => (
    <ChibiBase color="#64748b" hairColor="#334155" faceType={face || "happy"} gender="male" />
  ),
  Woman: ({face}: any) => (
    <ChibiBase color="#be185d" hairColor="#5e2a08" faceType={face || "happy"} gender="female" />
  ),
  Child: ({face}: any) => (
    <ChibiBase color="#fbbf24" hairColor="#fde047" faceType={face || "happy"} scale={0.75} gender="neutral" />
  ),
  Elder: ({face}: any) => (
    <ChibiBase color="#4b5563" hairColor="#e5e7eb" faceType={face || "sad"} beard={true} gender="male" />
  ),

  // --- RESOURCES ---
  Stone: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-md">
      <path d="M20 80 L30 50 L50 40 L80 50 L90 80 Z" fill="#9ca3af" stroke="#4b5563" strokeWidth="2" />
      <path d="M50 40 L40 60 L20 80" stroke="#4b5563" strokeWidth="1" fill="none"/>
      <path d="M50 40 L70 65 L90 80" stroke="#4b5563" strokeWidth="1" fill="none"/>
    </svg>
  ),
  Iron: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-md">
      <path d="M25 80 L35 45 L60 30 L85 50 L85 80 Z" fill="#57534e" stroke="#292524" strokeWidth="2" />
      {/* Rust veins */}
      <path d="M35 45 L50 60 L60 30" stroke="#ea580c" strokeWidth="3" fill="none" opacity="0.8" />
      <circle cx="50" cy="60" r="3" fill="#ea580c" />
      <circle cx="70" cy="50" r="4" fill="#ea580c" />
    </svg>
  ),
  BerryBush: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-sm">
      <circle cx="30" cy="60" r="15" fill="#166534" />
      <circle cx="50" cy="50" r="20" fill="#15803d" />
      <circle cx="70" cy="60" r="15" fill="#166534" />
      {/* Berries */}
      <circle cx="40" cy="50" r="3" fill="#ef4444" />
      <circle cx="50" cy="60" r="3" fill="#ef4444" />
      <circle cx="60" cy="45" r="3" fill="#ef4444" />
      <circle cx="30" cy="60" r="2" fill="#ef4444" />
      <circle cx="70" cy="60" r="2" fill="#ef4444" />
    </svg>
  ),
  FruitTree: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-md">
      <rect x="45" y="60" width="10" height="30" fill="#451a03" />
      <circle cx="50" cy="40" r="25" fill="#16a34a" />
      <circle cx="40" cy="35" r="4" fill="#ef4444" stroke="#7f1d1d" strokeWidth="1" />
      <circle cx="60" cy="40" r="4" fill="#ef4444" stroke="#7f1d1d" strokeWidth="1" />
      <circle cx="50" cy="55" r="4" fill="#ef4444" stroke="#7f1d1d" strokeWidth="1" />
      <circle cx="50" cy="25" r="4" fill="#ef4444" stroke="#7f1d1d" strokeWidth="1" />
    </svg>
  ),

  // --- STRUCTURES & ANIMALS ---
  Campfire: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-lg">
       <circle cx="50" cy="70" r="20" fill="#44403c" opacity="0.5" />
       <rect x="30" y="70" width="40" height="10" fill="#78350f" transform="rotate(10 50 75)" />
       <rect x="30" y="70" width="40" height="10" fill="#78350f" transform="rotate(-10 50 75)" />
       <path d="M50 30 Q65 50 60 70 Q50 80 40 70 Q35 50 50 30" fill="#ef4444" className="animate-pulse" style={{animationDuration: '0.8s'}} />
       <path d="M50 40 Q55 50 55 65 Q50 70 45 65 Q45 50 50 40" fill="#fbbf24" className="animate-pulse" style={{animationDuration: '0.6s', animationDelay: '0.2s'}} />
    </svg>
  ),
  Fence: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full">
       <rect x="20" y="30" width="10" height="60" fill="#78350f" />
       <rect x="70" y="30" width="10" height="60" fill="#78350f" />
       <rect x="10" y="40" width="80" height="8" fill="#92400e" />
       <rect x="10" y="60" width="80" height="8" fill="#92400e" />
    </svg>
  ),
  Hut: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-lg">
      <rect x="30" y="50" width="40" height="40" fill="#92400e" />
      <path d="M25 50 L50 25 L75 50" fill="#fcd34d" stroke="#b45309" strokeWidth="2" />
      <rect x="45" y="70" width="10" height="20" fill="#292524" />
    </svg>
  ),
  Treehouse: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-lg">
      <rect x="40" y="50" width="20" height="40" fill="#451a03" />
      <rect x="30" y="30" width="40" height="30" fill="#78350f" rx="2" />
      <path d="M25 30 L50 10 L75 30" fill="#166534" />
      <rect x="45" y="40" width="10" height="20" fill="#292524" />
      {/* Ladder */}
      <line x1="45" y1="60" x2="45" y2="90" stroke="#92400e" strokeWidth="2" />
      <line x1="55" y1="60" x2="55" y2="90" stroke="#92400e" strokeWidth="2" />
      <line x1="45" y1="70" x2="55" y2="70" stroke="#92400e" strokeWidth="2" />
      <line x1="45" y1="80" x2="55" y2="80" stroke="#92400e" strokeWidth="2" />
    </svg>
  ),
  BrickHouse: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-xl">
      <rect x="25" y="50" width="50" height="40" fill="#b91c1c" stroke="#7f1d1d" strokeWidth="2" />
      {/* Brick lines */}
      <line x1="25" y1="60" x2="75" y2="60" stroke="#7f1d1d" strokeWidth="1" />
      <line x1="25" y1="70" x2="75" y2="70" stroke="#7f1d1d" strokeWidth="1" />
      <line x1="25" y1="80" x2="75" y2="80" stroke="#7f1d1d" strokeWidth="1" />
      <path d="M20 50 L50 20 L80 50" fill="#374151" />
      <rect x="60" y="30" width="10" height="10" fill="#78350f" /> {/* Chimney */}
      <circle cx="65" cy="25" r="2" fill="#9ca3af" className="animate-ping" style={{animationDuration: '3s'}}/>
      <rect x="45" y="65" width="10" height="25" fill="#374151" />
    </svg>
  ),

  Wolf: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-md group">
      {/* Body Sitting */}
      <path d="M30 75 Q40 60 55 65 L55 90 L35 90 Z" fill="#4b5563" />
      {/* Chest/Neck */}
      <path d="M50 65 L65 40 L75 85 L50 85 Z" fill="#4b5563" />
      {/* Head */}
      <path d="M55 35 Q65 25 75 35 L85 45 L65 50 L55 45 Z" fill="#4b5563" />
      {/* Ears */}
      <path d="M60 35 L55 20 L65 30 Z" fill="#374151" />
      <path d="M70 35 L75 20 L75 30 Z" fill="#374151" />
      {/* Snout */}
      <path d="M85 45 L95 48 L85 50 Z" fill="#374151" />
      {/* Tail */}
      <path d="M30 85 Q10 70 20 50 Q30 60 35 75" fill="#6b7280" stroke="#4b5563" strokeWidth="1"/>
      {/* Legs */}
      <rect x="55" y="80" width="5" height="10" fill="#374151" />
      <rect x="65" y="80" width="5" height="10" fill="#374151" />
      <circle cx="65" cy="40" r="1.5" fill="#fff" />
    </svg>
  ),
  Deer: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-md">
      <path d="M35 85 Q50 95 65 85 L65 55 Q50 50 35 55 Z" fill="#a8a29e" /> 
      <circle cx="50" cy="45" r="18" fill="#a8a29e" /> 
      <path d="M35 20 L40 40" stroke="#78350f" strokeWidth="3" />
      <path d="M65 20 L60 40" stroke="#78350f" strokeWidth="3" />
      <path d="M35 25 L45 25" stroke="#78350f" strokeWidth="2" />
      <path d="M65 25 L55 25" stroke="#78350f" strokeWidth="2" />
      <circle cx="42" cy="45" r="2" fill="#333" /> 
      <circle cx="58" cy="45" r="2" fill="#333" /> 
      <ellipse cx="50" cy="52" rx="3" ry="2" fill="#333" />
    </svg>
  ),
  Cow: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-md">
      {/* Body */}
      <rect x="20" y="50" width="60" height="35" rx="10" fill="#fff" stroke="#000" strokeWidth="2" />
      {/* Spots */}
      <path d="M25 55 Q35 55 30 70 Q20 65 25 55" fill="#000" />
      <path d="M50 55 Q60 50 65 65 Q55 70 50 55" fill="#000" />
      <path d="M70 70 Q75 80 65 80 Q60 75 70 70" fill="#000" />
      {/* Head */}
      <path d="M65 30 L65 60 L95 60 L95 30 Z" fill="#fff" stroke="#000" strokeWidth="2" rx="5"/>
      {/* Pink Snout */}
      <rect x="67" y="48" width="26" height="10" rx="3" fill="#fca5a5" />
      <circle cx="75" cy="53" r="1.5" fill="#000" />
      <circle cx="87" cy="53" r="1.5" fill="#000" />
      {/* Horns */}
      <path d="M65 30 Q60 20 70 20" stroke="#d4d4d4" strokeWidth="3" fill="none" />
      <path d="M95 30 Q100 20 90 20" stroke="#d4d4d4" strokeWidth="3" fill="none" />
      {/* Ears */}
      <ellipse cx="62" cy="38" rx="5" ry="2" fill="#fff" stroke="#000" strokeWidth="1"/>
      <ellipse cx="98" cy="38" rx="5" ry="2" fill="#fff" stroke="#000" strokeWidth="1"/>
      {/* Legs */}
      <rect x="25" y="85" width="8" height="10" fill="#000" />
      <rect x="65" y="85" width="8" height="10" fill="#000" />
      {/* Udder */}
      <path d="M40 85 Q50 95 60 85" fill="#fca5a5" />
    </svg>
  ),
  Horse: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-md">
       <path d="M30 80 Q50 90 80 80 L80 50 Q50 40 30 50 Z" fill="#78350f" />
       <ellipse cx="40" cy="40" rx="15" ry="22" fill="#78350f" transform="rotate(-20 40 40)" />
       <path d="M45 20 Q55 30 50 60" stroke="#451a03" strokeWidth="5" fill="none" />
       <circle cx="35" cy="35" r="2" fill="#fff" />
    </svg>
  ),
  Rabbit: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-sm">
      <circle cx="50" cy="65" r="15" fill="#e5e7eb" />
      <circle cx="50" cy="50" r="12" fill="#e5e7eb" />
      <ellipse cx="45" cy="30" rx="4" ry="12" fill="#f3f4f6" stroke="#d1d5db" />
      <ellipse cx="55" cy="30" rx="4" ry="12" fill="#f3f4f6" stroke="#d1d5db" />
      <circle cx="46" cy="50" r="1.5" fill="#333" />
      <circle cx="54" cy="50" r="1.5" fill="#333" />
    </svg>
  ),
  Caravan: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-lg">
      <rect x="20" y="50" width="60" height="30" fill="#78350f" />
      <path d="M20 50 Q50 20 80 50" fill="#fef3c7" />
      <circle cx="30" cy="80" r="10" fill="#451a03" stroke="#78350f" strokeWidth="2" />
      <circle cx="70" cy="80" r="10" fill="#451a03" stroke="#78350f" strokeWidth="2" />
      <line x1="80" y1="70" x2="95" y2="70" stroke="#78350f" strokeWidth="4" />
    </svg>
  ),

  // --- ENVIRONMENT & STRUCTURES ---
  Castle: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-lg">
      <rect x="20" y="40" width="60" height="50" fill="#e5e7eb" stroke="#374151" strokeWidth="2"/>
      <path d="M20 40 L20 20 L30 30 L40 20 L50 30 L60 20 L70 30 L80 20 L80 40" fill="#ef4444"/>
      <rect x="40" y="60" width="20" height="30" fill="#374151" rx="10"/>
      <circle cx="50" cy="10" r="5" fill="#fbbf24" className="animate-bounce"/>
    </svg>
  ),
  Church: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-lg">
      <rect x="30" y="50" width="40" height="40" fill="#f3f4f6" stroke="#94a3b8" strokeWidth="2"/>
      <path d="M30 50 L50 20 L70 50" fill="#3b82f6"/>
      <rect x="45" y="70" width="10" height="20" fill="#475569"/>
      <circle cx="50" cy="35" r="6" fill="none" stroke="#fbbf24" strokeWidth="2" />
    </svg>
  ),
  Guild: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-lg">
      <rect x="25" y="45" width="50" height="45" fill="#7c3aed" stroke="#4c1d95" strokeWidth="2"/>
      <path d="M20 45 L50 25 L80 45" fill="#5b21b6"/>
      <circle cx="50" cy="35" r="5" fill="#c084fc" className="animate-pulse"/>
    </svg>
  ),
  House: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full">
      <rect x="25" y="50" width="50" height="40" fill="#fcd34d" stroke="#d97706" strokeWidth="2"/>
      <path d="M20 50 L50 20 L80 50" fill="#78350f"/>
      <rect x="40" y="65" width="20" height="25" fill="#78350f"/>
    </svg>
  ),
  Forest: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full">
      <circle cx="50" cy="40" r="30" fill="#15803d" />
      <circle cx="30" cy="60" r="25" fill="#166534" />
      <circle cx="70" cy="60" r="25" fill="#166534" />
      <rect x="45" y="70" width="10" height="20" fill="#451a03"/>
    </svg>
  ),
  River: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full bg-blue-400/20 rounded">
       <path d="M0 30 Q50 60 100 30" stroke="#60a5fa" strokeWidth="8" fill="none" strokeLinecap="round" className="animate-[pulse_3s_infinite]"/>
       <path d="M0 70 Q50 40 100 70" stroke="#60a5fa" strokeWidth="8" fill="none" strokeLinecap="round" className="animate-[pulse_4s_infinite]"/>
    </svg>
  ),
  Mountain: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full">
       <path d="M10 90 L40 30 L70 90" fill="#64748b" />
       <path d="M40 90 L70 40 L100 90" fill="#475569" />
       <path d="M40 30 L50 50 L30 50 Z" fill="#fff" opacity="0.8" />
    </svg>
  ),
  Grass: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full">
       <rect width="100" height="100" fill="#ecfccb" rx="10" />
       <path d="M20 80 L25 60 L30 80" stroke="#84cc16" strokeWidth="2" fill="none" />
       <path d="M70 85 L75 65 L80 85" stroke="#84cc16" strokeWidth="2" fill="none" />
    </svg>
  ),
  Road: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full">
       <rect width="100" height="100" fill="#d6d3d1" rx="2" />
       <path d="M10 20 Q50 10 90 20" stroke="#a8a29e" strokeWidth="2" fill="none" strokeDasharray="4 4"/>
       <path d="M10 50 Q50 60 90 50" stroke="#a8a29e" strokeWidth="2" fill="none" strokeDasharray="4 4"/>
       <path d="M10 80 Q50 70 90 80" stroke="#a8a29e" strokeWidth="2" fill="none" strokeDasharray="4 4"/>
       {/* Small pebbles */}
       <circle cx="30" cy="40" r="2" fill="#78716c" />
       <circle cx="70" cy="60" r="2" fill="#78716c" />
    </svg>
  ),
  Farm: () => (
    <svg viewBox="0 0 100 100" className="w-full h-full">
       <rect width="100" height="100" fill="#fef08a" rx="10" />
       <line x1="20" y1="20" x2="20" y2="80" stroke="#ca8a04" strokeWidth="4" strokeDasharray="5 5" />
       <line x1="50" y1="20" x2="50" y2="80" stroke="#ca8a04" strokeWidth="4" strokeDasharray="5 5" />
       <line x1="80" y1="20" x2="80" y2="80" stroke="#ca8a04" strokeWidth="4" strokeDasharray="5 5" />
    </svg>
  )
};

export const CodeEditor: React.FC<CodeEditorProps> = ({ fileName, content }) => {
  const [activeTab, setActiveTab] = useState<'script' | 'cellworld' | 'mind'>('cellworld');
  const [quaternion, setQuaternion] = useState({ w: 0.8, x: 0.2, y: 0.1, z: 0.9 });
  const [logs, setLogs] = useState<string[]>([]);
  const [simTime, setSimTime] = useState(0);
  const [selectedTile, setSelectedTile] = useState<{x:number, y:number, type:string, expression?: string} | null>(null);
  const [entityPaths, setEntityPaths] = useState<Record<string, { path: Point[]; index: number }>>({});
  const [activeEntityId, setActiveEntityId] = useState<string | null>(null);
  const [recentMoves, setRecentMoves] = useState<RecentMove[]>([]);
  
  // UI States for flexible layout
  const [showInspector, setShowInspector] = useState(true);
  const [gridScale, setGridScale] = useState(0.8);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const [dayPhaseIndex, setDayPhaseIndex] = useState(0);
  const [phaseProgress, setPhaseProgress] = useState(0);

  // --- SIMULATION & MIND LOGIC ---
  useEffect(() => {
    const timer = setInterval(() => {
      setSimTime(prev => prev + 1);
      
      setQuaternion(prev => ({
        w: Math.min(1, Math.max(0.5, prev.w + (Math.random() - 0.5) * 0.05)),
        x: Math.random() * 0.3,
        y: Math.random() * 0.3,
        z: Math.min(1, Math.max(0.7, prev.z + (Math.random() - 0.5) * 0.02)),
      }));

      if (Math.random() > 0.9) {
        const newLogs = [
          "Knight (Immune System) patrolling the High Road.",
          "Mage Guild interpreting high-frequency signals from the Capital.",
          "Cleric stabilizing societal harmony in the Village.",
          "Elder sharing wisdom with Child node near the Farm.",
          "Caravan unit transporting resources to the outer sectors.",
          "Wolf pack detected near the Northern Forests.",
          "Z-AXIS: West Continent Infrastructure Loaded.",
          "Bandit activity detected in Southern Wilderness.",
          "Resource Node (Iron) identified in Sector 7 - Structural Reinforcement possible.",
          "Metabolic Input (Fruit) harvested by Gathering Unit.",
        ];
        setLogs(prev => [newLogs[Math.floor(Math.random() * newLogs.length)], ...prev].slice(0, 10));
      }
    }, 1500);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setPhaseProgress(prev => {
        if (prev >= 1) {
          setDayPhaseIndex(idx => (idx + 1) % DAY_PHASES.length);
          return 0;
        }
        return Math.min(1, prev + 0.12);
      });
    }, 850);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const phase = DAY_PHASES[dayPhaseIndex];
    setLogs(prev => [`${phaseIcon[phase]} ${phaseNarrative[phase]}`, ...prev].slice(0, 10));
  }, [dayPhaseIndex]);

  // --- PARSE SCRIPT FOR INSPECTOR & MAP DATA ---
  const scriptData = useMemo(() => {
    const extendsMatch = content.match(/extends\s+(\w+)/);
    const classNameMatch = content.match(/class_name\s+(\w+)/);
    
    const variables = content.split('\n')
      .map(line => {
        const match = line.match(/^(?:var|const)\s+(\w+)\s*=?\s*(.*)/);
        if (match) return { name: match[1], value: match[2] || 'null' };
        return null;
      })
      .filter((v): v is { name: string; value: string } => v !== null);

    // PROCEDURAL GENERATION (Linked to Code)
    const sizeMatch = content.match(/const GRID_SIZE = (\d+)/);
    const gridSize = sizeMatch ? parseInt(sizeMatch[1]) : 6; 
    
    let mapMock;

    if (gridSize > 10) {
      // Large Map Generation (Procedural West Continent)
      mapMock = Array(gridSize).fill(null).map((_, r) => Array(gridSize).fill(null).map((_, c) => {
        // 1. Fixed Structures (Castle)
        if (r < 4 && c < 4) return 'Castle';
        
        // 2. Roads (Grid Spine)
        const isRoad = r === 4 || c === 4 || r === gridSize - 5 || c === gridSize - 5;
        if (isRoad) {
           if (Math.random() > 0.9) return 'Caravan';
           if (Math.random() > 0.92) return 'Merchant';
           if (Math.random() > 0.95) return 'Guard'; // Will default to Knight
           return 'Road';
        }

        // 3. Biomes
        // Mountains (Edges)
        if (r === 0 || c === 0 || r === gridSize-1 || c === gridSize-1) {
           if (Math.random() > 0.7) return 'Iron'; // Resource Spawn
           if (Math.random() > 0.6) return 'Stone'; // Resource Spawn
           return 'Mountain';
        }
        
        // Village Area (South Westish)
        if (r > gridSize - 8 && r < gridSize - 2 && c < 6) {
            if (Math.random() > 0.85) return 'Cow';
            if (Math.random() > 0.85) return 'Horse';
            if (Math.random() > 0.9) return 'Fence';
            if (Math.random() > 0.8) return 'Farm';
            if (Math.random() > 0.7) return 'BrickHouse'; // Advanced structure
            if (Math.random() > 0.6) return 'Campfire';
            if (Math.random() > 0.5) return 'Man';
            if (Math.random() > 0.5) return 'Woman';
            return 'Grass';
        }

        // Forest/Wilderness (South East)
        if (r > gridSize / 2 && c > gridSize / 2) {
            if (Math.random() > 0.92) return 'Wolf';
            if (Math.random() > 0.9) return 'Bandit';
            if (Math.random() > 0.8) return 'FruitTree'; // Resource
            if (Math.random() > 0.7) return 'BerryBush'; // Resource
            if (Math.random() > 0.6) return 'Treehouse'; // Wild habitation
            if (Math.random() > 0.4) return 'Forest';
            return 'Grass';
        }
        
        // River
        if (Math.abs(r - c) < 2) return 'River';

        // Random Scatter in Plains
        const rand = Math.random();
        if (rand > 0.98) return 'Hut';
        if (rand > 0.97) return 'Campfire';
        if (rand > 0.96) return 'Stone';
        if (rand > 0.95) return 'Rabbit';
        if (rand > 0.94) return 'Man';
        if (rand > 0.93) return 'Woman';
        if (rand > 0.90) return 'Villager';
        if (rand > 0.85) return 'BerryBush';
        
        return 'Grass';
      }));

      // Place Unique Units / Points of Interest
      mapMock[2][2] = 'King';
      mapMock[2][3] = 'Queen';
      mapMock[5][5] = 'Mage';
      mapMock[gridSize-4][2] = 'Elder';
      
      // Ensure some specific structures exist
      mapMock[6][6] = 'BrickHouse'; // A developed node
      mapMock[7][7] = 'Fence';

    } else {
      // Default Small 6x8 Map (Fallback)
      const defaultMap = [
          ["Mountain", "Castle", "Castle", "Mountain", "Forest", "Wolf", "Bandit", "Forest"],
          ["Mountain", "Knight", "King", "Queen", "Knight", "Road", "Caravan", "Ranger"],
          ["Guild", "Mage", "Road", "Horse", "Road", "Road", "Grass", "Deer"],
          ["BrickHouse", "Artisan", "Woman", "Man", "Hut", "Child", "Rabbit", "River"],
          ["Fence", "Merchant", "Farm", "Cow", "Elder", "Road", "River", "Mountain"],
          ["Forest", "Woman", "FruitTree", "Campfire", "Ranger", "Iron", "Stone", "Mountain"]
      ];
      mapMock = Array(6).fill(null).map((_, r) => Array(8).fill(null).map((_, c) => defaultMap[r]?.[c] || 'Grass'));
    }

    return {
      extends: extendsMatch ? extendsMatch[1] : 'Node',
      className: classNameMatch ? classNameMatch[1] : fileName.replace('.gd', ''),
      variables,
      mapMock
    };
  }, [content, fileName]);

  const patrolPath = useMemo(() => {
    const map = scriptData.mapMock;
    if (!map.length) return [];
    const targetRow = Math.min(map.length - 1, Math.floor(map.length / 2));
    const width = map[0]?.length || 0;
    if (!width) return [];
    return Array.from({ length: width }, (_, x) => ({ x, y: targetRow }));
  }, [scriptData]);

  const merchantPath = useMemo(() => {
    const map = scriptData.mapMock;
    if (!map.length) return [];
    const height = map.length;
    const width = map[0]?.length || 0;
    if (!width) return [];
    const column = Math.max(0, Math.min(width - 3, width - 1));
    const startRow = Math.max(0, Math.floor((height - 5) / 2));
    return Array.from({ length: Math.min(5, height) }, (_, idx) => ({
      x: column,
      y: Math.min(height - 1, startRow + idx)
    }));
  }, [scriptData]);

  const magePath = useMemo(() => {
    const map = scriptData.mapMock;
    if (!map.length) return [];
    const cols = map[0]?.length || 0;
    if (!cols) return [];
    const maxSteps = Math.min(map.length, cols);
    return Array.from({ length: maxSteps }, (_, idx) => ({ x: idx, y: idx }));
  }, [scriptData]);

  interface EntityDefinition {
    id: string;
    name: string;
    icon: string;
    accent: string;
    path: { x: number; y: number }[];
    message: (point: { x: number; y: number }) => string;
  }

  interface RecentMove {
    key: string;
    icon: string;
    color: string;
    expires: number;
  }

  const entityDefinitions = useMemo<EntityDefinition[]>(() => {
    const entities: EntityDefinition[] = [];
    if (patrolPath.length) {
      entities.push({
        id: 'knight-01',
        name: 'Knight Patrol',
        icon: '⚔️',
        accent: '#f97316',
        path: patrolPath,
        message: point => `scans [${point.y}, ${point.x}] with a vigilant stride.`
      });
    }
    if (merchantPath.length) {
      entities.push({
        id: 'merchant-01',
        name: 'Caravan Merchant',
        icon: '🛍️',
        accent: '#10b981',
        path: merchantPath,
        message: point => `shares wares near [${point.y}, ${point.x}] while humming trade chants.`
      });
    }
    if (magePath.length) {
      entities.push({
        id: 'mage-01',
        name: 'Mage Scout',
        icon: '✨',
        accent: '#a855f7',
        path: magePath,
        message: point => `weaves astral sigils over [${point.y}, ${point.x}].`
      });
    }
    return entities;
  }, [patrolPath, merchantPath, magePath]);

  useEffect(() => {
    const initialPaths = entityDefinitions.reduce<Record<string, { path: Point[]; index: number }>>((acc, entity) => {
      const pathCopy = [...entity.path];
      acc[entity.id] = { path: pathCopy, index: 0 };
      return acc;
    }, {});
    setEntityPaths(initialPaths);
    if (entityDefinitions.length) {
      setActiveEntityId(prev => prev || entityDefinitions[0].id);
    }
  }, [entityDefinitions]);

  const computePath = (start: Point, target: Point): Point[] | null => {
    const height = scriptData.mapMock.length;
    if (!height) return null;
    const width = scriptData.mapMock[0]?.length || 0;
    const queue: { point: Point; path: Point[] }[] = [{ point: start, path: [start] }];
    const visited = new Set<string>([`${start.y}-${start.x}`]);

    const directions: Point[] = [
      { x: 1, y: 0 },
      { x: -1, y: 0 },
      { x: 0, y: 1 },
      { x: 0, y: -1 }
    ];

    while (queue.length) {
      const { point, path } = queue.shift()!;
      if (point.x === target.x && point.y === target.y) {
        return path;
      }
      for (const delta of directions) {
        const candidate = { x: point.x + delta.x, y: point.y + delta.y };
        if (candidate.x < 0 || candidate.y < 0 || candidate.y >= height || candidate.x >= width) continue;
        const key = `${candidate.y}-${candidate.x}`;
        if (visited.has(key)) continue;
        visited.add(key);
        queue.push({ point: candidate, path: [...path, candidate] });
      }
    }

    return null;
  };

  useEffect(() => {
    const initialPositions = entityDefinitions.reduce<Record<string, number>>((acc, entity) => {
      acc[entity.id] = 0;
      return acc;
    }, {});
    setEntityIndices(initialPositions);
  }, [entityDefinitions]);

  useEffect(() => {
    if (!entityDefinitions.length) return;
    const interval = setInterval(() => {
      const now = Date.now();
      let moveEntries: RecentMove[] = [];
      setEntityIndices(prev => {
        const next = { ...prev };
        const movementLogs: string[] = [];
        const occupancy: Record<string, EntityDefinition[]> = {};

        entityDefinitions.forEach(entity => {
          if (!entity.path.length) return;
          const currentIndex = prev[entity.id] ?? 0;
          const nextIndex = (currentIndex + 1) % entity.path.length;
          next[entity.id] = nextIndex;
          const nextPoint = entity.path[nextIndex];
          movementLogs.push(`${entity.icon} ${entity.name} ${entity.message(nextPoint)}`);
          const key = `${nextPoint.y}-${nextPoint.x}`;
          occupancy[key] = [...(occupancy[key] || []), entity];
          moveEntries.push({
            key,
            icon: entity.icon,
            color: entity.accent,
            expires: now + MOVE_TRAIL_MS
          });
        });

        const intersection = Object.entries(occupancy).find(([, group]) => group.length > 1);
        if (intersection) {
          const [coord, crowd] = intersection;
          const [row, col] = coord.split('-');
          movementLogs.unshift(`🤝 ${crowd.map(e => e.name).join(' & ')} converge at [${row}, ${col}].`);
        }

        if (movementLogs.length) {
          setLogs(prev => [...movementLogs, ...prev].slice(0, 10));
        }

        return next;
      });

      setRecentMoves(prev => {
        const filtered = prev.filter(move => move.expires > now);
        const combined = [...filtered, ...moveEntries];
        return combined.slice(-16);
      });
    }, 950);
    return () => clearInterval(interval);
  }, [entityDefinitions]);

  const entityLookup = useMemo(() => {
    const lookup: Record<string, { id: string; icon: string; color: string; name: string }[]> = {};
    entityDefinitions.forEach(entity => {
      const state = entityPaths[entity.id];
      const index = state?.index ?? 0;
      const position = state?.path[index];
      if (!position) return;
      const key = `${position.y}-${position.x}`;
      lookup[key] = [...(lookup[key] || []), { id: entity.id, icon: entity.icon, color: entity.accent, name: entity.name }];
    });
    return lookup;
  }, [entityDefinitions, entityPaths]);

  const highlightCode = (code: string) => {
    return code.split('\n').map((line, i) => {
      if (line.trim().startsWith('#')) return <div key={i} className="text-green-600 font-mono whitespace-pre">{line}</div>;
      const parts = line.split(/(\s+|[().,])/);
      return (
        <div key={i} className="font-mono whitespace-pre">
          {parts.map((part, j) => {
             if (['extends', 'func', 'var', 'const', 'class_name', 'export', 'for', 'in', 'if', 'else'].includes(part.trim())) return <span key={j} className="text-pink-400">{part}</span>;
             if (['String', 'int', 'Vector2', 'Node', 'Sprite2D', 'Array', 'void'].includes(part.trim())) return <span key={j} className="text-godot-accent font-bold">{part}</span>;
             if (part.match(/".*"/)) return <span key={j} className="text-yellow-300">{part}</span>;
             if (part.match(/^\d+$/)) return <span key={j} className="text-blue-300">{part}</span>;
             return <span key={j} className="text-gray-300">{part}</span>;
          })}
        </div>
      );
    });
  };

  const currentPhase = DAY_PHASES[dayPhaseIndex];
  const phasePercent = Math.round(phaseProgress * 100);
  const dayOverlayStyle = useMemo(() => {
    const palette = overlayPalette[currentPhase];
    const tint = phaseTint[currentPhase];
    const baseIntensity = overlayIntensityMap[currentPhase];
    const dynamicIntensity = Math.min(0.98, Math.max(0.35, baseIntensity + (phaseProgress - 0.5) * 0.3));
    return {
      backgroundImage: palette.color,
      opacity: dynamicIntensity,
      boxShadow: `inset 0 0 55px ${tint.accent}`,
      mixBlendMode: 'multiply'
    };
  }, [currentPhase, phaseProgress]);

  const mapColumns = scriptData.mapMock[0]?.length || 0;
  const mapBackdropStyle = useMemo(() => {
    const colors: Record<DayPhase, string> = {
      dawn: 'rgba(17, 20, 40, 0.95)',
      day: 'rgba(22, 27, 45, 0.9)',
      dusk: 'rgba(10, 6, 24, 0.95)',
      night: 'rgba(3, 5, 18, 0.98)'
    };
    const brightness: Record<DayPhase, number> = {
      dawn: 0.9,
      day: 1,
      dusk: 0.65,
      night: 0.45
    };
    return {
      backgroundColor: colors[currentPhase],
      transition: 'background-color 0.9s ease, filter 0.9s ease',
      borderRadius: '1.2rem',
      filter: `brightness(${brightness[currentPhase]})`
    };
  }, [currentPhase]);

  const gridStyle = useMemo(() => {
    const tint = phaseTint[currentPhase];
    const baseColor = currentPhase === 'night' ? '#050b18' : '#161c2c';
    return {
      transform: `scale(${gridScale})`,
      gridTemplateColumns: `repeat(${mapColumns || 1}, minmax(0, 1fr))`,
      borderColor: tint.accent,
      backgroundColor: baseColor,
      boxShadow: `0 0 30px ${tint.accent}33`,
      transition: 'background-color 0.6s ease, border-color 0.6s ease, box-shadow 0.6s ease'
    };
  }, [currentPhase, gridScale, mapColumns]);

  const celestialStyle = useMemo(() => {
    const palette = celestialPalette[currentPhase];
    const glow = overlayPalette[currentPhase].accent;
    const bob = Math.sin(phaseProgress * Math.PI * 2) * 4;
    return {
      backgroundImage: palette.color,
      boxShadow: `0 0 30px ${glow}`,
      transform: `translateY(${bob}px)`
    };
  }, [currentPhase, phaseProgress]);

  // --- STATS ENGINE ---
  const getUnitStats = (type: string) => {
    const baseHp = 100;
    
    let stats = {
       hp: baseHp, maxHp: baseHp,
       mp: 50, maxMp: 50,
       str: 10, dex: 10, vit: 10, int: 10, wis: 10
    };

    switch(type) {
       case 'Knight': 
         stats = { hp: 180, maxHp: 180, mp: 30, maxMp: 30, str: 18, dex: 12, vit: 16, int: 6, wis: 8 }; break;
       case 'King': 
         stats = { hp: 200, maxHp: 200, mp: 100, maxMp: 100, str: 15, dex: 12, vit: 15, int: 16, wis: 20 }; break;
       case 'Mage': 
         stats = { hp: 80, maxHp: 80, mp: 200, maxMp: 200, str: 4, dex: 10, vit: 6, int: 20, wis: 16 }; break;
       case 'Bandit': 
         stats = { hp: 100, maxHp: 100, mp: 20, maxMp: 20, str: 14, dex: 16, vit: 10, int: 6, wis: 4 }; break;
       case 'Man':
       case 'Villager': 
         stats = { hp: 60, maxHp: 60, mp: 10, maxMp: 10, str: 10, dex: 10, vit: 10, int: 8, wis: 8 }; break;
       case 'Woman':
         stats = { hp: 55, maxHp: 55, mp: 15, maxMp: 15, str: 8, dex: 12, vit: 10, int: 10, wis: 10 }; break;
         
       // Animals
       case 'Wolf': stats = { hp: 80, maxHp: 80, mp: 10, maxMp: 10, str: 12, dex: 16, vit: 8, int: 4, wis: 10 }; break;
       case 'Caravan': stats = { hp: 300, maxHp: 300, mp: 0, maxMp: 0, str: 0, dex: 5, vit: 30, int: 0, wis: 0 }; break;

       // Structures (High HP)
       case 'BrickHouse': stats = { hp: 2000, maxHp: 2000, mp: 0, maxMp: 0, str: 0, dex: 0, vit: 100, int: 0, wis: 0 }; break;
       case 'Castle': stats = { hp: 5000, maxHp: 5000, mp: 0, maxMp: 0, str: 0, dex: 0, vit: 200, int: 0, wis: 0 }; break;
       case 'Fence': stats = { hp: 200, maxHp: 200, mp: 0, maxMp: 0, str: 0, dex: 0, vit: 10, int: 0, wis: 0 }; break;
       
       // Resources (No Stats, Materials)
       case 'Iron':
       case 'Stone':
       case 'BerryBush':
       case 'FruitTree':
         stats = { hp: 1, maxHp: 1, mp: 0, maxMp: 0, str: 0, dex: 0, vit: 0, int: 0, wis: 0 }; break;
    }
    return stats;
  };

  const renderAsset = (type: string, face?: string) => {
    const base = <Assets.Grass />;
    const roadBase = <Assets.Road />;
    
    let component = base;
    
    switch(type) {
      // Environment & Buildings
      case 'Castle': component = <Assets.Castle />; break;
      case 'Church': component = <Assets.Church />; break;
      case 'Guild': component = <Assets.Guild />; break;
      case 'House': component = <Assets.House />; break;
      case 'BrickHouse': component = <Assets.BrickHouse />; break;
      case 'Hut': component = <div className="relative w-full h-full"><Assets.Grass /><div className="absolute inset-0 p-1"><Assets.Hut /></div></div>; break;
      case 'Treehouse': component = <div className="relative w-full h-full"><Assets.Forest /><div className="absolute inset-0 p-0"><Assets.Treehouse /></div></div>; break;
      case 'Fence': component = <div className="relative w-full h-full"><Assets.Grass /><div className="absolute inset-0 p-0"><Assets.Fence /></div></div>; break;
      case 'Campfire': component = <div className="relative w-full h-full"><Assets.Grass /><div className="absolute inset-0 p-2"><Assets.Campfire /></div></div>; break;
      
      case 'Forest': component = <Assets.Forest />; break;
      case 'River': component = <Assets.River />; break;
      case 'Mountain': component = <Assets.Mountain />; break;
      case 'Farm': component = <Assets.Farm />; break;
      case 'Road': component = <Assets.Road />; break; 
      
      // Resources
      case 'Stone': component = <div className="relative w-full h-full"><Assets.Mountain /><div className="absolute inset-0 p-3"><Assets.Stone /></div></div>; break;
      case 'Iron': component = <div className="relative w-full h-full"><Assets.Mountain /><div className="absolute inset-0 p-3"><Assets.Iron /></div></div>; break;
      case 'BerryBush': component = <div className="relative w-full h-full"><Assets.Grass /><div className="absolute inset-0 p-2"><Assets.BerryBush /></div></div>; break;
      case 'FruitTree': component = <div className="relative w-full h-full"><Assets.Grass /><div className="absolute inset-0 p-1"><Assets.FruitTree /></div></div>; break;

      // Units (Overlays)
      case 'King': component = <div className="relative w-full h-full">{base}<div className="absolute inset-0 p-1"><Assets.King face={face} /></div></div>; break;
      case 'Queen': component = <div className="relative w-full h-full">{base}<div className="absolute inset-0 p-1"><Assets.Queen face={face} /></div></div>; break;
      case 'Knight': component = <div className="relative w-full h-full">{base}<div className="absolute inset-0 p-1"><Assets.Knight face={face} /></div></div>; break;
      case 'Mage': component = <div className="relative w-full h-full">{base}<div className="absolute inset-0 p-1"><Assets.Mage face={face} /></div></div>; break;
      case 'Cleric': component = <div className="relative w-full h-full">{base}<div className="absolute inset-0 p-1"><Assets.Cleric face={face} /></div></div>; break;
      case 'Ranger': component = <div className="relative w-full h-full"><Assets.Forest /><div className="absolute inset-0 p-1"><Assets.Ranger face={face} /></div></div>; break;
      case 'Merchant': component = <div className="relative w-full h-full">{roadBase}<div className="absolute inset-0 p-1"><Assets.Merchant face={face} /></div></div>; break;
      case 'Artisan': component = <div className="relative w-full h-full">{base}<div className="absolute inset-0 p-1"><Assets.Artisan face={face} /></div></div>; break;
      case 'Bandit': component = <div className="relative w-full h-full"><Assets.Mountain /><div className="absolute inset-0 p-1"><Assets.Bandit face={face} /></div></div>; break;
      
      // Civilians
      case 'Man': component = <div className="relative w-full h-full">{base}<div className="absolute inset-0 p-1"><Assets.Man face={face} /></div></div>; break;
      case 'Woman': component = <div className="relative w-full h-full">{base}<div className="absolute inset-0 p-1"><Assets.Woman face={face} /></div></div>; break;
      case 'Villager': component = <div className="relative w-full h-full">{base}<div className="absolute inset-0 p-1"><Assets.Man face={face} /></div></div>; break;
      case 'Child': component = <div className="relative w-full h-full">{roadBase}<div className="absolute inset-0 p-1"><Assets.Child face={face} /></div></div>; break;
      case 'Elder': component = <div className="relative w-full h-full">{base}<div className="absolute inset-0 p-1"><Assets.Elder face={face} /></div></div>; break;
      
      // Animals & Caravan
      case 'Wolf': component = <div className="relative w-full h-full"><Assets.Forest /><div className="absolute inset-0 p-2"><Assets.Wolf /></div></div>; break;
      case 'Deer': component = <div className="relative w-full h-full"><Assets.Grass /><div className="absolute inset-0 p-2"><Assets.Deer /></div></div>; break;
      case 'Cow': component = <div className="relative w-full h-full"><Assets.Farm /><div className="absolute inset-0 p-2"><Assets.Cow /></div></div>; break;
      case 'Horse': component = <div className="relative w-full h-full"><Assets.Grass /><div className="absolute inset-0 p-2"><Assets.Horse /></div></div>; break;
      case 'Rabbit': component = <div className="relative w-full h-full"><Assets.Grass /><div className="absolute inset-0 p-3"><Assets.Rabbit /></div></div>; break;
      case 'Caravan': component = <div className="relative w-full h-full">{roadBase}<div className="absolute inset-0 p-1"><Assets.Caravan /></div></div>; break;
      default: component = base;
    }
    return component;
  };

  const getRoleDescription = (type: string) => {
    switch(type) {
      case 'King': return { role: 'Ruler', faction: 'Court', desc: 'The Core Will of the Cell.' };
      case 'Child': return { role: 'Youth', faction: 'Civilian', desc: 'New growth, potential, and future.' };
      case 'Elder': return { role: 'Sage', faction: 'Civilian', desc: 'Memory storage and wisdom.' };
      case 'Man': return { role: 'Civilian', faction: 'Labor', desc: 'Standard structural unit (Male).' };
      case 'Woman': return { role: 'Civilian', faction: 'Labor', desc: 'Standard structural unit (Female).' };
      case 'Knight': return { role: 'Martial', faction: 'Order', desc: 'Immune system defenders.' };
      case 'Mage': return { role: 'Arcane', faction: 'Guild', desc: 'Signal processors and logic.' };
      case 'Cleric': return { role: 'Faith', faction: 'Church', desc: 'Maintainers of harmony/homeostasis.' };
      case 'Ranger': return { role: 'Scout', faction: 'Wild', desc: 'Explorers of external environments.' };
      case 'Merchant': return { role: 'Civil', faction: 'Trade', desc: 'Transporters of resources on the roads.' };
      case 'Bandit': return { role: 'Outlaw', faction: 'Rogue', desc: 'Disruptive elements/mutations.' };
      case 'Road': return { role: 'Path', faction: 'Environment', desc: 'Connectors facilitating flow between zones.' };
      case 'Wolf': return { role: 'Predator', faction: 'Nature', desc: 'Natural stressors and threats.' };
      case 'Caravan': return { role: 'Logistics', faction: 'Trade', desc: 'Heavy resource transport vehicle.' };
      
      // Resources
      case 'Iron': return { role: 'Material', faction: 'Resource', desc: 'Mineral density. Used for hardening cell structures.' };
      case 'Stone': return { role: 'Material', faction: 'Resource', desc: 'Basic matter for construction.' };
      case 'BerryBush': return { role: 'Food', faction: 'Resource', desc: 'Quick-access glucose/energy.' };
      case 'FruitTree': return { role: 'Food', faction: 'Resource', desc: 'Sustainable metabolic input.' };

      // Structures
      case 'Campfire': return { role: 'Utility', faction: 'Social', desc: 'Energy convergence point. Increases morale.' };
      case 'Fence': return { role: 'Defense', faction: 'Structure', desc: 'Permeable membrane. Defines territory.' };
      case 'BrickHouse': return { role: 'Home', faction: 'Structure', desc: 'Fortified storage node.' };
      case 'Treehouse': return { role: 'Outpost', faction: 'Structure', desc: 'Elevated observation point.' };
      case 'Hut': return { role: 'Home', faction: 'Structure', desc: 'Basic shelter unit.' };

      default: return { role: 'Entity', faction: 'Common', desc: 'Fundamental structural unit.' };
    }
  }

  // Zoom Handler
  const handleWheel = (e: React.WheelEvent) => {
    // Zoom on wheel
    if (activeTab === 'cellworld') {
       const delta = -e.deltaY * 0.0005;
       setGridScale(prev => Math.min(2.5, Math.max(0.2, prev + delta)));
    }
  };

  const handleCellCommand = (x: number, y: number) => {
    if (!activeEntityId) return;
    const entityState = entityPaths[activeEntityId];
    if (!entityState || !entityState.path.length) return;
    const currentPosition = entityState.path[entityState.index];
    const target: Point = { x, y };
    const path = computePath(currentPosition, target);
    if (!path) {
      setLogs(prev => [`⚠️ Cannot route ${activeEntityId} to [${y}, ${x}]`, ...prev].slice(0, 10));
      return;
    }
    setEntityPaths(prev => ({
      ...prev,
      [activeEntityId]: { path, index: 0 }
    }));
    const entity = entityDefinitions.find(item => item.id === activeEntityId);
    const label = entity ? entity.name : activeEntityId;
    setLogs(prev => [`🧭 ${label} redirected to [${y}, ${x}]`, ...prev].slice(0, 10));
  };

  const knightEntity = entityDefinitions.find(e => e.id === 'knight-01');
  const knightPathState = knightEntity ? entityPaths[knightEntity.id] : undefined;
  const currentPatrol = knightPathState ? knightPathState.path[knightPathState.index] ?? null : null;
  const activePath = activeEntityId ? entityPaths[activeEntityId]?.path ?? [] : [];
  const activePathIndex = activeEntityId ? entityPaths[activeEntityId]?.index ?? 0 : 0;
  const upcomingPath = activePath.slice(activePathIndex);
  const upcomingPathSet = new Set(upcomingPath.map(point => `${point.y}-${point.x}`));

  // Toggle fullscreen wrapper class
  const containerClass = isFullscreen 
    ? "fixed inset-0 z-50 flex flex-col bg-[#1a1b26]" 
    : "absolute inset-0 flex flex-col bg-[#1a1b26]";

  return (
    <div className="flex-1 flex flex-col bg-[#1e1e1e] h-full overflow-hidden relative">
      {/* Tab Bar */}
      <div className="flex bg-[#252526] h-9 border-b border-black select-none shrink-0">
        <button 
          onClick={() => setActiveTab('script')}
          className={`px-3 flex items-center text-xs space-x-2 border-r border-black ${activeTab === 'script' ? 'bg-[#1e1e1e] text-white border-t-2 border-t-godot-accent' : 'text-gray-500 hover:bg-[#2d2d2d]'}`}
        >
          <CodeIcon />
          <span>Script</span>
        </button>
        <button 
          onClick={() => setActiveTab('cellworld')}
          className={`px-3 flex items-center text-xs space-x-2 border-r border-black ${activeTab === 'cellworld' ? 'bg-[#1e1e1e] text-white border-t-2 border-t-green-500' : 'text-gray-500 hover:bg-[#2d2d2d]'}`}
        >
          <MapIcon />
          <span>West Continent (Visualizer)</span>
        </button>
        <button 
          onClick={() => setActiveTab('mind')}
          className={`px-3 flex items-center text-xs space-x-2 border-r border-black ${activeTab === 'mind' ? 'bg-[#1e1e1e] text-white border-t-2 border-t-amber-500' : 'text-gray-500 hover:bg-[#2d2d2d]'}`}
        >
          <span className={activeTab === 'mind' ? 'text-amber-500' : 'text-gray-500'}><BrainIcon /></span>
          <span>Elysia Mind</span>
        </button>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-hidden relative">
        
        {/* --- SCRIPT EDITOR --- */}
        {activeTab === 'script' && (
          <div className="absolute inset-0 overflow-auto p-4 flex bg-[#1e1e1e]">
            <div className="flex flex-col text-right pr-4 text-gray-600 select-none font-mono text-sm leading-6 border-r border-gray-800 mr-4">
              {content.split('\n').map((_, i) => <div key={i}>{i + 1}</div>)}
            </div>
            <div className="flex-1 text-sm leading-6 cursor-text">{highlightCode(content)}</div>
          </div>
        )}

        {/* --- CELL WORLD (CIVILIZATION MAP) --- */}
        {activeTab === 'cellworld' && (
          <div className={containerClass}>
            
            {/* Map Toolbar */}
             <div className="h-10 bg-[#16161e] border-b border-black flex items-center justify-between px-4 shadow-md z-10">
               <div className="flex items-center space-x-4">
                <div className="flex flex-col leading-none">
                  <span className="text-[10px] font-bold text-gray-500">REGION</span>
                  <span className="text-sm text-white font-bold">Kingdom of Silvercrest</span>
                </div>
                <div className="h-6 w-px bg-gray-700"></div>
                <div className="flex space-x-2">
                   <button onClick={() => setGridScale(s => Math.min(2.5, s + 0.1))} className="p-1.5 bg-gray-800 rounded text-gray-400 hover:text-white hover:bg-gray-700" title="Zoom In">
                     <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
                   </button>
                   <button onClick={() => setGridScale(s => Math.max(0.2, s - 0.1))} className="p-1.5 bg-gray-800 rounded text-gray-400 hover:text-white hover:bg-gray-700" title="Zoom Out">
                     <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
                   </button>
                   <div className="text-xs text-gray-500 flex items-center ml-2">(Scroll to Zoom)</div>
                </div>
              </div>
              <div className="text-[10px] text-gray-400 flex items-center gap-2 mt-1">
                <span className="uppercase tracking-[0.2em] text-white/70">Command</span>
                <div className="flex space-x-1">
                  {entityDefinitions.map(entity => {
                    const isActive = activeEntityId === entity.id;
                    return (
                      <button
                        key={entity.id}
                        onClick={() => setActiveEntityId(entity.id)}
                        className={`w-8 h-8 rounded-full border ${isActive ? 'border-amber-300' : 'border-white/30'} bg-black/30 flex items-center justify-center text-lg transition`}
                        style={{ boxShadow: isActive ? `0 0 12px ${entity.accent}` : undefined }}
                      >
                        {entity.icon}
                      </button>
                    );
                  })}
                </div>
                <span className="text-[9px] text-gray-500">Select icon, then click grid to route.</span>
              </div>
              
               <div className="flex items-center space-x-2">
                 <div className="text-[10px] text-gray-400 flex items-center space-x-2">
                   <span className="text-xs uppercase tracking-widest text-white">{phaseIcon[currentPhase]} {currentPhase}</span>
                   <span className="text-[10px] text-gray-400">{phasePercent}% of cycle</span>
                 </div>
                 <div className="text-xs text-gray-500 mr-2">
                    {showInspector ? 'Hide Details' : 'Show Details'}
                 </div>
                <button 
                  onClick={() => setShowInspector(!showInspector)}
                  className={`p-1.5 rounded ${showInspector ? 'bg-amber-900 text-amber-200' : 'bg-gray-700 text-gray-300'}`}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="18" y="3" width="4" height="18"/><rect x="2" y="3" width="16" height="18"/></svg>
                </button>
                <div className="w-px h-6 bg-gray-700 mx-2"></div>
                <button 
                  onClick={() => setIsFullscreen(!isFullscreen)}
                  className={`p-1.5 rounded hover:bg-godot-accent hover:text-white ${isFullscreen ? 'bg-gray-700 text-white' : 'bg-gray-800 text-gray-400'}`}
                  title={isFullscreen ? "Exit Fullscreen" : "Maximize Map"}
                >
                   {isFullscreen ? <MinimizeIcon /> : <MaximizeIcon />}
                </button>
              </div>
            </div>

            <div className="flex flex-1 overflow-hidden">
              {/* The Grid Map */}
              <div 
                ref={mapContainerRef}
                onWheel={handleWheel}
                className="flex-1 relative p-8 overflow-auto flex justify-center items-center"
                style={mapBackdropStyle}
              >
                 {/* Decorative Background */}
                <div className="absolute inset-0 opacity-10 pointer-events-none" 
                     style={{backgroundImage: 'radial-gradient(#414868 1px, transparent 1px)', backgroundSize: '20px 20px'}}></div>
                <div className="absolute inset-0 pointer-events-none transition-colors duration-1000" style={dayOverlayStyle}></div>
                <div
                  className="absolute top-4 right-4 flex flex-col items-center gap-1 pointer-events-none text-center"
                  aria-hidden="true"
                >
                  <div
                    className="w-14 h-14 rounded-full border border-white/30 flex items-center justify-center transition-transform duration-700"
                    style={celestialStyle}
                  >
                    <span className="text-2xl drop-shadow-lg">{phaseIcon[currentPhase]}</span>
                  </div>
                  <span className="text-[10px] uppercase tracking-widest text-white/70">
                    {celestialPalette[currentPhase].label}
                  </span>
                </div>

                <div 
                  className="grid gap-0.5 p-4 rounded-xl shadow-2xl transition-transform duration-75 ease-out origin-center border-8"
                  style={gridStyle}
                >
                  {scriptData.mapMock.map((row, r) => (
                    row.map((cellType, c) => {
                      const cellKey = `${r}-${c}`;
                      const isPatrolHere = currentPatrol?.x === c && currentPatrol?.y === r;
                      const cellEntities = entityLookup[cellKey] ?? [];
                      const moveTraces = recentMoves.filter(move => move.key === cellKey);
                      const isInActivePath = upcomingPathSet.has(cellKey);
                      return (
                      <div key={`${r}-${c}`} 
                           onClick={() => {
                             setSelectedTile({x:c, y:r, type: cellType, expression: 'happy'});
                             handleCellCommand(c, r);
                           }}
                            className={`w-16 h-16 relative transition-all duration-200 cursor-pointer
                                       hover:z-10 hover:scale-110 hover:shadow-[0_0_15px_rgba(255,255,255,0.2)]
                                       shadow-sm
                                       ${selectedTile?.x === c && selectedTile?.y === r ? 'ring-4 ring-amber-400 z-20 scale-110' : ''}
                                       ${cellType === 'Grass' ? 'bg-[#dcfce7]' : 
                                         cellType === 'Road' ? 'bg-[#d6d3d1]' : 'bg-[#f1f5f9]'}
                                       ${isInActivePath ? 'ring-2 ring-dotted ring-white/70' : ''}`}
                           style={{ boxShadow: cellEntities.length ? '0 0 12px rgba(59,130,246,0.5)' : undefined }}
                           title={`${cellType}`}>
                           
                          <div className="absolute inset-0 p-0.5 pointer-events-none">
                             {renderAsset(cellType, (selectedTile?.x === c && selectedTile?.y === r) ? selectedTile.expression : undefined)}
                             {cellEntities.length > 0 && (
                               <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                                 <div
                                   className="p-1 rounded-full border border-white/40 bg-black/60 animate-pulse"
                                   style={{ boxShadow: `0 0 15px ${cellEntities[0].color}` }}
                                 >
                                   <span className="text-lg" style={{ color: cellEntities[0].color }}>
                                     {cellEntities[0].icon}
                                   </span>
                                 </div>
                               </div>
                             )}
                             {moveTraces.map((trace, idx) => (
                               <span
                                 key={`${trace.icon}-${idx}`}
                                 className="absolute text-[10px] font-bold animate-pulse"
                                 style={{
                                   right: 4,
                                   top: 4 + idx * 10,
                                   color: trace.color,
                                   textShadow: '0 0 4px rgba(0,0,0,0.8)'
                                 }}
                               >
                                 {trace.icon}
                               </span>
                             ))}
                             {isPatrolHere && (
                               <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                                 <div className="w-6 h-6 rounded-full border border-amber-300/80 animate-ping opacity-80"></div>
                                 <div className="w-3 h-3 bg-amber-400 rounded-full shadow-[0_0_15px_rgba(251,191,36,0.9)]"></div>
                               </div>
                             )}
                          </div>
                       </div>
                       );
                    })
                  ))}
                </div>
              </div>

              {/* Right Side: Character Card / Inspector (Collapsible) */}
              {showInspector && (
                <div className="w-80 bg-[#16161e] border-l border-black flex flex-col shadow-xl animate-in slide-in-from-right duration-200 z-20">
                  <div className="p-3 bg-[#1a1b26] font-bold text-xs text-gray-300 border-b border-black flex items-center space-x-2">
                    <span className="text-amber-400">✦</span>
                    <span>INSPECTOR</span>
                  </div>
                  
                  {selectedTile ? (
                    <div className="flex flex-col h-full overflow-y-auto">
                       {/* Portrait Header */}
                       <div className="h-48 shrink-0 bg-gradient-to-b from-[#24283b] to-[#16161e] flex items-center justify-center border-b border-[#414868] relative overflow-hidden group">
                          <div className="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white via-transparent to-transparent"></div>
                          <div className="w-32 h-32 drop-shadow-2xl transform group-hover:scale-110 transition-transform duration-500">
                             {renderAsset(selectedTile.type, selectedTile.expression)}
                          </div>
                       </div>

                       {/* Expression Controls */}
                       {['King', 'Queen', 'Knight', 'Mage', 'Cleric', 'Ranger', 'Merchant', 'Artisan', 'Bandit', 'Villager', 'Child', 'Elder', 'Man', 'Woman'].includes(selectedTile.type) && (
                         <div className="flex flex-wrap justify-center gap-2 p-2 bg-[#1a1b26] border-b border-gray-800">
                           {['idle', 'happy', 'sad', 'angry', 'surprised', 'thinking', 'working'].map(exp => (
                             <button 
                               key={exp}
                               onClick={() => setSelectedTile({...selectedTile, expression: exp})}
                               className={`text-[10px] px-2 py-1 rounded capitalize ${selectedTile.expression === exp ? 'bg-amber-500 text-black font-bold' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}
                             >
                               {exp}
                             </button>
                           ))}
                         </div>
                       )}

                       <div className="p-5 flex-1 space-y-4">
                          <div>
                            <div className="flex items-baseline justify-between mb-1">
                              <h2 className="text-xl font-bold text-white">{selectedTile.type}</h2>
                              <span className="text-xs font-mono text-gray-500">ID: {selectedTile.type.substring(0,3).toUpperCase()}-{selectedTile.x}{selectedTile.y}</span>
                            </div>
                            <div className="text-xs text-blue-400 font-mono">Grid Position: [{selectedTile.x}, {selectedTile.y}]</div>
                          </div>
                          
                          {/* COMBAT STATS */}
                          <div className="bg-[#24283b] p-3 rounded-lg border border-[#414868]">
                             <div className="text-[10px] text-gray-500 uppercase font-bold mb-3 flex justify-between">
                                <span>Projection Data</span>
                                <span className="text-xs text-amber-500">Lv. 5</span>
                             </div>
                             
                             {(() => {
                                const stats = getUnitStats(selectedTile.type);
                                const isMaterial = stats.hp < 10 && stats.str === 0;
                                return (
                                  <div className="space-y-3">
                                    {isMaterial ? (
                                      <div className="text-center py-2 text-gray-400 text-xs">
                                         [INERT MATERIAL RESOURCE]
                                      </div>
                                    ) : (
                                      <>
                                        {/* HP Bar */}
                                        <div className="space-y-1">
                                           <div className="flex justify-between text-[10px] font-mono">
                                              <span className="text-red-400">HP</span>
                                              <span className="text-white">{stats.hp} / {stats.maxHp}</span>
                                           </div>
                                           <div className="h-1.5 w-full bg-gray-700 rounded-full overflow-hidden">
                                              <div className="h-full bg-red-500" style={{width: `${(stats.hp / stats.maxHp) * 100}%`}}></div>
                                           </div>
                                        </div>
                                        {/* MP Bar */}
                                        <div className="space-y-1">
                                           <div className="flex justify-between text-[10px] font-mono">
                                              <span className="text-blue-400">MP</span>
                                              <span className="text-white">{stats.mp} / {stats.maxMp}</span>
                                           </div>
                                           <div className="h-1.5 w-full bg-gray-700 rounded-full overflow-hidden">
                                              <div className="h-full bg-blue-500" style={{width: `${(stats.mp / stats.maxMp) * 100}%`}}></div>
                                           </div>
                                        </div>

                                        {/* Attributes Grid */}
                                        <div className="grid grid-cols-2 gap-2 mt-2 pt-2 border-t border-gray-700">
                                           <div className="flex justify-between bg-gray-800 px-2 py-1 rounded text-xs">
                                              <span className="text-gray-400">STR</span> <span className="text-amber-200 font-mono">{stats.str}</span>
                                           </div>
                                           <div className="flex justify-between bg-gray-800 px-2 py-1 rounded text-xs">
                                              <span className="text-gray-400">DEX</span> <span className="text-amber-200 font-mono">{stats.dex}</span>
                                           </div>
                                           <div className="flex justify-between bg-gray-800 px-2 py-1 rounded text-xs">
                                              <span className="text-gray-400">VIT</span> <span className="text-amber-200 font-mono">{stats.vit}</span>
                                           </div>
                                           <div className="flex justify-between bg-gray-800 px-2 py-1 rounded text-xs">
                                              <span className="text-gray-400">INT</span> <span className="text-amber-200 font-mono">{stats.int}</span>
                                           </div>
                                           <div className="flex justify-between bg-gray-800 px-2 py-1 rounded text-xs">
                                              <span className="text-gray-400">WIS</span> <span className="text-amber-200 font-mono">{stats.wis}</span>
                                           </div>
                                        </div>
                                      </>
                                    )}
                                  </div>
                                )
                             })()}
                          </div>

                          <div className="bg-[#24283b] p-3 rounded-lg border border-[#414868]">
                            <div className="text-[10px] text-gray-500 uppercase font-bold mb-2">Attributes</div>
                            <div className="space-y-1 text-xs">
                              <div className="flex justify-between"><span className="text-gray-400">Role</span> <span className="text-white">{getRoleDescription(selectedTile.type).role}</span></div>
                              <div className="flex justify-between"><span className="text-gray-400">Faction</span> <span className="text-pink-400">{getRoleDescription(selectedTile.type).faction}</span></div>
                              <div className="flex justify-between"><span className="text-gray-400">Theme</span> <span className="text-amber-400">West Continent</span></div>
                            </div>
                          </div>

                          <div className="bg-[#24283b] p-3 rounded-lg border border-[#414868]">
                             <div className="text-[10px] text-gray-500 uppercase font-bold mb-2">Elysia's Analysis</div>
                             <p className="text-xs text-gray-300 italic leading-relaxed">
                               "{getRoleDescription(selectedTile.type).desc}"
                             </p>
                          </div>
                       </div>
                    </div>
                  ) : (
                    <div className="flex-1 flex items-center justify-center text-gray-600 text-sm italic p-4 text-center">
                       Select a tile from the map to inspect its properties...
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* --- ELYSIA MIND (Z-AXIS) --- */}
        {activeTab === 'mind' && (
          <div className="absolute inset-0 flex bg-black">
            {/* Left: Quaternion Engine */}
            <div className="flex-1 relative flex items-center justify-center overflow-hidden">
              <div className="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-purple-900 via-black to-black"></div>
              
              <div className="relative w-64 h-64">
                 <div className="absolute inset-0 border-2 border-blue-500/30 rounded-full animate-[spin_10s_linear_infinite]"></div>
                 <div className="absolute inset-4 border-2 border-purple-500/30 rounded-full animate-[spin_7s_linear_infinite_reverse]"></div>
                 <div className="absolute inset-8 border-2 border-amber-500/30 rounded-full animate-[spin_15s_linear_infinite]"></div>
                 <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-20 h-20 bg-white/10 rounded-full blur-xl animate-pulse"></div>
                    <div className="text-4xl font-bold text-white opacity-80 tracking-widest">Q</div>
                 </div>
                 <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-6 text-purple-400 font-mono text-xs">W: ANCHOR ({(quaternion.w * 100).toFixed(0)}%)</div>
                 <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-6 text-amber-400 font-mono text-xs">Z: INTENT ({(quaternion.z * 100).toFixed(0)}%)</div>
              </div>
            </div>

            {/* Right: Telemetry */}
            <div className="w-80 bg-[#0a0a0a] border-l border-gray-800 flex flex-col font-mono text-xs">
              <div className="p-2 bg-[#1a1a1a] border-b border-gray-800 font-bold text-amber-500">
                ELYSIA PROTOCOL // TELEMETRY
              </div>
              <div className="flex-1 overflow-hidden flex flex-col p-2 space-y-2">
                 {logs.map((log, i) => (
                   <div key={i} className={`border-l-2 pl-2 py-1 ${
                     log.includes('SIGNAL') ? 'border-green-500 text-green-200' : 
                     log.includes('Z-AXIS') ? 'border-amber-500 text-amber-200' : 
                     'border-gray-600 text-gray-400'
                   }`}>
                     <span className="opacity-50 mr-2">T+{simTime - i}</span>
                     {log}
                   </div>
                 ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
