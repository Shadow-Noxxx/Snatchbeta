import random
import logging
import html
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from collections import defaultdict

WORD_LIST = [
            "ability", "able", "about", "above", "accept", "according", "account", "across", "act", "action",
            "activity", "actually", "add", "address", "administration", "admit", "adult", "affect", "after", "again",
            "against", "age", "agency", "agent", "ago", "agree", "agreement", "ahead", "air", "all",
            "allow", "almost", "alone", "along", "already", "also", "although", "always", "American", "among",
            "amount", "analysis", "and", "animal", "another", "answer", "any", "anyone", "anything", "appear",
            "apply", "approach", "area", "argue", "arm", "around", "arrive", "art", "article", "artist",
            "as", "ask", "assume", "at", "attack", "attention", "attorney", "audience", "author", "authority",
            "available", "avoid", "away", "baby", "back", "bad", "bag", "ball", "bank", "bar",
            "base", "be", "beat", "beautiful", "because", "become", "bed", "before", "begin", "behavior",
            "behind", "believe", "benefit", "best", "better", "between", "beyond", "big", "bill", "billion",
            "bit", "black", "blood", "blue", "board", "body", "book", "born", "both", "box",
            "boy", "break", "bring", "brother", "budget", "build", "building", "business", "but", "buy",
            "by", "call", "camera", "campaign", "can", "cancer", "candidate", "capital", "car", "card",
            "care", "career", "carry", "case", "catch", "cause", "cell", "center", "central", "century",
            "certain", "certainly", "chair", "challenge", "chance", "change", "character", "charge", "check", "child",
            "choice", "choose", "church", "citizen", "city", "civil", "claim", "class", "clear", "clearly",
            "close", "coach", "cold", "collection", "college", "color", "come", "commercial", "common", "community",
            "company", "compare", "computer", "concern", "condition", "conference", "Congress", "consider", "consumer", "contain",
            "continue", "control", "cost", "could", "country", "couple", "course", "court", "cover", "create",
            "crime", "cultural", "culture", "cup", "current", "customer", "cut", "dark", "data", "daughter",
            "day", "dead", "deal", "death", "debate", "decade", "decide", "decision", "deep", "defense",
            "degree", "democrat", "democratic", "describe", "design", "despite", "detail", "determine", "develop", "development",
            "die", "difference", "different", "difficult", "dinner", "direction", "director", "discover", "discuss", "discussion",
            "disease", "do", "doctor", "dog", "door", "down", "draw", "dream", "drive", "drop",
            "drug", "during", "each", "early", "east", "easy", "eat", "economic", "economy", "edge",
            "education", "effect", "effort", "eight", "either", "election", "else", "employee", "end", "energy",
            "enjoy", "enough", "enter", "entire", "environment", "environmental", "especially", "establish", "even", "evening",
            "event", "ever", "every", "everybody", "everyone", "everything", "evidence", "exactly", "example", "executive",
            "exist", "expect", "experience", "expert", "explain", "eye", "face", "fact", "factor", "fail",
            "fall", "family", "far", "fast", "father", "fear", "federal", "feel", "feeling", "few",
            "field", "fight", "figure", "fill", "film", "final", "finally", "financial", "find", "fine",
            "finger", "finish", "fire", "firm", "first", "fish", "five", "floor", "fly", "focus",
            "follow", "food", "foot", "for", "force", "foreign", "forget", "form", "former", "forward",
            "four", "free", "friend", "from", "front", "full", "fund", "future", "game", "garden",
            "gas", "general", "generation", "get", "girl", "give", "glass", "go", "goal", "good",
            "government", "great", "green", "ground", "group", "grow", "growth", "guess", "gun", "guy",
            "hair", "half", "hand", "hang", "happen", "happy", "hard", "have", "he", "head",
            "health", "hear", "heart", "heat", "heavy", "help", "her", "here", "herself", "high",
            "him", "himself", "his", "history", "hit", "hold", "home", "hope", "hospital", "hot",
            "hotel", "hour", "house", "how", "however", "huge", "human", "hundred", "husband", "I",
            "idea", "identify", "if", "image", "imagine", "impact", "important", "improve", "in", "include",
            "including", "increase", "indeed", "indicate", "individual", "industry", "information", "inside", "instead", "institution",
            "interest", "interesting", "international", "interview", "into", "investment", "involve", "issue", "it", "item",
            "its", "itself", "job", "join", "just", "keep", "key", "kid", "kill", "kind",
            "kitchen", "know", "knowledge", "land", "language", "large", "last", "late", "later", "laugh",
            "law", "lawyer", "lay", "lead", "leader", "learn", "least", "leave", "left", "leg",
            "legal", "less", "let", "letter", "level", "lie", "life", "light", "like", "likely",
            "line", "list", "listen", "little", "live", "local", "long", "look", "lose", "loss",
            "lot", "love", "low", "machine", "magazine", "main", "maintain", "major", "majority", "make",
            "man", "manage", "management", "manager", "many", "market", "marriage", "material", "matter", "may",
            "maybe", "me", "mean", "measure", "media", "medical", "meet", "meeting", "member", "memory",
            "mention", "message", "method", "middle", "might", "military", "million", "mind", "minute", "miss",
            "mission", "model", "modern", "moment", "money", "month", "more", "morning", "most", "mother",
            "mouth", "move", "movement", "movie", "Mr", "Mrs", "much", "music", "must", "my",
            "myself", "name", "nation", "national", "natural", "nature", "near", "nearly", "necessary", "need",
            "network", "never", "new", "news", "newspaper", "next", "nice", "night", "no", "none",
            "nor", "north", "not", "note", "nothing", "notice", "now", "number", "occur", "of",
            "off", "offer", "office", "officer", "official", "often", "oh", "oil", "ok", "old",
            "on", "once", "one", "only", "onto", "open", "operation", "opportunity", "option", "or",
            "order", "organization", "other", "others", "our", "out", "outside", "over", "own", "owner",
            "page", "pain", "painting", "paper", "parent", "part", "participant", "particular", "particularly", "partner",
            "party", "pass", "past", "patient", "pattern", "pay", "peace", "people", "per", "perform",
            "performance", "perhaps", "period", "person", "personal", "phone", "physical", "pick", "picture", "piece",
            "place", "plan", "plant", "play", "player", "PM", "point", "police", "policy", "political",
            "politics", "poor", "popular", "population", "position", "positive", "possible", "power", "practice", "prepare",
            "present", "president", "pressure", "pretty", "prevent", "price", "private", "probably", "problem", "process",
            "produce", "product", "production", "professional", "professor", "program", "project", "property", "protect", "prove",
            "provide", "public", "pull", "purpose", "push", "put", "quality", "question", "quickly", "quite",
            "race", "radio", "raise", "range", "rate", "rather", "reach", "read", "ready", "real",
            "reality", "realize", "really", "reason", "receive", "recent", "recently", "recognize", "record", "red",
            "reduce", "reflect", "region", "relate", "relationship", "religious", "remain", "remember", "remove", "report",
            "represent", "Republican", "require", "research", "resource", "respond", "response", "responsibility", "rest", "result",
            "return", "reveal", "rich", "right", "rise", "risk", "road", "rock", "role", "room",
            "rule", "run", "safe", "same", "save", "say", "scene", "school", "science", "scientist",
            "score", "sea", "season", "seat", "second", "section", "security", "see", "seek", "seem",
            "sell", "send", "senior", "sense", "series", "serious", "serve", "service", "set", "seven",
            "several", "sex", "sexual", "shake", "share", "she", "shoot", "short", "shot", "should",
            "shoulder", "show", "side", "sign", "significant", "similar", "simple", "simply", "since", "sing",
            "single", "sister", "sit", "site", "situation", "six", "size", "skill", "skin", "small",
            "smile", "so", "social", "society", "soldier", "some", "somebody", "someone", "something", "sometimes",
            "son", "song", "soon", "sort", "sound", "source", "south", "southern", "space", "speak",
            "special", "specific", "speech", "spend", "sport", "spring", "staff", "stage", "stand", "standard",
            "star", "start", "state", "statement", "station", "stay", "step", "still", "stock", "stop",
            "store", "story", "strategy", "street", "strong", "structure", "student", "study", "stuff", "style",
            "subject", "success", "successful", "such", "suddenly", "suffer", "suggest", "summer", "support", "sure",
            "surface", "system", "table", "take", "talk", "task", "tax", "teach", "teacher", "team",
            "technology", "television", "tell", "ten", "tend", "term", "test", "than", "thank", "that",
            "the", "their", "them", "themselves", "then", "theory", "there", "these", "they", "thing",
            "think", "third", "this", "those", "though", "thought", "thousand", "threat", "three", "through",
            "throughout", "throw", "thus", "time", "to", "today", "together", "tonight", "too", "top",
            "total", "tough", "toward", "town", "trade", "traditional", "training", "travel", "treat", "treatment",
            "tree", "trial", "trip", "trouble", "true", "truth", "try", "turn", "TV", "two",
            "type", "under", "understand", "unit", "until", "up", "upon", "us", "use", "usually",
            "value", "various", "very", "victim", "view", "violence", "visit", "voice", "vote", "wait",
            "walk", "wall", "want", "war", "watch", "water", "way", "we", "weapon", "wear",
            "week", "weight", "well", "west", "western", "what", "whatever", "when", "where", "whether",
            "which", "while", "white", "who", "whole", "whom", "whose", "why", "wide", "wife",
            "will", "win", "wind", "window", "wish", "with", "within", "without", "woman", "wonder",
            "word", "work", "worker", "world", "worry", "would", "write", "writer", "wrong", "yard",
            "yeah", "year", "yes", "yet", "you", "young", "your", "yourself",
            
        ]

active_explain_games = {}
explain_leaderboard = defaultdict(lambda: defaultdict(int))  # {chat_id: {user_id: points}}

def pick_random_word():
    word = random.choice(WORD_LIST)
    clue = f"Word length: {len(word)}"
    return clue, word

async def send_new_word(app: Client, chat_id, game, announce=True):
    clue, word = pick_random_word()
    game["word"] = word
    game["clue"] = clue
    game["guessed"] = False
    game["lead_dropped"] = False
    starter = game["starter"]

    try:
        await app.send_message(
            starter,
            f"🤫 <b>Your word to explain:</b> <code>{word.upper()}</code>\n"
            f"Don't say the word! Explain it in the group so others can guess.",
            parse_mode="html"
        )
    except Exception as e:
        try:
            await app.send_message(
                chat_id,
                "⚠️ <b>Couldn't DM the explainer the word. Please start a private chat with me first!</b>",
                parse_mode="html"
            )
        except Exception:
            pass
        active_explain_games.pop(chat_id, None)
        logging.error(f"Error DMing starter: {e}")
        return False

    if announce:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔄 Change Word", callback_data="explain_changeword"),
                InlineKeyboardButton("🪂 Drop Lead", callback_data="explain_droplead"),
            ]
        ])
        user = await app.get_users(starter)
        await app.send_message(
            chat_id,
            f"🎲 <b>New Round Started!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>{user.mention()}</b> is the explainer (lead).\n"
            f"❓ <b>Clue:</b> <i>{clue}</i>\n"
            f"Everyone else: Guess the word in chat!\n"
            f"<i>(The explainer can't say the word directly!)</i>",
            parse_mode="html",
            reply_markup=keyboard
        )
    return True

@Client.on_message(filters.command("explainword") & filters.group)
async def explainword_start(app: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id in active_explain_games:
        await message.reply("❗ <b>An explain & guess game is already running in this chat!</b>", parse_mode="html")
        return

    active_explain_games[chat_id] = {
        "word": None,
        "starter": user_id,
        "clue": None,
        "guessed": False,
        "lead_dropped": False,
    }

    await send_new_word(app, chat_id, active_explain_games[chat_id])

@Client.on_callback_query(filters.regex("^explain_"))
async def explainword_button_handler(app: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    game = active_explain_games.get(chat_id)
    if not game or game.get("guessed"):
        await query.answer("No active explain & guess game.", show_alert=True)
        return

    if query.data == "explain_changeword":
        if game["starter"] != user_id:
            await query.answer("Only the explainer can change the word.", show_alert=True)
            return
        clue, word = pick_random_word()
        game["word"] = word
        game["clue"] = clue
        await app.send_message(user_id, f"🤫 <b>Your new word:</b> <code>{word.upper()}</code>", parse_mode="html")
        await query.message.edit_text(
            f"🔄 <b>Word changed!</b>\n❓ <b>Clue:</b> <i>{clue}</i>",
            parse_mode="html",
            reply_markup=query.message.reply_markup
        )

    elif query.data == "explain_droplead":
        if game["starter"] != user_id:
            await query.answer("Only the explainer can drop the lead.", show_alert=True)
            return
        game["lead_dropped"] = True
        await query.message.edit_text(
            "🪂 <b>The explainer has dropped the lead!</b>\nAnyone can now take the lead.",
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎉 Take Lead", callback_data="explain_takelead")]])
        )
        await query.answer("Lead dropped!")

    elif query.data == "explain_takelead":
        if not game.get("lead_dropped"):
            await query.answer("Lead not dropped yet!", show_alert=True)
            return
        game["starter"] = user_id
        game["lead_dropped"] = False
        await send_new_word(app, chat_id, game, announce=True)
        await query.answer("You are now the explainer!")

@Client.on_message(filters.text & filters.group & ~filters.command(["explainword", "explainword_cancel", "explainword_leaderboard"]))
async def explainword_guess(app: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip().lower()

    if chat_id not in active_explain_games:
        return
    game = active_explain_games[chat_id]
    word = game["word"]
    starter = game["starter"]

    if user_id == starter:
        return

    if text == word.lower():
        game["guessed"] = True
        explain_leaderboard[chat_id][user_id] += 1
        explain_leaderboard[chat_id][starter] += 1
        starter_user = await app.get_users(starter)
        await message.reply(
            f"🏆 <b>Correct!</b>\n"
            f"<b>{message.from_user.mention()}</b> guessed the word <code>{word.upper()}</code>!\n"
            f"👏 <b>{starter_user.mention()}</b> explained it well!\n"
            f"Both get +1 point.\n🔄 Next round starting...",
            parse_mode="html"
        )
        game["starter"] = user_id
        await send_new_word(app, chat_id, game, announce=True)

    elif word.lower() in text:
        await message.reply("🚫 <b>No cheating! Don't say the word directly.</b>", parse_mode="html")

@Client.on_message(filters.command("explainword_cancel") & filters.group)
async def explainword_cancel(app: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in active_explain_games:
        active_explain_games.pop(chat_id)
        await message.reply("❌ <b>Game cancelled.</b>", parse_mode="html")
    else:
        await message.reply("No active game to cancel.")

@Client.on_message(filters.command("explainword_leaderboard") & filters.group)
async def explain_leaderboard_command(app: Client, message: Message):
    chat_id = message.chat.id
    board = explain_leaderboard[chat_id]
    if not board:
        await message.reply("🏅 No points yet! Play to start scoring.", parse_mode="html")
        return

    sorted_board = sorted(board.items(), key=lambda x: x[1], reverse=True)
    text = "<b>🏅 Leaderboard</b>\n━━━━━━━━━━━━━━\n"
    for i, (uid, pts) in enumerate(sorted_board, 1):
        try:
            user = await app.get_users(uid)
            mention = user.mention()
        except Exception:
            mention = f"<code>{uid}</code>"
        text += f"{i}. {mention} — <b>{pts}</b> points\n"
    await message.reply(text, parse_mode="html")
