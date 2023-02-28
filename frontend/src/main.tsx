import "./index.css";
import ReactDOM from "react-dom/client";
import { store } from "./redux/store.js";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { Routes } from "./enums/routes";
import { Provider } from "react-redux";
import { ErrorPage, HomePage, DashboardPage, LoginPage } from "./routes";
import { ProtectedRoute } from "./components/ProtectedRoute";

const router = createBrowserRouter([
  {
    path: Routes.HOME,
    element: (
      <ProtectedRoute>
        <HomePage />
      </ProtectedRoute>
    ),
    errorElement: (
      <ProtectedRoute>
        <ErrorPage />
      </ProtectedRoute>
    ),
  },
  {
    path: Routes.ROOT,
    element: <LoginPage />,
  },
  {
    path: Routes.YOUTUBE + "/:videoId",
    element: (
      <ProtectedRoute>
        <DashboardPage />
      </ProtectedRoute>
    ),
  },
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </GoogleOAuthProvider>
);
