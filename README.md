# Discord Moderation Bot with Firebase Integration

A fully-featured Discord bot with Auto-Moderation, Welcome & Goodbye Messages, and Moderator Action Logging using Firebase Firestore. This bot helps keep your server clean, organized, and fun.

---

## Features

- **Auto-Moderation**: Deletes messages with offensive words automatically.
- **Encouragement System**: Sends motivational messages when detecting sad words.
- **Welcome & Goodbye Messages**: Greets new members and notifies when they leave.
- **Kick, Ban, Mute Commands**: Moderators can easily manage users.
- **Moderator Action Logging**: Stores all mod actions (kick, ban, mute) in Firebase Firestore.
- **Retrieve Mod Logs**: Admins can fetch recent moderation actions with `!modlogs`.

---

## Project Background

This bot was developed for a local Christian group that needed a simple moderation tool for their Discord channel. The client wanted an easy-to-use bot that could automatically moderate chat, send welcome and goodbye messages, and provide encouragement to members. While the product wsn't too complicated it served as an opportunity to learn and apply **Scrum processes and Agile management** on a small scale, improve **client communication**, and deliver a **Minimum Viable Product (MVP)** quickly for instant feedback. 

Since most members of the Christian group were not technically inclined, I included a **step-by-step walkthrough** in the README to guide them through the installation and setup process. This ensured that they could deploy and maintain the bot without external assistance. Additionally, I served as a **moderator for the Discord channel** for a short time, allowing me to gain firsthand experience with the challenges members faced. This helped refine the bot’s features to better meet their needs.

---

# Discord Moderation Bot - Installation & Setup Guide

This guide provides step-by-step instructions for setting up and running the **Discord Moderation Bot** with Firebase integration.

---

## Installation & Setup

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install Dependencies

Make sure you have **Python 3.8+** installed. Then install the required dependencies:

```sh
pip install -r requirements.txt
```

### 3. Set Up Firebase Firestore

#### **Create a Firebase Project**
1. Go to [Firebase Console](https://console.firebase.google.com/).
2. Click **"Create a Project"**, then follow the setup process.
3. Navigate to **Firestore Database** under the **Build** section.
4. Click **"Create Database"**, select a location, and choose **Test Mode**.

#### **Download the Firebase Service Account Key**
1. In **Project Settings → Service Accounts**, click **"Generate new private key"** and download the JSON file.
2. Move this file into your project directory and rename it:
   ```
   firebase_key.json
   ```

### 4. Create a `.env` File

1. Inside your project directory, create a **`.env`** file.
2. Add your **Discord bot token**:
   ```
   DISCORD_TOKEN=your-bot-token-here
   ```

### 5. Enable Privileged Intents in Discord Developer Portal

1. Go to [Discord Developer Portal](https://discord.com/developers/applications).
2. Select your bot application.
3. Click on **Bot** in the left sidebar.
4. Scroll down to **Privileged Gateway Intents**.
5. Enable the following:
   - **MESSAGE CONTENT INTENT** (Required for reading messages)
   - **SERVER MEMBERS INTENT** (Required for `on_member_join` and `on_member_remove`)
6. Click **Save Changes**.

---

## Running the Bot

After setting up Firebase and the `.env` file, start the bot:

```sh
python main.py
```

If everything is working, you should see:

```
Bot is online as YourBotName
```

---

## Security Recommendations

### Add `.env` & `firebase_key.json` to `.gitignore`
Make sure your `.gitignore` file contains:
```
.env
firebase_key.json
```
This prevents **sensitive credentials** from being uploaded to GitHub.

### If You Accidentally Pushed Sensitive Files
Run the following to **remove them from Git history**:

```sh
git rm --cached .env firebase_key.json
git commit -m "Removed sensitive files"
git push origin main
```

Then regenerate your **Discord bot token** in the [Developer Portal](https://discord.com/developers/applications).

---

## Hosting the Bot

### Running Locally
Keep the bot running with:

```sh
python main.py
```

### Deploy on a Cloud Service
You can deploy this bot using:
- **Replit**
- **Heroku** (Use `Procfile` for deployment)
- **Railway.app**



