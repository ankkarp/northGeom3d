import { StlViewer } from "react-stl-viewer";

const OutputForm = ({ stlURL, points }) => {
  return (
    <div>
      {/* {stlURL && <StlViewer orbitControls shadows url={stlURL} />} */}
      {points && <div dangerouslySetInnerHTML={{ __html: points }} />}
    </div>
  );
};

export default OutputForm;
