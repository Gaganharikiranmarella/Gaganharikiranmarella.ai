import { useState, useEffect, useRef } from "react";
import { BookOpen, Cpu, Activity, ArrowLeft } from "lucide-react";

// Inline Latex Renderer Component
interface LatexProps {
  math: string;
  block?: boolean;
}

function Latex({ math, block = false }: LatexProps) {
  const containerRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      const katex = (window as any).katex;
      if (katex) {
        try {
          katex.render(math, containerRef.current, {
            displayMode: block,
            throwOnError: false,
          });
        } catch (e) {
          containerRef.current.textContent = math;
        }
      } else {
        containerRef.current.textContent = math;
      }
    }
  }, [math, block]);

  return <span ref={containerRef} className="font-mono text-sky-400" />;
}

export default function Overview() {
  const [activeNode, setActiveNode] = useState<string | null>(null);

  const nodes = {
    input: {
      title: "Video Feed Input (Tensorization & Normalization)",
      desc: "Converts raw RGB video frames from the IP Webcam stream into normalized float tensors. This stage involves frame resizing, channel transposition (HWC to CHW), and pixel value scaling to match the neural network input distribution.",
      metric: "Input Shape: [1, 3, 640, 640] | Normalization: Min-Max Scaling",
      formulaTitle: "Tensorization & Standardization Formulations",
      formulaDesc: "Raw pixel matrices are transformed into standardized input tensors using mean subtraction and variance division:",
      formulas: [
        "X_{tensor} = \\frac{\\frac{X_{raw}}{255.0} - \\mu}{\\sigma}",
        "f_{reshape}: \\mathbb{R}^{H \\times W \\times C} \\to \\mathbb{R}^{1 \\times C \\times H_{target} \\times W_{target}}"
      ]
    },
    yolo: {
      title: "YOLOv8 Object Detection (Deep CNN Inference)",
      desc: "Uses an anchor-free Convolutional Neural Network (CNN) consisting of a DarkNet backbone, a Path Aggregation Network (PANet) neck, and decoupled detection heads. The network outputs bounding box coordinates and classification logits simultaneously.",
      metric: "Backbone: DarkNet-53 | Loss: CIoU + Distribution Focal Loss",
      formulaTitle: "Decoupled Bounding Box Regression & Loss Functions",
      formulaDesc: "The detection head uses Complete IoU (CIoU) loss for spatial alignment, and Distribution Focal Loss (DFL) to model the uncertainty of box boundaries:",
      formulas: [
        "L_{CIoU} = 1 - IoU + \\frac{\\rho^2(b, b^{gt})}{c^2} + \\alpha \\cdot v",
        "L_{DFL}(S_i, S_{i+1}) = -\\left((y_{i+1} - y)\\log(S_i) + (y - y_i)\\log(S_{i+1})\\right)"
      ]
    },
    tracking: {
      title: "DeepSORT Tracking (Kalman Filtering & Deep Association)",
      desc: "Maintains target identity across frames. Uses a linear Kalman Filter for state estimation in a 8D space, and associates new detections using a combination of Mahalanobis motion distance and deep appearance feature cosine similarity.",
      metric: "Feature Extractor: WideResNet | Association: Hungarian Algorithm",
      formulaTitle: "Kalman State Prediction & Appearance Similarity Metric",
      formulaDesc: "The state covariance is predicted, and the cost matrix is computed using both motion statistics and cosine similarity of deep embeddings:",
      formulas: [
        "x_k = F_k x_{k-1} + w_k, \\quad w_k \\sim \\mathcal{N}(0, Q_k)",
        "d^{(2)}(i, j) = 1 - \\frac{r_i \\cdot r_j}{\\|r_i\\| \\|r_j\\|}",
        "c_{i,j} = \\lambda \\cdot d^{(1)}(i,j) + (1-\\lambda) \\cdot d^{(2)}(i,j)"
      ]
    },
    cognitive: {
      title: "Cognitive Threat Engine (DBSCAN & Logit Regression)",
      desc: "Applies unsupervised density-based spatial clustering to group drones into tactical swarms without prior assumptions of cluster shapes. A calibrated logit regression model assesses the threat probability of each target.",
      metric: "Clustering: DBSCAN | Classification: Logistic Probability Calibration",
      formulaTitle: "Epsilon-Neighborhood & Logit Threat Probability",
      formulaDesc: "Swarms are defined as density-connected components. The threat score is mapped to a probability space using a Sigmoid activation function:",
      formulas: [
        "N_{\\epsilon}(p) = \\{q \\in P \\mid \\text{dist}(p, q) \\le \\epsilon\\}",
        "P(\\text{Threat} \\mid x) = \\sigma(w^T \\phi(x) + b) = \\frac{1}{1 + e^{-(w^T \\phi(x) + b)}}"
      ]
    },
    counter: {
      title: "Countermeasures (Reinforcement Learning Policy)",
      desc: "Selects the optimal mitigation action (e.g., jamming, EMP, GPS spoofing) based on the threat state. The decision-making process is modeled as a Markov Decision Process (MDP) solved via policy gradient optimization.",
      metric: "Model: Deep Q-Network (DQN) / PPO | Action Space: Discrete [5]",
      formulaTitle: "Softmax Policy & Policy Gradient Objective",
      formulaDesc: "The mitigation controller parameterizes a probability distribution over actions, maximizing the expected cumulative security reward:",
      formulas: [
        "\\pi_\\theta(a \\mid s) = \\frac{e^{\\theta^T \\phi(s, a)}}{\\sum_{a'} e^{\\theta^T \\phi(s, a')}}",
        "\\nabla_\\theta J(\\theta) = \\mathbb{E}_{\\pi_\\theta} \\left[ \\nabla_\\theta \\log \\pi_\\theta(a \\mid s) \\cdot A^{\\pi_\\theta}(s, a) \\right]"
      ]
    }
  };

  return (
    <div className="p-6 bg-background min-h-screen space-y-6 text-gray-300">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold tracking-wider font-mono text-white flex items-center gap-2">
          <BookOpen className="w-6 h-6 text-sky-400" />
          SYSTEM IDEA & THEORETICAL MODEL
        </h1>
        <p className="text-xs text-gray-400 mt-1 font-mono">
          MATHEMATICAL FORMULATIONS AND PIPELINE ARCHITECTURE
        </p>
      </div>

      {/* Concept Slide */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left 2 Columns: Detailed Explanation (Dynamic) */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-[#121A22]/60 backdrop-blur-md border border-[#243244]/80 rounded-xl p-6 shadow-[0_8px_32px_rgba(0,0,0,0.4)] min-h-[520px] flex flex-col justify-between">
            
            {activeNode ? (
              // Display detail of selected node
              <div className="space-y-6 animate-fadeIn">
                <div className="flex justify-between items-center pb-3 border-b border-[#243244]/50">
                  <div className="flex items-center gap-2">
                    <Activity className="w-5 h-5 text-sky-400 animate-pulse" />
                    <h2 className="text-base font-bold font-mono text-white uppercase">
                      {nodes[activeNode as keyof typeof nodes].title}
                    </h2>
                  </div>
                  <button 
                    onClick={() => setActiveNode(null)}
                    className="flex items-center gap-1 text-xs font-mono text-gray-400 hover:text-white border border-[#243244] bg-[#0B0F14]/40 px-2.5 py-1 rounded transition-colors cursor-pointer"
                  >
                    <ArrowLeft className="w-3.5 h-3.5" />
                    Core Models
                  </button>
                </div>

                <div className="space-y-4">
                  <p className="text-sm leading-relaxed text-gray-300">
                    {nodes[activeNode as keyof typeof nodes].desc}
                  </p>

                  <div className="p-4 rounded-lg bg-[#0B0F14]/50 border border-border/40 text-xs font-mono text-emerald-400">
                    {nodes[activeNode as keyof typeof nodes].metric}
                  </div>

                  <div className="space-y-3 bg-[#0B0F14]/30 p-4 rounded-lg border border-[#243244]/40">
                    <h3 className="text-sm font-semibold text-white font-mono flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-sky-400" />
                      {nodes[activeNode as keyof typeof nodes].formulaTitle}
                    </h3>
                    <p className="text-xs text-gray-400 leading-relaxed">
                      {nodes[activeNode as keyof typeof nodes].formulaDesc}
                    </p>
                    
                    {nodes[activeNode as keyof typeof nodes].formulas.map((formula, idx) => (
                      <div key={idx} className="py-4 flex justify-center bg-black/30 rounded border border-border/50">
                        <Latex math={formula} block />
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              // Default view: Core System Models
              <div className="space-y-6">
                <div className="flex items-center gap-2 pb-3 border-b border-[#243244]/50">
                  <Activity className="w-5 h-5 text-sky-400" />
                  <h2 className="text-base font-bold font-mono text-white uppercase">Core ML & Clustering Models</h2>
                </div>

                <div className="space-y-6">
                  {/* Formula 1 */}
                  <div className="space-y-3 bg-[#0B0F14]/40 p-4 rounded-lg border border-[#243244]/40">
                    <h3 className="text-sm font-semibold text-white font-mono flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-sky-400" />
                      1. Density-Based Swarm Clustering (DBSCAN Model)
                    </h3>
                    <p className="text-xs text-gray-400 leading-relaxed">
                      To isolate coordinated swarms from background noise, we model the drone distribution as a set of core and density-reachable points. A swarm forms when a core point has at least <Latex math="N_{min}" /> neighbors within distance <Latex math="\epsilon" />.
                    </p>
                    <div className="py-4 flex justify-center bg-black/30 rounded border border-border/50">
                      <Latex math="N_{\epsilon}(p) = \{q \in P \mid \text{dist}(p, q) \le \epsilon\}" block />
                    </div>
                    <div className="py-4 flex justify-center bg-black/30 rounded border border-border/50">
                      <Latex math="\text{Density Connected}(p, q) \iff \exists o \in P \text{ s.t. } p \text{ and } q \text{ are density-reachable from } o" block />
                    </div>
                  </div>

                  {/* Formula 2 */}
                  <div className="space-y-3 bg-[#0B0F14]/40 p-4 rounded-lg border border-[#243244]/40">
                    <h3 className="text-sm font-semibold text-white font-mono flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-sky-400" />
                      2. Calibrated Threat Probability Regression
                    </h3>
                    <p className="text-xs text-gray-400 leading-relaxed">
                      We model the threat level as a probability distribution calibrated via a Sigmoid activation over the target's kinematic feature vector <Latex math="\phi(x)" /> (composed of altitude, velocity, and distance to perimeter):
                    </p>
                    <div className="py-4 flex justify-center bg-black/30 rounded border border-border/50">
                      <Latex math="P(\text{Threat} \mid x) = \sigma(w^T \phi(x) + b) = \frac{1}{1 + e^{-(w_1 \cdot \frac{v}{v_{max}} + w_2 \cdot (1 - \frac{h}{h_{max}}) + w_3 \cdot e^{-\lambda d})}}" block />
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div className="text-[10px] text-gray-500 font-mono mt-4 pt-2 border-t border-[#243244]/30">
              * Click on the pipeline nodes on the right to load detailed mathematical formulations for each step.
            </div>
          </div>
        </div>

        {/* Right 1 Column: Interactive Pipeline Architecture */}
        <div className="space-y-6">
          <div className="bg-[#121A22]/60 backdrop-blur-md border border-[#243244]/80 rounded-xl p-5 shadow-[0_8px_32px_rgba(0,0,0,0.4)] h-full flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 mb-4 pb-2 border-b border-[#243244]/50">
                <Cpu className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-bold font-mono tracking-wider text-white uppercase">
                  Pipeline Architecture
                </h3>
              </div>

              {/* Interactive SVG Diagram */}
              <div className="flex flex-col items-center justify-center py-4 bg-[#0B0F14]/50 rounded-xl border border-border/40 p-3">
                <svg className="w-full h-[240px]" viewBox="0 0 200 240">
                  {/* Node 1: Video Input */}
                  <g 
                    className="cursor-pointer group" 
                    onClick={() => setActiveNode("input")}
                  >
                    <rect x="40" y="10" width="120" height="25" rx="4" fill={activeNode === "input" ? "#0284c7" : "#1e293b"} stroke="#0ea5e9" strokeWidth="1" className="transition-colors group-hover:fill-sky-900" />
                    <text x="100" y="26" fill="#fff" fontSize="8" fontFamily="monospace" textAnchor="middle">VIDEO FEED (IP WEBCAM)</text>
                  </g>

                  {/* Arrow 1 */}
                  <path d="M 100 35 L 100 50" stroke="#38bdf8" strokeWidth="1.5" fill="none" />

                  {/* Node 2: YOLO */}
                  <g 
                    className="cursor-pointer group" 
                    onClick={() => setActiveNode("yolo")}
                  >
                    <rect x="40" y="50" width="120" height="25" rx="4" fill={activeNode === "yolo" ? "#0284c7" : "#1e293b"} stroke="#0ea5e9" strokeWidth="1" className="transition-colors group-hover:fill-sky-900" />
                    <text x="100" y="66" fill="#fff" fontSize="8" fontFamily="monospace" textAnchor="middle">YOLOv8 DETECTION</text>
                  </g>

                  {/* Arrow 2 */}
                  <path d="M 100 75 L 100 90" stroke="#38bdf8" strokeWidth="1.5" fill="none" />

                  {/* Node 3: DeepSORT */}
                  <g 
                    className="cursor-pointer group" 
                    onClick={() => setActiveNode("tracking")}
                  >
                    <rect x="40" y="90" width="120" height="25" rx="4" fill={activeNode === "tracking" ? "#0284c7" : "#1e293b"} stroke="#0ea5e9" strokeWidth="1" className="transition-colors group-hover:fill-sky-900" />
                    <text x="100" y="106" fill="#fff" fontSize="8" fontFamily="monospace" textAnchor="middle">DeepSORT TRACKING</text>
                  </g>

                  {/* Arrow 3 */}
                  <path d="M 100 115 L 100 130" stroke="#38bdf8" strokeWidth="1.5" fill="none" />

                  {/* Node 4: Threat Engine */}
                  <g 
                    className="cursor-pointer group" 
                    onClick={() => setActiveNode("cognitive")}
                  >
                    <rect x="40" y="130" width="120" height="25" rx="4" fill={activeNode === "cognitive" ? "#0284c7" : "#1e293b"} stroke="#0ea5e9" strokeWidth="1" className="transition-colors group-hover:fill-sky-900" />
                    <text x="100" y="146" fill="#fff" fontSize="8" fontFamily="monospace" textAnchor="middle">THREAT & CLUSTERING</text>
                  </g>

                  {/* Arrow 4 */}
                  <path d="M 100 155 L 100 170" stroke="#38bdf8" strokeWidth="1.5" fill="none" />

                  {/* Node 5: Countermeasures */}
                  <g 
                    className="cursor-pointer group" 
                    onClick={() => setActiveNode("counter")}
                  >
                    <rect x="40" y="170" width="120" height="25" rx="4" fill={activeNode === "counter" ? "#10b981" : "#1e293b"} stroke="#10b981" strokeWidth="1" className="transition-colors group-hover:fill-emerald-900" />
                    <text x="100" y="186" fill="#fff" fontSize="8" fontFamily="monospace" textAnchor="middle">MITIGATION SYSTEM</text>
                  </g>
                </svg>
                <span className="text-[9px] text-gray-500 font-mono mt-2 animate-pulse">Click nodes to inspect pipeline details</span>
              </div>
            </div>

            <div className="text-[10px] text-gray-500 font-mono mt-4 pt-2 border-t border-[#243244]/30 text-center">
              SCAS PIPELINE DIAGRAM v1.2
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
