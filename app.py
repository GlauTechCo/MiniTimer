
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import threading

app = Flask(__name__)

# Timer state
timer_data = {
    'start_time': None,
    'duration': timedelta(minutes=15),
    'is_running': False
}

lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_timer():
    with lock:
        timer_data['start_time'] = datetime.utcnow()
        timer_data['is_running'] = True
    return jsonify({'status': 'started'})

@app.route('/reset', methods=['POST'])
def reset_timer():
    with lock:
        timer_data['start_time'] = None
        timer_data['is_running'] = False
    return jsonify({'status': 'reset'})

@app.route('/time')
def get_time():
    with lock:
        if timer_data['is_running'] and timer_data['start_time']:
            elapsed = datetime.utcnow() - timer_data['start_time']
            remaining = timer_data['duration'] - elapsed
            if remaining.total_seconds() <= 0:
                remaining = timedelta(seconds=0)
                timer_data['is_running'] = False
        else:
            remaining = timer_data['duration']
    return jsonify({
        'minutes': remaining.seconds // 60,
        'seconds': remaining.seconds % 60
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
