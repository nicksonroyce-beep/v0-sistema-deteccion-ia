import cv2, threading, time
from db import SessionLocal
from models import Evento, Persona
from face_recognition import detect_faces, crop_face, compute_embedding, find_best_match
from config import SIMILARITY_THRESHOLD
from email_notify import send_alert_email

class CameraWorker:
    def __init__(self, source=0, camera_name='CAM', empresa_id=None):
        self.source = source
        self.camera_name = camera_name
        self.empresa_id = empresa_id
        self.frame = None
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
        self.cap = None
        self.last_alert_time = {}

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        if self.cap:
            self.cap.release()
            self.cap = None

    def _loop(self):
        if not self.empresa_id:
            print(f"[CameraWorker] Advertencia: empresa_id es None para cámara {self.camera_name}")
        
        self.cap = cv2.VideoCapture(self.source, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print(f"[CameraWorker] No se pudo abrir la cámara {self.source}")
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        while self.running:
            ok, frame = self.cap.read()
            if not ok:
                time.sleep(0.1)
                continue

            draw = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detect_faces(gray)

            session = SessionLocal()
            try:
                for (x, y, w, h) in faces:
                    face_img = crop_face(frame, (x, y, w, h))
                    emb = compute_embedding(face_img)

                    label = "Desconocido"
                    persona_id = None
                    es_desconocido = True
                    similarity_score = 0.0

                    if emb is not None and self.empresa_id:
                        persona_id, sim = find_best_match(self.empresa_id, emb)
                        similarity_score = sim
                        if persona_id and sim >= SIMILARITY_THRESHOLD:
                            es_desconocido = False
                            p = session.get(Persona, persona_id)
                            label = p.nombre if p else f"ID:{persona_id}"
                            print(f"[CameraWorker] Persona reconocida: {label} (similitud: {sim:.3f})")
                        else:
                            print(f"[CameraWorker] Persona desconocida detectada (similitud: {sim:.3f})")

                    ev = Evento(
                        persona_id=persona_id,
                        label=label,
                        es_desconocido=es_desconocido,
                        similarity=similarity_score,
                        camera=self.camera_name,
                        empresa_id=self.empresa_id
                    )
                    session.add(ev)
                    session.commit()

                    if es_desconocido and self.empresa_id:
                        current_time = time.time()
                        last_alert = self.last_alert_time.get('unknown', 0)
                        if current_time - last_alert > 300:  # 5 minutos entre alertas
                            try:
                                # Obtener email de la empresa
                                from models import Empresa
                                empresa = session.get(Empresa, self.empresa_id)
                                if empresa and empresa.email:
                                    send_alert_email(
                                        empresa.email, 
                                        empresa.nombre, 
                                        self.camera_name,
                                        face_img
                                    )
                                    self.last_alert_time['unknown'] = current_time
                                    print(f"[CameraWorker] Alerta enviada a {empresa.email}")
                            except Exception as e:
                                print(f"[CameraWorker] Error enviando alerta: {e}")

                    color = (0, 255, 0) if not es_desconocido else (0, 0, 255)
                    cv2.rectangle(draw, (x, y), (x+w, y+h), color, 2)
                    display_label = f"{label} ({similarity_score:.2f})" if similarity_score > 0 else label
                    cv2.putText(draw, display_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    
            except Exception as e:
                print(f"[CameraWorker] Error en loop: {e}")
            finally:
                session.close()

            with self.lock:
                self.frame = draw

        if self.cap:
            self.cap.release()
            self.cap = None

    def get_frame(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

def mjpeg_generator(worker):
    while True:
        frame = worker.get_frame()
        if frame is None:
            time.sleep(0.05)
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
