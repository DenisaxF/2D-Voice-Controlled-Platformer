# Joc Platformer 2D Controlat Vocal

Proiect de licență ce implementează un joc platformer 2D controlat prin voce. Sistemul utilizează procesarea semnalului audio în Python pentru detectarea frecvenței dominante și transmite datele către jocul dezvoltat în Godot Engine prin protocolul UDP.

## Tehnologii utilizate

- Python 3.11
- NumPy
- PyAudio
- Godot Engine 4.x
- UDP

## Funcționalități

- Detecție vocală în timp real folosind FFT
- Controlul mișcării personajului prin frecvența vocii
- Sărituri cu înălțime variabilă
- Filtrare și netezire a semnalului audio

## Rulare

```bash
python voice_detection.py
```

Apoi deschideți proiectul în Godot și rulați scena principală.
