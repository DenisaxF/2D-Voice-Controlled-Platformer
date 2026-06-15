"""
Grafic: Latența UDP în timp pentru CHUNK=4096 (Evidențiere Min/Max)
Salvează: graphs/output/latency_udp.pdf (vectorial)
Rulare: python graphs/graph_latency.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# ── Citește datele ──
# Notă: Asigură-te că fișierul se află în folderul 'data' sau modifică calea dacă este direct în rădăcină
cale_fisier = 'data/latency_4096_log.csv'
if not os.path.exists(cale_fisier) and os.path.exists('latency_4096_log.csv'):
    cale_fisier = 'latency_4096_log.csv'

df4 = pd.read_csv(cale_fisier)

# Normalizează timestamp la 0
df4['timestamp'] = df4['timestamp'] - df4['timestamp'].iloc[0]

# Convertește ms → secunde pentru axa X
df4['time_s'] = df4['timestamp'] / 1000.0

# ── Calculează statistici și puncte cheie ──
mean4 = df4['latency_ms'].mean()
min4 = df4['latency_ms'].min()
max4 = df4['latency_ms'].max()

# Determinarea indicilor pentru punctele de minim și maxim
idx_min = df4['latency_ms'].idxmin()
idx_max = df4['latency_ms'].idxmax()

time_min = df4['time_s'].iloc[idx_min]
time_max = df4['time_s'].iloc[idx_max]

# ── Grafic unic (doar pentru CHUNK=4096) ──
fig, ax1 = plt.subplots(figsize=(10, 5.5))

# Plotarea liniei de latență
ax1.plot(df4['time_s'], df4['latency_ms'], color='#028090', linewidth=1.4, alpha=0.8, label='Latență măsurată')
ax1.fill_between(df4['time_s'], df4['latency_ms'], alpha=0.1, color='#028090')

# Linia orizontală pentru valoarea medie
ax1.axhline(y=mean4, color='#1E2761', linestyle='--', linewidth=1.5, label=f'Medie: {mean4:.2f} ms')

# ── Marcarea punctelor de Minim și Maxim ──
ax1.scatter(time_min, min4, color='#2a9d8f', s=100, zorder=5, edgecolor='black', label=f'Minim: {min4:.1f} ms')
ax1.scatter(time_max, max4, color='#e76f51', s=100, zorder=5, edgecolor='black', label=f'Maxim: {max4:.1f} ms')

# Adăugarea săgeților și etichetelor explicative (Adnotări)
ax1.annotate(f'Minim ({min4:.1f} ms)', 
             xy=(time_min, min4), 
             xytext=(time_min + 0.4, min4 + 1.0),
             arrowprops=dict(facecolor='#2a9d8f', shrink=0.08, width=1, headwidth=6, headlength=6),
             fontsize=10, fontweight='bold', color='#217066')

ax1.annotate(f'Maxim ({max4:.1f} ms)', 
             xy=(time_max, max4), 
             xytext=(time_max - 1.5, max4 - 2.0),
             arrowprops=dict(facecolor='#e76f51', shrink=0.08, width=1, headwidth=6, headlength=6),
             fontsize=10, fontweight='bold', color='#a63c24')

# ── Detalii axă și design academic ──
ax1.set_xlabel('Timp de la începerea rulării (s)', fontsize=11)
ax1.set_ylabel('Latență transport UDP (ms)', fontsize=11)
ax1.set_title(f'Evoluția latenței de rețea în timp (Fereastră CHUNK = 4096)\n'
              f'Valoare Medie: {mean4:.2f} ms  |  Minim: {min4:.1f} ms  |  Maxim: {max4:.1f} ms', 
              fontsize=12, fontweight='bold', pad=12)

ax1.grid(True, alpha=0.3, linestyle=':')
ax1.set_ylim(bottom=0, top=max4 + 3) # Oferă spațiu deasupra maximului pentru o lizibilitate crescută
ax1.legend(fontsize=10, loc='upper right')

plt.tight_layout()

# ── Salvează PDF-ul vectorial pentru lucrare ──
os.makedirs('graphs/output', exist_ok=True)
plt.savefig('graphs/output/latency_udp.pdf', format='pdf', bbox_inches='tight', dpi=300)
print("Graficul a fost salvat cu succes în: graphs/output/latency_udp.pdf")

plt.show() # Dezactivat conform bunelor practici de automatizare, îl poți decommenta local dacă vrei previzualizare ferestrată