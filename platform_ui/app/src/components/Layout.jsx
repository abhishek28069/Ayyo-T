import React, { useContext } from "react";
import { Outlet } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export const Layout = () => {
  const { logout, authUser } = useContext(AuthContext);

  return (
    <div className="flex flex-col h-screen">
      <div className="absolute top-0 z-10 flex items-center justify-end gap-4 w-full h-12 p-2 px-4 bg-[#212121]">
        <h3 className="text-white">{authUser}</h3>
        <button
              onClick={logout}
              className="p-1 bg-[#94f494] rounded-lg font-bold text-[#0d0d0d] opacity-95 hover:opacity-100 active:scale-[0.99] hover:shadow-lg"
            >
              Logout
            </button>
      </div>

      <Outlet />
    </div>
  );
};
