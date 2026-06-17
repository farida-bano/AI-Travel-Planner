import streamlit as st
import os
from dotenv import load_dotenv

st.set_page_config(page_title="AI Travel Planner", layout="wide")

st.write("🔄 Loading app...")

load_dotenv()

try:
    groq_api_key = None
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
        st.write("✅ Found GROQ_API_KEY in secrets")
    else:
        groq_api_key = os.getenv("GROQ_API_KEY")
        st.write("⚠️ GROQ_API_KEY not in secrets, checking environment")

    if not groq_api_key:
        st.error("❌ GROQ_API_KEY not found in secrets or environment!")
        st.stop()

    st.write("✅ API key loaded")
    os.environ["GROQ_API_KEY"] = groq_api_key

except Exception as e:
    st.error(f"❌ Error loading secrets: {e}")
    import traceback
    st.write(traceback.format_exc())
    st.stop()

try:
    st.write("📦 Importing main app...")
    from main import app
    from langchain_core.messages import HumanMessage
    st.write("✅ App imported successfully")
except Exception as e:
    st.error(f"❌ Error importing app: {e}")
    import traceback
    st.write(traceback.format_exc())
    st.stop()

st.title("🌍 AI Travel Planner")
st.write("Plan your perfect trip with AI-powered recommendations!")

user_input = st.text_input("Enter your travel request:")

if user_input:
    with st.spinner("Planning your trip..."):
        try:
            st.write(f"Processing: {user_input}")

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
            st.error(f"❌ Error planning trip: {e}")
            import traceback
            st.write(traceback.format_exc())


