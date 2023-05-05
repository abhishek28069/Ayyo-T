import React from "react";
import { Box, Button } from "@chakra-ui/react";

const Navbar = ({ buttonDefinition, buttonName }) => {
  return (
    <div className="fixed top-0 z-10 w-screen gap-4 px-6 py-4 shadow-2xl bg-slate-900">
      <div className="relative flex items-center justify-between">
        <h1 className="text-xl font-bold">Sensor Registrar Dashboard</h1>
        <h1 className="absolute text-xl font-bold transform -translate-x-1/2 left-1/2">Smart City</h1>
        <Button colorScheme="blue" onClick={buttonDefinition}>
          {buttonName}
        </Button>
      </div>
    </div>
  );
};

export default Navbar;
