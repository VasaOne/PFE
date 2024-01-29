from ultralytics import YOLO
import torch

torch.cuda.set_device(0)

model = YOLO('yolov8s.pt')

results = model.track("car.jpg", device='gpu')

print(results[0].boxes)
