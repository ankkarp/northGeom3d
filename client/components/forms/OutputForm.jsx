import { StlViewer } from "react-stl-viewer";
import React from "react";
import dynamic from "next/dynamic";
import styles from "./OutputForm.module.css";

const OutputForm = ({ stlURL, points }) => {
  const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

  const layout = {
    title: "3D Scatter Plot Example",
    autosize: true,
    // width: 500,
    // height: 500,
    scene: {
      xaxis: { title: "X-axis", automargin: true },
      yaxis: { title: "Y-axis", automargin: true },
      zaxis: { title: "Z-axis", automargin: true },
    },
  };

  return (
    <div className={styles.container}>
      {points && (
        <Plot
          data={[
            {
              x: points["x"],
              y: points["y"],
              z: points["z"],
              colors: points["colors"],
              mode: "markers",
              marker: { size: 2, color: "blue", opacity: 0.8 },
              type: "scatter3d",
            },
          ]}
          layout={layout}
          className={styles.plot}
        />
      )}
      {stlURL && (
        <StlViewer
          orbitControls
          shadows
          showAxes
          url={stlURL}
          className={styles.stl}
        />
      )}
    </div>
  );
};

export default OutputForm;
