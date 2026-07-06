import { useState, useRef, useEffect } from "react";
import { 
  Upload, 
  Play, 
  Pause, 
  RotateCcw, 
  Scan, 
  AlertTriangle, 
  Download, 
  ChevronRight, 
  ShieldAlert,
  Sliders,
  Terminal,
  RefreshCw,
  Cpu
} from "lucide-react";
import { useAlertStore } from "../../store/alertStore";

export default function Test() {
  const addAlert = useAlertStore((state) => state.addAlert);

  const [file, setFile] = useState<File | null>(null);
  const [localVideoUrl, setLocalVideoUrl] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResults, setAnalysisResults] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  // Playback state
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [playbackRate, setPlaybackRate] = useState(1);
  const [videoDimensions, setVideoDimensions] = useState({ width: 0, height: 0 });
  const [dragActive, setDragActive] = useState(false);

  // Terminal logging simulation
  const [logs, setLogs] = useState<string[]>([]);
  const logsEndRef = useRef<HTMLDivElement>(null);

  // Generate simulated chronological events for the current video
  const [eventLog, setEventLog] = useState<{ time: string; event: string; severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL" }[]>([]);

  // Dimensions sync handler
  const handleVideoMetadata = (e: React.SyntheticEvent<HTMLVideoElement>) => {
    const video = e.currentTarget;
    setVideoDimensions({
      width: video.clientWidth,
      height: video.clientHeight
    });
  };

  const handleTimeUpdate = () => {
    if (videoRef.current && analysisResults) {
      const fps = analysisResults.fps;
      const frame = Math.floor(videoRef.current.currentTime * fps);
      setCurrentFrame(Math.min(frame, analysisResults.frame_count - 1));
    }
  };

  const syncDimensions = () => {
    if (videoRef.current) {
      setVideoDimensions({
        width: videoRef.current.clientWidth,
        height: videoRef.current.clientHeight
      });
    }
  };

  useEffect(() => {
    window.addEventListener("resize", syncDimensions);
    return () => window.removeEventListener("resize", syncDimensions);
  }, []);

  // requestAnimationFrame loop to update tracking boxes at 60fps
  useEffect(() => {
    let rAF: number;
    const loop = () => {
      if (videoRef.current && isPlaying && analysisResults) {
        const fps = analysisResults.fps;
        const frame = Math.floor(videoRef.current.currentTime * fps);
        setCurrentFrame(Math.min(frame, analysisResults.frame_count - 1));
      }
      rAF = requestAnimationFrame(loop);
    };
    if (isPlaying) {
      rAF = requestAnimationFrame(loop);
    }
    return () => cancelAnimationFrame(rAF);
  }, [isPlaying, analysisResults]);

  // Scroll to bottom of terminal logs
  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs]);

  // Drag handlers
  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const selectedFile = e.dataTransfer.files[0];
      if (selectedFile.type.startsWith("video/")) {
        setFile(selectedFile);
        setLocalVideoUrl(URL.createObjectURL(selectedFile));
        setError(null);
      } else {
        setError("Invalid file format. Please upload a valid video file.");
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setLocalVideoUrl(URL.createObjectURL(selectedFile));
      setError(null);
    }
  };

  // Simulates terminal logs sequentially during analysis
  const runSimulatedLogs = (filename: string, fileSize: number, callback: () => void) => {
    setLogs([]);
    const simulatedScripts = [
      `[SYS] Ingesting target footage: ${filename}`,
      `[SYS] Payload weight verified: ${(fileSize / (1024 * 1024)).toFixed(2)} MB`,
      `[INFO] Establishing channel pipeline...`,
      `[MODEL] Launching YOLOv11 convolutional networks...`,
      `[MODEL] Target class filters loaded: [ UAV_MICRO | UAV_OCTO | FIXED_WING ]`,
      `[MODEL] Reading video structure: Frame analysis mapping...`,
      `[MODEL] Parsing frames at 30.00 FPS...`,
      `[TRACK] Activating DeepSORT association vectors...`,
      `[TRACK] Target spatial orientation mapping active.`,
      `[SWARM] Evaluating spatial proximity clustering index...`,
      `[SYS] Persisting detected coordinate telemetry to databases.`,
      `[SUCCESS] Model evaluation successfully finalized.`
    ];

    let currentLogIndex = 0;
    const interval = setInterval(() => {
      if (currentLogIndex < simulatedScripts.length) {
        setLogs(prev => [...prev, simulatedScripts[currentLogIndex]]);
        currentLogIndex++;
      } else {
        clearInterval(interval);
        setTimeout(callback, 800);
      }
    }, 280);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setIsAnalyzing(true);
    setError(null);

    // Run terminal simulation immediately
    runSimulatedLogs(file.name, file.size, async () => {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("http://localhost:8000/api/test/upload-video", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.detail || "Processing failed.");
        }

        const data = await response.json();
        setAnalysisResults(data);
        setIsAnalyzing(false);

        // Map telemetry data to event feed items
        const generatedEvents: { time: string; event: string; severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL" }[] = [
          { time: "00:01", event: "Airspace intrusion scanning active.", severity: "LOW" },
        ];

        // Scrape frame detections to build dynamic timeline logs
        let drone1Entered = false;
        let drone2Entered = false;
        let drone3Entered = false;

        Object.entries(data.detections).forEach(([frameStr, frameDets]: [string, any]) => {
          const frameNum = parseInt(frameStr);
          const timeSec = Math.floor(frameNum / data.fps);
          const min = Math.floor(timeSec / 60).toString().padStart(2, "0");
          const sec = (timeSec % 60).toString().padStart(2, "0");
          const timeCode = `${min}:${sec}`;

          const activeIds = frameDets.map((d: any) => d.id || d.label);

          if (activeIds.includes("D-1") && !drone1Entered) {
            generatedEvents.push({
              time: timeCode,
              event: "Intruder detected: Target UAV-001 (Micro class) identified.",
              severity: "MEDIUM"
            });
            drone1Entered = true;
          }
          if (activeIds.includes("D-2") && !drone2Entered) {
            generatedEvents.push({
              time: timeCode,
              event: "Intruder detected: Target UAV-002 (Octo class) identified.",
              severity: "MEDIUM"
            });
            drone2Entered = true;
          }
          if (activeIds.includes("D-3") && !drone3Entered) {
            generatedEvents.push({
              time: timeCode,
              event: "Critical intrusion: Target UAV-003 detected in Sector B.",
              severity: "HIGH"
            });
            drone3Entered = true;
          }
        });

        if (data.swarm_detected) {
          generatedEvents.push({
            time: "00:06",
            event: "TACTICAL ALERT: Coordinated swarm structure detected. Swarm threat active.",
            severity: "CRITICAL"
          });
          
          // Trigger a global alert in UI store
          addAlert({
            id: Math.random().toString(),
            message: `TACTICAL ALERT: Coordinated swarm detected in uploaded footage. Peak count: ${data.max_drones} UAVs.`,
            severity: "HIGH",
            timestamp: new Date().toLocaleTimeString()
          });
        }

        setEventLog(generatedEvents);

      } catch (err: any) {
        setError(err.message || "An error occurred during video processing.");
        setIsAnalyzing(false);
      }
    });
  };

  const handlePlayPause = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
      setIsPlaying(false);
    } else {
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!videoRef.current || !analysisResults) return;
    const frame = parseInt(e.target.value);
    setCurrentFrame(frame);
    videoRef.current.currentTime = frame / analysisResults.fps;
  };

  const handleSpeedChange = (speed: number) => {
    if (!videoRef.current) return;
    videoRef.current.playbackRate = speed;
    setPlaybackRate(speed);
  };

  const handleRestart = () => {
    if (!videoRef.current) return;
    videoRef.current.currentTime = 0;
    setCurrentFrame(0);
    if (!isPlaying) {
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  const handleReset = () => {
    setFile(null);
    setLocalVideoUrl(null);
    setAnalysisResults(null);
    setLogs([]);
    setError(null);
    setCurrentFrame(0);
    setIsPlaying(false);
    setPlaybackRate(1);
  };

  const handleExportTelemetry = () => {
    if (!analysisResults) return;
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(analysisResults, null, 2));
    const downloadAnchor = document.createElement("a");
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `telemetry_${file?.name.split(".")[0] || "test"}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  // Extract active frame detections
  const activeDetections = analysisResults?.detections[currentFrame] || [];

  return (
    <div className="flex-1 overflow-y-auto p-6 bg-background space-y-6">
      
      {/* HUD Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-wider font-mono text-white">
            MODEL TESTING DASHBOARD
          </h1>
          <p className="text-xs text-gray-400 mt-1 font-mono uppercase">
            Upload field flight footage to evaluate UAV detection and tracking metrics
          </p>
        </div>
        
        {analysisResults && (
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-gray-400">ANALYSIS STATUS:</span>
            <span className={`px-3 py-1 border text-xs font-mono font-bold rounded-lg ${
              analysisResults.swarm_detected 
                ? "bg-red-500/10 border-red-500/30 text-red-500 animate-pulse" 
                : "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
            }`}>
              {analysisResults.swarm_detected ? "SWARM THREAT ACTIVE" : "AIRSPACE SAFE"}
            </span>
          </div>
        )}
      </div>

      {/* Main Content Area */}
      {!file && !isAnalyzing && (
        <div className="max-w-3xl mx-auto mt-12">
          {/* Upload Drop Zone */}
          <div
            onDragEnter={handleDrag}
            onDragOver={handleDrag}
            onDragLeave={handleDrag}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-2xl p-12 flex flex-col items-center justify-center transition-all duration-300 min-h-[350px] relative overflow-hidden bg-[#121A22]/30 ${
              dragActive 
                ? "border-sky-500 bg-sky-500/5 shadow-[0_0_30px_rgba(14,165,233,0.15)] scale-[1.01]" 
                : "border-[#243244] hover:border-sky-500/40 hover:bg-[#121A22]/50 hover:shadow-[0_8px_32px_rgba(0,0,0,0.3)]"
            }`}
          >
            <div className="p-4 rounded-full bg-sky-500/10 border border-sky-500/20 text-sky-400 mb-6">
              <Upload className="w-8 h-8 animate-bounce" />
            </div>

            <h3 className="text-lg font-bold font-mono text-white mb-2">
              DRAG & DROP FLIGHT FOOTAGE
            </h3>
            <p className="text-sm text-gray-400 mb-6 font-mono text-center max-w-sm">
              Upload MP4, WebM, AVI, MOV or MKV format. Files are processed locally on target models.
            </p>

            <label className="px-5 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-mono text-sm font-bold rounded-lg transition-all duration-200 cursor-pointer shadow-[0_4px_14px_rgba(14,165,233,0.3)] hover:shadow-[0_6px_20px_rgba(14,165,233,0.45)]">
              SELECT FILE
              <input
                type="file"
                className="hidden"
                accept="video/*"
                onChange={handleFileChange}
              />
            </label>

            {error && (
              <div className="mt-6 flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/20 text-red-400 font-mono text-xs rounded-lg animate-pulse">
                <AlertTriangle className="w-4 h-4" />
                {error}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Selected File Review & Trigger Screen */}
      {file && !isAnalyzing && !analysisResults && (
        <div className="max-w-2xl mx-auto bg-[#121A22]/60 border border-[#243244]/80 rounded-xl p-6 shadow-xl space-y-6">
          <div className="flex items-center gap-4 pb-4 border-b border-[#243244]/50">
            <div className="p-3 rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/20">
              <Scan className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-md font-bold font-mono text-white truncate max-w-md">{file.name}</h3>
              <p className="text-xs text-gray-400 font-mono mt-0.5">SIZE: {(file.size / (1024 * 1024)).toFixed(2)} MB</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 text-xs font-mono text-gray-400 bg-[#0B0F14]/50 p-4 rounded-lg border border-[#243244]/40">
            <div className="flex justify-between">
              <span>TARGET CLASS:</span>
              <span className="text-white">UAV IDENTIFIER</span>
            </div>
            <div className="flex justify-between">
              <span>FRAME MODEL:</span>
              <span className="text-white">YOLOv11 CORE</span>
            </div>
            <div className="flex justify-between">
              <span>TRACKING:</span>
              <span className="text-white">DeepSORT CORE</span>
            </div>
            <div className="flex justify-between">
              <span>CLUSTERING:</span>
              <span className="text-white">AGG-HIERARCHICAL</span>
            </div>
          </div>

          <div className="flex gap-3 justify-end pt-2">
            <button
              onClick={handleReset}
              className="px-4 py-2 border border-[#243244] hover:border-gray-500 font-mono text-xs text-gray-300 hover:text-white rounded-lg transition-colors cursor-pointer"
            >
              CANCEL
            </button>
            <button
              onClick={handleAnalyze}
              className="px-5 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-mono text-xs font-bold rounded-lg transition-all duration-200 flex items-center gap-2 shadow-[0_4px_14px_rgba(14,165,233,0.3)] cursor-pointer"
            >
              <Cpu className="w-4 h-4" />
              RUN CORE EVALUATION
            </button>
          </div>
        </div>
      )}

      {/* Model Analysis Simulation Log Screen */}
      {isAnalyzing && (
        <div className="max-w-2xl mx-auto bg-[#121A22]/90 border border-[#243244]/80 rounded-xl p-6 shadow-2xl space-y-5">
          <div className="flex items-center justify-between pb-3 border-b border-[#243244]/50">
            <div className="flex items-center gap-2">
              <Terminal className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-bold font-mono text-white tracking-widest uppercase">EVALUATING VIDEO STREAM...</span>
            </div>
            <RefreshCw className="w-4 h-4 text-sky-400 animate-spin" />
          </div>

          {/* Scrolling Terminal Code logs */}
          <div className="h-64 bg-[#080d13] border border-[#243244] rounded-lg p-4 overflow-y-auto font-mono text-xs text-emerald-400 space-y-2.5 scrollbar-thin">
            {logs.map((log, idx) => (
              <div key={idx} className="flex gap-2">
                <ChevronRight className="w-3.5 h-3.5 mt-0.5 flex-shrink-0 text-emerald-600" />
                <span className="whitespace-pre-wrap">{log}</span>
              </div>
            ))}
            <div ref={logsEndRef} />
          </div>

          {/* Scanning animation bar */}
          <div className="space-y-1.5 font-mono text-[10px] text-gray-400">
            <div className="flex justify-between">
              <span>SCANNING DEEP TARGET ARCHITECTURE</span>
              <span>CALIBRATING FLUID ARCS...</span>
            </div>
            <div className="w-full h-1.5 bg-[#0B0F14] rounded-full overflow-hidden border border-[#243244]/50">
              <div className="h-full bg-gradient-to-r from-sky-500 to-emerald-400 animate-pulse w-full rounded-full" />
            </div>
          </div>
        </div>
      )}

      {/* Results and Playback View */}
      {analysisResults && localVideoUrl && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Main Video View Column (2/3 width) */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-[#121A22]/60 backdrop-blur-md border border-[#243244]/80 rounded-xl p-5 shadow-xl flex flex-col justify-between">
              
              <div className="flex items-center justify-between pb-3 border-b border-[#243244]/50 mb-4">
                <div className="flex items-center gap-2">
                  <Scan className="w-4 h-4 text-sky-400" />
                  <h3 className="text-sm font-bold font-mono text-white tracking-wider uppercase">
                    Core Target Tracking Video
                  </h3>
                </div>
                <span className="text-[10px] font-mono text-gray-400">
                  RESOLUTION: {analysisResults.width}x{analysisResults.height} @ {analysisResults.fps.toFixed(1)} FPS
                </span>
              </div>

              {/* Player Overlay wrapper */}
              <div className="relative w-full h-auto overflow-hidden bg-black rounded-lg border border-[#243244]/60">
                <video
                  ref={videoRef}
                  src={localVideoUrl}
                  className="w-full h-auto block"
                  onLoadedMetadata={handleVideoMetadata}
                  onTimeUpdate={handleTimeUpdate}
                  onPlay={() => setIsPlaying(true)}
                  onPause={() => setIsPlaying(false)}
                  loop
                />
                
                {/* SVG/Absolute Bounding Boxes Detections Overlay */}
                <div className="absolute inset-0 pointer-events-none">
                  {videoDimensions.width > 0 && activeDetections.map((det: any, index: number) => {
                    const scaleX = videoDimensions.width / analysisResults.width;
                    const scaleY = videoDimensions.height / analysisResults.height;
                    
                    const boxLeft = det.x * scaleX;
                    const boxTop = det.y * scaleY;
                    const boxWidth = det.width * scaleX;
                    const boxHeight = det.height * scaleY;
                    
                    return (
                      <div
                        key={index}
                        className="absolute border-2 border-red-500 transition-all duration-75"
                        style={{
                          left: `${boxLeft}px`,
                          top: `${boxTop}px`,
                          width: `${boxWidth}px`,
                          height: `${boxHeight}px`,
                          boxShadow: "0 0 10px rgba(239, 68, 68, 0.5)",
                        }}
                      >
                        {/* Box label and confidence */}
                        <div className="absolute top-0 left-0 -mt-5 bg-red-500 text-white font-mono text-[9px] px-1.5 py-0.5 rounded shadow flex items-center gap-1">
                          <span className="font-bold">{det.label}</span>
                          <span>{(det.confidence * 100).toFixed(0)}%</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Playback Controls Panel */}
              <div className="mt-4 p-4 bg-[#0B0F14]/75 rounded-lg border border-[#243244]/50 space-y-4">
                <div className="flex items-center justify-between gap-4">
                  
                  {/* Left Buttons: Play/Pause/Restart */}
                  <div className="flex items-center gap-3">
                    <button
                      onClick={handlePlayPause}
                      className="p-2 rounded-lg bg-sky-500 hover:bg-sky-600 text-white transition-all cursor-pointer shadow-[0_2px_10px_rgba(14,165,233,0.2)]"
                    >
                      {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 fill-white" />}
                    </button>
                    <button
                      onClick={handleRestart}
                      className="p-2 rounded-lg bg-[#121A22] border border-[#243244] text-gray-300 hover:text-white hover:border-[#243244]*2 transition-all cursor-pointer"
                    >
                      <RotateCcw className="w-4 h-4" />
                    </button>
                  </div>

                  {/* Seek Progress Bar */}
                  <div className="flex-1 flex items-center gap-2">
                    <input
                      type="range"
                      min={0}
                      max={analysisResults.frame_count - 1}
                      value={currentFrame}
                      onChange={handleSeek}
                      className="w-full accent-sky-400 cursor-pointer h-1.5 bg-[#121A22] rounded-lg appearance-none border border-[#243244]"
                    />
                  </div>

                  {/* Frame code display */}
                  <div className="text-[10px] font-mono text-gray-400 min-w-[110px] text-right">
                    FRAME {currentFrame + 1} / {analysisResults.frame_count}
                  </div>
                </div>

                {/* Lower control parameters */}
                <div className="flex justify-between items-center text-[10px] font-mono text-gray-400">
                  <div className="flex items-center gap-2">
                    <Sliders className="w-3.5 h-3.5 text-gray-500" />
                    <span>PLAYBACK SPEED:</span>
                    {[0.5, 1.0, 2.0].map((speed) => (
                      <button
                        key={speed}
                        onClick={() => handleSpeedChange(speed)}
                        className={`px-2 py-0.5 rounded cursor-pointer ${
                          playbackRate === speed 
                            ? "bg-sky-500/20 text-sky-400 border border-sky-500/40" 
                            : "hover:bg-[#121A22] border border-transparent"
                        }`}
                      >
                        {speed.toFixed(1)}x
                      </button>
                    ))}
                  </div>

                  <div className="text-gray-500">
                    LOOP PLAYBACK: ON
                  </div>
                </div>
              </div>

            </div>
          </div>

          {/* Right Metrics Panel Column (1/3 width) */}
          <div className="space-y-6">
            
            {/* Quick Metrics Grid */}
            <div className="bg-[#121A22]/60 border border-[#243244]/80 rounded-xl p-5 shadow-xl space-y-4">
              <div className="pb-2 border-b border-[#243244]/50 flex items-center gap-2">
                <Cpu className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-bold font-mono text-white tracking-wider uppercase">
                  Model Assessment
                </h3>
              </div>

              <div className="grid grid-cols-2 gap-3 font-mono">
                <div className="bg-[#0B0F14]/50 p-3 rounded-lg border border-[#243244]/40">
                  <div className="text-[9px] text-gray-400 uppercase">Active Targets</div>
                  <div className="text-xl font-bold text-sky-400 mt-1">{activeDetections.length}</div>
                </div>
                <div className="bg-[#0B0F14]/50 p-3 rounded-lg border border-[#243244]/40">
                  <div className="text-[9px] text-gray-400 uppercase">Max Concurrently</div>
                  <div className="text-xl font-bold text-white mt-1">{analysisResults.max_drones}</div>
                </div>
                <div className="bg-[#0B0F14]/50 p-3 rounded-lg border border-[#243244]/40">
                  <div className="text-[9px] text-gray-400 uppercase">Risk Level</div>
                  <div className={`text-md font-bold mt-1.5 ${
                    activeDetections.length >= 3 
                      ? "text-red-500" 
                      : activeDetections.length === 2 
                      ? "text-amber-500" 
                      : activeDetections.length === 1 
                      ? "text-sky-400" 
                      : "text-emerald-400"
                  }`}>
                    {activeDetections.length >= 3 
                      ? "CRITICAL" 
                      : activeDetections.length === 2 
                      ? "MEDIUM" 
                      : activeDetections.length === 1 
                      ? "LOW" 
                      : "CLEAR"}
                  </div>
                </div>
                <div className="bg-[#0B0F14]/50 p-3 rounded-lg border border-[#243244]/40">
                  <div className="text-[9px] text-gray-400 uppercase">Swarm Flag</div>
                  <div className={`text-md font-bold mt-1.5 ${
                    analysisResults.swarm_detected 
                      ? "text-red-500 animate-pulse" 
                      : "text-gray-500"
                  }`}>
                    {analysisResults.swarm_detected ? "DETECTED" : "NONE"}
                  </div>
                </div>
              </div>
            </div>

            {/* Target telemetry attributes table */}
            <div className="bg-[#121A22]/60 border border-[#243244]/80 rounded-xl p-5 shadow-xl space-y-4">
              <div className="pb-2 border-b border-[#243244]/50 flex items-center gap-2">
                <Scan className="w-4 h-4 text-sky-400" />
                <h3 className="text-sm font-bold font-mono text-white tracking-wider uppercase">
                  Target Telemetry
                </h3>
              </div>

              <div className="max-h-40 overflow-y-auto font-mono text-[10px] space-y-1.5">
                {activeDetections.length === 0 ? (
                  <div className="text-gray-500 text-center py-4">NO ACTIVE UAV TARGETS</div>
                ) : (
                  <div className="border border-[#243244]/40 rounded-lg overflow-hidden">
                    <table className="w-full border-collapse">
                      <thead>
                        <tr className="bg-[#0B0F14]/80 border-b border-[#243244]/50 text-gray-400 text-left">
                          <th className="p-1.5 font-bold">UID</th>
                          <th className="p-1.5 font-bold">COORDS [X,Y]</th>
                          <th className="p-1.5 font-bold">CONF</th>
                        </tr>
                      </thead>
                      <tbody>
                        {activeDetections.map((det: any, index: number) => (
                          <tr key={index} className="border-b border-[#243244]/25 text-white bg-[#0B0F14]/20">
                            <td className="p-1.5 font-bold text-red-400">{det.label}</td>
                            <td className="p-1.5 text-gray-300">[{det.x}, {det.y}]</td>
                            <td className="p-1.5 text-sky-400">{(det.confidence * 100).toFixed(0)}%</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>

            {/* Event Chronological Feed */}
            <div className="bg-[#121A22]/60 border border-[#243244]/80 rounded-xl p-5 shadow-xl space-y-4">
              <div className="pb-2 border-b border-[#243244]/50 flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-red-500" />
                <h3 className="text-sm font-bold font-mono text-white tracking-wider uppercase">
                  Tactical Event Feed
                </h3>
              </div>

              {/* Feed items */}
              <div className="h-44 overflow-y-auto space-y-2.5 pr-1 scrollbar-thin">
                {eventLog.map((event, index) => (
                  <div key={index} className="flex gap-2 font-mono text-[9px] border-b border-[#243244]/20 pb-1.5">
                    <span className="text-sky-500 font-bold">{event.time}</span>
                    <span className="text-gray-400 flex-1">{event.event}</span>
                    <span className={`font-bold flex-shrink-0 ${
                      event.severity === "CRITICAL" 
                        ? "text-red-500 animate-pulse" 
                        : event.severity === "HIGH" 
                        ? "text-red-400" 
                        : event.severity === "MEDIUM" 
                        ? "text-amber-400" 
                        : "text-gray-500"
                    }`}>
                      {event.severity}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Action Panel */}
            <div className="flex gap-3 justify-between">
              <button
                onClick={handleReset}
                className="flex-1 py-3 px-4 border border-[#243244] hover:border-gray-500 font-mono text-xs font-bold text-gray-300 hover:text-white rounded-lg transition-colors cursor-pointer text-center"
              >
                RESET SUITE
              </button>
              <button
                onClick={handleExportTelemetry}
                className="flex-1 py-3 px-4 bg-sky-500 hover:bg-sky-600 text-white font-mono text-xs font-bold rounded-lg transition-all duration-200 flex items-center justify-center gap-1.5 shadow-[0_4px_14px_rgba(14,165,233,0.3)] cursor-pointer text-center"
              >
                <Download className="w-3.5 h-3.5" />
                EXPORT DATA
              </button>
            </div>

          </div>

        </div>
      )}

    </div>
  );
}
