from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = '727557656873534892372'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('terminal.html')

@socketio.on('text update')
def handle_text_update(json, methods=['GET', 'POST']):
    print('received text update: ' + str(json))
    emit('update text', json, broadcast=True)

@socketio.on('run code')
def handle_run_code(json, methods=['GET', 'POST']):
    code = json.get('code', '')
    try:
        result = subprocess.check_output(['python', '-c', code], stderr=subprocess.STDOUT, text=True)
        emit('code result', {'result': result})
    except subprocess.CalledProcessError as e:
        emit('code result', {'result': f"Error: {e.output}"})

if __name__ == '__main__':
    socketio.run(app, debug=True)