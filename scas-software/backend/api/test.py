import os
import shutil
import uuid
from fastapi import APIRouter, File, UploadFile, HTTPException
from detection.yolo_detector import YOLODetector
from database.session import SessionLocal
from database.models import Alert

router = APIRouter(
    prefix="/api/test",
    tags=["Test"]
)

TEMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp_uploads")

@router.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    # Validate the file type extension
    allowed_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.webm')
    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400, 
            detail="Invalid video file format. Supported: MP4, WebM, AVI, MOV, MKV."
        )
    
    # Ensure temporary directory exists
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Create a unique name to prevent collisions during simultaneous uploads
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_file_path = os.path.join(TEMP_DIR, unique_filename)
    
    try:
        # Save file to disk
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Run drone detection tracking
        results = YOLODetector.detect_drones_in_video(temp_file_path)
        if not results:
            raise HTTPException(
                status_code=500, 
                detail="Detection model failed to process video."
            )
            
        # Analyze detection metrics (check for drone swarm threat)
        has_swarm = False
        max_drones = 0
        for frame_idx, detections in results["detections"].items():
            count = len(detections)
            if count > max_drones:
                max_drones = count
            if count >= 3:
                has_swarm = True
                
        # Trigger and store tactical alarm if a swarm is detected
        if has_swarm:
            db = SessionLocal()
            try:
                alert = Alert(
                    severity="CRITICAL" if max_drones >= 3 else "HIGH",
                    message=f"TACTICAL ALERT: Coordinated swarm structure detected in test video. Active targets: {max_drones} UAVs."
                )
                db.add(alert)
                db.commit()
            except Exception as db_err:
                print(f"Error persisting swarm threat alert: {db_err}")
            finally:
                db.close()
                
        return {
            "status": "success",
            "filename": file.filename,
            "fps": results["fps"],
            "frame_count": results["frame_count"],
            "width": results["width"],
            "height": results["height"],
            "detections": results["detections"],
            "max_drones": max_drones,
            "swarm_detected": has_swarm
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error during processing: {str(e)}")
    finally:
        # Clean up saved video file to free disk space
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as cleanup_err:
                print(f"Failed to clean up temp file {temp_file_path}: {cleanup_err}")
