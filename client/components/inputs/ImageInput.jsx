import UploadIcon from "@icons/UploadIcon";
import { useRef } from "react";
import styles from "./ImageInput.module.css";

const ImageInput = ({ setImageFile, setInputImageURL }) => {
  const inputRef = useRef(null);

  return (
    <button
      className={styles.container}
      onClick={(e) => handleChoose(e, inputRef)}
    >
      <input
        className={styles.upload}
        ref={inputRef}
        type="file"
        onChange={(e) => {
          setImageFile(e.target.files[0]);
          setInputImageURL(URL.createObjectURL(e.target.files[0]));
        }}
        disabled={inputRef.current}
        accept=".png,.jpeg,.jpg"
      />
      <UploadIcon width={200} height={200} />
      <div className="footer">Загрузите изображение</div>
    </button>
  );
};

export default ImageInput;
