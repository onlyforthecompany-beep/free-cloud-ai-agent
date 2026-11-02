# Zero-Cost Cloud AI Agent Starter Kit

A ready-to-deploy Python AI agent powered by the [Gemini Developer API Free Tier](https://ai.google.dev/gemini-api/docs/pricing) (`gemini-3.8-flash`), [Google Gen AI Python SDK (`google-genai`)](https://googleapis.github.io/python-genai/), and [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud)—requiring **$0.00 and no credit card**.

## Included Files

- `app.py` — Streamlit chat web UI and persistent `gemini-3.8-flash` tool-calling session
- `tools.py` — Three keyless tools: live weather ([Open-Meteo](https://open-meteo.com/en/docs)), reference summaries ([Wikimedia REST API](https://www.mediawiki.org/wiki/Wikimedia_REST_API)), and CSV study search
- `study_resources.csv` — Curated free AI & cloud learning catalog
- `requirements.txt` — Lean Python package list for automatic cloud container builds
- `.gitignore` & `.streamlit/secrets.toml.example` — Secret-protection rules and TOML template
- `docs/zero_cost_cloud_ai_agent_guide.pdf` — Full step-by-step illustrated guide

## 3-Minute Cloud Deployment ($0)

1. Create a **Public** repository on [GitHub](https://github.com/) and upload the contents of this folder (`app.py`, `tools.py`, `study_resources.csv`, `requirements.txt`, `.gitignore`, and `README.md`).
2. Generate a free API key in [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key).
3. Sign in to [Streamlit Community Cloud (`share.streamlit.io`)](https://share.streamlit.io/), click **Create app**, select your repository (`main` branch, `app.py`), open **Advanced settings -> Secrets** ([docs](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)), and paste:
   ```toml
   GEMINI_API_KEY = "your_actual_google_ai_studio_key"
   ```
4. Click **Save** and **Deploy!**.

## Optional Local Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
export GEMINI_API_KEY="your_actual_google_ai_studio_key"
streamlit run app.py
```
