from ultralytics import YOLO

model = YOLO("yolo11s.pt")
trt_model = model.export(format="engine")