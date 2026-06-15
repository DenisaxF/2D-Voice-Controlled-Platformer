"""
Grafic: Comparație rezoluție spectrală FFT — CHUNK=4096 vs CHUNK=2048
Captează 1 secundă de sunet și aplică FFT cu ambele dimensiuni de fereastră.
Salvează: graphs/output/fft_resolution.pdf (vectorial)
Rulare: python graphs/graph_fft_resolution.py
"""

import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# ── Parametri ──
RATE = 44100
RECORD_SECONDS = 1
FORMAT = pyaudio.paInt16
CHANNELS = 1

print("Pregătește-te să emiți un sunet constant (fredonează o notă)...")
input("Apasă Enter când ești gata, apoi fredonează timp de 1 secundă.")

# ── Înregistrează audio ──
p = pyaudio.PyAudio()

input_index = None
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if dev['maxInputChannels'] > 0 and input_index is None:
        input_index = i

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=input_index,
    frames_per_buffer=RATE  # înregistrează 1 secundă
)

print("Înregistrare... fredonează!")
data = stream.read(RATE, exception_on_overflow=False)
print("Gata!")

stream.stop_stream()
stream.close()
p.terminate()

# Convertește la numpy
audio = np.frombuffer(data, dtype=np.int16).astype(np.float32)

# ─────────────────────────────────────────────
# Găsește automat cea mai stabilă zonă vocală
# ─────────────────────────────────────────────

window_search = 4096
hop = 512

energies = []

for i in range(0, len(audio) - window_search, hop):
    segment = audio[i:i + window_search]
    energies.append(np.sum(segment ** 2))

best_start = np.argmax(energies) * hop

# ── FFT cu CHUNK=4096 ──
chunk4 = 4096

segment4 = audio[best_start:best_start + chunk4]

if len(segment4) < chunk4:
    segment4 = np.pad(segment4, (0, chunk4 - len(segment4)))

window4 = np.hamming(chunk4)

fft4 = np.abs(np.fft.rfft(segment4 * window4))
freq4 = np.fft.rfftfreq(chunk4, 1 / RATE)

fft4 = fft4 / np.max(fft4)

res4 = RATE / chunk4

# ── FFT cu CHUNK=2048 ──
chunk2 = 2048

segment2 = audio[best_start:best_start + chunk2]

if len(segment2) < chunk2:
    segment2 = np.pad(segment2, (0, chunk2 - len(segment2)))

window2 = np.hamming(chunk2)

fft2 = np.abs(np.fft.rfft(segment2 * window2))
freq2 = np.fft.rfftfreq(chunk2, 1 / RATE)

fft2 = fft2 / np.max(fft2)

res2 = RATE / chunk2

# ── Grafic ──
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

fig.suptitle(
    'Comparație rezoluție spectrală FFT\nCHUNK=4096 vs CHUNK=2048',
    fontsize=13,
    fontweight='bold'
)

freq_min = 80
freq_max = 1500

mask4 = (freq4 >= freq_min) & (freq4 <= freq_max)
mask2 = (freq2 >= freq_min) & (freq2 <= freq_max)

# CHUNK 4096
ax1.plot(freq4[mask4], fft4[mask4], linewidth=1.3)
ax1.fill_between(freq4[mask4], fft4[mask4], alpha=0.2)

ax1.set_title(
    f'CHUNK = 4096 | Rezoluție frecvențială = {res4:.2f} Hz/bin',
    fontsize=10
)

ax1.set_ylabel('Amplitudine normalizată')
ax1.set_ylim(0, 1.05)
ax1.grid(True, alpha=0.3)

# CHUNK 2048
ax2.plot(freq2[mask2], fft2[mask2], linewidth=1.3)
ax2.fill_between(freq2[mask2], fft2[mask2], alpha=0.2)

ax2.set_title(
    f'CHUNK = 2048 | Rezoluție frecvențială = {res2:.2f} Hz/bin',
    fontsize=10
)

ax2.set_xlabel('Frecvență (Hz)')
ax2.set_ylabel('Amplitudine normalizată')
ax2.set_ylim(0, 1.05)
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# Salvează PDF
os.makedirs('graphs/output', exist_ok=True)

plt.savefig(
    'graphs/output/fft_resolution.pdf',
    format='pdf',
    bbox_inches='tight'
)

print(f"Zona analizată începe la eșantionul {best_start}")
print(f"Rezoluție 4096: {res4:.2f} Hz/bin")
print(f"Rezoluție 2048: {res2:.2f} Hz/bin")
print("Salvat: graphs/output/fft_resolution.pdf")

plt.show()