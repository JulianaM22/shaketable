import numpy as np
from shake_table import ShakeTable

def sine_wave(amplitude, frequency, duration, sampling_rate=10000):
    """
    Generate sine wave trajectory data.
    
    amplitude (int): Amplitude of sine wave in steps (not real-world units)
    frequency (float): Frequency of sine wave in Hz
    duration (float): Duration in seconds
    sampling_rate (int): Samples per second
        
    returns: tuple: (time_points, amplitude_points) as numpy arrays
    """
    time_points = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    amplitude_points = amplitude * np.sin(2 * np.pi * frequency * time_points)
    return time_points, amplitude_points


def sine_test(amplitude, frequency, duration):
    """
    Run a sine wave test on the shake table.

    amplitude (int): Amplitude of sine wave in steps
    frequency (float): Frequency of sine wave in Hz
    duration (float): Duration in seconds
    """
    table = ShakeTable()
    time_points, amplitude_points = sine_wave(amplitude, frequency, duration)
    table.run_trajectory(time_points, amplitude_points)