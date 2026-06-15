import { Search } from "lucide-react";

export default function GlobalSearch(){

  return(

    <div
      className="
      relative
      w-[400px]
    "
    >

      <Search
        size={18}
        className="
        absolute
        left-3
        top-3
      "
      />

      <input

        placeholder="
Search UAV / Swarm / Asset
"

        className="
        w-full
        bg-card
        border
        border-border
        rounded-lg
        pl-10
        p-2
      "

      />

    </div>
  );
}