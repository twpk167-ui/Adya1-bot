# Adya - Human-like Telegram Bot 💛

AI jaisa boring bot nahi, bilkul **Adya** ki tarah human jaisa behave karne wala bot.

**Persona:**
- Naam: Adya
- Btech kar rahi hai
- Noida se belong karti hai
- Casual Hinglish me baat karti hai, dost ki tarah

## Human jaisa behavior kya-kya hai?

- ⌨️ Reply se pehle **"typing..."** dikhta hai
- ⏱️ Reply ki length ke hisab se **delay** hota hai (turant answer nahi)
- 💬 Lambe reply **2 chhote messages** me aate hain (double texting)
- 😊 Kabhi emoji, kabhi bina emoji - har baar same nahi
- 🧠 Tumhara **naam yaad** rakhti hai ("mera naam Rahul hai" bolo)
- 🎭 **Mood** samajhti hai - sad ho toh empathetic, happy ho toh celebrate
- 🕐 Time ke hisab se greeting (good morning / good evening)
- 🤷 Samajh na aaye toh AI jaisa lecture nahi, human jaisa react karti hai - "accha? aur batao", "wait kya matlab?"
- 📚 Btech, exam, assignment, canteen, Noida - in sab pe natural baat karti hai

## Bot banane ke steps (ek baar)

1. Telegram kholo aur **@BotFather** ko message karo
2. `/newbot` likho
3. Bot ka naam: `Adya`
4. Bot ka username: kuch bhi, jaise `adya_ki_bot` (end me `bot` hona chahiye)
5. BotFather token dega, jaise `123456789:AAE...`

## Run karne ke steps

```bash
cd adya-bot
pip install -r requirements.txt
cp .env.example .env
# .env file kholo aur BOT_TOKEN me apna token paste karo
python bot.py
```

Fir Telegram par apne bot ko `/start` karo. Bas, Adya online! 💛

## Bina token ke test

```bash
python brain.py
```

Isse pata chalega Adya kaise reply karti hai, bina Telegram ke.

## 24x7 chalana hai?

Ye bot yahan sandbox me tab tak chalega jab tak run hai. Hamesha chalu rakhne ke liye Railway / Render / VPS par deploy karna padega - mujhse pucho, mai steps bata dunga.

## Files

| File | Kaam |
|---|---|
| `bot.py` | Telegram se connect hota hai, typing indicator, delay |
| `brain.py` | Adya ka dimaag - persona, mood, memory, replies |
| `requirements.txt` | Python libraries |
| `.env` | Tumhara secret token (ye file kisi ko mat bhejna!) |

## Customization

`brain.py` me `PERSONA` aur replies change karke Adya ko aur apne jaisa bana sakte ho. Naye topics add karne hain toh mujhe batao, mai add kar dunga.
