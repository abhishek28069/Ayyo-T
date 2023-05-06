import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { supabase } from "../config/supabase";
import { Table } from "@mantine/core";
import { Link } from "react-router-dom";

export const EndUser = () => {
  const { authUser } = useContext(AuthContext);
  const [instances, setInstances] = React.useState([]);
  const platform_backend_base_url = "http://localhost:3001";

  const rows = instances.map((element) => {
    if (element.location && element.app_id && element.instance_id) {
      return (
        <tr key={element.instance_id}>
          <td>{element.instance_id}</td>
          <td>{element.app_id}</td>
          <td>{element.app_name}</td>
          <td>{element.location}</td>
          <td>{element.status}</td>
          <td>
            <button onClick={() => kill(element)}>kill</button>
          </td>
          <td>
            {element.port && element.status !== "stopped" && (
              <a
                key={element.instance_id}
                className="p-1 px-2 text-white bg-blue-400 rounded"
                target="_blank"
                href={`http://localhost:${element.port}`}
              >
                Link
              </a>
            )}
          </td>
        </tr>
      );
    }
  });

  const kill = async (row) => {
    try {
      const response = await fetch(platform_backend_base_url + "/schedule-app", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          enduser_name: authUser,
          app_id: row.app_id,
          instance_id: row.instance_id,
          app_name: row.app_name,
          user_kill: true,
        }),
      });
      const result = await response.text();
      console.log(result);
    } catch (error) {
      console.log("error", error);
    }
  };

  const fetchAppStates = async () => {
    let { data: scheduled_apps, error } = await supabase.from("scheduled_apps").select("*").eq("enduser_name", authUser);
    console.log(scheduled_apps);
    if (scheduled_apps.length > 0) {
      let inst = await Promise.all(
        scheduled_apps.map(async (i) => {
          let { data: app_instances, error } = await supabase.from("app_instance_states").select("*").eq("instance_id", i.instance_id);
          console.log(app_instances);
          return { ...app_instances[0], location: i.location };
        })
      );
      setInstances(inst);
    }
  };

  React.useEffect(() => {
    fetchAppStates();
    const appInstanceStates = supabase
      .channel("app-states" + authUser)
      .on("postgres_changes", { event: "*", schema: "public", table: "app_instance_states" }, async (payload) => {
        console.log("Change received!", payload);
        await fetchAppStates();
      })
      .subscribe();
    return () => {
      appInstanceStates.unsubscribe();
    };
  }, []);
  return (
    <div className="p-8 mt-12">
      <Link className="float-left bg-[#94f494] rounded-lg font-bold text-[#0d0d0d] px-4 py-1 my-4" to="/end-user/new">
        Schedule an App
      </Link>
      <Table highlightOnHover fontSize={"md"}>
        <thead>
          <tr>
            <th style={{ color: "#94f494", "font-size": "18px" }}>App Instance</th>
            <th style={{ color: "#94f494", "font-size": "18px" }}>App Id</th>
            <th style={{ color: "#94f494", "font-size": "18px" }}>App Name</th>
            <th style={{ color: "#94f494", "font-size": "18px" }}>Location</th>
            <th style={{ color: "#94f494", "font-size": "18px" }}>Status</th>
            <th style={{ color: "#94f494", "font-size": "18px" }}>Kills</th>
            <th style={{ color: "#94f494", "font-size": "18px" }}></th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </Table>
    </div>
  );
};
