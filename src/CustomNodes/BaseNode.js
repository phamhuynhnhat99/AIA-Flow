import React from "react";

import { Handle } from "react-flow-renderer";

export const baseNode = (data, isConnectable, num_inp, num_out) => {

  let componentInputReturn = [];
  let componentOutputReturn = [];

  const inp_step = 250 / (num_inp + 1)
  const out_step = 250 / (num_out + 1)

  for (let index = 0; index < num_inp; index++) {
    componentInputReturn.push(
      <Handle
        type="target"
        position="top"
        id={"_inp_" + index.toString()}
        style={{ left: inp_step*(index+1), background: "#000000" }}
        onConnect={(params) => console.log("handle onConnect", params)}
        isConnectable={isConnectable}
      />
      );
  }

  for (let index = 0; index < num_out; index++) {
    componentOutputReturn.push(
      <Handle
        type="source"
        position="bottom"
        id={"_out_" + index.toString()}
        style={{ bottom: 7, left: out_step*(index+1), background: "#000000" }}
        isConnectable={isConnectable}
      />
      );
  }

  return (
    <>
      {componentInputReturn}

      <div className="dndnode custom show"> {data.nameNode} </div>

      {componentOutputReturn}
    </>
  );
} 