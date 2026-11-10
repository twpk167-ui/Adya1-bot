# Adya Bot ko 24x7 Online Karna (Permanent Fix) 🚀

## Problem kya thi?
Yahan Arena sandbox me bot tab tak chalta hai jab tak mai usko run rakhta hu.
Jaise hi ye chat wala turn khatam hota hai, bot ka process band ho jata hai.
Isliye tumne `/start` bheja, lekin bot offline tha — reply nahi aaya.

**Solution:** Bot ko kisi free hosting (Railway / Render) par deploy karo.
Wahan wo 24x7 online rahega, tum kabhi bhi message karo, Adya turant reply degi.

---

## Option 1: Railway par Deploy (Sabse easy, 2-3 minute)

### Step 1: Code GitHub par daalo
1. github.com par jao → **New repository** banao, naam `adya-bot`
2. Apne computer par ye files upload karo:
   - `bot.py`
   - `brain.py`
   - `requirements.txt`
   - `Procfile`
   - `Dockerfile`
   - `README.md`
   - ⚠️ **`.env` file upload MAT karo** — usme token hai, wo secret hai!

### Step 2: Railway par deploy
1. railway.app par jao → GitHub se login karo
2. **New Project** → **Deploy from GitHub repo** → `adya-bot` select karo
3. Deploy ho jayega (2 minute lagega)

### Step 3: Token add karo
1. Railway project me **Variables** tab kholo
2. Add karo:
   - Key: `BOT_TOKEN`
   - Value: tumhara bot token (jo tumne mujhe bheja tha)
3. Service **Redeploy** karo

Bas! Ab bot 24x7 online hai. Telegram par `@Adya121_bot` ko `/start` karo. 💛

---

## Option 2: Render par Deploy (Free tier)

1. render.com par GitHub se login karo
2. **New → Web Service** → apna GitHub repo `adya-bot` select karo
3. Settings:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -u bot.py`
   - **Plan:** Free
4. **Environment Variables** me `BOT_TOKEN` add karo
5. **Create Web Service** dabao

Note: Render free tier kabhi-kabhi so jata hai (15 min inactive ke baad),
pehla message thoda slow aa sakta hai. Railway zyada reliable hai.

---

## Deploy ke baad test kaise karein?
1. Telegram kholo → `@Adya121_bot` search karo
2. `/start` bhejo → Adya ka welcome aana chahiye
3. `hi`, `kaise ho`, `bore ho raha hu`, `joke sunao` try karo

## Agar kuch gadbad ho toh?
- Railway/Render ke logs dekho — wahan error dikhega
- Mujhe error ka screenshot / text bhejo, mai fix bata dunga
- Bot ka naam, replies, ya naye features change karne hain toh `brain.py` edit karke GitHub par update karo, Railway auto-redeploy kar dega

## Security yaad rakho 🔐
- Token kisi ko mat bhejo, GitHub par public mat karo
- Agar token leak ho jaye toh @BotFather par `/revoke` karke naya token banao aur Railway me update kar do
