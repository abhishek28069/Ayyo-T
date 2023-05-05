import React from "react";
import { supabase } from "../../Utils/db";
import { Switch } from "@chakra-ui/react";

export const Controllers = () => {
  const [data, setData] = React.useState([]);
  const [newData, setNewData] = React.useState("");
  React.useEffect(() => {
    const initializeControllers = async () => {
      let { data: controller_registry, error } = await supabase
        .from("controller_registry")
        .select("*")
        .order("group_name")
        .order("controller_name")
        .order("created_at", { ascending: false });
      setData(() => {
        return controller_registry.map((s) => ({
          type: s.controller_type,
          name: s.controller_name,
          group: s.group_name,
          activated: s.activated,
          id: s.id,
        }));
      });
    };
    initializeControllers();
    const sub = supabase
      .channel("contorller-changes")
      .on("postgres_changes", { event: "*", schema: "public", table: "controller_registry" }, (payload) => {
        console.log("Change received!", payload);
        initializeControllers();
      })
      .subscribe();
    return () => {
      sub.unsubscribe();
    };
  }, []);

  const handleSliderChange = async (e, id) => {
    const state = e.target.checked;
    await supabase.from("controller_registry").update({ activated: state }).eq("id", id);
  };
  return (
    <div className="p-6 no-scrollbar">
      <div className="grid grid-cols-6 gap-4 no-scrollbar" id="cards">
        {data.map((card) => (
          <div key={card.id} className="flex flex-col gap-2 p-4 rounded-md shadow-2xl bg-slate-900">
            <p className="text-2xl">{card.name}</p>
            <p className="text-md">Device Type: {card.type}</p>
            <p className="text-md">Device Location: {card.group}</p>
            <Switch
              size={"lg"}
              isChecked={card.activated}
              onChange={(e) => {
                handleSliderChange(e, card.id);
              }}
            />
          </div>
        ))}
      </div>
    </div>
  );
};
