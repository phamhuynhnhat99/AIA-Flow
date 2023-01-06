import ReadImage from './ReadImage';
import SaveImage from './SaveImage';
import TextInput from './TextInput';
import Yolov5s from './Yolov5s';

const exportNodeTypes = {
    readImageNode: ReadImage,
    saveImageNode: SaveImage,
    textInputNode: TextInput,
    yolov5sNode: Yolov5s

};

const exportNodeNames = {
    readImageNode: "Read Image",
    saveImageNode: "Save Image",
    textInputNode: "Text Input",
    yolov5sNode: "People Detector (Yolov5s)"
  };

export default { exportNodeTypes, exportNodeNames };