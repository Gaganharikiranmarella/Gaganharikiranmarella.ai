import Sidebar from "../components/layout/Sidebar";
import Topbar from "../components/layout/Topbar";
import Dashboard from "../pages/Dashboard/Dashboard";

export default function MainLayout() {

  return (
    <div className="flex h-screen">

      <Sidebar />

      <div className="flex flex-col flex-1">

        <Topbar />

        <Dashboard />

      </div>

    </div>
  );
}