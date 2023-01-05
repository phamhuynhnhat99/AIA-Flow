import React, { useState, useRef, useCallback } from "react";
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  removeElements,
  Controls
} from "react-flow-renderer";
import "./styles.css";
import InitialElements from "./initialElements";

import exportNodeTypes from "./CustomNodes/exportNodes";
import exportNodeNames from "./CustomNodes/exportNodes";

import Sidebar from "./sidebar.js";
let id = 0;
const getId = () => `dndnode_${id++}`;

export const nodeTypes = exportNodeTypes.exportNodeTypes
export const nodeNames = exportNodeNames.exportNodeNames


function download(content, fileName, contentType) {
  const a = document.createElement("a");
  const file = new Blob([content], { type: contentType });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
}

export default function App() {
  const reactFlowWrapper = useRef(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [elements, setElements] = useState(InitialElements);
  const onConnect = (params) => setElements((els) => addEdge(params, els));
  const onElementsRemove = (elementsToRemove) =>
    setElements((els) => removeElements(elementsToRemove, els));
  const onSave = useCallback(() => {
    if (reactFlowInstance) {
      const flow = reactFlowInstance.toObject();
      var aia_json = JSON.stringify(flow)
      // console.log(aia_json)
      download(aia_json, "aia-flow.json", "text/plain");
    }
  }, [reactFlowInstance]);
  const onLoad = (_reactFlowInstance) =>
    setReactFlowInstance(_reactFlowInstance);
  const onDragOver = (event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  };
  const onDrop = (event) => {
    event.preventDefault();
    const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
    const type = event.dataTransfer.getData("application/reactflow");
    const position = reactFlowInstance.project({
      x: event.clientX - reactFlowBounds.left,
      y: event.clientY - reactFlowBounds.top
    });
    const newNode = {
      id: getId(),
      type,
      position,
      data: { label: `${type} node` }
    };
    // console.log(newNode);
    setElements((es) => es.concat(newNode));
  };
  return (
    <div className="dndflow">
      <div>
        <button onClick={onSave}>save</button>
      </div>
      <ReactFlowProvider>
        <div
          className="reactflow-wrapper"
          style={{ height: "100vh", width: "500px" }}
          ref={reactFlowWrapper}
        >
          <ReactFlow
            elements={elements}
            onConnect={onConnect}
            onElementsRemove={onElementsRemove}
            onLoad={onLoad}
            onDrop={onDrop}
            onDragOver={onDragOver}
            nodeTypes={nodeTypes}
          >
            <Controls style={{marginBottom: '50vh'}}/>
          </ReactFlow>
        </div>
        <Sidebar nodeTypes= {nodeTypes} nodeNames = {nodeNames} />
      </ReactFlowProvider>
    </div>
  );
}
