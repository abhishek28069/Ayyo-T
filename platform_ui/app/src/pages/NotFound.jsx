import React from "react";
import { Link } from "react-router-dom";

export const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen font-bold">
      <p className="text-9xl">Not Found</p>
      <Link className="text-6xl hover:text-7xl transition-all duration-100 text-[#94f494]" to="/login">
        Go Home ↗️
      </Link>
    </div>
  );
};