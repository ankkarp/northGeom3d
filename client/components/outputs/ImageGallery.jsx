import styles from "./ImageGallery.module.css";

const ImageGallery = ({ namedData }) => {
  return (
    <div className={styles.gallery}>
      {Object.entries(namedData).forEach(([name, images]) => {
        <div>
          <p>{name}</p>
          {Object.entries(images).forEach((imgName, image) => {
              <p>{imgName}</p>
              image
          }}
          </div>;
        })}
    </div>
  );
};

export default ImageGallery;
