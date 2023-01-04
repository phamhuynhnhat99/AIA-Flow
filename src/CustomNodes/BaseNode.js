import React from "react";

import { Handle } from "react-flow-renderer";

export const baseNode = (nameNode, isConnectable, num_inp, num_out) => {

  let componentInputReturn = [];
  let componentOutputReturn = [];


  for (let index = 0; index < num_inp; index++) {
    componentInputReturn.push(
      <Handle
      key={index}
      type="target"
      position="top"
      style={{ left: 30*(index+1), background: "#555" }}
      onConnect={(params) => console.log("handle onConnect", params)}
      isConnectable={isConnectable}
    />
      );
  }

  for (let index = 0; index < num_out; index++) {
    componentOutputReturn.push(
    <Handle
      key={index}
      type="source"
      position="bottom"
      id="a"
      style={{ bottom: 7, left: 30*(index+1), background: "#555" }}
      isConnectable={isConnectable}
    />);
  }

  return (
    <>
      {componentInputReturn}

      <div className="dndnode custom"> {nameNode} </div>

      {componentOutputReturn}
    </>
  );
} 