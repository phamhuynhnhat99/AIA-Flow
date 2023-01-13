import torch

class Yolov5sWidget:

    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    def get_predict_df(self, image):
        self.predict_df = self.model(image).pandas().xyxy[0]
        return self.predict_df


class export_widgets:
    
    Yolov5sWidget = Yolov5sWidget


