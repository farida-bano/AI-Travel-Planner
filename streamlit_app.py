import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Travel Planner", layout="wide")

# Get GROQ API key from Streamlit secrets or environment
groq_api_key = None

try:
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception as e:
    st.warning(f"Could not read from secrets: {e}")

if not groq_api_key:
    groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found!\n\nPlease add it to Streamlit secrets:\n1. Go to your app settings\n2. Click 'Secrets'\n3. Add: GROQ_API_KEY = your_key_here")
    st.stop()

# Set environment variable for the modules to use
os.environ["GROQ_API_KEY"] = groq_api_key

try:
    from main import app
    from langchain_core.messages import HumanMessage
except Exception as e:
    st.error(f"❌ Error loading app: {e}")
    st.stop()

st.title("🌍 AI Travel Planner")
st.write("Plan your perfect trip with AI-powered recommendations!")

user_input = st.text_input("Enter your travel request:")

if user_input:
    with st.spinner("Planning your trip..."):
        try:
            config = {
                "configurable": {
                    "thread_id": "streamlit_user"
                }
            }

            result = app.invoke(
                {
                    "messages": [HumanMessage(content=user_input)],
                    "user_query": user_input,
                    "flight_results": "",
                    "hotel_results": "",
                    "itinerary": "",
                    "llm_calls": 0
                },
                config=config
            )

            st.success("✅ Trip planned!")
            for msg in result["messages"]:
                st.write(msg.content)
        except Exception as e:
            st.error(f"❌ Error: {e}")

