import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import butter, filtfilt
from scipy.fft import fft, fftfreq
from datetime import datetime
import tkinter as tk
from tkinter import ttk

# Ensure a folder exists for saving plots
os.makedirs('plots', exist_ok=True)

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# Signal generation and filters
def generate_sine_wave(freq, sample_rate, duration, amplitude=1.0):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * freq * t)
    return t, signal

def moving_average(signal, window_size=5):
    return np.convolve(signal, np.ones(window_size) / window_size, mode='same')

def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# Plotting helper
def save_and_show_plot(fig, filename):
    save_path = f"plots/{filename}_{timestamp()}.png"
    fig.savefig(save_path, dpi=300)
    print(f"Saved plot to: {save_path}")

# GUI main function
def run_signal_processing():
    try:
        # Get values from GUI
        freq = float(freq_entry.get())
        duration = float(duration_entry.get())
        noise_level = float(noise_entry.get())
        cutoff_freq = float(cutoff_entry.get())
        sample_rate = 1000

        # Generate noisy signal
        t, signal = generate_sine_wave(freq, sample_rate, duration)
        noise = noise_level * np.random.normal(size=len(signal))
        noisy_signal = signal + noise

        # Apply filters
        ma_filtered = moving_average(noisy_signal, window_size=10)
        bw_filtered = butter_lowpass_filter(noisy_signal, cutoff_freq, sample_rate)

        # --- Time Domain Plot ---
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.plot(t, noisy_signal, label='Noisy Signal', alpha=0.6)
        ax1.plot(t, ma_filtered, label='Moving Average', alpha=0.8)
        ax1.plot(t, bw_filtered, label='Butterworth Filtered', linewidth=2)
        ax1.set_title("Signal Filtering Comparison")
        ax1.set_xlabel("Time [s]")
        ax1.set_ylabel("Amplitude")
        ax1.grid(True)
        ax1.legend()
        save_and_show_plot(fig1, "signal_comparison")
        plt.show()

        # --- FFT Plots ---
        def plot_fft(signal, title, filename):
            N = len(signal)
            yf = fft(signal)
            xf = fftfreq(N, 1 / sample_rate)[:N // 2]
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
            ax.set_title(title)
            ax.set_xlabel("Frequency [Hz]")
            ax.set_ylabel("Magnitude")
            ax.grid(True)
            save_and_show_plot(fig, filename)
            plt.show()

        plot_fft(noisy_signal, "Noisy Signal Spectrum", "noisy_fft")
        plot_fft(bw_filtered, "Butterworth Filtered Spectrum", "filtered_fft")

    except Exception as e:
        print(f"Error: {e}")

# --- GUI Layout ---
root = tk.Tk()
root.title("Signal Processing Toolkit")
root.geometry("400x300")

ttk.Label(root, text="Frequency (Hz):").pack()
freq_entry = ttk.Entry(root)
freq_entry.insert(0, "50")  # Default
freq_entry.pack()

ttk.Label(root, text="Duration (seconds):").pack()
duration_entry = ttk.Entry(root)
duration_entry.insert(0, "1.0")
duration_entry.pack()

ttk.Label(root, text="Noise Level (0-1):").pack()
noise_entry = ttk.Entry(root)
noise_entry.insert(0, "0.3")
noise_entry.pack()

ttk.Label(root, text="Low-pass Cutoff Frequency (Hz):").pack()
cutoff_entry = ttk.Entry(root)
cutoff_entry.insert(0, "60")
cutoff_entry.pack()

ttk.Button(root, text="Run Signal Processing", command=run_signal_processing).pack(pady=10)

root.mainloop()
