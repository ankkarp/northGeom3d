import { useState } from "react";
import InputForm from "@forms/InputForm";
import OutputForm from "@forms/OutputForm";

export default function Home() {
  const [points, setPoints] = useState();
  const [stlURL, setStlURL] = useState();

  return (
    <main>
      <InputForm setPoints={setPoints} setStlURL={setStlURL} />
      <OutputForm points={points} stlURL={stlURL} />
    </main>
  );
}
