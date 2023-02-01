import { memo } from "react";

import {baseNode} from "./BaseNode";

export default memo(({ data, isConnectable }) => {
  data["nameNode"] = "Remove Background";
  const num_inp = 1;
  const num_out = 1;
  return baseNode(data, isConnectable, num_inp, num_out)
});