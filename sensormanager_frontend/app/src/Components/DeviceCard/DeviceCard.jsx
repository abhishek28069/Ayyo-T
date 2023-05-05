import React, { useState } from "react";
import { Box, Button, HStack } from "@chakra-ui/react";
import { LiveGraph } from "../LiveGraph/LiveGraph";

const DeviceCard = ({ card, onUnplug }) => {
  const [isFetching, setIsFetching] = useState(false);
  const [liveData, setLiveData] = useState("");

  const onem2m_api_base_url = "http://localhost:8069";

  const handleActivate = () => {
    console.log("Activate button pressed for", card.name);

    fetch(onem2m_api_base_url + "/rundevicescript", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ device_type: card.type, device_group: card.group, device_name: card.name, container: card.name + "_data" }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      })
      .catch((error) => {
        console.error("Failed to activate", error);
      });
  };

  const handleDeactivate = () => {
    console.log("Deactivate button pressed for", card.name);

    fetch(onem2m_api_base_url + "/stopdevicescript", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ device_type: card.type, device_group: card.group, device_name: card.name, container: card.name + "_data" }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Response:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleFetchLiveData = () => {
    if (isFetching || !card.activated) {
      setIsFetching(false);
      return;
    } else {
      setIsFetching(true);
    }
  };

  const handleUnplug = () => {
    onUnplug(card);
  };

  return (
    <div key={card.id} className="p-4 rounded-md shadow-2xl bg-slate-800">
      <Box mb={2} fontWeight="bold" fontSize={"1.5rem"}>
        {card.name}
      </Box>
      <Box>Device Type: {card.type}</Box>
      <Box>Device Location: {card.group}</Box>
      <HStack spacing="16px">
        <Box>
          <Button mt={4} colorScheme={card.activated ? "red" : "green"} onClick={card.activated ? handleDeactivate : handleActivate}>
            {card.activated ? "Deactivate" : "Activate"}
          </Button>
        </Box>
        <Box>
          <Button mt={4} colorScheme="red" onClick={() => handleUnplug(card)}>
            Un-Plug
          </Button>
        </Box>
        <Box>
          {!isFetching ? (
            <Button mt={4} colorScheme="blue" onClick={() => handleFetchLiveData(card)}>
              Fetch Live Data
            </Button>
          ) : (
            <Button mt={4} colorScheme="red" onClick={() => handleFetchLiveData(card)}>
              Stop Fetch Live Data
            </Button>
          )}
        </Box>
      </HStack>

      {isFetching && (
        // <Tabs mt={4} variant="enclosed">
        //   <TabPanels>
        //     <TabPanel>
        //       <Box mt={4}>{liveData}</Box>
        //     </TabPanel>
        //   </TabPanels>
        // </Tabs>
        <LiveGraph sensor_name={card.name} />
      )}
    </div>
  );
};

export default DeviceCard;
