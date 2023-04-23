import React from "react";
import { Box, Button, Link } from "@chakra-ui/react";

const Navbar = ({ buttonDefinition, buttonName }) => {
  return (
    <Box as="nav" display="flex" justifyContent="flex-end" alignItems="center" gap={4} py={4} px={6} boxShadow="md">
      <Button colorScheme="blue" onClick={buttonDefinition}>
        {buttonName}
      </Button>
      <Button colorScheme="red">
      </Button>
    </Box>
  );
};

export default Navbar;
