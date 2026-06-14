interface Detection {

  x:number;

  y:number;

  width:number;

  height:number;

  label:string;

  confidence:number;
}

interface Props {

  detections: Detection[];
}

export default function DetectionOverlay({

  detections

}: Props) {

  return (

    <>

      {detections.map((det,index) => (

        <div

          key={index}

          style={{

            position:"absolute",

            left:det.x,

            top:det.y,

            width:det.width,

            height:det.height,

            border:"2px solid red",

            pointerEvents:"none"
          }}
        >

          <div

            style={{

              background:"red",

              color:"white",

              padding:"2px 5px",

              fontSize:"10px"
            }}
          >

            {det.label}

            {" "}

            {(det.confidence*100)
              .toFixed(1)}%

          </div>

        </div>

      ))}

    </>
  );
}