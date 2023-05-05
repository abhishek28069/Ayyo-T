import React from "react";
import { supabase } from "../../Utils/db";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Card, CardBody, Stat, StatHelpText, StatLabel, StatNumber } from "@chakra-ui/react";

export const LiveGraph = ({ sensor_name }) => {
  const [data, setData] = React.useState([]);
  const [newData, setNewData] = React.useState("");

  React.useEffect(() => {
    const subscription = supabase
      .channel("table-db-changes" + sensor_name)
      .on("postgres_changes", { event: "INSERT", schema: "public", table: "sensor_data" }, (payload) => {
        // console.log("Change received!", payload);
        if (payload?.new?.sensor_name === sensor_name) {
          let value = JSON.parse(payload?.new?.data)[1];
          let timestamp = JSON.parse(payload?.new?.data)[0];
          console.log(sensor_name, timestamp, value);
          setNewData(value);
          setData((data) => [...data.slice(-10), { timestamp, value }]);
        }
      })
      .subscribe();
    return () => {
      console.log("disconnect from subscription, ", sensor_name);
      subscription.unsubscribe();
    };
  }, []);

  return (
    <>
      <ResponsiveContainer height={250} className={"bg-slate-700 mt-4 rounded-lg"}>
        <LineChart data={data}>
          <Tooltip />
          <YAxis />
          <Line type="basisOpen" dataKey="value" stroke="#8884d8" strokeWidth={3} activeDot={false} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </>
  );
};
