import { Audio } from "react-loader-spinner";

export const Loader = ({ visible = false, height = 0, width = 0 }) => {
  // https://mhnpd.github.io/react-loader-spinner/docs/components/audio/
  return (
    <div
      className="loader"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        fontSize: "18px",
      }}
    >
      <Audio
        height={height ? String(height) : "80"}
        width={width ? String(width) : "80"}
        color="#4fa94d"
        ariaLabel="grid-loading"
        wrapperClass=""
        visible={visible}
      />
      <p>Please wait for the analysis ⏳</p>
    </div>
  );
};
