# Zoya Lvanova Telegram Bot ++(Render Deployment)

## 🚀 Deployment Steps

1. Push this repo to GitHub.
2. Go to [https://render.com](https://render.com) → New Web Service.
3. Connect your GitHub and select this repo.
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn main:app`
5. Add Environment Variables:
   - `TELEGRAM_TOKEN`: 8039860946:AAGT3Vu_DLUrZqIz1Twze4_xLcUPbC0FEPY
   - `OPENROUTER_API_KEY`: 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

6. After deploy, set your webhook:
   Visit:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://your-render-url.onrender.com/<YOUR_TOKEN>
   ```