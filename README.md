# Apple-Inspired Streamlit App

This repository contains a multipage Streamlit app styled with Tailwind CSS and inspired by Apple's design language.

## Files
- `app.py` - Main Streamlit application.
- `requirements.txt` - Python dependencies.
- `.streamlit/config.toml` - (Optional) Streamlit config.

## Quick start (Streamlit Community Cloud)
1. Create a new GitHub repo and push these files.
2. On https://share.streamlit.io, connect your GitHub repo and deploy.

## Run locally
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
```

## Notes
- The app uses CDN-hosted Tailwind and Lucide icons, so no additional build step needed.
- To customize icons or CSS, edit `app.py` and update the `<link>` tags.