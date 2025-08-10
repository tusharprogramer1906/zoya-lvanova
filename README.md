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