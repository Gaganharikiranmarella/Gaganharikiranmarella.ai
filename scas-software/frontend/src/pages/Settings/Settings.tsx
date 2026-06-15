import ThemeSettings
from "../../components/settings/ThemeSettings";

import SystemSettings
from "../../components/settings/SystemSettings";

export default function Settings(){

  return(

    <div
      className="
      p-5
      bg-background
      min-h-screen
    "
    >

      <h1
        className="
        text-2xl
        font-bold
      "
      >
        System Settings
      </h1>

      <div
        className="
        grid
        grid-cols-2
        gap-5
        mt-5
      "
      >

        <ThemeSettings />

        <SystemSettings />

      </div>

    </div>
  );
}