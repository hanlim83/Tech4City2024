import model

model = model.load_model()
results = model(
    "./images/newsmoke2_mp4-19_jpg.rf.a9c891012654fdd371a618ccfdfb591c.jpg", show_conf=True)
for result in results:
    print(result.names)
    for box in result.boxes:
        print(result.names[box.cls.item()])
        print(box.cls.item())
        print(box.conf.item())
        print(str(box.xywh.item()))
    print(result.save(
        "results/newsmoke2_mp4-19_jpg.rf.a9c891012654fdd371a618ccfdfb591c.jpg"))
