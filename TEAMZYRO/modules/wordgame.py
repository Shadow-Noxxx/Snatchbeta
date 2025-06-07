import random
import logging
import html
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from collections import defaultdict
from datetime import datetime, timedelta

# Enhanced word list with categories
WORD_CATEGORIES = {
    "general": [
        "ability", "able", "about", "above", "accept", "account", "across", "act", "action",
        "activity", "add", "address", "adult", "after", "again", "age", "ago", "air", "all",
        "animal", "answer", "any", "appear", "area", "arm", "art", "ask", "attack", "baby",
        "back", "bad", "bag", "ball", "bank", "base", "beach", "bear", "beat", "beautiful",
        "bed", "before", "begin", "behavior", "behind", "believe", "best", "better", "between",
        "big", "bird", "birth", "bit", "black", "blood", "blue", "board", "boat", "body",
        "bone", "book", "born", "both", "bottom", "box", "boy", "branch", "bread", "break",
        "bridge", "bright", "bring", "brother", "brown", "brush", "build", "building", "burn",
        "business", "busy", "but", "buy", "cake", "call", "camp", "can", "candle", "card",
        "care", "carry", "case", "cat", "catch", "cause", "center", "chain", "chair", "chance",
        "change", "chase", "check", "cheese", "chicken", "child", "children", "choice", "choose",
        "circle", "city", "class", "clean", "clear", "climb", "clock", "close", "cloth", "cloud",
        "coat", "cold", "collect", "color", "come", "common", "company", "compare", "cook", "cool",
        "copy", "corn", "corner", "correct", "cost", "cotton", "count", "country", "cover", "cow",
        "cross", "cry", "cup", "cut", "dance", "dark", "date", "daughter", "day", "dead",
        "deal", "dear", "death", "decide", "deep", "deer", "desk", "die", "different", "dinner",
        "dirty", "discover", "dog", "door", "double", "draw", "dream", "dress", "drink", "drive",
        "drop", "dry", "duck", "dust", "duty", "each", "ear", "early", "earth", "east",
        "easy", "eat", "egg", "eight", "either", "electric", "else", "empty", "end", "enjoy",
        "enough", "enter", "equal", "even", "evening", "event", "ever", "every", "exact", "example",
        "except", "exercise", "expect", "explain", "eye", "face", "fact", "fair", "fall", "family",
        "famous", "far", "farm", "fast", "fat", "father", "fear", "feed", "feel", "few",
        "field", "fight", "figure", "fill", "film", "final", "find", "fine", "finger", "finish",
        "fire", "first", "fish", "five", "flag", "flat", "floor", "flower", "fly", "fold",
        "food", "foot", "for", "force", "forest", "forget", "form", "forward", "four", "fox",
        "free", "fresh", "friend", "from", "front", "fruit", "full", "fun", "game", "garden",
        "gas", "gave", "general", "get", "girl", "give", "glass", "go", "gold", "good",
        "got", "grass", "great", "green", "ground", "group", "grow", "guess", "gun", "hair",
        "half", "hand", "hang", "happy", "hard", "hat", "have", "head", "hear", "heart",
        "heat", "heavy", "held", "help", "her", "here", "high", "hill", "him", "his",
        "hit", "hold", "hole", "home", "hope", "horse", "hot", "hour", "house", "how",
        "huge", "human", "hundred", "hunt", "hurry", "hurt", "ice", "idea", "if", "important",
        "inch", "include", "indeed", "inside", "instead", "into", "iron", "island", "it", "job",
        "join", "jump", "just", "keep", "key", "kill", "kind", "king", "knee", "knife",
        "know", "lady", "lake", "land", "language", "large", "last", "late", "laugh", "law",
        "lay", "lead", "learn", "least", "leave", "left", "leg", "length", "less", "let",
        "letter", "level", "lie", "life", "lift", "light", "like", "line", "lion", "list",
        "listen", "little", "live", "locate", "long", "look", "lost", "lot", "loud", "love",
        "low", "machine", "made", "main", "major", "make", "man", "many", "map", "mark",
        "market", "mass", "master", "match", "material", "matter", "may", "mean", "meant", "measure",
        "meat", "meet", "melody", "men", "metal", "method", "middle", "might", "mile", "milk",
        "million", "mind", "mine", "minute", "miss", "mix", "modern", "molecule", "moment", "money",
        "month", "moon", "more", "morning", "most", "mother", "motion", "mountain", "mouth", "move",
        "much", "music", "must", "name", "nation", "nature", "near", "necessary", "neck", "need",
        "never", "new", "next", "night", "nine", "no", "noise", "noon", "nor", "north",
        "nose", "note", "nothing", "notice", "now", "number", "numeral", "object", "observe", "ocean",
        "of", "off", "offer", "office", "often", "oil", "old", "on", "once", "one",
        "only", "open", "operate", "opposite", "or", "order", "organ", "original", "other", "our",
        "out", "over", "own", "oxygen", "page", "paint", "pair", "paper", "paragraph", "parent",
        "part", "particular", "party", "pass", "past", "path", "pattern", "pay", "people", "perhaps",
        "period", "person", "phrase", "pick", "picture", "piece", "pitch", "place", "plain", "plan",
        "plane", "planet", "plant", "play", "please", "plural", "poem", "point", "poor", "populate",
        "port", "pose", "position", "possible", "post", "pound", "power", "practice", "prepare", "present",
        "press", "pretty", "print", "probable", "problem", "process", "produce", "product", "proper", "property",
        "protect", "prove", "provide", "pull", "push", "put", "quart", "question", "quick", "quiet",
        "quite", "race", "radio", "rail", "rain", "raise", "ran", "range", "rather", "reach",
        "read", "ready", "real", "reason", "receive", "record", "red", "refer", "region", "remember",
        "repeat", "reply", "represent", "require", "rest", "result", "rich", "ride", "right", "ring",
        "rise", "river", "road", "rock", "roll", "room", "root", "rope", "rose", "round",
        "row", "rub", "rule", "run", "safe", "said", "sail", "salt", "same", "sand",
        "sat", "save", "say", "scale", "school", "science", "score", "sea", "search", "season",
        "seat", "second", "section", "see", "seed", "seem", "select", "self", "sell", "send",
        "sense", "sent", "serve", "set", "settle", "seven", "several", "shall", "shape", "share",
        "sharp", "she", "sheet", "shell", "shine", "ship", "shirt", "shoe", "shop", "shore",
        "short", "should", "shoulder", "shout", "show", "side", "sight", "sign", "silent", "silver",
        "similar", "simple", "since", "sing", "single", "sister", "sit", "six", "size", "skill",
        "skin", "sky", "slave", "sleep", "slip", "slow", "small", "smell", "smile", "snow",
        "so", "soft", "soil", "soldier", "solution", "some", "son", "song", "soon", "sound",
        "south", "space", "speak", "special", "speed", "spell", "spend", "spoke", "spot", "spread",
        "spring", "square", "stand", "star", "start", "state", "station", "stay", "steam", "steel",
        "step", "stick", "still", "stone", "stood", "stop", "store", "story", "straight", "strange",
        "stream", "street", "stretch", "string", "strong", "student", "study", "subject", "substance", "such",
        "sudden", "suffix", "sugar", "suggest", "summer", "sun", "supply", "support", "sure", "surface",
        "surprise", "swim", "syllable", "symbol", "system", "table", "tail", "take", "talk", "tall",
        "teach", "team", "teeth", "tell", "temperature", "ten", "term", "test", "than", "thank",
        "that", "the", "their", "them", "then", "there", "these", "they", "thick", "thin",
        "thing", "think", "third", "this", "those", "though", "thought", "thousand", "three", "through",
        "throw", "tie", "time", "tiny", "tire", "to", "together", "told", "tone", "too",
        "took", "tool", "top", "total", "touch", "toward", "town", "track", "trade", "train",
        "travel", "tree", "triangle", "trip", "trouble", "truck", "true", "try", "tube", "turn",
        "twelve", "twenty", "two", "type", "under", "unit", "until", "up", "upon", "us",
        "use", "usual", "valley", "value", "vary", "verb", "very", "view", "village", "visit",
        "voice", "vowel", "wait", "walk", "wall", "want", "war", "warm", "was", "wash",
        "watch", "water", "wave", "way", "we", "wear", "weather", "week", "weight", "well",
        "went", "were", "west", "what", "wheel", "when", "where", "whether", "which", "while",
        "white", "who", "whole", "whose", "why", "wide", "wife", "wild", "will", "win",
        "wind", "window", "wing", "winter", "wire", "wish", "with", "within", "without", "woman",
        "wonder", "wood", "word", "work", "world", "would", "write", "wrong", "wrote", "yard",
        "year", "yellow", "yes", "yet", "you", "young", "your"
    ],
    "animals": [
        "alligator", "ant", "bear", "bee", "bird", "camel", "cat", "cheetah", "chicken", "chimpanzee",
        "cow", "crocodile", "deer", "dog", "dolphin", "duck", "eagle", "elephant", "fish", "fly",
        "fox", "frog", "giraffe", "goat", "goldfish", "hamster", "hippopotamus", "horse", "kangaroo", "kitten",
        "lion", "lobster", "monkey", "octopus", "owl", "panda", "pig", "puppy", "rabbit", "rat",
        "scorpion", "seal", "shark", "sheep", "snail", "snake", "spider", "squirrel", "tiger", "turtle",
        "wolf", "zebra"
    ],
    "food": [
        "apple", "banana", "bread", "broccoli", "cake", "carrot", "cheese", "chicken", "chocolate", "coffee",
        "cookie", "corn", "egg", "fish", "fruit", "grape", "hamburger", "icecream", "juice", "lemon",
        "lettuce", "meat", "milk", "onion", "orange", "pasta", "pear", "pepper", "pie", "pizza",
        "potato", "rice", "salad", "sandwich", "soup", "steak", "strawberry", "sugar", "tea", "tomato",
        "vegetable", "water", "watermelon", "wine"
    ],
    "science": [
        "atom", "biology", "cell", "chemical", "chemistry", "computer", "data", "earth", "electric", "energy",
        "experiment", "force", "gas", "gravity", "heat", "light", "liquid", "machine", "magnet", "math",
        "metal", "microscope", "molecule", "motion", "oxygen", "physics", "plant", "power", "pressure", "radio",
        "robot", "science", "solar", "solid", "sound", "space", "star", "sun", "technology", "temperature",
        "universe", "vacuum", "virus", "water", "weather", "weight"
    ]
}

# Game settings
MAX_ROUNDS = 10
ROUND_TIME_LIMIT = 120  # 2 minutes per round in seconds

class ExplainGame:
    def __init__(self, chat_id, starter_id):
        self.chat_id = chat_id
        self.starter_id = starter_id
        self.current_word = None
        self.current_clue = None
        self.category = "general"
        self.guessed = False
        self.lead_dropped = False
        self.round_start_time = None
        self.rounds_played = 0
        self.scores = defaultdict(int)
        self.previous_words = set()
    
    def pick_random_word(self):
        # Get words from selected category
        words = WORD_CATEGORIES.get(self.category, WORD_CATEGORIES["general"])
        
        # Filter out previously used words
        available_words = [w for w in words if w not in self.previous_words]
        if not available_words:
            available_words = words  # Reset if all words used
        
        word = random.choice(available_words)
        self.previous_words.add(word)
        
        # Generate clue based on word length
        clue = f"📏 Word length: {len(word)} letters"
        if len(word) > 6:
            clue += f"\n🔤 Starts with: '{word[0]}'"
        
        return clue, word
    
    def time_remaining(self):
        if not self.round_start_time:
            return ROUND_TIME_LIMIT
        elapsed = (datetime.now() - self.round_start_time).total_seconds()
        return max(0, ROUND_TIME_LIMIT - int(elapsed))

active_games = {}  # {chat_id: ExplainGame}
global_leaderboard = defaultdict(int)  # {user_id: total_points}

async def send_new_round(app: Client, chat_id, announce=True):
    game = active_games.get(chat_id)
    if not game:
        return False
    
    clue, word = game.pick_random_word()
    game.current_word = word
    game.current_clue = clue
    game.guessed = False
    game.lead_dropped = False
    game.round_start_time = datetime.now()
    game.rounds_played += 1
    
    try:
        # DM the explainer
        await app.send_message(
            game.starter_id,
            f"🤫 <b>Your word to explain:</b> <code>{word.upper()}</code>\n"
            f"📚 Category: {game.category.title()}\n"
            f"💡 <i>Don't say the word! Describe it creatively.</i>",
            parse_mode="html"
        )
    except Exception as e:
        try:
            await app.send_message(
                chat_id,
                "⚠️ <b>Couldn't DM the explainer. Please start a conversation with me first!</b>",
                parse_mode="html"
            )
        except Exception:
            pass
        active_games.pop(chat_id, None)
        logging.error(f"Error DMing explainer: {e}")
        return False

    if announce:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔄 Change Word", callback_data="explain_changeword"),
                InlineKeyboardButton("🔄 Change Category", callback_data="explain_changecategory"),
            ],
            [
                InlineKeyboardButton("🪂 Drop Lead", callback_data="explain_droplead"),
                InlineKeyboardButton("⏱️ Time Left", callback_data="explain_timeleft"),
            ]
        ])
        
        explainer = await app.get_users(game.starter_id)
        time_limit = ROUND_TIME_LIMIT // 60  # Convert to minutes
        
        await app.send_message(
            chat_id,
            f"🎲 <b>Round {game.rounds_played}/{MAX_ROUNDS}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🧑‍🏫 <b>Explainer:</b> {explainer.mention()}\n"
            f"📚 <b>Category:</b> {game.category.title()}\n"
            f"❓ <b>Clue:</b> <i>{clue}</i>\n"
            f"⏳ <b>Time limit:</b> {time_limit} minutes\n\n"
            f"<i>Guess the word in chat! The explainer will give hints.</i>",
            parse_mode="html",
            reply_markup=keyboard
        )
    return True

@Client.on_message(filters.command(["explain", "explainword"]) & filters.group)
async def explain_start(app: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if chat_id in active_games:
        game = active_games[chat_id]
        if game.rounds_played >= MAX_ROUNDS:
            await end_game(app, chat_id)
            return
        await message.reply("❗ A game is already running! Use /explain_cancel to end it first.", parse_mode="html")
        return
    
    # Check if user is in private chat with bot
    try:
        await app.send_message(user_id, "✅ You can now start explaining words in groups!")
    except Exception:
        await message.reply(
            "⚠️ Please start a private chat with me first!\n"
            "This is needed so I can DM you the words to explain.",
            parse_mode="html"
        )
        return
    
    active_games[chat_id] = ExplainGame(chat_id, user_id)
    await send_new_round(app, chat_id)

@Client.on_callback_query(filters.regex("^explain_"))
async def explain_button_handler(app: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    game = active_games.get(chat_id)
    
    if not game:
        await query.answer("No active game.", show_alert=True)
        return
    
    if query.data == "explain_changeword":
        if game.starter_id != user_id:
            await query.answer("Only the explainer can change the word.", show_alert=True)
            return
        
        await query.answer("Changing word...")
        await send_new_round(app, chat_id, announce=False)
        
        # Edit original message
        explainer = await app.get_users(game.starter_id)
        await query.message.edit_text(
            f"🔄 <b>Word changed by {explainer.mention()}!</b>\n"
            f"📚 Category: {game.category.title()}\n"
            f"❓ <b>New Clue:</b> <i>{game.current_clue}</i>",
            parse_mode="html",
            reply_markup=query.message.reply_markup
        )
    
    elif query.data == "explain_changecategory":
        if game.starter_id != user_id:
            await query.answer("Only the explainer can change the category.", show_alert=True)
            return
        
        # Show category selection
        buttons = []
        for category in WORD_CATEGORIES.keys():
            buttons.append([InlineKeyboardButton(
                f"{'✅ ' if game.category == category else ''}{category.title()}",
                callback_data=f"explain_setcategory_{category}"
            )])
        
        buttons.append([InlineKeyboardButton("🔙 Back", callback_data="explain_back")])
        
        await query.message.edit_text(
            "📚 <b>Select a category:</b>",
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    
    elif query.data.startswith("explain_setcategory_"):
        if game.starter_id != user_id:
            await query.answer("Only the explainer can change the category.", show_alert=True)
            return
        
        new_category = query.data.split("_")[2]
        game.category = new_category
        await query.answer(f"Category set to {new_category}")
        await send_new_round(app, chat_id, announce=False)
        
        # Edit original message
        explainer = await app.get_users(game.starter_id)
        await query.message.edit_text(
            f"🔄 <b>Category changed by {explainer.mention()}!</b>\n"
            f"📚 <b>New Category:</b> {game.category.title()}\n"
            f"❓ <b>Clue:</b> <i>{game.current_clue}</i>",
            parse_mode="html",
            reply_markup=query.message.reply_markup
        )
    
    elif query.data == "explain_back":
        explainer = await app.get_users(game.starter_id)
        await query.message.edit_text(
            f"🎲 <b>Round {game.rounds_played}/{MAX_ROUNDS}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🧑‍🏫 <b>Explainer:</b> {explainer.mention()}\n"
            f"📚 <b>Category:</b> {game.category.title()}\n"
            f"❓ <b>Clue:</b> <i>{game.current_clue}</i>\n\n"
            f"<i>Guess the word in chat! The explainer will give hints.</i>",
            parse_mode="html",
            reply_markup=query.message.reply_markup
        )
    
    elif query.data == "explain_droplead":
        if game.starter_id != user_id:
            await query.answer("Only the explainer can drop the lead.", show_alert=True)
            return
        
        game.lead_dropped = True
        await query.message.edit_text(
            "🪂 <b>The explainer has dropped the lead!</b>\n"
            "Anyone can now take over as explainer.",
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎉 Take Lead", callback_data="explain_takelead")]
            ])
        )
        await query.answer("Lead dropped!")
    
    elif query.data == "explain_takelead":
        if not game.lead_dropped:
            await query.answer("Lead not dropped yet!", show_alert=True)
            return
        
        game.starter_id = user_id
        game.lead_dropped = False
        await send_new_round(app, chat_id)
        await query.answer("You are now the explainer!")
    
    elif query.data == "explain_timeleft":
        remaining = game.time_remaining()
        mins = remaining // 60
        secs = remaining % 60
        await query.answer(f"⏳ Time left: {mins}m {secs}s", show_alert=True)

@Client.on_message(filters.text & filters.group & ~filters.command(["explain", "explain_cancel", "explain_leaderboard", "explain_help"]))
async def explain_guess(app: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip().lower()
    
    game = active_games.get(chat_id)
    if not game or game.guessed:
        return
    
    # Check if time expired
    if game.time_remaining() <= 0:
        await message.reply(
            f"⏰ <b>Time's up!</b>\n"
            f"The word was: <code>{game.current_word.upper()}</code>\n"
            f"🔄 Starting new round...",
            parse_mode="html"
        )
        game.starter_id = user_id  # Let the last guesser be the next explainer
        await send_new_round(app, chat_id)
        return
    
    # Explainer can't guess
    if user_id == game.starter_id:
        # Check if explainer is saying the word directly
        if game.current_word in text:
            await message.reply("🚫 <b>No cheating! Don't say the word directly.</b>", parse_mode="html")
        return
    
    # Check guess
    if text == game.current_word:
        game.guessed = True
        game.scores[user_id] += 2  # Guesser gets 2 points
        game.scores[game.starter_id] += 1  # Explainer gets 1 point
        global_leaderboard[user_id] += 2
        global_leaderboard[game.starter_id] += 1
        
        guesser_mention = message.from_user.mention()
        explainer = await app.get_users(game.starter_id)
        
        await message.reply(
            f"🏆 <b>Correct!</b> {guesser_mention} guessed the word <code>{game.current_word.upper()}</code>!\n"
            f"👏 {explainer.mention()} explained it well!\n\n"
            f"➕ <b>Points:</b>\n"
            f"{guesser_mention}: +2\n"
            f"{explainer.mention()}: +1\n\n"
            f"🔄 Next round starting...",
            parse_mode="html"
        )
        
        # Check if max rounds reached
        if game.rounds_played >= MAX_ROUNDS:
            await end_game(app, chat_id)
            return
        
        # Next round with guesser as new explainer
        game.starter_id = user_id
        await send_new_round(app, chat_id)

async def end_game(app: Client, chat_id):
    game = active_games.pop(chat_id, None)
    if not game:
        return
    
    # Prepare scores
    sorted_scores = sorted(game.scores.items(), key=lambda x: x[1], reverse=True)
    
    # Build results message
    result_text = "🎉 <b>Game Over!</b> 🎉\n🏆 <b>Final Scores:</b>\n━━━━━━━━━━━━━━\n"
    
    for i, (user_id, score) in enumerate(sorted_scores[:10], 1):  # Top 10 only
        try:
            user = await app.get_users(user_id)
            mention = user.mention()
        except Exception:
            mention = f"User #{user_id}"
        result_text += f"{i}. {mention}: <b>{score}</b> points\n"
    
    await app.send_message(chat_id, result_text, parse_mode="html")
    
    # Check for global high scores
    global_sorted = sorted(global_leaderboard.items(), key=lambda x: x[1], reverse=True)
    if game.scores and global_sorted and game.scores.get(sorted_scores[0][0]) == global_sorted[0][1]:
        top_player = await app.get_users(sorted_scores[0][0])
        await app.send_message(
            chat_id,
            f"🌟 <b>Global High Score Alert!</b> 🌟\n"
            f"{top_player.mention()} has reached the global top score of {global_sorted[0][1]} points!",
            parse_mode="html"
        )

@Client.on_message(filters.command(["explain_cancel", "explain_stop"]) & filters.group)
async def explain_cancel(app: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in active_games:
        await end_game(app, chat_id)
        await message.reply("❌ <b>Game cancelled.</b>", parse_mode="html")
    else:
        await message.reply("No active game to cancel.")

@Client.on_message(filters.command(["explain_leaderboard", "explain_top"]) & filters.group)
async def explain_leaderboard(app: Client, message: Message):
    chat_id = message.chat.id
    game = active_games.get(chat_id)
    
    # Check for game-specific leaderboard
    if game and game.scores:
        sorted_scores = sorted(game.scores.items(), key=lambda x: x[1], reverse=True)
        text = "<b>🏅 Current Game Leaderboard</b>\n━━━━━━━━━━━━━━━━━━━\n"
        
        for i, (uid, pts) in enumerate(sorted_scores[:10], 1):  # Top 10 only
            try:
                user = await app.get_users(uid)
                mention = user.mention()
            except Exception:
                mention = f"User #{uid}"
            text += f"{i}. {mention} — <b>{pts}</b> points\n"
        
        await message.reply(text, parse_mode="html")
        return
    
    # Check for global leaderboard
    if global_leaderboard:
        sorted_global = sorted(global_leaderboard.items(), key=lambda x: x[1], reverse=True)
        text = "<b>🌍 Global Leaderboard</b>\n━━━━━━━━━━━━━━━━━━━\n"
        
        for i, (uid, pts) in enumerate(sorted_global[:10], 1):  # Top 10 only
            try:
                user = await app.get_users(uid)
                mention = user.mention()
            except Exception:
                mention = f"User #{uid}"
            text += f"{i}. {mention} — <b>{pts}</b> points\n"
        
        await message.reply(text, parse_mode="html")
    else:
        await message.reply("No scores yet! Start a game with /explain to begin scoring.")

@Client.on_message(filters.command("explain_help"))
async def explain_help(app: Client, message: Message):
    help_text = """
🎮 <b>Explain & Guess Game Help</b> 🎮

<b>How to Play:</b>
1. Use /explain to start a game
2. The explainer gets a word via DM
3. Others guess the word based on clues
4. Correct guesser becomes next explainer

<b>Commands:</b>
/explain - Start a new game
/explain_cancel - End current game
/explain_leaderboard - Show scores
/explain_help - Show this help

<b>Rules:</b>
- Explainer can't say the word directly
- Each round has a time limit
- Guesser gets 2 points, explainer gets 1
- Game ends after 10 rounds

<b>Tips:</b>
- Be creative with your explanations!
- Use synonyms and related words
- The clue shows word length and first letter
    """
    await message.reply(help_text, parse_mode="html")
