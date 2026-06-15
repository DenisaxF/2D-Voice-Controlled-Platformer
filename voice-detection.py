import numpy as np
import pyaudio
import socket
import time

# ── Parametri — schimbă doar CHUNK între teste ──
CHUNK = 4096  # Test 1: 4096 | Test 2: 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SMOOTHING = 0.3

frame_count = [0]
interval_start = [time.time()]
THROUGHPUT_INTERVAL = 5

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
    frames_per_buffer=CHUNK
)

smoothed_pitch = 0.0

print(f"Listening... | CHUNK={CHUNK} | Teoretic: {RATE/CHUNK:.2f} frame/s")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        amplitude = np.abs(audio_data).mean()

        # ── Numără TOATE frame-urile, inclusiv cele silențioase ──
        frame_count[0] += 1
        elapsed = time.time() - interval_start[0]
        if elapsed >= THROUGHPUT_INTERVAL:
            throughput = frame_count[0] / elapsed
            teoretic = RATE / CHUNK
            print(f"[CHUNK={CHUNK}] Throughput: {throughput:.2f} fps | Teoretic: {teoretic:.2f} fps | Diferenta: {abs(throughput - teoretic):.2f}")
            frame_count[0] = 0
            interval_start[0] = time.time()

        # ── Procesare FFT doar dacă e sunet ──
        if amplitude < 20:
            continue

        window = np.hamming(len(audio_data))
        fft_data = np.fft.rfft(audio_data * window)
        frequencies = np.fft.rfftfreq(len(audio_data), 1 / RATE)
        fft_magnitude = np.abs(fft_data)

        valid = (frequencies > 80) & (frequencies < 1500)
        peak_frequency = np.clip(
            frequencies[valid][np.argmax(fft_magnitude[valid])], 80, 1500
        )

        smoothed_pitch = SMOOTHING * smoothed_pitch + (1 - SMOOTHING) * peak_frequency

        send_time = time.time()
        message = f"{smoothed_pitch:.2f},{send_time:.4f},{CHUNK}".encode('utf-8')
        udp_socket.sendto(message, ('127.0.0.1', 5005))

except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    udp_socket.close()