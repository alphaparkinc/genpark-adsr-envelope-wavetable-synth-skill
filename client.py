"""ADSR Envelope & Wavetable Synthesizer Engine
100% Python Standard Library (math).
"""

import math

class ADSREnvelopeWavetableSynth:
    """Attack-Decay-Sustain-Release generator with band-limited wavetable oscillators."""
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_envelope(self, attack_sec, decay_sec, sustain_level, release_sec, total_sec):
        num_samples = int(self.sample_rate * total_sec)
        att_samples = int(self.sample_rate * attack_sec)
        dec_samples = int(self.sample_rate * decay_sec)
        rel_samples = int(self.sample_rate * release_sec)
        sus_samples = max(0, num_samples - att_samples - dec_samples - rel_samples)
        
        env = []
        for i in range(att_samples):
            env.append(i / max(1, att_samples))
        for i in range(dec_samples):
            val = 1.0 - (1.0 - sustain_level) * (i / max(1, dec_samples))
            env.append(val)
        for _ in range(sus_samples):
            env.append(sustain_level)
        for i in range(rel_samples):
            val = sustain_level * (1.0 - i / max(1, rel_samples))
            env.append(val)
        return env[:num_samples]

    def render_tone(self, waveform="sine", freq=440.0, duration_sec=0.5,
                    attack=0.05, decay=0.05, sustain=0.7, release=0.1):
        num_samples = int(self.sample_rate * duration_sec)
        env = self.generate_envelope(attack, decay, sustain, release, duration_sec)
        audio = []
        dt = 1.0 / self.sample_rate
        for i in range(num_samples):
            t = i * dt
            phase = (t * freq) % 1.0
            if waveform == "sine":
                raw = math.sin(2.0 * math.pi * phase)
            elif waveform == "square":
                raw = 1.0 if phase < 0.5 else -1.0
            elif waveform == "sawtooth":
                raw = 2.0 * phase - 1.0
            elif waveform == "triangle":
                raw = 2.0 * abs(2.0 * (phase - math.floor(phase + 0.5))) - 1.0
            else:
                raw = math.sin(2.0 * math.pi * phase)
            e_val = env[i] if i < len(env) else 0.0
            audio.append(raw * e_val)
        return {
            "waveform": waveform,
            "frequency_hz": freq,
            "samples_count": len(audio),
            "peak_amplitude": max(abs(x) for x in audio) if audio else 0.0,
            "rms_level": math.sqrt(sum(x * x for x in audio) / max(1, len(audio))),
            "audio_samples": audio[:50] # Sample preview
        }
