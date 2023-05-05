import { useEffect, useState } from "react";
import myData from "./bindings.json";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  const [bind, setBind] = useState([]);
  const [data, setData] = useState("");
  const [selected, setSelected] = useState("");
  let loadDataFromJson = (event) => {
    console.log("clicked on load data");
    // fetch("bindings.json")
    //   .then((resp) => resp.json())
    //   .then((data) => setBind(data));
    console.log(myData);
    setBind(myData);
  };
  // return (
  //   <div className="App">
  //     <h1>Sample App</h1>
  //     <button onClick={loadDataFromJson}>load data</button>
  //     <ul>{Object.keys(myData).map(key=><li key={key}> {myData[key]}</li>)}</ul>
  //   </div>
  // );
  const fetchData = (sensorName) => {
    const requestOptions = {
      method: "GET",
      redirect: "follow",
    };
    console.log("inside fetch");
    console.log(sensorName);
    fetch(
      `http://localhost:2000/api/sensor/latestdata?sensor_id=${sensorName}`,
      // `https://catfact.ninja/fact`,
      requestOptions
    )
      .then((response) => response.text())
      .then((result) => {
        console.log("result is " + result);
        setData(result);
        setSelected(sensorName);
      })
      .catch((error) => console.log("error", error));
  };
  return (
    <div className="text-center">
      {Object.keys(myData).map((key) => (
        <div key={key}>
          <h3>{key}</h3>
          <ul>
            {myData[key].map((value) => (
              <li key={value}>
                <button className="btn btn-primary" onClick={() => fetchData(value)}>
                  {value}
                </button>
                <br></br>
                {selected === value ? (
                  <div>
                    <span>{data}</span>
                  </div>
                ) : (
                  ""
                )}
                <br />
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
export default App;
