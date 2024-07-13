import model

model = model.load_model()
results = model("./images/fire2_mp4-68_jpg.rf.8cba43ae545a7f06cd149426135dc6c9.jpg")
for result in results:
    print(result.boxes)
    print(result.masks)
    print(result.keypoints)
    print(result.obb)
    print(result.names)
    print(result.probs)
    print(
        result.save(
            "annotated_images/fire2_mp4-68_jpg.rf.8cba43ae545a7f06cd149426135dc6c9.jpg"
        )
    )
