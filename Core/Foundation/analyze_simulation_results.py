#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultra-Dense Simulation Results Analyzer
========================================
완료된 시뮬레이션의 결과를 분석하고 Experience Digestion 재실행
"""

import sys
sys.path.insert(0, '.')

from pathlib import Path
import json
from datetime import datetime

def main():
    runs_dir = Path('runs')
    if not runs_dir.exists():
        print("❌ No runs directory found")
        return 1
    
    # 가장 최근 시뮬레이션 찾기
    run_dirs = list(runs_dir.glob('ultra_dense_*'))
    if not run_dirs:
        print("❌ No simulation runs found")
        return 1
    
    latest_run = max(run_dirs, key=lambda p: p.stat().st_mtime)
    print(f"\n{'='*70}")
    print(f"📊 Latest Simulation Run: {latest_run.name}")
    print(f"{'='*70}")
    
    # 파일 목록
    print(f"\nFiles in run:")
    total_size = 0
    for f in sorted(latest_run.glob('*')):
        size_mb = f.stat().st_size / 1024 / 1024
        total_size += f.stat().st_size
        print(f"  {f.name:40} {size_mb:8.2f} MB")
    
    print(f"\n  {'Total':40} {total_size/1024/1024:8.2f} MB")
    
    # 결과 파일 분석
    results_file = latest_run / 'results.json'
    if results_file.exists():
        print(f"\n{'='*70}")
        print(f"📈 Simulation Results")
        print(f"{'='*70}")
        
        with open(results_file, encoding='utf-8') as f:
            results = json.load(f)
        
        # Metadata
        meta = results.get('metadata', {})
        print(f"\nMetadata:")
        print(f"  Total Ticks: {meta.get('total_ticks'):,}")
        print(f"  Final Particles: {meta.get('final_particles'):,}")
        print(f"  Subjective Years: {meta.get('subjective_years'):.2e}")
        print(f"  Real Time: {meta.get('real_time_seconds'):,.1f}s ({meta.get('real_time_seconds')/60:.1f} min)")
        print(f"  Acceleration: {meta.get('effective_acceleration'):.2e}x")
        
        # Configuration
        config = results.get('configuration', {})
        print(f"\nConfiguration:")
        print(f"  Max Particles: {config.get('max_particles')}")
        print(f"  Interference Freq: {config.get('interference_freq')}")
        print(f"  Depth: {config.get('depth')}")
        print(f"  Batch Size: {config.get('batch_size')}")
        
        # Results summary
        res = results.get('results', {})
        print(f"\nExperience Summary:")
        print(f"  Unique Concepts: {res.get('unique_concepts', 'N/A')}")
        print(f"  Relationships: {res.get('relationships_discovered', 'N/A')}")
        print(f"  Language Turns: {res.get('language_turns', 'N/A')}")
        print(f"  Resonance Events: {res.get('resonance_events_detected', 'N/A')}")
        
        # Wisdom
        wisdom = results.get('wisdom', [])
        print(f"\nWisdom Extracted ({len(wisdom)} insights):")
        for i, w in enumerate(wisdom[:5], 1):
            print(f"  {i}. {w.get('insight', 'N/A')[:60]}...")
        if len(wisdom) > 5:
            print(f"  ... and {len(wisdom)-5} more")
    
    # Checkpoint 파일들
    checkpoint_files = sorted(latest_run.glob('checkpoint_*.json'))
    if checkpoint_files:
        print(f"\n{'='*70}")
        print(f"📋 Checkpoints ({len(checkpoint_files)} found)")
        print(f"{'='*70}")
        
        # 첫 번째, 중간, 마지막 checkpoint
        checkpoints_to_show = [checkpoint_files[0], checkpoint_files[len(checkpoint_files)//2], checkpoint_files[-1]]
        for cp_file in checkpoints_to_show:
            with open(cp_file) as f:
                cp = json.load(f)
            print(f"\n  {cp_file.name}:")
            print(f"    Tick: {cp.get('tick'):,}")
            print(f"    Elapsed: {cp.get('elapsed_seconds'):.1f}s")
            print(f"    Particles: {cp.get('particles_count'):,}")
    
    # Logs 확인
    logs_dir = Path('logs')
    if logs_dir.exists():
        print(f"\n{'='*70}")
        print(f"📝 Log Files")
        print(f"{'='*70}")
        
        log_files = [
            'resonance_patterns.jsonl',
            'resonance_events.jsonl',
            'language_progress.jsonl'
        ]
        
        for log_file in log_files:
            path = logs_dir / log_file
            if path.exists():
                lines = sum(1 for _ in open(path))
                size_mb = path.stat().st_size / 1024 / 1024
                print(f"\n  {log_file}:")
                print(f"    Lines: {lines:,}")
                print(f"    Size: {size_mb:.2f} MB")
    
    print(f"\n{'='*70}")
    print(f"✅ Simulation analysis complete")
    print(f"{'='*70}\n")
    
    return 0

if __name__ == "__main__":
    exit(main())
