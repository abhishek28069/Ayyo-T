import React, { useState } from "react";
import { Button, Modal, useMantineTheme, TextInput, Table, Container } from "@mantine/core";

function SensorRegistrar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isShowSensorType, setIsShowSensorType] = useState(false);
  const [isShowSensor, setIsShowSensor] = useState(false);
  const [isShowData, setIsShowData] = useState(false);
  const [activeButtonIndex, setActiveButtonIndex] = useState(null);
  const [sensorTypes, setSensorTypes] = useState([]);
  const [sensorNodes, setSensorNodes] = useState([]);
  const [sensorData, setSensorData] = useState([]);
  const [signature, setSignature] = useState("");
  const [sensorTypeTextArea, setSensorTypeTextArea] = useState("");
  const [sensorDataTextArea, setSensorDataTextArea] = useState("");

  const theme = useMantineTheme();

  const handleButtonClick = (buttonIndex) => {
    setIsOpen(true);
    setActiveButtonIndex(buttonIndex);
  };

  const handleSensorTypeButton = async () => {
    fetch("http://localhost:3000/sensor/types", {
      method: "GET",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("🧠");
        console.log(data);
        setIsShowSensorType(true);
        setSensorTypes(data["data"]);
        console.log(isShowSensorType);
        console.log(sensorTypes);
      })
      .catch((err) => {});
  };

  const handleSensorNodeButton = async () => {
    console.log(`aaa ${sensorTypeTextArea}`);
    fetch(`http://localhost:3000/sensor/type/nodes/${sensorTypeTextArea}`)
      .then((response) => response.json())
      .then((data) => {
        setIsOpen(false);

        console.log("🧠");
        console.log(data["data"]);
        setIsShowSensorType(false);
        setIsShowSensor(true);
        setSensorNodes(data["data"]);
        setSignature(data["signature"]);
        console.log(isShowSensorType);
        console.log(sensorTypes);
      })
      .catch((err) => {});
  };

  const handleClose = () => {
    setIsOpen(false);
    setActiveButtonIndex(null);
  };

  const getSensorTypes = () => {
    const rows = sensorTypes.map((element) => (
      <tr key={element}>
        <td>{element}</td>
      </tr>
    ));
    return rows;
  };
  const getSensorNodes = () => {
    const rows = sensorNodes?.map((element) => (
      <tr key={element}>
        <td>{element}</td>
      </tr>
    ));
    return rows;
  };
  const getSensorData = () => {
    console.log(typeof sensorData);
    const rows = Object.entries(sensorData).map(([key, value]) => (
      <tr key={key}>
        <td>{value}</td>
      </tr>
    ));
    return rows;
  };

  const handleSensorDataButton = async () => {
    console.log(`🙁 zaza ${sensorDataTextArea}`);
    let temp = sensorDataTextArea;
    console.log(typeof temp);
    fetch(`http://localhost:3000/sensor/data/${sensorDataTextArea}`)
      .then((response) => response.json())
      .then((data) => {
        setIsOpen(false);

        console.log(data);
        console.log("🧠");
        console.log(data["data"]);
        setIsShowSensorType(false);
        setIsShowSensor(false);
        setIsShowData(true);
        setSensorData(data["data"]);
        setActiveButtonIndex(5);
        console.log(isShowSensorType);
        console.log(sensorData);
      })
      .catch((err) => {
        console.log("🤡");
        console.log(err);
      });
  };

  const renderForm = () => {
    switch (activeButtonIndex) {
      case 0:
        return <></>;
        break;
      case 1:
        console.log("SK");
        return (
          <>
            <TextInput
              placeholder="Sensor Type"
              label="Sensor Type"
              radius="lg"
              withAsterisk
              value={sensorTypeTextArea}
              onChange={(event) => setSensorTypeTextArea(event.currentTarget.value)}
            />
            <Button color="teal" radius="md" size="lg" onClick={handleSensorNodeButton}>
              Submit
            </Button>
          </>
        );
        break;
      case 2:
        console.log("OM!OM!");
        return (
          <>
            <TextInput
              placeholder="Sensor Node ID"
              label="Node ID"
              radius="lg"
              withAsterisk
              value={sensorDataTextArea}
              onChange={(event) => setSensorDataTextArea(event.currentTarget.value)}
            />
            <Button color="teal" radius="md" size="lg" onClick={handleSensorDataButton}>
              Submit
            </Button>
          </>
        );
        break;
      default:
        return null;
    }
  };

  const showData = () => {
    if (isShowSensorType) {
      return (
        <Container size="xs">
          <Table>
            <thead>
              <tr>
                <th>Sensor Types</th>
              </tr>
            </thead>
            <tbody>{getSensorTypes()}</tbody>
          </Table>
        </Container>
      );
    } else if (isShowSensor) {
      return (
        <Table>
          <thead>
            <tr>
              <th>Nodes</th>
            </tr>
          </thead>
          <tbody>{getSensorNodes()}</tbody>
        </Table>
      );
    } else if (isShowData) {
      return (
        <Table>
          <thead>
            <tr>{/* <th>Nodes</th> */}</tr>
          </thead>
          <tbody>{getSensorData()}</tbody>
        </Table>
      );
    }
  };

  return (
    <div style={{ padding: theme.spacing.md, marginTop: "50px" }}>
      {/* <> */}
      <Button color="teal" radius="md" size="lg" onClick={() => handleSensorTypeButton()}>
        Show Sensor types
      </Button>
      {/* </> */}
      <Button color="teal" radius="md" size="lg" onClick={() => handleButtonClick(1)}>
        Show Sensor nodes
      </Button>
      <Button color="teal" radius="md" size="lg" onClick={() => handleButtonClick(2)}>
        Get Sensor data
      </Button>
      {/* <Button onClick={() => handleButtonClick(2)}>Button 3</Button> */}

      <Modal title={`Form for Button ${activeButtonIndex + 1}`} opened={isOpen} onClose={handleClose} size="sm">
        {renderForm()}
      </Modal>
      <br />
      {showData()}
    </div>
  );
}

export default SensorRegistrar;
