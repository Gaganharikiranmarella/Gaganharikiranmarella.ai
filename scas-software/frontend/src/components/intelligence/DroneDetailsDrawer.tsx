import { X } from "lucide-react";

interface Props {

  open:boolean;

  onClose:() => void;

  drone:any;
}

export default function DroneDetailsDrawer({

  open,

  onClose,

  drone

}:Props){

  if(!open) return null;

  return(

    <div
      className="
      fixed
      top-0
      right-0
      h-full
      w-[450px]
      bg-card
      border-l
      border-border
      z-50
      p-5
    "
    >

      <div
        className="
        flex
        justify-between
        items-center
      "
      >

        <h2
          className="
          text-xl
          font-bold
        "
        >
          UAV Intelligence
        </h2>

        <button onClick={onClose}>
          <X />
        </button>

      </div>

      <div className="mt-5">

        <div>ID: UAV-017</div>

        <div>Threat: HIGH</div>

        <div>Altitude: 122m</div>

        <div>Velocity: 41km/h</div>

        <div>Swarm: ALPHA</div>

        <div>Status: HOSTILE</div>

      </div>

    </div>
  );
}