import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

active_rps_games = {}

RPS_CHOICES = ["🪨 Rock", "📄 Paper", "✂️ Scissors"]
RPS_EMOJI = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

def rps_result(choice1, choice2):
    if choice1 == choice2:
        return 0  # Draw
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    return 1 if wins[choice1] == choice2 else 2

# Start Game
@Client.on_message(filters.command("rps"))
async def rps(client, message: Message):
    try:
        chat_id = message.chat.id
        if chat_id in active_rps_games:
            await message.reply("❗ <b>A game is already running in this chat!</b>", parse_mode="html")
            return

        active_rps_games[chat_id] = {
            "players": [message.from_user.id],
            "usernames": {message.from_user.id: message.from_user.first_name},
            "choices": {},
            "started": False
        }

        await message.reply(
            f"🎮 <b>Rock Paper Scissors Game Started!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Player 1: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n"
            f"Waiting for second player...\n"
            f"<i>Send /joinrps to join the game!</i>",
            parse_mode="html"
        )
    except Exception as e:
        logging.error(e)
        await message.reply("❌ <b>Failed to start the game.</b>", parse_mode="html")

# Join Game
@Client.on_message(filters.command("joinrps"))
async def join_rps(client, message: Message):
    chat_id = message.chat.id
    game = active_rps_games.get(chat_id)

    if not game:
        await message.reply("❌ <b>No active game. Start one with /rps</b>", parse_mode="html")
        return
    if len(game["players"]) >= 2:
        await message.reply("❌ <b>Game already has 2 players!</b>", parse_mode="html")
        return
    if message.from_user.id in game["players"]:
        await message.reply("❗ <b>You already joined the game.</b>", parse_mode="html")
        return

    game["players"].append(message.from_user.id)
    game["usernames"][message.from_user.id] = message.from_user.first_name
    game["started"] = True

    await message.reply(
        f"✅ <b>{message.from_user.first_name} joined!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>Both players, please select your move:</b>",
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🪨 Rock", callback_data="rps_choice:rock"),
                InlineKeyboardButton("📄 Paper", callback_data="rps_choice:paper"),
                InlineKeyboardButton("✂️ Scissors", callback_data="rps_choice:scissors")
            ]
        ])
    )

# Cancel Game
@Client.on_message(filters.command("cancelrps"))
async def cancel_rps(client, message: Message):
    chat_id = message.chat.id
    if chat_id in active_rps_games:
        active_rps_games.pop(chat_id)
        await message.reply("❌ <b>Rock Paper Scissors game cancelled.</b>", parse_mode="html")
    else:
        await message.reply("No active game to cancel.")

# Handle Player Choice
@Client.on_callback_query(filters.regex(r"^rps_choice:"))
async def rps_button(client, query: CallbackQuery):
    try:
        choice = query.data.split(":")[1]
        chat_id = query.message.chat.id
        user_id = query.from_user.id

        game = active_rps_games.get(chat_id)
        if not game or not game.get("started"):
            await query.message.edit_text("❌ <b>No active game. Start one with /rps</b>", parse_mode="html")
            return

        if user_id not in game["players"]:
            await query.answer("❌ You are not part of this game!", show_alert=True)
            return

        if user_id in game["choices"]:
            await query.answer("❗ You already made a choice.", show_alert=True)
            return

        if choice not in RPS_EMOJI:
            await query.answer("❌ Invalid choice.", show_alert=True)
            return

        game["choices"][user_id] = choice
        await query.answer(f"You chose {RPS_EMOJI[choice]}")

        # Show result when both played
        if len(game["choices"]) == 2:
            p1, p2 = game["players"]
            c1, c2 = game["choices"][p1], game["choices"][p2]
            u1, u2 = game["usernames"][p1], game["usernames"][p2]

            result_text = (
                "🪨📄✂️ <b>Rock Paper Scissors Result</b> 🪨📄✂️\n"
                "━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{u1}: <b>{RPS_EMOJI[c1]}</b>\n"
                f"{u2}: <b>{RPS_EMOJI[c2]}</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━\n"
            )

            result = rps_result(c1, c2)
            if result == 0:
                result_text += "🤝 <b>It's a draw!</b>"
            elif result == 1:
                result_text += f"🏆 <b>{u1} wins!</b>"
            else:
                result_text += f"🏆 <b>{u2} wins!</b>"

            await query.message.edit_text(result_text, parse_mode="html")
            active_rps_games.pop(chat_id, None)
        else:
            await query.answer("✅ Choice registered. Waiting for the other player...")
    except Exception as e:
        logging.error(e)
        await query.answer("❌ Error occurred.", show_alert=True)
