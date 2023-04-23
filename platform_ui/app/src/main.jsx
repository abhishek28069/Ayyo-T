import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import { BrowserRouter } from "react-router-dom";
import { MantineProvider } from "@mantine/core";
import AuthContextProvider from "./context/AuthContext";

ReactDOM.createRoot(document.getElementById("root")).render(
  <AuthContextProvider>
    <MantineProvider theme={{ colorScheme: 'dark', fontFamily: "Athletics" }}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </MantineProvider>
  </AuthContextProvider>
);
