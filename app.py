import streamlit as st
import streamlit.components.v1 as components
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Virtual Triple Beam Balance Lab",
    page_icon="⚖️",
    layout="centered"
)

# --- ANTI-SLEEP / KEEP-ALIVE COMPONENT ---
components.html(
    """
    <script>
    const keepAlive = () => {
        fetch(window.location.href, { method: 'HEAD', cache: 'no-store' })
            .then(() => console.log('Keep-alive ping successful.'))
            .catch((err) => console.warn('Keep-alive ping failed:', err));
    };
    keepAlive();
    setInterval(keepAlive, 30000); 
    </script>
    """,
    height=0,
    width=0,
)

# --- LAB DATA (Hidden Actual Masses) ---
LAB_OBJECTS = {
    "Copper Cylinder 🪙": {"actual_mass": 145.30, "description": "A dense metallic cylinder used for density verification."},
    "Wooden Block 🪵": {"actual_mass": 62.45, "description": "A lightweight pine block. Keep away from water!"},
    "Unknown Powdery Substance (in 50g Beaker) 🧪": {"actual_mass": 118.85, "description": "Total mass of the chemical inside a 50.00g glass beaker."},
    "Mystery Antique Coin 🪙": {"actual_mass": 12.15, "description": "A worn-out historical coin. What is it made of?"}
}

# --- APP TITLE & INTRO ---
st.title("⚖️ Virtual Triple Beam Balance Lab")
st.markdown("""
Welcome to the interactive mass measurement lab. In this exercise, you will practice 
calibrating an analog balance and adjusting the three sliding riders to find the mass of unknown objects.
""")

# --- STEP 1: PRE-LAB CALIBRATION ---
st.header("Step 1: Calibration (Zeroing the Scale)")
st.info("Before placing an object on the scale, the balance pointer must line up exactly with **0.00**.")

calibration_error = st.slider(
    "Zero Adjustment Knob (Calibrate the balance pointer):", 
    min_value=-2.0, max_value=2.0, value=1.2, step=0.1,
    help="Turn this knob until the alignment pointer below hits exactly 0.00 when riders are at zero."
)

# --- STEP 2: SELECT LAB OBJECT ---
st.header("Step 2: Choose Your Object")
selected_object_name = st.selectbox("Select an object to place on the pan:", list(LAB_OBJECTS.keys()))
object_info = LAB_OBJECTS[selected_object_name]

st.markdown(f"**Object Description:** *{object_info['description']}*")

# --- STEP 3: READ THE SCALE & ADJUST RIDERS ---
st.header("Step 3: Adjust the Riders")
st.write("Slide the heavy, medium, and fine tracks until the balance pointer lands exactly on **0.00**.")

col1, col2, col3 = st.columns(3)

with col1:
    rider_100 = st.slider("Hundreds Beam (g)", min_value=0, max_value=500, value=0, step=100)
with col2:
    rider_10 = st.slider("Tens Beam (g)", min_value=0, max_value=100, value=0, step=10)
with col3:
    rider_1 = st.slider("Ones / Tenths Beam (g)", min_value=0.00, max_value=10.00, value=0.00, step=0.05)

current_rider_sum = rider_100 + rider_10 + rider_1
target_mass_with_calibration = object_info["actual_mass"] + calibration_error
pointer_deflection = current_rider_sum - target_mass_with_calibration

# --- STEP 4: LAB INTERFACE DISPLAY ---
st.subheader("Balance Indicator")

if abs(pointer_deflection) < 0.02:
    st.success("🟢 **BALANCED! The pointer points exactly to 0.00.**")
    pointer_text = "🎯 [==== 0.00 ====]"
elif pointer_deflection > 0:
    st.warning("🔼 **TOO HEAVY.** The riders outweigh the object. Slide them back to the left.")
    pointer_text = f"📈 Pointer Deflection: +{pointer_deflection:.2f} g (Tilted Down)"
else:
    st.warning("🔽 **TOO LIGHT.** The object outweighs the riders. Slide them further to the right.")
    pointer_text = f"📉 Pointer Deflection: {pointer_deflection:.2f} g (Tilted Up)"

st.code(pointer_text, language="text")

# --- STEP 5: SUBMIT DATA FOR GRADING ---
st.header("Step 4: Record Your Lab Measurement")
st.write("Sum the values of your riders and log your data.")

col_sum1, col_sum2 = st.columns(2)
with col_sum1:
    st.metric("Your Total Rider Setting", f"{current_rider_sum:.2f} g")

with col_sum2:
    user_guess = st.number_input("Enter your finalized mass reading to record (g):", min_value=0.00, step=0.01, format="%.2f")

if st.button("Check My Lab Notebook Reading"):
    if abs(calibration_error) > 0.05 and abs(user_guess - object_info["actual_mass"]) < 0.1:
        st.error("❌ **Measurement Error:** Your slider sum looks close, but you forgot to calibrate your scale to 0.00 first! Your data has a systematic error.")
    elif abs(user_guess - object_info["actual_mass"]) <= 0.05:
        st.balloons()
        st.success(f"🎉 **Correct!** You successfully measured the {selected_object_name} at **{object_info['actual_mass']:.2f}g**.")
        
        if "Beaker" in selected_object_name:
            st.markdown("""
            ***🧪 Post-Lab Challenge Note:*** 
            Since the empty container has a known mass of **50.00g**, what is the net mass of the liquid inside?
            * Net Mass = Total Mass ({:.2f}g) - Container Mass (50.00g) = **{:.2f}g**
            """.format(object_info['actual_mass'], object_info['actual_mass'] - 50.00))
    else:
        st.error(f"❌ **Incorrect Reading:** Your recorded mass of {user_guess:.2f}g is off. Adjust the sliders until the indicator turns green.")
