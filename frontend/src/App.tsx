import { useEffect } from "react";
import { ApplicationShell } from "./components/ApplicationShell";

export default function App() {
  useEffect(() => {
    void import("./legacy");
  }, []);

  return <ApplicationShell />;
}
