import { memo } from "react";

import {baseNode} from "./BaseNode";

export default memo(({ isConnectable }) => {
  const nameNode = "Read Image"
  const num_inp = 2;
  const num_out = 1;
  return baseNode(nameNode, isConnectable, num_inp, num_out)
});