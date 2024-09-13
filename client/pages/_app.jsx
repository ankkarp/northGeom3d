import "../style.css";
import Head from "next/head";

export const metadata = {
  title: "NorthGeom3D",
  description: "высокоточные 3D измерения геометрии",
};

export default function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>NorthGeom3D - высокоточные 3D измерения геометрии</title>
        <meta name="description" content="Высокоточные измерения геометрии" />
      </Head>
      <header>
        <h1>NorthGeom3D</h1>
        <h2>
          <span>высокоточные</span> измерения геометрии
        </h2>
      </header>
      <Component {...pageProps} />
    </>
  );
}
