
import os
import streamlit as st
from groq import Groq, AuthenticationError

st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="🎯"
)

st.title("🎯 AI Learning Roadmap Generator")
st.write("Create a personalized learning plan with AI.")

field = st.text_input(
    "What do you want to learn?",
    placeholder="e.g. Machine Learning"
)

level = st.selectbox(
    "Your skill level",
    ["Beginner", "Intermediate", "Advanced"]
)

duration = st.selectbox(
    "Learning duration",
    ["1 month", "3 months", "6 months", "12 months"]
)

hours = st.selectbox(
    "Study hours per day",
    [1, 2, 3, 4, 5]
)

if st.button("Generate My Roadmap"):
    if not field.strip():
        st.warning("Please enter a learning field.")
    else:
        try:
            # Read the API key from Streamlit secrets,
            # or fall back to an environment variable.
            try:
                api_key = st.secrets.get("GROQ_API_KEY", "")
            except Exception:
                api_key = ""

            api_key = (
                api_key or os.getenv("GROQ_API_KEY", "")
            ).strip()

            if not api_key:
                st.error(
                    "Groq API key is missing. "
                    "Check .streamlit/secrets.toml."
                )
                st.stop()

            client = Groq(api_key=api_key)

            prompt = f"""
Create a practical learning roadmap.

Subject: {field}
Skill level: {level}
Duration: {duration}
Study time: {hours} hours per day

Include:
1. Weekly learning plan
2. Important topics
3. Hands-on projects
4. Free learning resources
5. Weekly goals
6. Final portfolio project

Use clear headings and beginner-friendly language.
"""

            with st.spinner("Creating your roadmap..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_completion_tokens=3000
                )

            st.markdown(
                response.choices[0].message.content
            )

        except AuthenticationError:
            st.error(
                "Groq rejected your API key. Create a new key "
                "at https://console.groq.com/keys and update "
                "your secrets.toml file."
            )
        except Exception as e:
            st.error(f"Something went wrong: {e}")
