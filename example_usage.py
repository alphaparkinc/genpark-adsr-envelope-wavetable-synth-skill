from client import ADSREnvelopeWavetableSynth

def main():
    synth = ADSREnvelopeWavetableSynth(sample_rate=44100)
    res = synth.render_tone(waveform="triangle", freq=440.0, duration_sec=0.2)
    print("ADSR Wavetable Synth Verification:")
    print(f"Waveform: {res['waveform']}, Frequency: {res['frequency_hz']} Hz")
    print(f"Samples: {res['samples_count']}, Peak: {res['peak_amplitude']:.4f}, RMS: {res['rms_level']:.4f}")

if __name__ == "__main__":
    main()
