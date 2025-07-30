import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.fft import fft, fftfreq
from datetime import datetime

# Make sure there's a "plots" folder to store images
os.makedirs('plots', exist_ok=True)

# Generate a timestamp for file naming (so each run is unique)
def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# Generate synthetic sine wave
def generate_sine_wave(freq, sample_rate, duration, amplitude=1.0):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * freq * t)
    return t, signal

# Moving average filter
def moving_average(signal, window_size=5):
    return np.convolve(signal, np.ones(window_size) / window_size, mode='same')

# Butterworth low-pass filter
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# Plot signals overlayed, save & show
def plot_signals(t, signals, labels, filename, title='Signals', xlabel='Time [s]', ylabel='Amplitude'):
    plt.figure(figsize=(12, 5))
    for sig, label in zip(signals, labels):
        plt.plot(t, sig, label=label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save to file
    save_path = f'plots/{filename}_{timestamp()}.png'
    plt.savefig(save_path, dpi=300)
    print(f"Saved: {save_path}")

    # Show plot on screen
    plt.show()

# FFT plot, save & show
def plot_fft(signal, sample_rate, filename, title='Frequency Spectrum'):
    N = len(signal)
    yf = fft(signal)
    xf = fftfreq(N, 1 / sample_rate)[:N // 2]
    plt.figure(figsize=(12, 4))
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
    plt.title(title)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.tight_layout()

    # Save to file
    save_path = f'plots/{filename}_{timestamp()}.png'
    plt.savefig(save_path, dpi=300)
    print(f"Saved: {save_path}")

    # Show plot on screen
    plt.show()

if __name__ == '__main__':
    sample_rate = 1000  # Hz
    duration = 1.0      # seconds
    freq = 50           # Hz sine wave frequency

    # Generate synthetic sine wave and add noise
    t, signal = generate_sine_wave(freq, sample_rate, duration)
    noise = 0.3 * np.random.normal(size=len(signal))
    noisy_signal = signal + noise

    # Apply filters
    ma_filtered = moving_average(noisy_signal, window_size=10)
    cutoff_freq = 60  # Hz
    bw_filtered = butter_lowpass_filter(noisy_signal, cutoff_freq, sample_rate)

    # Generate and save all plots
    plot_signals(
        t,
        [noisy_signal, ma_filtered, bw_filtered],
        'signal_comparison',
        title='Signal Filtering Comparison'
    )
    plot_fft(noisy_signal, sample_rate, 'noisy_fft', title='Noisy Signal Frequency Spectrum')
    plot_fft(bw_filtered, sample_rate, 'filtered_fft', title='Butterworth Filtered Frequency Spectrum')
