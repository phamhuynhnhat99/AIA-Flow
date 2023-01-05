import TestNode from "./TestNode";

import ReadImage from './ReadImage';
import SaveImage from './SaveImage';
import TextInput from './TextInput';
import Yolov5s from './Yolov5s';

const exportNodeTypes = {
    testNode: TestNode,
    readImageNode: ReadImage,
    saveImageNode: SaveImage,
    textInputNode: TextInput,
    yolov5sNode: Yolov5s

};

const exportNodeNames = {
    testNode: "Test Node",
    readImageNode: "Read Image",
    saveImageNode: "Save Image",
    textInputNode: "Text Input",
    yolov5sNode: "People Detector (Yolov5s)"
  };

export default { exportNodeTypes, exportNodeNames };