# Deploying Your Telegram Reposter Bot to Render.com

This guide will walk you through deploying your Telegram Reposter Bot to Render.com, a free hosting service, so it can run 24/7. This process assumes you have already created a GitHub repository containing your bot's files (`telegram_reposter_bot.py`, `requirements.txt`, and `Procfile`).

## Files You Need in Your GitHub Repository

Before you start, ensure your GitHub repository contains the following files:

1.  **`telegram_reposter_bot.py`**: Your main bot script.
2.  **`requirements.txt`**: Lists all Python libraries your bot needs. It should contain:
    ```
    python-telegram-bot==22.6
    openai==1.14.0
    ```
3.  **`Procfile`**: Tells Render.com how to run your application. It should contain:
    ```
    web: python3.11 telegram_reposter_bot.py
    ```

## Step-by-Step Deployment to Render.com

### 1. Create a Render.com Account

If you don't have one, sign up for a free account on [Render.com](https://render.com/). You can sign up using your GitHub account for easier integration.

### 2. Connect Your GitHub Repository

*   After logging in, go to your Render Dashboard.
*   Click on **New** -> **Web Service**.
*   Connect your GitHub account if you haven't already. Then, select the repository where you've stored your bot's files.

### 3. Configure Your Web Service

Fill in the following details for your new web service:

*   **Name**: Give your service a memorable name (e.g., `telegram-reposter-bot`).
*   **Region**: Choose a region close to you or your target audience.
*   **Branch**: Select the branch of your repository you want to deploy (usually `main` or `master`).
*   **Root Directory**: Leave this blank if your files are at the root of your repository.
*   **Runtime**: Select `Python 3`.
*   **Build Command**: `pip install -r requirements.txt`
*   **Start Command**: `python3.11 telegram_reposter_bot.py` (This will use the `Procfile` if present, but it's good to specify).

### 4. Set Environment Variables

This is crucial for your bot to function correctly. You need to provide your OpenAI API key.

*   In the service configuration page, scroll down to **Environment Variables**.
*   Click **Add Environment Variable**.
    *   **Key**: `OPENAI_API_KEY`
    *   **Value**: Your actual OpenAI API key (e.g., `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`).

### 5. Create Web Service

*   Click the **Create Web Service** button at the bottom of the page.
*   Render.com will now start building and deploying your bot. This might take a few minutes.

### 6. Monitor Deployment and Logs

*   Once deployed, you can view the deployment logs on your service dashboard to ensure everything is running smoothly.
*   Your bot should now be running 24/7, monitoring the specified Telegram channels and reposting content.

## Important Considerations for Free Tier

*   **Free Tier Limitations**: Render.com's free tier services might spin down after a period of inactivity. This means your bot might pause and restart. For continuous operation without interruptions, a paid plan is usually required.
*   **Bot Token**: The `BOT_TOKEN` is hardcoded in `telegram_reposter_bot.py`. For better security, you might consider also adding `BOT_TOKEN` as an environment variable on Render.com and modifying your script to read it from `os.environ.get("BOT_TOKEN")`.
*   **Source and Target Channels**: Remember to update `SOURCE_CHANNEL_USERNAMES` and `TARGET_CHANNEL_USERNAME` in your `telegram_reposter_bot.py` file if you wish to change the channels the bot monitors or posts to.
