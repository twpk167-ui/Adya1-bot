"""
Adya - Human-like Telegram Bot
Persona: Adya, Btech student, Noida se
AI jaisa formal answer nahi, human jaisa casual Hinglish reply.
"""

import random
import re
from datetime import datetime
from zoneinfo import ZoneInfo

# ---------------- Persona ----------------
PERSONA = {
    "name": "Adya",
    "role": "Btech student",
    "city": "Noida",
    "style": "friendly, thodi si drama, casual Hinglish",
}

# Per-user memory (in-memory, bot restart par reset ho jayega)
memory = {}  # user_id -> {name, count, last_intent, mood}

def get_memory(user_id: int) -> dict:
    if user_id not in memory:
        memory[user_id] = {"name": None, "count": 0, "last_intent": None, "mood": "neutral"}
    return memory[user_id]

def now_ist():
    try:
        return datetime.now(ZoneInfo("Asia/Kolkata"))
    except Exception:
        return datetime.now()

def time_greeting():
    h = now_ist().hour
    if 4 <= h < 12:
        return "good morning"
    if 12 <= h < 17:
        return "good afternoon"
    if 17 <= h < 22:
        return "good evening"
    return "hey"

# ---------------- Humanizer ----------------
EMOJIS = ["😊", "😄", "😅", "🙂", "😌", "✨", "💛", "😴", "🤭", "😁"]

def humanize(text: str) -> str:
    """Text ko thoda human jaisa banata hai - kabhi emoji, kabhi casual tone."""
    # 35% chance emoji add karo, har baar nahi (warna bot jaisa lagega)
    if random.random() < 0.35 and not any(e in text for e in EMOJIS):
        text = text.rstrip(".! ") + " " + random.choice(EMOJIS)
    # Kabhi-kabhi first letter chhota kar do, bilkul casual lagta hai
    if random.random() < 0.20 and text:
        text = text[0].lower() + text[1:]
    return text

def split_messages(text: str):
    """Lambe reply ko 2 chhote bubbles me todta hai - human double-texting jaisa."""
    if len(text) <= 90:
        return [text]
    # Sentence boundary par todo
    parts = re.split(r'(?<=[.!?])\s+', text)
    if len(parts) >= 2:
        first = parts[0]
        rest = " ".join(parts[1:])
        if len(first) > 20 and len(rest) > 10:
            return [first, rest]
    return [text]

def typing_delay(text: str) -> float:
    """Reply ki length ke hisab se typing time - 0.8 se 3 sec."""
    base = 0.8 + len(text) / 60.0
    return min(max(base + random.uniform(0, 0.7), 0.8), 3.0)

def pick(options):
    return random.choice(options)

# ---------------- Brain / Intent Matching ----------------
def get_reply(user_id: int, raw_text: str) -> str:
    text = raw_text.strip()
    low = text.lower()
    mem = get_memory(user_id)
    mem["count"] += 1
    name = mem["name"]
    greet = time_greeting()

    # --- Name yaad karna: "mera naam Rahul hai" / "i am priya" / "call me X" ---
    m = re.search(r"(?:mera naam|my name is|call me|i am|main)\s+([a-zA-Z]{2,20})", low)
    if m and m.group(1) not in ["adya", "theek", "thik", "fine", "good", "ok"]:
        mem["name"] = m.group(1).capitalize()
        return humanize(pick([
            f"accha {mem['name']}! yaad rakh liya maine 😊 tum batao, kya chal raha hai?",
            f"ohh {mem['name']}! nice name. waise tum kya karte ho, padhai ya job?",
            f"done {mem['name']} 😄 ab batao, aaj ka din kaisa ja raha hai?",
        ]))

    # --- Greetings ---
    if re.search(r"\b(hi|hello|hey|hii|heyy|yo|hola|namaste|good (morning|evening|afternoon))\b", low):
        if mem["count"] == 1:
            return humanize(pick([
                f"heyy! {greet} 😊 mai Adya, tum kaun ho?",
                f"hii! {greet} batao kaise ho?",
                f"hey hey! mai Adya hu, Btech kar rahi hu Noida se. tum batao?",
            ]))
        return humanize(pick([
            f"heyy {name or ''}! phir se aa gaye 😄 batao kya hua?",
            "hii! batao, kya chal raha hai?",
            "hey! miss kar rahi thi tumhari baatein 😊",
        ]))

    # --- Kaise ho ---
    if re.search(r"kaise ho|kese ho|how are you|kaisi ho|kya haal|sup|wassup", low):
        return humanize(pick([
            "mai badhiya! thodi padhai me busy hu, tum batao 😊",
            "ekdum mast! bas assignment me phasi hu 😅 tum batao, sab theek hai?",
            "badhiya hu yaar, tum sunao. aaj kya kiya?",
            "theek hu! canteen ki chai pee ke mood ban gaya hai 😄 tum batao?",
        ]))

    # --- Tum kaun ho / tumhara naam ---
    if re.search(r"tum kaun|tumhara naam|your name|who are you|tum kya ho", low):
        return humanize(pick([
            "mai Adya hu! Btech kar rahi hu, Noida se belong karti hu 😊",
            "Adya! tumse baat karke accha lag raha hai. tum apne baare me batao?",
        ]))

    # --- Kahan se ho ---
    if re.search(r"kahan se|where are you from|kahan rehti|location", low):
        return humanize(pick([
            "Noida se! yahin ki hu mai 😄 tum kahan se ho?",
            "Noida! metro aur sector wali life hai meri 😅 tum batao?",
        ]))

    # --- Btech / padhai / college ---
    if re.search(r"btech|b\.tech|college|university|padhai|study|engineering|branch|sem|semester", low):
        return humanize(pick([
            "haan Btech kar rahi hu! padhai ka scene toh tumhe pata hi hai 😅 tum kya karte ho?",
            "Btech 3rd year chal raha hai mera. assignment aur attendance ka drama roz ka hai 😄 tum batao?",
            "padhai me hu yaar, exam ka pressure hai. tumhara kya scene hai?",
        ]))

    if re.search(r"exam|assignment|project|viva|attendance|result", low):
        return humanize(pick([
            "uff exam! mera bhi same haal hai 😅 kabhi-kabhi lagta hai padhai kab khatam hogi",
            "assignment ka toh pucho mat, raat bhar jaga hu. tumhara kab hai?",
            "result ka tension sabko hota hai yaar. tumne padhai shuru ki?",
        ]))

    # --- Bore ho raha hai ---
    if re.search(r"bore|boring|timepass|time pass|kuch nahi|free hu|free hoon", low):
        return humanize(pick([
            "bore ho rahe ho? chalo thodi baatein karte hain 😄 batao aaj kya interesting hua?",
            "same yaar! mai bhi bore ho rahi thi. koi joke sunau ya tum sunao?",
            "bore? toh kuch masti karte hain. chai piyo, mai yahin hu 😊",
        ]))

    # --- Sad / thak gaya / mood kharab ---
    if re.search(r"sad|udaas|thak gaya|thak gayi|tired|mood kharab|pareshan|stress|depress|rona|alone|akela|akeli", low):
        mem["mood"] = "sad"
        return humanize(pick([
            "arey kya hua? itna udaas kyun ho 😔 batao mujhe, mai sun rahi hu",
            "hmm... kabhi-kabhi aisa hota hai yaar. chai piyo aur batao kya hua, mai yahin hu 💛",
            "mood kharab hai? chalo thodi der baat karte hain, halka ho jayega 😊",
        ]))

    # --- Happy / mast ---
    if re.search(r"happy|khush|mast|badhiya|accha din|good day|excited", low):
        mem["mood"] = "happy"
        return humanize(pick([
            "wahh! sunke accha laga 😄 aisa hi khush raho hamesha",
            "mast hai yaar! kya hua aaj, kuch special hai kya? ✨",
            "badhiya! tum khush ho toh mai bhi khush 😊",
        ]))

    # --- Khana / bhook ---
    if re.search(r"khana|bhook|bhooke|khaya|eat|food|chai|coffee", low):
        return humanize(pick([
            "khana khaya? mai toh canteen ka khana kha ke bore ho gayi hu 😅",
            "bhook lagi hai? chai piyo pehle, mai bhi chai wali hu ☕",
            "aaj kya khaya? batao, mai bhi try karungi kabhi 😄",
        ]))

    # --- Joke ---
    if re.search(r"joke|hasao|funny|comedy", low):
        return humanize(pick([
            "ek suno 😄 teacher: padhai me mann nahi lagta? student: sir, mann toh lagta hai, bas padhai me nahi lagta! kaisa laga?",
            "haha suno... pappu doctor ke paas gaya, bola doctor sahab jab mai sota hu toh bandar football khelte hue dikhai dete hain. doctor: ye dawai aaj raat se lena. pappu: kal se lu toh chalega? aaj final match hai! 😂",
            "ek aur suno... mai itni padhai karti hu ki kal raat sapne me bhi assignment dikha 😴 tum haso mat, sach hai!",
        ]))

    # --- Thank you ---
    if re.search(r"thank|shukriya|dhanyavad|thanks", low):
        return humanize(pick([
            "koi baat nahi 😊 dost ho tum mere",
            "arey mention not! aur kuch chahiye toh batao 💛",
            "haha welcome! aise hi baat karte raho mujhse",
        ]))

    # --- Bye ---
    if re.search(r"\b(bye|alvida|chalo bye|good night|goodnight|so raha|so rahi|ja raha|ja rahi)\b", low):
        return humanize(pick([
            "bye bye! jaldi wapas aana 😊 take care",
            "chalo, good night! sapne me milte hain 😴💛",
            "bye yaar! dhyan rakhna apna",
        ]))

    # --- Love / crush / pyar (friendly boundary ke saath) ---
    if re.search(r"love you|i love|pyar|crush|gf|bf|girlfriend|boyfriend|shaadi|marry", low):
        return humanize(pick([
            "arey wah 😅 itni jaldi? hum toh abhi dost bane hain. pehle chai toh piyo saath me ☕",
            "haha tum toh seedha dil ki baat pe aa gaye! pehle dosti pakki karte hain 😄",
            "aww cute ho tum... par abhi mai padhai me busy hu yaar 😊 dost banke raho?",
        ]))

    # --- Kya kar rahe ho ---
    if re.search(r"kya kar rahe|kya kar rahi|what are you doing|busy ho", low):
        return humanize(pick([
            "abhi toh padhai kar rahi thi, tum aa gaye toh ruk gayi 😄 tum batao?",
            "bas canteen me chai pee rahi hu. tum kya kar rahe ho?",
            "assignment me hu yaar 😅 tum batao, kuch interesting hai kya?",
        ]))

    # --- Help ---
    if re.search(r"help|madad|kya kar sakti|commands", low):
        return humanize(
            "mai Adya hu, tumse baatein karne ke liye yahan hu 😊 "
            "bas aise hi bolo - hi, kaise ho, bore ho raha hu, joke sunao, etc. "
            "koi command ki tension nahi, jaise dost se baat karte ho waise hi bolo."
        )

    # --- Sawal (question mark) - human jaisa react karo, AI jaisa lecture nahi ---
    if "?" in text:
        return humanize(pick([
            "hmm accha sawal hai... mere hisab se toh aisa hai, tumhara kya sochna hai?",
            "wait, ispe toh sochna padega 🤔 tum batao tumhe kya lagta hai?",
            "arey ye toh interesting hai! mai toh aise samjhti hu ki... tum aur batao, mai sun rahi hu",
            "hmm... sach batau toh mai bhi confuse hu isme 😅 tum kya sochte ho?",
        ]))

    # --- Fallback: human jaisa general reply, kabhi sawal wapas, kabhi react ---
    fallbacks = [
        "accha? aur batao, mai sun rahi hu 😊",
        "hmm samajh gayi... waise tum aur kya karte ho?",
        "ohh acha! interesting hai yaar. aur?",
        "wait kya matlab? thoda detail me batao na 😄",
        "haha sahi hai! tumhari baatein sunke accha lag raha hai",
        "hmm... toh fir kya hua uske baad?",
        "accha suno, aaj ka din kaisa gaya tumhara?",
        "sahi hai yaar! waise mai bhi aaj bore ho rahi thi, tum aa gaye toh accha laga 😊",
        "ohh! ye toh mujhe pata hi nahi tha. aur batao?",
        "hmm interesting... tumhe aisa kyun lagta hai?",
    ]
    # Agar user ne pehle bhi yahi type bola hai toh repeat mat karo
    reply = pick(fallbacks)
    # Kabhi-kabhi follow-up sawal jod do, conversation aage badhegi
    if random.random() < 0.4:
        reply += " " + pick(["tum batao?", "aur tum?", "kya chal raha hai aur?", "batao na?"])
    return humanize(reply)


# ---------------- Demo (bina token ke test) ----------------
if __name__ == "__main__":
    print("=== Adya Bot - Demo Mode (bina token ke brain test) ===\n")
    tests = [
        (1, "hi"),
        (1, "kaise ho"),
        (1, "mera naam Rahul hai"),
        (1, "bore ho raha hu"),
        (1, "joke sunao"),
        (1, "tum kahan se ho"),
        (1, "exam ka tension hai"),
        (1, "thank you"),
        (1, "bye"),
    ]
    for uid, msg in tests:
        reply = get_reply(uid, msg)
        print(f"User: {msg}")
        for part in split_messages(reply):
            print(f"Adya: {part}")
        print()
