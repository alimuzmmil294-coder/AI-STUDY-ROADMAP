# 🗺️ AI Study Roadmap Planner

An interactive web application built with **Streamlit** and the **Google GenAI SDK** (`google-genai`) that generates personalized, time-bound learning roadmaps for any programming language, tech stack, or academic subject.

## ✨ Features
- **Streamlit Secrets & BYOK Support:** Automatically reads `GEMINI_API_KEY` from Streamlit Cloud Secrets or lets users enter their own key in the sidebar.
- **Custom Timeframe & Pacing:** Adjusts curriculum density based on total duration and daily study hours.
- **Skill-Level Adaptation:** Tailors starting points from complete beginners to advanced learners.
- **Model Selection:** Switch between `gemini-2.5-flash` (fast) and `gemini-2.5-pro` (deep reasoning).
- **Markdown Export:** Download your generated study plan as a `.md` file.

---

## ☁️ Deploying on Streamlit Community Cloud (via GitHub)

1. **Push files to GitHub:**
   Create a new GitHub repository and add `app.py`, `requirements.txt`, and `README.md` to the root folder. *(Never commit your API key to GitHub!)*

2. **Connect to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
   - Click **New app**, select your repository, branch (`main`), and set the main file path to `app.py`.

3. **Add your API Key in Secrets:**
   - Before or after deploying, open your app's **Settings → Secrets** in Streamlit Cloud.
   - Paste the following and click **Save**:
     ```toml
     GEMINI_API_KEY = "AIzaSyYourActualApiKeyHere"
     ```

---

## 💻 Running Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name
