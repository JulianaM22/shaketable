import numpy as np

def discretize_waveform_steps(time_array, amplitude_array):
    """
    Converts waveform data into a series of discrete, unit-sized steps (+1 or -1)
    and interpolates the time required for each step.

    Args:
        time_array (np.ndarray): Array of time points.
        amplitude_array (np.ndarray): Array of the signal's amplitude (numbers are in steps NOT REAL WORLD UNITS)

    Returns:
        direction_array (np.ndarray): An array of 1 or -1 for each step.
        time_diff_array (np.ndarray): An array of time durations for each step.
        end_time_array (np.ndarray): The absolute timestamp when each step finished.
    """
    if time_array.shape != amplitude_array.shape or time_array.ndim != 1:
        raise ValueError("Inputs must be 1 dimensional NumPy arrays of the same shape.")
    if time_array.shape != amplitude_array.shape or time_array.ndim != 1:
        raise ValueError("Bad Inputs")
        return None
    values = []

    min_amp = np.floor(np.min(amplitude_array))
    max_amp = np.ceil(np.max(amplitude_array))
    integer_levels = np.arange(min_amp, max_amp + 1) #List of all integers in the waveform

    '''
    SHOULD PROBABLY INTERPOLATE EXTRA VALUES SO THAT THERE IS NOT A CASE OF A +2 or -2 change, etc, that gets marked down as a +1 or -1.
    RIGHT NOW THIS ASSUMES THAT THE SIGNAL HAS A DECENTLY HIGH SAMPLING RATE
    '''
    for level in integer_levels:
        #Find indices where the amplitude crosses level
        increase_indices = np.where((amplitude_array[:-1] < level) & (amplitude_array[1:] >= level))[0]
        
        decrease_indices = np.where((amplitude_array[:-1] > level) & (amplitude_array[1:] <= level))[0]

        #Interpolate the time for each increasing integer crossing
        for i in increase_indices:
            t = np.interp(level, [amplitude_array[i], amplitude_array[i+1]], [time_array[i], time_array[i+1]])
            values.append((t, 1))

        #Interpolate the time for each decreasing integer crossing
        for i in decrease_indices:
            t = np.interp(level, [amplitude_array[i+1], amplitude_array[i]], [time_array[i+1], time_array[i]])
            values.append((t, -1))

    values.sort(key=lambda x: x[0]) #sorts by the time values

    if not values:
        return None

    end_times_list, directions_list = zip(*values)

    end_time_array = np.array(end_times_list)
    direction_array = np.array(directions_list)

    start_times = np.insert(end_time_array[:-1], 0, time_array[0])
    time_diff_array = end_time_array - start_times

    return direction_array, time_diff_array, end_time_array
