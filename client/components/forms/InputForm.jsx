import styles from "./InputForm.module.css";

import { useState, useRef } from "react";
import UploadIcon from "@icons/UploadIcon";
import http from "@api/http-common";
import Router from "next/router";
import LoadingIcon from "@icons/LoadingIcon";
import Image from "next/image";
import ImageInput from "@inputs/ImageInput";
import TextFileInput from "@inputs/TextFileInput";

export default function InputForm({ setPoints, setStlURL }) {
  const [loading, setLoading] = useState(false);
  const [imageFile, setImageFile] = useState(null);
  const [imageFile2, setImageFile2] = useState(null);
  const [imageURL, setImageURL] = useState(null);
  const [imageURL2, setImageURL2] = useState(null);
  const [schema, setSchema] = useState(null);

  const handleClear = (e) => {
    setImageFile(null);
    setImageFile2(null);
    setImageURL(null);
    setImageURL2(null);
    setPoints(null);
    setStlURL(null);
  };

  const handleSubmit = () => {
    let formData = new FormData();
    formData.append("image1", imageFile);
    formData.append("image2", imageFile2);
    formData.append("yaml_file", schema);
    try {
      http
        .post(`api/test/ply`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((r) => setPoints(r.data))
        .then(() => setLoading(true));
      // .then(() => formData.delete("yaml_file"));
      http
        .post(`api/test/stl`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob",
        })
        .then((r) => {
          console.log(r.data);
          // const blob = new Blob(r.data, { type: "model/stl" });
          setStlURL(URL.createObjectURL(r.data));
        });
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <div className={styles.form}>
      <ImageInput
        setImageFile={setImageFile}
        setImageURL={setImageURL}
        imageURL={imageURL}
        // inputImageRef={inputImageRef}
      />
      <ImageInput
        setImageFile={setImageFile2}
        setImageURL={setImageURL2}
        imageURL={imageURL2}
        // inputImageRef={inputImageRef2}
      />
      <TextFileInput setSchema={setSchema} schema={schema} />
      <div className={styles.buttons}>
        <button className={styles.submit} onClick={() => handleSubmit()}>
          <p>Запустить</p>
        </button>
        <button className={styles.cancel} onClick={() => handleClear()}>
          <p>Сбросить</p>
        </button>
      </div>
    </div>
  );
}
