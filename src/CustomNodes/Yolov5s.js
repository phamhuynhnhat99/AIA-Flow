import { memo } from "react";

import {baseNode} from "./BaseNode";

export default memo(({ data , isConnectable }) => {
  data["nameNode"] = "People Detector (Yolov5s)";
  const num_inp = 2;
  const num_out = 1;
  return baseNode(data, isConnectable, num_inp, num_out)
});