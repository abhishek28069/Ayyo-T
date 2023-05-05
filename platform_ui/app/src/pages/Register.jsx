import { SegmentedControl } from "@mantine/core";
import React, { useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export const Register = () => {
  const usernameRef = React.useRef();
  const emailRef = React.useRef();
  const passwordRef = React.useRef();
  const [role, setRole] = React.useState("sensor-registrar");

  const { isAuthenticated, login, register, logout, authRole } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleRegister = (e) => {
    e.preventDefault();
    let username = usernameRef?.current?.value;
    let email = emailRef?.current?.value;
    let password = passwordRef?.current?.value;
    console.log(username, email, password, role);
    if (username && email && password && role) {
      register(username, email, password, role);
    }
  };
  React.useEffect(() => {
    if (isAuthenticated) {
      const token = localStorage.getItem("token");
      navigate("/" + authRole, { replace: true });
    }
  }, [isAuthenticated]);
  return (
    <div className="flex h-screen">
      <div className="w-1/3 bg-[#0d0d0d] flex flex-col items-center justify-center p-10"></div>
      <div className="w-2/3 bg-[#121212] flex flex-col items-center justify-center p-10">
        <form className="max-w-lg" onSubmit={handleRegister}>
          <h1 className="my-2">IOT Platform</h1>
          <p className="mb-8 text-base">Welcome to our intuitive iot platform.</p>
          <div className="flex flex-col gap-2 my-2">
            <label className="block">Role</label>
            <SegmentedControl
              value={role}
              onChange={setRole}
              data={["sensor-registrar", "platform-manager", "app-developer", "end-user"]}
              className="text-[#0d0d0d]"
              color="teal"
            />
          </div>
          <div className="flex flex-col gap-2 my-2">
            <label className="block" htmlFor="username">
              Username
            </label>
            <input className="p-2 rounded-lg text-[#0d0d0d]" type="text" name="username" ref={usernameRef} />
          </div>
          <div className="flex flex-col gap-2 my-2">
            <label className="block" htmlFor="email">
              Email
            </label>
            <input className="p-2 rounded-lg text-[#0d0d0d]" type="email" name="email" ref={emailRef} />
          </div>
          <div className="flex flex-col gap-2 my-2">
            <label className="block" htmlFor="password">
              Password
            </label>
            <input className="p-2 rounded-lg text-[#0d0d0d]" type="password" name="password" ref={passwordRef} />
          </div>
          <div className="flex justify-end my-4">
            <p className="text-[#94f494]">Forgot Passsword?</p>
          </div>
          <div className="my-4">
            <button
              type="submit"
              className="w-full px-4 py-2 bg-[#94f494] rounded-lg font-bold text-[#0d0d0d] opacity-95 hover:opacity-100 active:scale-[0.99] hover:shadow-lg"
            >
              Register
            </button>
          </div>
          <Link className="flex justify-center mt-8" to="/login">
            Already have an account? Sign in here
          </Link>
        </form>
      </div>
    </div>
  );
};
