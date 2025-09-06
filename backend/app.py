from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from auth import auth_bp
from routes_people import people_bp
from routes_events import events_bp
from db import engine, Base
from config import SECRET_KEY
from detection import CameraWorker, mjpeg_generator
import os

Base.metadata.create_all(bind=engine)

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '../static')
)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

# Guardar workers activos dinámicamente
workers = {}

app.register_blueprint(auth_bp)
app.register_blueprint(people_bp)
app.register_blueprint(events_bp)

@app.route('/')
def index():
    if 'empresa_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('index.html', empresa=session.get('empresa_nombre',''))

@app.route('/profile')
def profile():
    if 'empresa_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('profile.html', empresa=session.get('empresa_nombre',''))

@app.route('/about')
def about():
    if 'empresa_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('about.html', empresa=session.get('empresa_nombre',''))

@app.route('/instructions')
def instructions():
    if 'empresa_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('instructions.html', empresa=session.get('empresa_nombre',''))

@app.route('/stream/<int:cam_id>')
def stream(cam_id):
    if 'empresa_id' not in session:
        return redirect(url_for('auth.login'))
    
    worker_key = f"{session['empresa_id']}_{cam_id}"
    
    if worker_key not in workers:
        workers[worker_key] = CameraWorker(
            source=cam_id, 
            camera_name=f"CAM{cam_id}", 
            empresa_id=session['empresa_id']  # Esto es clave para el reconocimiento
        )
        workers[worker_key].start()

    worker = workers[worker_key]
    return app.response_class(
        mjpeg_generator(worker),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/api/cameras')
def get_cameras():
    if 'empresa_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    # Simular múltiples cámaras disponibles
    cameras = [
        {'id': 0, 'name': 'Cámara Principal', 'status': 'active'},
        {'id': 1, 'name': 'Cámara Entrada', 'status': 'active'},
        {'id': 2, 'name': 'Cámara Salida', 'status': 'inactive'},
        {'id': 3, 'name': 'Cámara Parking', 'status': 'inactive'}
    ]
    return jsonify(cameras)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



#hdhdhd#