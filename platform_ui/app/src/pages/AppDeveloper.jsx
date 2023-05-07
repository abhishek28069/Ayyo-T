import { FileInput } from "@mantine/core";
import React, { useContext } from "react";
import { supabase } from "../config/supabase";
import { useLocation } from "react-router-dom";
import { v4 as uuidv4 } from "uuid";
import { AuthContext } from "../context/AuthContext";
import { validateJSON } from "../utils/validateJson";

const platform_backend_base_url = "http://localhost:3001";

export const AppDeveloper = () => {
  const [zip, setZip] = React.useState(null);
  const [config, setConfig] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const { pathname } = useLocation();
  const { authUser } = useContext(AuthContext);

  const upload = async (e) => {
    e.preventDefault();
    setLoading(true);
    if (!zip && !config) {
      return;
    }
    // todo validate json
    const formData = new FormData();
    formData.append("zip", zip);
    formData.append("config", config);
    formData.append("authUser", authUser); // assuming authUser is defined
    try {
      const response = await fetch(platform_backend_base_url + "/upload-files", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        console.log("File upload successful");
        alert("File upload successful");
        // Handle success
      } else {
        console.log("File upload failed");
        alert("File upload failed");
      }
    } catch (error) {
      console.log("File upload failed", error);
      alert("File upload failed", error);
    }
    setLoading(false);
  };

  React.useEffect(() => {
    console.log(pathname);
  });

  return (
    <div className="flex h-screen">
      <div className="w-1/3 bg-[#0d0d0d] flex flex-col items-center justify-center p-10">
        <h1 className="my-2">
          <span className="mr-2 text-7xl">1</span>Upload files
        </h1>
      </div>
      <div className="w-2/3 bg-[#121212] flex flex-col items-center justify-center p-10">
        <form className="max-w-lg" onSubmit={upload}>
          <div className="flex flex-col gap-2 my-2">
            <label htmlFor="zip" className="inline-block">
              Application Zip
            </label>
            <input
              onChange={(e) => setZip(e.target.files[0])}
              className="relative m-0 block w-full min-w-0 flex-auto rounded border border-solid border-neutral-300 bg-clip-padding px-3 py-[0.32rem] text-base font-normal text-neutral-700 transition duration-300 ease-in-out file:cursor-pointer file:-mx-3 file:-my-[0.32rem] file:overflow-hidden file:rounded-none file:border-0 file:border-solid file:border-inherit file:bg-neutral-100 file:px-3 file:py-[0.32rem] file:text-neutral-700 file:transition file:duration-150 file:ease-in-out file:[border-inline-end-width:1px] file:[margin-inline-end:0.75rem] hover:file:bg-neutral-200 focus:border-primary focus:text-neutral-700 focus:shadow-te-primary focus:outline-none"
              type="file"
              id="zip"
            />
          </div>
          <div className="flex flex-col gap-2 my-2">
            <label htmlFor="config" className="inline-block">
              Config Json
            </label>
            <input
              onChange={(e) => setConfig(e.target.files[0])}
              className="relative m-0 block w-full min-w-0 flex-auto rounded border border-solid border-neutral-300 bg-clip-padding px-3 py-[0.32rem] text-base font-normal text-neutral-700 transition duration-300 ease-in-out file:cursor-pointer file:-mx-3 file:-my-[0.32rem] file:overflow-hidden file:rounded-none file:border-0 file:border-solid file:border-inherit file:bg-neutral-100 file:px-3 file:py-[0.32rem] file:text-neutral-700 file:transition file:duration-150 file:ease-in-out file:[border-inline-end-width:1px] file:[margin-inline-end:0.75rem] hover:file:bg-neutral-200 focus:border-primary focus:text-neutral-700 focus:shadow-te-primary focus:outline-none"
              type="file"
              id="config"
            />
          </div>
          <div className="my-4">
            <button
              type="submit"
              className={`w-full px-4 py-2 bg-[#94f494] rounded-lg font-bold text-[#0d0d0d] opacity-95 hover:opacity-100 active:scale-[0.99] hover:shadow-lg ${
                loading ? "animate-pulse opacity-75" : " "
              }`}
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
