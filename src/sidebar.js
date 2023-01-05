import React from "react";

export default ({ nodeTypes, nodeNames }) => {

  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData("application/reactflow", nodeType);
    event.dataTransfer.effectAllowed = "move";
  };


  const mapNodeName = (nameNode) => {
    return Object.keys(nodeNames).map((key) => nameNode === key ? nodeNames[key] : '');
  }


  return (
    <aside>
      <div className="description">
        You can drag these nodes to the pane on the right.
      </div>


      {
        Object.keys(nodeTypes).map((key) => {
          return (
            <div
              key={key}
              className="dndnode custom"
              onDragStart={(event) => onDragStart(event, key)}
              draggable
            >
              {mapNodeName(key)}
            </div>
          );
        })
      }

      {/* <div
        className="dndnode input"
        onDragStart={(event) => onDragStart(event, "input")}
        draggable
      >
        Input Node
      </div>
      <div
        className="dndnode"
        onDragStart={(event) => onDragStart(event, "default")}
        draggable
      >
        Default Node
      </div>

      <div
        className="dndnode output"
        onDragStart={(event) => onDragStart(event, "output")}
        draggable
      >
        Output Node
      </div> */}

    </aside>
  );
};
