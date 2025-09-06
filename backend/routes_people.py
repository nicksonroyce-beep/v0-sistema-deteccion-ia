# backend/routes_people.py
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from db import SessionLocal
from models import Persona, FaceEmbedding
from face_recognition import compute_embedding
from werkzeug.utils import secure_filename
import numpy as np, json, cv2, os

people_bp = Blueprint('people_bp', __name__, template_folder='../templates')

# Carpeta para guardar fotos
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@people_bp.route('/people', methods=['GET'])
def people_page():
    if 'empresa_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('people.html')


@people_bp.route('/api/people', methods=['GET'])
def list_people():
    if 'empresa_id' not in session:
        return jsonify([]), 401
    empresa_id = session['empresa_id']
    s = SessionLocal()
    try:
        rows = s.query(Persona).filter(Persona.empresa_id == empresa_id).all()
        out = []
        for p in rows:
            out.append({
                'id': p.id,
                'nombre': p.nombre,
                'cargo': p.cargo,
                'employee_id': p.employee_id,
                'embeddings': len(p.embeddings)
            })
        return jsonify(out)
    finally:
        s.close()


@people_bp.route('/api/people', methods=['POST'])
def create_person():
    if 'empresa_id' not in session:
        return jsonify({'ok': False}), 401
    data = request.json
    s = SessionLocal()
    try:
        p = Persona(
            nombre=data.get('nombre') or data.get('full_name'),
            cargo=data.get('cargo'),
            employee_id=data.get('employee_id'),
            empresa_id=session['empresa_id']
        )
        s.add(p)
        s.commit()
        return jsonify({'ok': True, 'id': p.id})
    finally:
        s.close()


@people_bp.route('/api/people/<int:pid>/photo', methods=['POST'])
def upload_face(pid):
    if 'empresa_id' not in session:
        return jsonify({'ok': False}), 401
    
    # Verificar archivo
    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({'ok': False, 'error': 'file missing'}), 400

    # Guardar físicamente la foto
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Leer bytes para embeddings
    img = cv2.imread(filepath)
    if img is None:
        return jsonify({'ok': False, 'error': 'invalid image'}), 400

    emb = compute_embedding(img)
    if emb is None:
        return jsonify({'ok': False, 'error': 'face not found'}), 400

    # Guardar en BD
    s = SessionLocal()
    try:
        p = s.get(Persona, pid)
        if not p or p.empresa_id != session['empresa_id']:
            return jsonify({'ok': False, 'error': 'person not found'}), 404

        fe = FaceEmbedding(person_id=p.id, embedding=json.dumps(list(emb)))
        s.add(fe)
        s.commit()

        return jsonify({'ok': True, 'embedding_id': fe.id, 'file': filename})
    finally:
        s.close()
