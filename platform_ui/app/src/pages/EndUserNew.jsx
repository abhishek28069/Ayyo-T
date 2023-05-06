import { FileInput, Group } from "@mantine/core";
import React, { useContext } from "react";
import { supabase } from "../config/supabase";
import { useLocation, useNavigate } from "react-router-dom";
import { v4 as uuidv4 } from "uuid";
import { AuthContext } from "../context/AuthContext";
import { DatePicker } from "@mantine/dates";
import moment from "moment";

const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

const platform_backend_base_url = "http://localhost:3001";
export const EndUserNew = () => {
  const { pathname } = useLocation();
  const { authUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const firstRef = React.useRef();
  const secondRef = React.useRef();
  const thirdRef = React.useRef();
  const [stage, setStage] = React.useState(1);
  const [loading, setLoading] = React.useState(false);
  const [apps, setApps] = React.useState([]);
  const [bindings, setBindings] = React.useState([]);
  const [selectedApp, setSelectedApp] = React.useState({});
  const [selectedGroup, setSelectedGroup] = React.useState();
  const [selectedBinding, setSelectedBinding] = React.useState({});
  const [value, setValue] = React.useState([]); // start date, end date
  const [schedule, setSchedule] = React.useState({
    monday: { start_hour: "", end_hour: "" },
    tuesday: { start_hour: "", end_hour: "" },
    wednesday: { start_hour: "", end_hour: "" },
    thursday: { start_hour: "", end_hour: "" },
    friday: { start_hour: "", end_hour: "" },
    saturday: { start_hour: "", end_hour: "" },
    sunday: { start_hour: "", end_hour: "" },
  });

  const isScheduleValid = () => {
    for (const day in schedule) {
      const { start_hour, end_hour } = schedule[day];
      if (start_hour !== "" && end_hour === "") {
        return false;
      }
    }
    return true;
  };

  const handleApp = async (e) => {
    e.preventDefault();
    setSelectedBinding({});
    setSelectedGroup();
    setLoading(true);
    // fetch groups and filter based on selectedApp
    console.log(selectedApp.app_config);
    if (selectedApp.app_config.sensors["AQI"] !== undefined) {
      setBindings(() => ({
        KH03: {
          AQI: ["SR-AQ-KH03-00", "SR-AQ-KH03-01"],
          SL: ["SR-OC-GW-KH00-00", "SR-OC-GW-KH00-01"],
          EM: ["SR-AC-KH03-00"],
        },
        KH00: {
          AQI: ["SR-AQ-KH00-00", "SR-AQ-KH00-01"],
          SL: ["SR-OC-GW-KH00-00", "SR-OC-GW-KH00-01"],
          EM: ["SR-AC-KH00-00"],
        },
        KH95: {
          AQI: ["SR-AQ-KH95-01", "SR-AQ-KH95-02"],
          SL: ["SR-OC-GW-KH95-00", "SR-OC-GW-KH95-01"],
          EM: ["SR-AC-KH95-01"],
        },
      }));
      setLoading(false);
      secondRef.current.scrollIntoView({ behavior: "smooth" });
      return;
    }
    try {
      const response = await fetch(platform_backend_base_url + "/sensor-bindings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ sensors: selectedApp.app_config.sensors }),
      });
      const result = await response.text();
      setBindings(JSON.parse(result));
    } catch (error) {
      console.log("error", error);
    }
    setLoading(false);
    secondRef.current.scrollIntoView({ behavior: "smooth" });
  };

  const handleSensor = (e) => {
    e.preventDefault();
    if (Object.keys(selectedApp).length === 0) {
      firstRef.current.scrollIntoView({ behavior: "smooth" });
      return;
    }
    thirdRef.current.scrollIntoView({ behavior: "smooth" });
  };

  const handleSchedule = async (e, sched_flag = 1) => {
    e.preventDefault();
    if (Object.keys(selectedApp).length === 0) {
      firstRef.current.scrollIntoView({ behavior: "smooth" });
      return;
    }
    if (Object.keys(selectedBinding).length === 0) {
      secondRef.current.scrollIntoView({ behavior: "smooth" });
      return;
    }
    if (value.length === 0) {
      return;
    }
    if (!isScheduleValid()) {
      console.log("schedule not valid");
      return;
    }
    setLoading(true);
    // build schedule object
    let scheduleJson = {};
    scheduleJson.start_date = value[0];
    if (value[1] === null) {
      scheduleJson.end_date = value[0];
    } else {
      scheduleJson.end_date = value[1];
    }
    scheduleJson.timings = schedule;
    // insert into db
    try {
      const response = await fetch(platform_backend_base_url + "/schedule-app", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          enduser_name: authUser,
          app_id: selectedApp.app_id,
          app_name: selectedApp.app_config.app_name,
          schedule_info: scheduleJson,
          sensor_binding: selectedBinding,
          location: selectedGroup,
          sched_flag: sched_flag,
          user_kill: false,
        }),
      });
      const result = await response.text();
      console.log(result);
    } catch (error) {
      console.log("error", error);
    }
    setLoading(false);
    navigate("/end-user");
  };

  const loadAppData = async () => {
    setApps([]);
    let { data, error } = await supabase.from("apps").select("username,app_id");
    data.map(async (d) => {
      let configPath = d.app_id + "/config.json";
      let { data: config, error } = await supabase.storage.from("public/application").download(configPath);
      console.log(config);
      const reader = new FileReader();
      reader.readAsText(config);
      reader.onload = (event) => {
        const jsonData = event.target.result;
        const parsedData = JSON.parse(jsonData);
        console.log(parsedData);
        let tempAppData = {
          app_config: parsedData,
          app_id: d.app_id,
          app_name: parsedData.app_name,
          app_description: parsedData.app_description,
          developer_name: d.username,
        };
        setApps((value) => [...value, tempAppData]);
      };
    });
  };

  React.useEffect(() => {
    loadAppData();
  }, []);

  // to set the form stage (from chaptgpt)
  const handleScroll = () => {
    const ref1Rect = firstRef.current.getBoundingClientRect();
    const ref2Rect = secondRef.current.getBoundingClientRect();
    const ref3Rect = thirdRef.current.getBoundingClientRect();
    if (ref1Rect.top >= -200 && ref1Rect.bottom <= window.innerHeight + 400) {
      setStage(1);
    } else if (ref2Rect.top >= -200 && ref2Rect.bottom <= window.innerHeight + 400) {
      setStage(2);
    } else if (ref3Rect.top >= -200 && ref3Rect.bottom <= window.innerHeight + 400) {
      setStage(3);
    } else {
      setStage(0);
    }
  };

  return (
    <div className="flex h-screen">
      <div className="w-1/3 bg-[#0d0d0d] flex flex-col items-center justify-center p-10 animate-pulse">
        {stage === 1 && (
          <h1>
            <span className="mr-2 text-7xl">1</span>Choose Your App
          </h1>
        )}
        {stage === 2 && (
          <h1>
            <span className="mr-2 text-7xl">2</span>Select Your Location
          </h1>
        )}
        {stage === 3 && (
          <h1>
            <span className="mr-2 text-7xl">3</span>Schedule Your App
          </h1>
        )}
      </div>

      <div className="flex flex-1 overflow-hidden">
        <div className="flex-1 overflow-y-scroll" onScroll={handleScroll}>
          <div className="bg-[#121212] flex flex-col items-center justify-center p-2">
            <form ref={firstRef} className="flex flex-col justify-center w-5/6 h-screen gap-2 p-6" onSubmit={handleApp}>
              <div className="flex overflow-hidden w-full gap-16 bg-[#0d0d0d] p-10 rounded-lg h-[450px]">
                <div className="grid content-start w-full grid-cols-2 gap-2 overflow-y-scroll no-scrollbar">
                  {/* /* -------------------------------- app grid -------------------------------- */}
                  {apps.map((app) => (
                    <div
                      key={app.app_id}
                      className={`h-24 flex items-center gap-3 p-4 rounded-lg cursor-pointer ${
                        selectedApp?.app_id === app.app_id ? "" : "hover:bg-[#202020]"
                      } active:bg-[#515151] ${selectedApp?.app_id !== app.app_id ? "bg-[#151515]" : "bg-[#515151]"}`}
                      onClick={() => setSelectedApp(app)}
                    >
                      <div className="w-16 h-16 bg-teal-200 rounded-lg shrink-0"></div>
                      <h3 className="w-5/6 p-0 m-0 overflow-hidden grow text-ellipsis">{app.app_name}</h3>
                    </div>
                  ))}
                </div>
              </div>
              <div className="my-4">
                <button
                  type="submit"
                  className={`w-full px-4 py-2 bg-[#94f494] rounded-lg font-bold text-[#0d0d0d] opacity-95 hover:opacity-100 active:scale-[0.99] hover:shadow-lg ${
                    loading ? "animate-pulse opacity-75" : " "
                  }`}
                >
                  Next: Select Location
                </button>
              </div>
            </form>
            <form ref={secondRef} className="flex flex-col justify-center w-5/6 h-screen gap-2 p-6" onSubmit={handleSensor}>
              <div className="flex flex-col items-stretch gap-16 justify-stretch bg-[#0d0d0d] p-10 rounded-lg">
                {/* {JSON.stringify(selectedApp?.app_config.sensors)} */}
                <div key={selectedApp?.app_id} className="flex items-center h-24 gap-3 p-4 rounded-lg">
                  <div className="w-16 h-16 bg-teal-200 rounded-lg shrink-0"></div>
                  <div className="flex flex-col gap-2">
                    <h3 className="w-5/6 p-0 m-0 overflow-hidden grow text-ellipsis">{selectedApp?.app_name}</h3>
                    <p>{selectedApp?.app_description}</p>
                  </div>
                </div>
                <div className="flex gap-2 bg-[#151515] p-4 rounded-lg">
                  <div className="flex flex-col justify-between w-1/2 gap-2">
                    <h3>Required Sensors</h3>
                    {selectedApp?.app_config?.sensors &&
                      Object.entries(selectedApp?.app_config?.sensors).map((s) => (
                        <p key={s[0]}>
                          {s[0]}: {s[1]}
                        </p>
                      ))}
                  </div>
                  <div className="flex flex-col gap-2 flex-1 w-1/2 overflow-hidden h-[300px]">
                    <h3>Suitable Locations</h3>
                    <div className="flex flex-col flex-1 gap-2 overflow-y-scroll no-scrollbar">
                      {Object.keys(bindings).map((group) => (
                        <div
                          key={group}
                          onClick={() => {
                            setSelectedGroup(group);
                            setSelectedBinding(bindings[group]);
                          }}
                          className={`h-16 flex justify-center items-center rounded-lg shrink-0 cursor-pointer ${
                            selectedGroup === group ? "" : "hover:bg-[#202020]"
                          } active:bg-[#515151] ${selectedGroup !== group ? "bg-[#1d1d1d]" : "bg-[#515151]"}`}
                        >
                          <p className={`${selectedGroup === group ? "text-[#94f494]" : " "} text-lg`}>{group}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
                {/* <h1 className="animate-pulse">TODO: use sensor_query service to show locations based on the config</h1> */}
              </div>
              <div className="my-4">
                <button
                  type="submit"
                  className="w-full px-4 py-2 bg-[#94f494] rounded-lg font-bold text-[#0d0d0d] opacity-95 hover:opacity-100 active:scale-[0.99] hover:shadow-lg"
                >
                  Next: Schedule your app
                </button>
              </div>
            </form>
            <form ref={thirdRef} className="flex flex-col justify-center w-5/6 h-screen gap-2 p-6" onSubmit={(e) => handleSchedule(e, 1)}>
              <div className="flex items-stretch gap-16 justify-stretch bg-[#0d0d0d] p-10 rounded-lg">
                <div className="w-1/2">
                  <Group className="bg-[#121212] p-2 rounded" position="center">
                    <DatePicker type="range" value={value} onChange={setValue} size="xl" minDate={new Date()} defaultDate={new Date()} />
                  </Group>
                </div>

                <div className="flex flex-col items-stretch self-stretch w-1/2 gap-5">
                  {days.map((day) => (
                    <div key={day} className="flex items-center gap-2">
                      <label className="w-5/12">{day}:</label>
                      <div className="flex w-full gap-3">
                        <input
                          className="p-2 rounded-lg text-[#0d0d0d] w-1/2"
                          placeholder="Start Hour"
                          max={23}
                          type="time"
                          value={schedule[day.toLowerCase()]["start_hour"]}
                          onChange={(e) =>
                            setSchedule({
                              ...schedule,
                              [day.toLowerCase()]: {
                                ...schedule[day.toLowerCase()],
                                start_hour: moment(e.target.value, "HH:mm").format("HH:mm:ss"),
                              },
                            })
                          }
                        />
                        <input
                          className="p-2 rounded-lg text-[#0d0d0d] w-1/2"
                          placeholder="End Hour"
                          min={schedule[day.toLowerCase()]["start_hour"]}
                          type="time"
                          value={schedule[day.toLowerCase()]["end_hour"]}
                          onChange={(e) =>
                            setSchedule({
                              ...schedule,
                              [day.toLowerCase()]: {
                                ...schedule[day.toLowerCase()],
                                end_hour: moment(event.target.value, "HH:mm").format("HH:mm:ss"),
                              },
                            })
                          }
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <div className="my-4">
                <button
                  type="submit"
                  className="w-full px-4 py-2 bg-[#94f494] rounded-lg font-bold text-[#0d0d0d] opacity-95 hover:opacity-100 active:scale-[0.99] hover:shadow-lg"
                >
                  Schedule
                </button>
              </div>
              <div className="flex items-center justify-center w-full gap-2">
                <div className="flex-grow border-b-2 border-white"></div>
                <div>Or</div>
                <div className="flex-grow border-b-2 border-white"></div>
              </div>
              <div className="my-4">
                <button
                  onClick={(e) => handleSchedule(e, 0)}
                  className={`w-full px-4 py-2 bg-[#94f494] rounded-lg font-bold text-[#0d0d0d] opacity-95 hover:opacity-100 active:scale-[0.99] hover:shadow-lg ${
                    loading ? "animate-pulse opacity-75" : " "
                  }`}
                >
                  Run Now
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
