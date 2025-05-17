# Save this as app.py and run with `streamlit run app.py`
import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# Navbar-like header (Streamlit doesn't support a sticky navbar directly)
st.markdown("""
    <style>
        .title {
            background: linear-gradient(to right, #004080, #0066cc);
            padding: 1rem;
            color: white;
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 2rem;
        }
    </style>
    <div class="title">Resume Matchmaker - Analyze Your Resume</div>
""", unsafe_allow_html=True)

st.markdown("### Paste your resume image URL")
st.info("Use a publicly accessible image URL (e.g., from Imgur or your web server)")

image_url = st.text_input("Resume Image URL", "")

if st.button("Upload & Analyze"):
    if image_url:
        with st.spinner("Analyzing resume..."):
            try:
                response = requests.post("http://127.0.0.1:5000/analyze", json={"image_url": image_url})
                if response.ok:
                    result = response.json()
                    if "result" in result:
                        st.success("Analysis Complete!")
                        st.markdown("### AI Analysis Result:")
                        st.code(result["result"], language="text")
                    else:
                        st.error(result.get("error", "Unknown error from API."))
                else:
                    st.error("Failed to connect to the analysis server.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please paste a valid image URL.")

st.markdown("---")
st.markdown("### 🔍 What You'll Get")
st.markdown("""
- ✅ Detailed resume analysis and scoring  
- ✅ Personalized improvement suggestions  
- ✅ Job matching based on your skills  
- ✅ Career path recommendations  
- ✅ AI-generated resume improvements
""")
