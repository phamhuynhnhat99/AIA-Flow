import ReadImage from './ReadImage';
import SaveImage from './SaveImage';
import TextInput from './TextInput';
import RemoveBackground from './RemoveBackground';
import Yolov5s from './Yolov5s';

const exportNodeTypes = {
    readImageNode: ReadImage,
    saveImageNode: SaveImage,
    textInputNode: TextInput,
    removeBackgroundNode: RemoveBackground,
    yolov5sNode: Yolov5s
};

const exportNodeNames = {
    readImageNode: "Read Image",
    saveImageNode: "Save Image",
    textInputNode: "Text Input",
    removeBackgroundNode: "Remove Background",
    yolov5sNode: "People Detector"
  };

export default { exportNodeTypes, exportNodeNames };