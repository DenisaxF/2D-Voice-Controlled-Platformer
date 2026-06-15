"""
Grafic: Comparație CHUNK=4096 vs CHUNK=2048
Arată: throughput real vs teoretic și latența bufferului
Salvează: graphs/output/chunk_comparison.pdf (vectorial)
Rulare: python graphs/graph_chunk.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# ── Date ──
RATE = 44100
chunks       = [4096, 2048]
teoretic_fps = [RATE / c for c in chunks]       # throughput teoretic
real_fps     = [10.76, 21.50]                   # throughput real măsurat
lat_buffer   = [c / RATE * 1000 for c in chunks] # latența bufferului în ms

df4 = pd.read_csv('data/latency_4096_log.csv')
df2 = pd.read_csv('data/latency_2048_log.csv')
lat_udp = [df4['latency_ms'].mean(), df2['latency_ms'].mean()]
lat_total = [lat_buffer[i] + lat_udp[i] for i in range(2)]

labels = ['CHUNK = 4096', 'CHUNK = 2048']
x = np.arange(len(labels))
width = 0.35

# ── Figura cu 2 subploturi ──
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Comparație configurații buffer audio: CHUNK=4096 vs CHUNK=2048',
             fontsize=13, fontweight='bold')

# ── Subplot 1: Throughput ──
bars1 = ax1.bar(x - width/2, teoretic_fps, width, label='Teoretic', color='#1E2761', alpha=0.85)
bars2 = ax1.bar(x + width/2, real_fps,     width, label='Real măsurat', color='#028090', alpha=0.85)

ax1.set_ylabel('Frame-uri pe secundă (fps)', fontsize=11)
ax1.set_title('Throughput', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontsize=10)
ax1.legend(fontsize=9)
ax1.grid(True, axis='y', alpha=0.3)

# Valori pe bare
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=9, color='#1E2761')
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=9, color='#028090')

# ── Subplot 2: Latență ──
lat_buf_vals = lat_buffer
lat_udp_vals = lat_udp

bars_buf = ax2.bar(x, lat_buf_vals, width*2, label='Latență buffer (teoretică)',
                   color='#1E2761', alpha=0.85)
bars_udp = ax2.bar(x, lat_udp_vals, width*2, bottom=lat_buf_vals,
                   label='Latență UDP (măsurată)', color='#028090', alpha=0.85)

ax2.set_ylabel('Latență (ms)', fontsize=11)
ax2.set_title('Latență totală', fontsize=11, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(labels, fontsize=10)
ax2.legend(fontsize=9)
ax2.grid(True, axis='y', alpha=0.3)

# Total pe fiecare bară
for i, total in enumerate(lat_total):
    ax2.text(x[i], total + 0.5, f'{total:.1f} ms',
             ha='center', va='bottom', fontsize=10, fontweight='bold', color='#B85042')

plt.tight_layout()

# ── Salvează PDF vectorial ──
os.makedirs('graphs/output', exist_ok=True)
plt.savefig('graphs/output/chunk_comparison.pdf', format='pdf', bbox_inches='tight', dpi=300)
print("Salvat: graphs/output/chunk_comparison.pdf")
plt.show()
