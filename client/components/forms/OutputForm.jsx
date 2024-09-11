// import { StlViewer } from "react-stl-viewer";
import React from "react";
import dynamic from "next/dynamic";
import styles from "./OutputForm.module.css";

const OutputForm = ({ stlURL, points }) => {
  const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });
  const data = [
    {
      x: [1, 2, 3, 4, 5],
      y: [2, 3, 4, 5, 6],
      z: [5, 6, 7, 8, 9],
      mode: "markers",
      marker: { size: 2, color: "blue", opacity: 0.8 },
      type: "scatter3d",
    },
  ];

  const layout = {
    title: "3D Scatter Plot Example",
    autosize: true,
    scene: {
      xaxis: { title: "X-axis" },
      yaxis: { title: "Y-axis" },
      zaxis: { title: "Z-axis" },
    },
  };

  return (
    <div className={styles.container}>
      <Plot
        data={data}
        layout={layout}
        style={{ width: "100%", height: "100%" }}
      />
      );
      {/* {stlURL && <StlViewer orbitControls shadows url={stlURL} />} */}
    </div>
  );
};

export default OutputForm;
