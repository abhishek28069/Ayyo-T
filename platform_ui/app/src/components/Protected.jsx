import React, { useContext } from "react";
import { Outlet, Navigate, useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export const Protected = ({ redirectTo }) => {
  const { isAuthenticated, authRole } = useContext(AuthContext);
  const { pathname } = useLocation();
  const token = localStorage.getItem("token");
  const path_list = {
    "sensor-registrar": ["sensor-registrar"],
    "app-developer": ["app-developer"],
    "platform-manager": ["platform-manager"],
    "end-user": ["end-user", "end-user/new"],
  };
  return isAuthenticated && path_list[authRole].includes(pathname.slice(1)) ? <Outlet /> : <Navigate to={redirectTo} />;
  // return <Outlet />;
};
