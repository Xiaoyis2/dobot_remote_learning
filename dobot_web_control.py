from flask import Flask, render_template, request, jsonify
from pydobot import Dobot
from serial.tools import list_ports

# Initialize Flask app
app = Flask('WebControl:5000')

# List available ports and connect to Dobot
ports = list_ports.comports()
port = next((port.device for port in ports if "ttyUSB" in port.device), None)
if not port:
    raise Exception("Dobot not found!")

device = Dobot(port=port, verbose=True)

@app.route('/')
def index():
    """Render the main control page."""
    return render_template('index.html')

@app.route('/move_cartesian', methods=['POST'])
def move_cartesian():
    """Move Dobot to the specified Cartesian position."""
    data = request.json
    x, y, z, r = data.get('x'), data.get('y'), data.get('z'), data.get('r')
    device.move_to(x, y, z, r)
    return jsonify({'status': 'success', 'message': 'Cartesian move command sent!'})

@app.route('/move_joint', methods=['POST'])
def move_joint():
    """Move Dobot to the specified joint positions."""
    data = request.json
    j1, j2, j3, j4 = data.get('j1'), data.get('j2'), data.get('j3'), data.get('j4')
    device.move_to(j1, j2, j3, j4, mode='j')
    return jsonify({'status': 'success', 'message': 'Joint move command sent!'})

@app.route('/pose', methods=['GET'])
def pose():
    """Get the current pose of the Dobot."""
    pose = device.pose()
    return jsonify({
        'x': pose[0],
        'y': pose[1],
        'z': pose[2],
        'r': pose[3],
        'j1': pose[4],
        'j2': pose[5],
        'j3': pose[6],
        'j4': pose[7]
    })

@app.route('/home', methods=['POST'])
def home():
    """Send the Dobot to the home position."""
    device.home()
    return jsonify({'status': 'success', 'message': 'Home command sent!'})

@app.route('/suction', methods=['POST'])
def suction():
    """Enable or disable the suction end effector."""
    data = request.json
    enable = data.get('enable', False)
    device.suck(enable)
    return jsonify({'status': 'success', 'message': f'Suction {"enabled" if enable else "disabled"}!'})

@app.route('/connect', methods=['POST'])
def connect():
    """Connect to the Dobot."""
    try:
        global device
        ports = list_ports.comports()
        port = next((port.device for port in ports if "ttyUSB" in port.device), None)
        if not port:
            return jsonify({'status': 'error', 'message': 'No Dobot found!'})
        
        device = Dobot(port=port, verbose=True)
        return jsonify({'status': 'success', 'message': 'Connected to Dobot successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to connect: {str(e)}'})

@app.route('/disconnect', methods=['POST'])
def disconnect():
    """Disconnect from Dobot."""
    device.close()
    return jsonify({'status': 'success', 'message': 'Dobot disconnected!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
