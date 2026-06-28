import Sidebar from "../components/layout/Sidebar";
import Topbar from "../components/layout/Topbar";
import AppRoutes from "../routes/AppRoutes";

export default function MainLayout() {
  return (
    <div className="flex h-screen bg-background text-foreground">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Topbar />
        <main className="flex-1 overflow-y-auto">
          <AppRoutes />
        </main>
      </div>
    </div>
  );
}