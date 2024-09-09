import { useRef } from "react";
import styles from "./TextFileInput.module.css";
import UploadIcon from "@icons/UploadIcon";

const TextFileInput = ({ setSchema, schema }) => {
  const inputRef = useRef(null);

  return (
    <div className={styles.container}>
      <div className={styles.button}>
        <button onClick={(e) => inputRef.current.click()}>
          <p>Загрузите оптическую схему</p>
        </button>
        <input
          className={styles.upload}
          ref={inputRef}
          type="file"
          onChange={(e) => {
            setSchema(e.target.files[0]);
          }}
          accept=".yaml,.json"
        />
      </div>
      {schema && (
        <p className={styles.confirm}>{`Файл ${schema.name} загружен`}</p>
      )}
    </div>
  );
};

export default TextFileInput;
