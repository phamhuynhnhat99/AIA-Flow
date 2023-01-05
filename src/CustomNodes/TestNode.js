import { memo } from "react";

import {baseNode} from "./BaseNode";

export default memo(({ isConnectable }) => {
  const nameNode = "Test Node"
  const num_inp = 5;
  const num_out = 7;
  return baseNode(nameNode, isConnectable, num_inp, num_out)
});