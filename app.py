import streamlit as st
from google import genai
import pandas as pd
import time

# ==========================================
# 1. HARDCODED CONFIGURATION
# ==========================================
# Keep your working API key pasted inside the quotes below:
GEMINI_API_KEY = "AQ.Ab8RN6KhwZ7pFyffIPuXvSaQNmKmerUxNyFGTe3CKRL-4kwBTQ"

st.set_page_config(
    page_title="RoamSmart AI | Student Travel Planner", 
    page_icon="✈️", 
    layout="wide"
)

st.title("✈️ RoamSmart AI")
st.subheader("Next-Gen Predictive Budget Optimization Engine | Capstone Project")
st.markdown("---")

# ==========================================
# 2. INTERACTIVE PARAMETERS PANEL
# ==========================================
col1, col2 = st.columns([5, 7], gap="large")

with col1:
    st.subheader("🗺️ Trip Parameters")
    destination = st.text_input("Target Destination City/Country", placeholder="e.g., Goa, Kyoto, Paris", value="Goa")
    
    c1, c2 = st.columns(2)
    with c1:
        days = st.number_input("Trip Duration (Days)", min_value=1, max_value=14, value=3)
    with c2:
        currency = st.selectbox("Preferred Currency Array", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"])
        
    budget = st.selectbox(
        "Financial Constraint Matrix",
        ["Shoestring (Hostels, street food, free landmarks)", 
         "Backpacker (Affordable guesthouses, public transit, local cafes)", 
         "Moderate (Mid-range stays, comfortable dining)"]
    )
    
    interests = st.multiselect(
        "Primary Activity Focus Core",
        ["History & Culture", "Nature & Adventure", "Food & Cafes", "Nightlife & Pubs", "Local Shopping", "Relaxation Tracks"],
        default=["History & Culture", "Food & Cafes"]
    )
    
    st.markdown("---")
    st.subheader("🚀 Standout Modules Enabled")
    include_weather = st.checkbox("Enable AI Weather & Smart Packing Assistant", value=True)
    include_safety = st.checkbox("Enable Local Emergency & Student Safety Framework", value=True)
    
    submit_button = st.button("Compute Optimized Analytics Route ✨", type="primary", use_container_width=True)

# ==========================================
# 3. SELF-HEALING RUNTIME ENGINE
# ==========================================
with col2:
    st.subheader("🗓️ Real-Time Computational Itinerary Output")
    
    if submit_button:
        if not destination:
            st.warning("Input Error: Target destination field cannot be left blank.")
        elif GEMINI_API_KEY == "PASTE_YOUR_ACTUAL_API_KEY_HERE":
            st.error("Developer Action Required: Please paste your Gemini API key on line 10.")
        else:
            # Set up our display components first
            st.markdown("### 📈 Visual Budget Allocation Breakdown")
            chart_data = pd.DataFrame(
                [35, 30, 20, 15],
                index=["Accommodation", "Food & Dining", "Local Transport", "Activities & Sights"],
                columns=["Allocation (%)"]
            )
            st.bar_chart(chart_data)
            st.markdown("---")

            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                
                prompt = f"""
                You are an advanced AI travel optimization machine specializing in student budget analytics, meteorological tracking, and international safety frameworks.
                Generate an exhaustive, practical travel deployment framework for a student visiting {destination} for {days} days.
                
                Target Currency: {currency}
                Budget Profile Matrix: {budget}
                Interests Constellation: {', '.join(interests)}
                
                Strictly structure the document using clean Markdown headers matching these exact sections:
                # 📊 CORE TRANSACTIONAL OPTIMIZATION REPORT
                ### 💡 Student Hyper-Local Financial Hacks
                ### 📅 Complete Day-by-Day Tactical Route Plan
                ### 📊 Target Expense Distribution Matrix
                """
                
                if include_weather:
                    prompt += f"\n# 🌤️ AI WEATHER PREDICTION & SMART PACKING PROFILE\nProvide a calculated meteorological profile for {destination}."
                if include_safety:
                    prompt += f"\n# 🚨 LOCAL EMERGENCY & STUDENT SAFETY FRAMEWORK\nList verified local emergency contact hotlines for {destination}."

                # Attempt execution with automatic high-demand traffic recovery handling
                response_text = None
                with st.spinner("Processing routes and analyzing traffic capacity..."):
                    for attempt in range(3):
                        try:
                            response = client.models.generate_content(
                                model='gemini-2.5-flash',
                                contents=prompt,
                            )
                            response_text = response.text
                            break  # Success! Exit loop.
                        except Exception as inner_error:
                            if "503" in str(inner_error) and attempt < 2:
                                time.sleep(2)  # Wait 2 seconds for traffic spike to clear
                                continue
                            else:
                                raise inner_error

                if response_text:
                    # Render final success layout
                    m1, m2, m3 = st.columns(3)
                    with m1: st.metric(label="Target Hub", value=destination.title())
                    with m2: st.metric(label="Window Array", value=f"{days} Days")
                    with m3: st.metric(label="Currency Layer", value=currency.split()[0])
                    
                    st.markdown("---")
                    st.markdown(response_text)
                    st.success("🎉 Advanced algorithmic routing map successfully calculated!")
                    
                    st.download_button(
                        label="📥 Export Optimized Structural Plan (.txt)",
                        data=response_text,
                        file_name=f"roamsmart_{destination.lower()}_itinerary.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            except Exception as e:
                if "503" in str(e):
                    st.warning("⏱️ The public Google server is currently experiencing extremely high traffic. Please tap 'Compute Optimized Analytics Route ✨' once more to bypass the queue.")
                else:
                    st.error(f"System Pipeline Crash: {e}")
    else:
        st.info("System Ready. Click 'Compute Optimized Analytics Route ✨' to generate the entire itinerary instantly.")