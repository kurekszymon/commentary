import { RootState } from "../redux/store";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router";
import { Routes } from "../enums/routes";

export const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const user = useSelector((state: RootState) => state.user);
  const navigate = useNavigate();

  // TODO use local storage

  if (!user.email) {
    return (
      <div
        style={{
          height: "100vh",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <h1>You are not logged in. 😕</h1>
        <p>
          To log in click{" "}
          <span
            onClick={() => {
              navigate(Routes.ROOT);
            }}
            style={{
              cursor: "pointer",
              color: "blueviolet",
              textDecoration: "underline",
            }}
          >
            here
          </span>
        </p>
      </div>
    );
  }

  return children;
};
