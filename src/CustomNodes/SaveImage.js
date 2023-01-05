import { memo } from "react";

import {baseNode} from "./BaseNode";

export default memo(({ isConnectable }) => {
  const nameNode = "Save Image"
  const num_inp = 1;
  const num_out = 0;
  return baseNode(nameNode, isConnectable, num_inp, num_out)
});