from flask import Flask, render_template, request, jsonify
from shake_table.shake_table import ShakeTable
from shake_table.trajectories import sine_wave
import threading

app = Flask(__name__)

app.config['table'] = None
app.config['table_lock'] = threading.Lock()

def get_table():
    """Get or initialize the shake table."""
    if app.config['table'] is None:
        with app.config['table_lock']:
            if app.config['table'] is None:
                print("Initializing ShakeTable...")
                app.config['table'] = ShakeTable()
                print("ShakeTable initialized and calibrated")
    return app.config['table']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_sine', methods=['POST'])
def run_sine():
    data = request.json
    amplitude = int(data.get('amplitude', 250))
    frequency = float(data.get('frequency', 5.0))
    duration = float(data.get('duration', 3.0))
    
    try:
        table = get_table()
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to initialize table: {str(e)}'}), 500
    
    def run_movement():
        with app.config['table_lock']:
            try:
                print(f"Running sine wave: amp={amplitude}, freq={frequency}, dur={duration}")
                time_points, amplitude_points = sine_wave(amplitude, frequency, duration)
                table.run_trajectory(time_points, amplitude_points)
                print("Movement complete")
            except Exception as e:
                print(f"Error during movement: {e}")
    
    movement_thread = threading.Thread(target=run_movement)
    movement_thread.start()
    
    return jsonify({
        'status': 'success',
        'amplitude': amplitude,
        'frequency': frequency,
        'duration': duration
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)