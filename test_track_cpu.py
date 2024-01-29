from ultralytics import YOLO

model = YOLO('yolov8s.pt')

results = model.track("car.jpg")

print(results[0].boxes)
