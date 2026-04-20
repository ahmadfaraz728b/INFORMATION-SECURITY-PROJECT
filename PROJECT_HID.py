import time
import threading
import collections
import statistics
import tkinter as tk
from tkinter import messagebox, scrolledtext
from pynput import keyboard
from datetime import datetime

class HID_Biometric_Shield:
    def __init__(self, root):
        self.root = root
        self.root.title("PUCIT Security - HID Biometric Shield")
        self.root.geometry("750x600")
        self.root.configure(bg="#0d1117")

        # Store typing behavior data
        self.typing_rhythm_history = collections.deque(maxlen=25)
        self.time_of_last_keystroke = None
        self.is_monitoring_active = False
        
        # Thresholds to differentiate human vs automated typing
        self.ROBOTIC_PRECISION_LIMIT = 0.0004   # Very low variance = likely bot
        self.HUMAN_SPEED_THRESHOLD = 0.07       # Extremely fast typing threshold
        
        self.initialize_user_interface()

    def initialize_user_interface(self):
        # Top navigation bar
        nav_bar = tk.Frame(self.root, bg="#161b22", height=60)
        nav_bar.pack(fill="x")
        
        tk.Label(nav_bar, text="BAD USB / HID INJECTION DETECTOR",
                 fg="#58a6ff", bg="#161b22", 
                 font=("Segoe UI", 14, "bold")).pack(pady=15)

        # Main content area
        content = tk.Frame(self.root, bg="#0d1117")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel: live typing stats
        analytics_frame = tk.LabelFrame(content, text=" Real-Time Biometrics ",
                                        fg="#8b949e", bg="#0d1117", font=("Arial", 10))
        analytics_frame.pack(side="left", fill="both", expand=True, padx=5)

        self.display_velocity = self.add_stat_row(analytics_frame, "Typing Velocity:")
        self.display_rhythm = self.add_stat_row(analytics_frame, "Rhythm Variance:")
        self.display_threat = self.add_stat_row(analytics_frame, "Threat Probability:")

        # Right panel: threat indicator
        gauge_frame = tk.LabelFrame(content, text=" Threat Intelligence ",
                                   fg="#8b949e", bg="#0d1117", font=("Arial", 10))
        gauge_frame.pack(side="right", fill="both", expand=True, padx=5)

        self.threat_canvas = tk.Canvas(gauge_frame, width=200, height=120,
                                      bg="#0d1117", highlightthickness=0)
        self.threat_canvas.pack(pady=20)

        self.threat_gauge = self.threat_canvas.create_rectangle(10, 80, 190, 100, fill="#21262d")
        self.threat_level_fill = self.threat_canvas.create_rectangle(10, 80, 10, 100, fill="#238636")
        self.threat_text = self.threat_canvas.create_text(100, 50, text="SAFE",
                                                          fill="#3fb950",
                                                          font=("Arial", 16, "bold"))

        # Audit log section
        tk.Label(self.root, text="SECURITY AUDIT LOG",
                 fg="#8b949e", bg="#0d1117",
                 font=("Arial", 9, "bold")).pack(pady=(10,0))

        self.audit_log = scrolledtext.ScrolledText(self.root, width=80, height=8,
                                                   bg="#010409", fg="#d1d5da",
                                                   font=("Consolas", 10))
        self.audit_log.pack(pady=10, padx=20)

        # Control buttons
        control_frame = tk.Frame(self.root, bg="#0d1117")
        control_frame.pack(fill="x", padx=20, pady=10)

        self.btn_toggle = tk.Button(control_frame,
                                   text="ARM SECURITY SHIELD",
                                   command=self.toggle_security_system,
                                   bg="#238636", fg="white",
                                   font=("Arial", 11, "bold"),
                                   height=2, width=25)
        self.btn_toggle.pack(side="left", padx=5)

        self.btn_simulate = tk.Button(control_frame,
                                     text="SIMULATE ATTACK",
                                     command=self.simulate_injection,
                                     bg="#30363d", fg="white",
                                     font=("Arial", 11),
                                     height=2, width=20)
        self.btn_simulate.pack(side="right", padx=5)

    def add_stat_row(self, parent, label_text):
        row = tk.Frame(parent, bg="#0d1117")
        row.pack(fill="x", pady=12, padx=10)

        tk.Label(row, text=label_text,
                 fg="#8b949e", bg="#0d1117",
                 font=("Arial", 10)).pack(side="left")

        val_label = tk.Label(row, text="Waiting...",
                             fg="#ffffff", bg="#0d1117",
                             font=("Arial", 10, "bold"))
        val_label.pack(side="right")

        return val_label

    def log_incident(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.audit_log.insert(tk.END, f"[{timestamp}] [{level}] {message}\n")
        self.audit_log.see(tk.END)

        # Save logs to file
        with open("security_audit.txt", "a") as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")

    def toggle_security_system(self):
        if not self.is_monitoring_active:
            self.is_monitoring_active = True
            self.btn_toggle.config(text="DISARM SHIELD", bg="#da3633")

            self.log_incident("Biometric Shield activated. Monitoring input patterns.")

            self.listener = keyboard.Listener(on_press=self.capture_input_pattern)
            self.listener.start()
        else:
            self.is_monitoring_active = False
            self.btn_toggle.config(text="ARM SECURITY SHIELD", bg="#238636")

            self.log_incident("System stopped. Monitoring paused.")
            self.listener.stop()

    def capture_input_pattern(self, key):
        current_time = time.time()

        if self.time_of_last_keystroke:
            interval = current_time - self.time_of_last_keystroke
            self.typing_rhythm_history.append(interval)

            self.analyze_behavioral_biometrics()

        self.time_of_last_keystroke = current_time

    def analyze_behavioral_biometrics(self):
        if len(self.typing_rhythm_history) < 12:
            return
        
        rhythm_variance = statistics.variance(self.typing_rhythm_history)
        avg_speed = statistics.mean(self.typing_rhythm_history)
        
        # Simple threat scoring
        threat_score = 0

        if rhythm_variance < self.ROBOTIC_PRECISION_LIMIT:
            threat_score += 50

        if avg_speed < self.HUMAN_SPEED_THRESHOLD:
            threat_score += 50
        
        self.update_live_dashboard(rhythm_variance, avg_speed, threat_score)

        if threat_score >= 100:
            self.execute_mitigation_protocol(rhythm_variance, avg_speed)

    def update_live_dashboard(self, variance, speed, score):
        self.display_rhythm.config(text=f"{variance:.6f}")
        self.display_velocity.config(text=f"{speed:.3f}s")
        self.display_threat.config(text=f"{score}%")
        
        # Update visual threat bar
        fill_width = 10 + (score * 1.8)

        color = "#3fb950" if score < 50 else "#d29922" if score < 100 else "#f85149"
        status_text = "SAFE" if score < 50 else "SUSPICIOUS" if score < 100 else "ATTACK!"

        self.threat_canvas.coords(self.threat_level_fill, 10, 80, fill_width, 100)
        self.threat_canvas.itemconfig(self.threat_level_fill, fill=color)
        self.threat_canvas.itemconfig(self.threat_text, text=status_text, fill=color)

    def execute_mitigation_protocol(self, var, speed):
        self.log_incident(f"Injection detected (variance: {var:.6f})", "CRITICAL")

        messagebox.showerror(
            "SECURITY BREACH",
            "Non-human typing pattern detected.\nInput flagged as malicious."
        )

        self.typing_rhythm_history.clear()

    def simulate_injection(self):
        # Simulate fast, perfectly timed keystrokes (bot-like)
        if not self.is_monitoring_active:
            messagebox.showinfo("System Info", "Please arm the shield first.")
            return

        self.log_incident("Running simulated HID attack...", "WARN")

        start_time = time.time()

        for i in range(15):
            self.capture_input_pattern(None)
            time.sleep(0.01)


if __name__ == "__main__":
    root = tk.Tk()
    app = HID_Biometric_Shield(root)
    root.mainloop()