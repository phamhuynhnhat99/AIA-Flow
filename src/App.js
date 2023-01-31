import React, { useState, useRef, useCallback } from "react";
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  removeElements,
  useZoomPanHelper,
  Controls
} from "react-flow-renderer";

import "./styles.css";
import InitialElements from "./initialElements";

import exportNodeTypes from "./CustomNodes/exportNodes";
import exportNodeNames from "./CustomNodes/exportNodes";

import Sidebar from "./sidebar.js";

import { v4 as uuid4 } from "uuid";
import axios from 'axios';
// import Popup from 'reactjs-popup';

const getId = () => `dndnode_${+ new Date()}`;

export const nodeTypes = exportNodeTypes.exportNodeTypes
export const nodeNames = exportNodeNames.exportNodeNames



function download(content, fileName, contentType) {
  const a = document.createElement("a");
  const file = new Blob([content], { type: contentType });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
}

const App = () => {
  const reactFlowWrapper = useRef(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [elements, setElements] = useState(InitialElements);
  const onConnect = (params) => setElements((els) => addEdge(params, els));

  const onElementsRemove = (elementsToRemove) =>
    setElements((els) => removeElements(elementsToRemove, els));

  const onBuild = useCallback(() => {
    if (reactFlowInstance) {
      const flow = reactFlowInstance.toObject();
      var aia_json = JSON.stringify(flow)
      const config = { 'content-type': 'application/json' };
      const response = axios.post('http://127.0.0.1:5000/build_graph', flow , config).then(res => {
        if (res.data.status === 'success') {
          alert("Message OK.");
        } else if (res.data.status === 'fail') {
           alert("Message failed to send, please try again.")}
          }); 
      console.log(response.data);
      // download(aia_json, "aia-flow.json", "text/plain");
    }
  }, [reactFlowInstance]);     
  
  const onDownload = useCallback(() => {
    if (reactFlowInstance) {
      const flow = reactFlowInstance.toObject();
      var aia_json = JSON.stringify(flow)
      download(aia_json, "aia-flow.json", "text/plain");
    }
  }, [reactFlowInstance]);

  const { transform } = useZoomPanHelper();
  const [files, setFiles] = useState("");
  const onUpload = useCallback((e) => {
    const fileReader = new FileReader();
    fileReader.readAsText(e.target.files[0], "UTF-8");
    fileReader.onload = e => {
      setFiles(e.target.result);
      var flow = JSON.parse(e.target.result);
      if (flow) {
        const [x = 0, y = 0] = flow.position;
        setElements(flow.elements || []);
        transform({ x, y, zoom: flow.zoom || 0 });
      }
    };
  }, [setElements, transform]);


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
      newNode.data["text"] = "";
    }

    // console.log(newNode);
    setElements((es) => es.concat(newNode));
  };

  return (
    <div className="dndflow">

      <div className="down-up">
      <label className="button-down-up">
          Build Graph
          <button onClick={onBuild} hidden></button>
        </label>
        <label className="button-down-up">
          Download JSON
          <button onClick={onDownload} hidden></button>
        </label>
        <label className="button-down-up">
          Upload JSON
          <input onChange={onUpload} type="file" hidden/>
        </label>
      </div>

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
      
    </div>
  );
}

export default () => {
  return (
    <ReactFlowProvider>
      <App />
    </ReactFlowProvider>
  );
};