from ultralytics import YOLO

print("Starting training...")

# Load model
model = YOLO("yolov8n.pt")

# Train
model.train(

    data="dataset/data.yaml",

    epochs=100,

    imgsz=640,

    batch=8,

    name="fire_smoke_model"

)

print("Training completed!")