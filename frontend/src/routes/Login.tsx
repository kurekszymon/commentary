import { useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { useDispatch } from "react-redux";

import axios from "axios";

import { login } from "../redux/reducers/user";
import { Routes } from "../enums/routes";
import { Button } from "@mui/material";

export const LoginPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        width: "100vw",
      }}
    >
      <div
        style={{
          minWidth: "240px",
          fontSize: "48px",
          backgroundColor: "white",
          borderRadius: "15px",
          width: "30vw",
          height: "30vh",
          display: "flex",
          justifyContent: "space-around",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <p>👋</p>
        <GoogleLogin
          size="medium"
          text="signin"
          shape="pill"
          theme="filled_blue"
          onSuccess={({ credential }) => {
            axios
              .post(`http://${import.meta.env.VITE_SERVER_URL}:5003/google`, {
                credential,
              })
              .then(({ data: user }) => {
                if (user) {
                  dispatch(login(user));
                  navigate(Routes.HOME);
                }
              });
          }}
          onError={() => {
            console.log("Login Failed");
          }}
        />
        <Button
          size={"small"}
          variant={"contained"}
          onClick={() => {
            dispatch(
              login({
                email: "guest123@gmail.com",
                name: "guest123",
                picture: "https://picsum.photos/200",
              })
            );
            navigate(Routes.HOME);
          }}
        >
          Preview as guest
        </Button>
      </div>
    </div>
  );
};
