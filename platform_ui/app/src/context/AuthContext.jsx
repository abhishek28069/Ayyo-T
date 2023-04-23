import React, { useState, createContext, useEffect } from "react";
const platform_backend_base_url = "http://localhost:3001";

export const AuthContext = createContext();

const AuthContextProvider = (props) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authUser, setAuthUser] = React.useState(false);
  const [authRole, setAuthRole] = React.useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // check if the user is already authenticated
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
      setAuthRole(JSON.parse(token)?.role);
      setAuthUser(JSON.parse(token)?.username);
    }
    setLoading(false);
  }, []);

  const login = async (username, password, role) => {
    try {
      const response = await fetch(platform_backend_base_url + "/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password, role }),
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Authentication Success", data);
        localStorage.setItem("token", JSON.stringify({ username, role }));
        setIsAuthenticated(true);
        setAuthRole(role);
        setAuthUser(username);
      } else {
        throw new Error("Authentication failed");
      }
    } catch (error) {
      console.error(error);
    }
  };

  const register = async (username, email, password, role) => {
    try {
      const response = await fetch(platform_backend_base_url + "/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password, role }),
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Registration Success", data);
        localStorage.setItem("token", JSON.stringify({ username, role }));
        setIsAuthenticated(true);
        setAuthRole(role);
        setAuthUser(username);
      } else {
        throw new Error("Registration failed");
      }
    } catch (error) {
      console.error(error);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    console.log("Logout success");
    setIsAuthenticated(false);
    setAuthRole(false);
    setAuthUser(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, loading, login, register, logout, authUser, authRole }}>
      {!loading && props.children}
    </AuthContext.Provider>
  );
};

export default AuthContextProvider;
