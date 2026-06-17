import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Get GROQ API key from Streamlit secrets or environment
groq_api_key = st.secrets.get("GROQ_API_KEY") if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ GROQ_API_KEY not found! Please add it to Streamlit secrets.")
    st.stop()

# Set environment variable for the modules to use
os.environ["GROQ_API_KEY"] = groq_api_key

# Now import main after setting the environment variable
from main import app

st.title("🌍 AI Travel Planner")
st.write("Plan your perfect trip with AI-powered recommendations!")

user_input = st.text_input("Enter your travel request:")

if user_input:
    with st.spinner("Planning your trip..."):
        config = {
            "configurable": {
                "thread_id": "streamlit_user"
            }
        }

        from langchain_core.messages import HumanMessage

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
