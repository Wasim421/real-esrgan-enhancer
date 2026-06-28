import cv2
import numpy as np
import onnxruntime as ort
from pathlib import Path

class RealESRGANEnhancer:
    def __init__(self, model_path="assets/model.onnx"):
        self.session = None
        self.model_path = model_path

    def load_model(self):
        if Path(self.model_path).exists():
            self.session = ort.InferenceSession(self.model_path)
            return True
        return False

    def enhance_frame(self, frame):
        # Resize to model input size
        h, w = frame.shape[:2]
        inp = cv2.resize(frame, (256, 256))
        inp = inp.astype(np.float32) / 255.0
        inp = np.transpose(inp, (2, 0, 1))
        inp = np.expand_dims(inp, 0)

        if self.session:
            input_name = self.session.get_inputs()[0].name
            out = self.session.run(None, {input_name: inp})[0]
            out = np.squeeze(out, 0)
            out = np.transpose(out, (1, 2, 0))
            out = np.clip(out * 255, 0, 255).astype(np.uint8)
            # Upscale back to original*2
            out = cv2.resize(out, (w * 2, h * 2))
        else:
            # Fallback: OpenCV sharpen + upscale
            out = cv2.resize(frame, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)
            kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
            out = cv2.filter2D(out, -1, kernel)

        return out

    def enhance_video(self, input_path, output_path, progress_callback=None):
        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (w*2, h*2))

        for i in range(total):
            ret, frame = cap.read()
            if not ret:
                break
            enhanced = self.enhance_frame(frame)
            out.write(enhanced)
            if progress_callback:
                progress_callback(int((i+1)/total*100))

        cap.release()
        out.release()
        return output_path
