import React from "react";
import { Route, Routes } from "react-router-dom";
import { Protected } from "./components/Protected";
import { Layout } from "./components/Layout";
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import { AppDeveloper } from "./pages/AppDeveloper";
import  SensorRegistrar  from "./pages/SensorRegistrar";
import { PlatformManager } from "./pages/PlatformManager";
import { EndUser } from "./pages/EndUser";
import { NotFound } from "./pages/NotFound";
import { ScheduleForm } from "./pages/ScheduleForm";
import { EndUserNew } from "././pages/EndUserNew";

function App() {
  return (
    <Routes>
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
      <Route element={<Protected redirectTo="/login" />}>
        <Route element={<Layout />}>
          <Route path="/" element={<ScheduleForm />} />
          <Route path="/app-developer" element={<AppDeveloper />} />
          <Route path="/sensor-registrar" element={<SensorRegistrar />} />
          <Route path="/platform-manager" element={<PlatformManager />} />
          <Route path="/end-user" element={<EndUser />} />
          <Route path="/end-user/new" element={<EndUserNew />} />
        </Route>
      </Route>
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;
