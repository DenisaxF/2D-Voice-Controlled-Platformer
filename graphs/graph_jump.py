"""
Grafic: Frecvența vocală vs Înălțimea săriturii
Salvează: graphs/output/pitch_vs_jump.pdf (vectorial)
Rulare: python graphs/graph_jump.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# ── Citește datele ──
df = pd.read_csv('data/jump_log.csv')

# Elimină valorile la limita de 800Hz (clamp artificial)
df = df[df['pitch'] < 800]

# Sortează după pitch pentru linia de trend
df = df.sort_values('pitch')

# ── Linie de trend ──
z = np.polyfit(df['pitch'], df['jump_height_px'], 1)
p = np.poly1d(z)
x_trend = np.linspace(df['pitch'].min(), df['pitch'].max(), 100)

# ── Grafic ──
fig, ax = plt.subplots(figsize=(9, 5))

ax.scatter(df['pitch'], df['jump_height_px'],
           color='#028090', s=80, zorder=5, label='Sărituri înregistrate')

ax.plot(x_trend, p(x_trend),
        color='#1E2761', linestyle='--', linewidth=1.5, label='Linie de tendință')

# Zone colorate
ax.axvspan(420, 650, alpha=0.06, color='#028090', label='Zonă săritură (420–650 Hz)')
ax.axvline(x=420, color='orange', linestyle=':', linewidth=1.2, label='Prag săritură (420 Hz)')

ax.set_xlabel('Frecvență vocală (Hz)', fontsize=12)
ax.set_ylabel('Înălțimea săriturii (px)', fontsize=12)
ax.set_title('Relația dintre frecvența vocală și înălțimea săriturii', fontsize=13, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Adaugă valorile pe puncte
for _, row in df.iterrows():
    ax.annotate(f'{row["pitch"]:.0f} Hz',
                xy=(row['pitch'], row['jump_height_px']),
                xytext=(5, 5), textcoords='offset points',
                fontsize=8, color='#64748B')

plt.tight_layout()

# ── Salvează PDF vectorial ──
os.makedirs('graphs/output', exist_ok=True)
plt.savefig('graphs/output/pitch_vs_jump.pdf', format='pdf', bbox_inches='tight', dpi=300)
print("Salvat: graphs/output/pitch_vs_jump.pdf")
plt.show()
