import { memo } from "react";

import {baseNode} from "./BaseNode";

export default memo(({ isConnectable }) => {
  const nameNode = "Text Input"
  const num_inp = 0;
  const num_out = 1;
  return baseNode(nameNode, isConnectable, num_inp, num_out)
});