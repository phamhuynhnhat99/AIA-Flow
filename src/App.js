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
  const { setViewport } = useRef();

  const onConnect = (params) => setElements((els) => addEdge(params, els));

  const onElementsRemove = (elementsToRemove) =>
    setElements((els) => removeElements(elementsToRemove, els));

  const onDownload = useCallback(() => {
    if (reactFlowInstance) {
      const flow = reactFlowInstance.toObject();
      var aia_json = JSON.stringify(flow)
      download(aia_json, "aia-flow.json", "text/plain");
    }
  }, [reactFlowInstance]);

  const [files, setFiles] = useState("");
  const onUpload = e => {
    const fileReader = new FileReader();
    fileReader.readAsText(e.target.files[0], "UTF-8");
    fileReader.onload = e => {
      setFiles(e.target.result);
      var flow = JSON.parse(e.target.result);
      if (flow) {
        // console.log(flow.position);
        const x = flow.position["0"];
        const y = flow.position["1"];
        const zoom = flow.position["zoom"];
        setElements(flow.elements || []);
        // setViewport({ x, y, zoom });
      }
    };
  };


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
    let newNode = {
      id: getId(),
      type,
      position,
      data: { label: `${type} node`}
    };
    if (newNode.type === "textInputNode") {
      newNode.data["text"] = "0";
    }

    // console.log(newNode);
    setElements((es) => es.concat(newNode));
  };

  return (
    <div className="dndflow">
      <div>
        <button className="downandup" onClick={onDownload}>Download JSON</button>
        <br />
        <div className="downandup">
          <h5>Upload JSON</h5>
          <input onChange={onUpload} type="file" />
        </div>
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
