import React, { useState } from "react";
import { supabase } from "../../Utils/db";
import {
  Container,
  Box,
  Select,
  FormControl,
  FormLabel,
  Input,
  Button,
  Divider,
  Grid,
  Drawer,
  DrawerBody,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
} from "@chakra-ui/react";
import Navbar from "../../Components/Navbar/Navbar";
import DeviceCard from "../../Components/DeviceCard/DeviceCard";
import { Controllers } from "../../Components/Controllers/Controllers";

const onem2m_api_base_url = "http://localhost:8069";
const onem2m_base_url = "http://onem2m_server:5089";

const SensorRegistration = () => {
  const [type, setType] = useState("");
  const [name, setName] = useState("");
  const [group, setGroup] = useState("");
  const [desc, setDesc] = useState("");
  const [cards, setCards] = useState([]);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const types = ["SELECT", "Temperature", "Air Quality", "Solar", "Humidity", "Luminosity", "Power", "Presence", "Lamp", "Buzzer"];

  const description = {
    Temperature: '["Timestamp", "Temperature in celsius"]',
    "Air Quality": '["Timestamp", "Air Quality in PPM"]',
    Solar: '["Timestamp", "Solar Energy Generation in kilowatt-hour"]',
    Humidity: '["Timestamp", "Humidity in percent"]',
    Luminosity: '["Timestamp", "Luminosity in lux"]',
    Power: '["Timestamp", "Power consumption in kilowatt-hour"]',
    Presence: '["Timestamp", "Presence as true/false"]',
    Lamp: '["Timestamp", "Lamp state as on/off"]',
    Buzzer: '["Timestamp", "Buzz command"]',
  };

  const handleTypeChange = (event) => {
    setType(event.target.value);
  };

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handleGroupChange = (event) => {
    setGroup(event.target.value);
  };

  const handleDescChange = (event) => {
    setDesc(event.target.value);
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    createDevice();
  };

  const createDevice = () => {
    console.log(type, name);
    if (type && name) {
      setType("");
      setName("");

      const requestBody = {
        uri_ae: onem2m_base_url + "/~/in-cse/in-name/IIITH/",
        device_name: name,
        device_type: type,
        device_group: group,
        device_description: desc,
        device_labels: [type, group],
        description: description[type],
        data_format: "json",
      };

      fetch(onem2m_api_base_url + "/createdevice", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to create Device");
          }
          return response;
        })
        .then((data) => {
          console.log("Device created successfully:", data);
        })
        .catch((error) => {
          console.error("Failed to create Device:", error);
        });
    }
  };

  const handleDrawerOpen = () => {
    setIsDrawerOpen(true);
  };

  const handleDrawerClose = () => {
    setIsDrawerOpen(false);
  };

  const handleUnplug = (cardToRemove) => {
    const deleteUri = onem2m_api_base_url + `/delete?uri=${onem2m_base_url}/~/in-cse/in-name/IIITH/${cardToRemove.name}`;

    const requestBody = {
      device_name: cardToRemove.name,
      device_type: cardToRemove.type,
      device_group: cardToRemove.group,
    };
    fetch(deleteUri, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to Delete Device");
        }
        return response;
      })
      .then((data) => {
        console.log("Response:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  React.useEffect(() => {
    const initializeCards = async () => {
      let { data: sensor_registry, error } = await supabase.from("sensor_registry").select("*").order("created_at", { ascending: false });
      console.log("updated", sensor_registry);
      setCards(() => {
        return sensor_registry.map((s) => ({
          type: s.sensor_type,
          name: s.sensor_name,
          group: s.group_name,
          desc: s.description,
          activated: s.activated,
          id: s.id,
        }));
      });
    };
    initializeCards();
    const subscription = supabase
      .channel("table-db-changes")
      .on("postgres_changes", { event: "*", schema: "public", table: "sensor_registry" }, async (payload) => {
        initializeCards();
      })
      .subscribe();
    return () => {
      subscription.unsubscribe();
    };
  }, []);

  return (
    <div className="w-screen min-h-screen pt-24 text-blue-200 bg-slate-950 no-scrollbar">
      <Navbar buttonDefinition={handleDrawerOpen} buttonName="Register Sensor" />
      <Box>
        <Drawer isOpen={isDrawerOpen} placement="left" onClose={handleDrawerClose}>
          <DrawerOverlay />
          <DrawerContent>
            <DrawerCloseButton />
            <DrawerHeader>Create New Device</DrawerHeader>
            <DrawerBody>
              <form name="myForm" onSubmit={handleFormSubmit}>
                <FormControl mb={4}>
                  <FormLabel htmlFor="type">Type:</FormLabel>
                  <Select id="type" value={type} onChange={handleTypeChange}>
                    {types.map((type, key) => (
                      <option key={key}>{type}</option>
                    ))}
                  </Select>
                </FormControl>
                <FormControl mb={4}>
                  <FormLabel htmlFor="name">Name:</FormLabel>
                  <Input id="name" value={name} onChange={handleNameChange} required />
                </FormControl>
                <FormControl mb={4}>
                  <FormLabel htmlFor="name">Group:</FormLabel>
                  <Input id="group" value={group} onChange={handleGroupChange} required />
                </FormControl>
                <FormControl mb={4}>
                  <FormLabel htmlFor="desc">Description:</FormLabel>
                  <Input id="desc" value={desc} onChange={handleDescChange} required />
                </FormControl>
                <Button type="submit" colorScheme="blue" mt={2}>
                  Create new device
                </Button>
              </form>
            </DrawerBody>
          </DrawerContent>
        </Drawer>
      </Box>
      <Controllers />
      <div className="p-6 no-scrollbar">
        <div className="grid grid-cols-3 gap-4 no-scrollbar" id="cards">
          {cards.map((card) => (
            <DeviceCard key={card.id} card={card} onUnplug={handleUnplug} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default SensorRegistration;
