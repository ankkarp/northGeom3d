import UploadIcon from "@icons/UploadIcon";
import { useRef } from "react";

import styles from "./ImageInput.module.css";
import Image from "next/image";

const ImageInput = ({ setImageFile, setImageURL, imageURL }) => {
  const inputRef = useRef(null);

  return (
    <div className={styles.container}>
      {imageURL ? (
        <Image
          src={imageURL}
          alt="Загруженное изображение"
          fill={true}
          style={{
            overflow: "hidden",
            borderRadius: "30px",
            objectFit: "cover",
          }}
        />
      ) : (
        <button onClick={(e) => inputRef.current.click()}>
          <input
            className={styles.upload}
            ref={inputRef}
            type="file"
            onChange={(e) => {
              setImageFile(e.target.files[0]);
              setImageURL(URL.createObjectURL(e.target.files[0]));
            }}
            accept=".png,.jpeg,.jpg"
          />
          <UploadIcon width={"200px"} height={"200px"} />
          <p>Загрузите изображение</p>
        </button>
      )}
    </div>
  );
};

export default ImageInput;
