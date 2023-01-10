import React, { memo, useState } from "react";

import { Handle } from "react-flow-renderer";

export default memo(({ data, isConnectable }) => {
  data["nameNode"] = "Input";

  const [text, setText] = useState("");

  const onChange = ( e ) => {
    data.text = e.target.value;
    setText(e.target.value);
  }

  return (
    <>
      <div className="dndnode custom input"> 
        {data.nameNode}
        <input 
          type="text"
          value={data.text}
          onChange={
            onChange
          }
        />
      </div>

      <Handle
        type="source"
        position="bottom"
        id={"_out_0"}
        style={{ bottom: 7, left: 125, background: "#555" }}
        isConnectable={isConnectable}
      />
    </>
  );
});