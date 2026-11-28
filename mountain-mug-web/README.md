# The Mountain Mug AI Cafe Assistant

A Flask + OpenAI customer chatbot configured for The Mountain Mug in Library Bazaar, Mussoorie.

## Deploy on Vercel

1. Put this project in a GitHub repository, or import/upload the project to Vercel.
2. Create a new Vercel project from it. Vercel automatically detects the Flask `app` in `app.py`; no build command or output directory is required.
3. In Vercel: Project -> Settings -> Environment Variables, add:
   - Name: `OPENAI_API_KEY`
   - Value: your OpenAI API key
   - Type: **Secret**
   - Environments: Production (and Preview if you want preview deployments to work)
4. Optional: add `OPENAI_MODEL` if you want to override the default model in `app.py`.
5. Redeploy after adding/changing environment variables.
6. Open the Production URL Vercel provides. Visitors need only a browser.

Never commit a `.env` file or API key to source control.

## Local development (optional)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows, or cp .env.example .env
python app.py
```

Then open http://localhost:8000.
