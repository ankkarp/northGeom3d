import { useState } from "react";
import InputForm from "@forms/InputForm";

export default function Home() {
  const [points, setPoints] = useState();
  const [stlURL, setStlURL] = useState();

  return (
    <main>
      <InputForm setPoints={setPoints} setStlURL={setStlURL} />
    </main>
  );
}
