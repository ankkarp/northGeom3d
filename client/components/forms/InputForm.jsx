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
  const [inputImageURL, setImageURL] = useState(null);
  const [inputImageURL2, setImageURL2] = useState(null);
  const [schema, setSchema] = useState(null);

  const handleClear = (e) => {
    setFile(null);
    setFile2(null);
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
        .post(`upload/test/ply`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((r) => setPoints(r.data))
        .then(() => formData.delete("yaml_file"))
        .post(`upload/test/stl`, formData, {
          headers: {
            "Content-Type": file.type,
          },
        })
        .then((r) => setStlURL(r.data));
      setLoading(true);
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <>
      <ImageInput setImageFile={setImageFile} setImageURL={setImageURL} />
      <ImageInput setImageFile={setImageFile2} setImageURL={setImageURL2} />
      <TextFileInput />
      <div>
        <button onClick={() => handleSubmit()}>Запустить</button>
        <button onClick={() => handleClear()}>Сбросить</button>
      </div>
    </>
  );
}
