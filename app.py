import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import time
import threading

# ==========================================
# 🛰️ AUTOMATED ANTI-SLEEP ENGINE (KEEPALIVE)
# ==========================================
def background_ping():
    """Background loop that executes internal pings to maintain resource engagement."""
    while True:
        # Internal minimal heartbeat calculation to keep the engine hot
        _ = np.sin(time.time())
        time.sleep(600)  # Runs quietly every 10 minutes

# Initialize the keep-alive thread globally so it persists across user sessions
if "keep_alive_active" not in st.session_state:
    st.session_state.keep_alive_active = True
    threading.Thread(target=background_ping, daemon=True).start()

# ==========================================
# 🔬 STREAMLIT PAGE CONFIGURATIONS & LAYOUT
# ==========================================
st.set_page_config(
    page_title="Virtual Physics Lab Suite",
    page_icon="🔬",
    layout="wide"
)

# Professional Academic Banner honoring Abraham P.Z. Kamara
st.markdown(
    """
    <div style="background-color: #0f172a; padding: 20px; border-radius: 12px; margin-bottom: 25px; border-left: 6px solid #eab308; text-align: center;">
        <h3 style="color: #ffffff; margin: 0; font-weight: 700; letter-spacing: 0.5px;">🏫 VIRTUAL PHYSICS SIMULATION SUITE</h3>
        <p style="color: #94a3b8; margin: 5px 0 0 0; font-size: 0.95em;">
            Developed by: <strong style="color: #f8fafc;">Abraham P.Z. Kamara, BSc in Biomedical Science</strong><br>
            <span style="color: #eab308; font-weight: 600;">🏆 MVP of Academic Excellence, University of Liberia</span>
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Hidden Browser-Side Keep-Alive Component
components.html(
    """
    <script>
        console.log("Anti-Sleep Heartbeat Engine Initialized.");
        setInterval(function() {
            window.parent.postMessage({type: 'streamlit:keepalive'}, '*');
        }, 300000); // Heartbeat executes cleanly every 5 minutes
    </script>
    """,
    height=0,
    width=0
)

# Sidebar Lab Selection Toggle
st.sidebar.header("🔬 Experiment Bench Setup")
lab_selection = st.sidebar.selectbox(
    "Choose Active Lab Module:",
    ["1. Simple Pendulum Lab", "2. Mass-Spring Hooke's Law Lab"]
)

st.sidebar.markdown("---")

# ==========================================
# 🏛️ MODULE 1: SIMPLE PENDULUM LAB
# ==========================================
if lab_selection == "1. Simple Pendulum Lab":
    st.subheader("🏛️ Simple Pendulum Lab Module")
    st.markdown(
        "Adjust length and gravity metrics, drag and release the pendulum bob inside the simulator canvas, "
        "and time the oscillations manually using the stopwatch."
    )
    
    # Pendulum Controls
    length = st.sidebar.slider("String Length (L) in meters", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
    gravity = st.sidebar.slider("Gravitational Field (g) in m/s²", min_value=1.0, max_value=25.0, value=9.8, step=0.1)
    mass = st.sidebar.slider("Bob Mass (m) in kg", min_value=0.5, max_value=5.0, value=1.5, step=0.1)
    
    # HTML Sandbox Injection for Pendulum Lab
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; background: transparent; margin:0; padding:0; display:flex; flex-wrap:wrap; gap:20px; justify-content:center; }}
            .box {{ background: white; border-radius: 12px; border: 1px solid #e2e8f0; padding: 20px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
            canvas {{ background: #ffffff; border: 2px solid #f1f5f9; border-radius: 8px; cursor: grab; }}
            canvas:active {{ cursor: grabbing; }}
            .stopwatch-display {{ font-family: monospace; font-size: 2.8em; color: #0f172a; margin: 15px 0; background: #f8fafc; padding: 10px 25px; border-radius: 8px; border: 2px solid #cbd5e1; letter-spacing: 2px; text-align: center; min-width: 220px; }}
            .btn-row {{ display: flex; gap: 10px; }}
            .btn {{ padding: 10px 20px; font-size: 0.95em; font-weight: 500; border-radius: 6px; border: none; cursor: pointer; transition: background 0.2s; }}
            .btn-primary {{ background: #2563eb; color: white; }}
            .btn-danger {{ background: #dc2626; color: white; }}
            .btn-secondary {{ background: #64748b; color: white; }}
        </style>
    </head>
    <body>
        <div class="box">
            <canvas id="simCanvas" width="400" height="380"></canvas>
            <button class="btn btn-secondary" id="resetAngle" style="margin-top:15px;">Reset Angle</button>
        </div>
        <div class="box" style="justify-content: center; min-width: 280px;">
            <span style="font-weight:600; color:#475569;">⏱️ Student Stopwatch</span>
            <div class="stopwatch-display" id="swDisplay">00:00.00</div>
            <div class="btn-row">
                <button class="btn btn-primary" id="startStopBtn">Start</button>
                <button class="btn btn-danger" id="resetBtn">Reset</button>
            </div>
            <p style="font-size: 0.85em; color: #64748b; margin-top: 20px; text-align: center; max-width: 240px; line-height: 1.4;">
                <strong>Lab Action:</strong> Record 10 full back-and-forth oscillations, then divide the time by 10.
            </p>
        </div>
        <script>
            const lengthSetting = {length} * 100; const gravitySetting = {gravity}; const massSetting = {mass};
            const canvas = document.getElementById('simCanvas'); const ctx = canvas.getContext('2d'); const pivotX = canvas.width / 2; const pivotY = 40;
            let angle = Math.PI / 4; let angleVelocity = 0; let angleAcceleration = 0; let isDragging = false;
            let swTimer = null; let swStartTime = 0; let swElapsedTime = 0; let swIsRunning = false;

            canvas.addEventListener('mousedown', (e) => {{
                const r = canvas.getBoundingClientRect(); const mx = e.clientX - r.left; const my = e.clientY - r.top;
                const bx = pivotX + lengthSetting * Math.sin(angle); const by = pivotY + lengthSetting * Math.cos(angle);
                if (Math.hypot(mx - bx, my - by) < (10 + massSetting * 3)) {{ isDragging = true; angleVelocity = 0; }}
            }});
            canvas.addEventListener('mousemove', (e) => {{ if (isDragging) {{ const r = canvas.getBoundingClientRect(); angle = Math.atan2((e.clientX - r.left) - pivotX, (e.clientY - r.top) - pivotY); }} }});
            window.addEventListener('mouseup', () => isDragging = false);
            document.getElementById('resetAngle').onclick = () => {{ angle = Math.PI / 4; angleVelocity = 0; angleAcceleration = 0; }};

            const swDisplay = document.getElementById('swDisplay'); const startStopBtn = document.getElementById('startStopBtn');
            function updateClock() {{
                let t = swElapsedTime + (swIsRunning ? (Date.now() - swStartTime) : 0);
                let m = Math.floor(t / 60000).toString().padStart(2, '0'); let s = Math.floor((t % 60000) / 1000).toString().padStart(2, '0'); let ms = Math.floor((t % 1000) / 10).toString().padStart(2, '0');
                swDisplay.innerText = m + ":" + s + "." + ms;
            }}
            startStopBtn.onclick = () => {{
                if (!swIsRunning) {{ swIsRunning = true; swStartTime = Date.now(); swTimer = setInterval(updateClock, 10); startStopBtn.innerText = "Stop"; startStopBtn.style.background = "#dc2626"; }}
                else {{ swIsRunning = false; swElapsedTime += Date.now() - swStartTime; clearInterval(swTimer); startStopBtn.innerText = "Start"; startStopBtn.style.background = "#2563eb"; }}
            }};
            document.getElementById('resetBtn').onclick = () => {{ swIsRunning = false; clearInterval(swTimer); swElapsedTime = 0; startStopBtn.innerText = "Start"; startStopBtn.style.background = "#2563eb"; swDisplay.innerText = "00:00.00"; }}

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                if (!isDragging) {{ let dt = 0.12; angleAcceleration = (-1 * (gravitySetting * 15) / lengthSetting) * Math.sin(angle); angleVelocity += angleAcceleration * dt; angle += angleVelocity * dt; }}
                const bx = pivotX + lengthSetting * Math.sin(angle); const by = pivotY + lengthSetting * Math.cos(angle);
                ctx.beginPath(); ctx.arc(pivotX, pivotY, 5, 0, 2*Math.PI); ctx.fillStyle = '#475569'; ctx.fill();
                ctx.beginPath(); ctx.moveTo(pivotX, pivotY); ctx.lineTo(bx, by); ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 2; ctx.stroke();
                ctx.beginPath(); ctx.arc(bx, by, 10 + (massSetting * 3), 0, 2*Math.PI); ctx.fillStyle = '#2563eb'; ctx.fill(); ctx.strokeStyle = '#1d4ed8'; ctx.stroke();
                requestAnimationFrame(draw);
            }}
            draw();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=460, scrolling=False)
    
    # Formula Sheet
    st.subheader("📊 Pendulum Analysis Framework")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(r"**Theoretical Formulation:** $$\text{Period } (T) = 2\pi \sqrt{\frac{L}{g}}$$")
        theoretical_T = 2 * np.pi * np.sqrt(length / gravity)
        st.metric("Expected Theoretical Period (T)", f"{theoretical_T:.3f} seconds")
    with col2:
        st.info(f"📐 **Length (L):** `{length:.2f} m` | 🌍 **Gravity (g):** `{gravity:.1f} m/s²` | ⚖️ **Mass (m):** `{mass:.2f} kg` ")

# ==========================================
# 🌀 MODULE 2: MASS-SPRING HOOKE'S LAW LAB
# ==========================================
else:
    st.subheader("🌀 Mass-Spring Hooke's Law Lab Module")
    st.markdown(
        "Adjust mass load and spring constants, click and stretch the attached block vertically "
        "to set it in motion, and calculate the bounce periodicity manually."
    )
    
    # Spring Controls
    mass_spring = st.sidebar.slider("Hanging Mass (m) in kg", min_value=0.5, max_value=10.0, value=2.0, step=0.1)
    k_spring = st.sidebar.slider("Spring Constant (k) in N/m", min_value=10.0, max_value=200.0, value=50.0, step=5.0)
    damping = st.sidebar.slider("Damping Coefficient (c)", min_value=0.0, max_value=1.0, value=0.05, step=0.01)

    # HTML Sandbox Injection for Spring Lab
    html_code_spring = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; background: transparent; margin:0; padding:0; display:flex; flex-wrap:wrap; gap:20px; justify-content:center; }}
            .box {{ background: white; border-radius: 12px; border: 1px solid #e2e8f0; padding: 20px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
            canvas {{ background: #ffffff; border: 2px solid #f1f5f9; border-radius: 8px; cursor: grab; }}
            canvas:active {{ cursor: grabbing; }}
            .stopwatch-display {{ font-family: monospace; font-size: 2.8em; color: #0f172a; margin: 15px 0; background: #f8fafc; padding: 10px 25px; border-radius: 8px; border: 2px solid #cbd5e1; letter-spacing: 2px; text-align: center; min-width: 220px; }}
            .btn-row {{ display: flex; gap: 10px; }}
            .btn {{ padding: 10px 20px; font-size: 0.95em; font-weight: 500; border-radius: 6px; border: none; cursor: pointer; transition: background 0.2s; }}
            .btn-primary {{ background: #2563eb; color: white; }}
            .btn-danger {{ background: #dc2626; color: white; }}
            .btn-secondary {{ background: #64748b; color: white; }}
        </style>
    </head>
    <body>
        <div class="box">
            <canvas id="springCanvas" width="400" height="380"></canvas>
            <button class="btn btn-secondary" id="reset