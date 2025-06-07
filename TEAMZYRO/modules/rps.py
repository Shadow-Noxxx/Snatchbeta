import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio

active_rps_games = {}

RPS_CHOICES = ["🪨 Rock", "📄 Paper", "✂️ Scissors"]
RPS_EMOJI = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

def rps_result(choice1, choice2):
    if choice1 == choice2:
        return 0
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    return 1 if wins[choice1] == choice2 else 2

# Start Game
@Client.on_message(filters.command("rps"))
async def rps(client, message: Message):
    chat_id = message.chat.id
    if chat_id in active_rps_games:
        await message.reply("❗ A game is already running in this chat!", parse_mode="html")
        return

    active_rps_games[chat_id] = {
        "players": [message.from_user.id],
        "usernames": {message.from_user.id: message.from_user.first_name},
        "choices": {},
        "started": False,
        "msg_id": None
    }

    sent = await message.reply(
        f"🎮 <b>Rock Paper Scissors Game Started!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Player 1: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n"
        f"⌛ Waiting for Player 2...\n"
        f"/joinrps to join.",
        parse_mode="html"
    )

    active_rps_games[chat_id]["msg_id"] = sent.id

    # Timeout if no one joins in 60 sec
    await asyncio.sleep(60)
    if chat_id in active_rps_games and not active_rps_games[chat_id]["started"]:
        await client.send_message(chat_id, "⌛ Game timed out due to inactivity.")
        active_rps_games.pop(chat_id, None)

# Join Game
@Client.on_message(filters.command("joinrps"))
async def join_rps(client, message: Message):
    chat_id = message.chat.id
    game = active_rps_games.get(chat_id)

    if not game:
        await message.reply("❌ No active game. Use /rps to start one.", parse_mode="html")
        return
    if len(game["players"]) >= 2:
        await message.reply("❗ Game already has 2 players.", parse_mode="html")
        return
    if message.from_user.id in game["players"]:
        await message.reply("⚠️ You already joined.", parse_mode="html")
        return

    game["players"].append(message.from_user.id)
    game["usernames"][message.from_user.id] = message.from_user.first_name
    game["started"] = True

    await message.reply(
        f"✅ <b>{message.from_user.first_name} joined!</b>\n"
        f"🎮 Game Started! Both players, choose your move:",
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
        await message.reply("🚫 Game cancelled.", parse_mode="html")
    else:
        await message.reply("⚠️ No game to cancel.")

# Handle Player Choice
@Client.on_callback_query(filters.regex(r"^rps_choice:"))
async def rps_button(client, query: CallbackQuery):
    try:
        choice = query.data.split(":")[1]
        chat_id = query.message.chat.id
        user_id = query.from_user.id

        game = active_rps_games.get(chat_id)
        if not game or not game.get("started"):
            await query.answer("❌ Game not active.", show_alert=True)
            return

        if user_id not in game["players"]:
            await query.answer("🚫 You're not part of this game.", show_alert=True)
            return

        if user_id in game["choices"]:
            await query.answer("⚠️ You've already picked.", show_alert=True)
            return

        if choice not in RPS_EMOJI:
            await query.answer("❌ Invalid choice.", show_alert=True)
            return

        game["choices"][user_id] = choice
        await query.answer(f"You chose {RPS_EMOJI[choice]}")

        if len(game["choices"]) == 2:
            p1, p2 = game["players"]
            c1, c2 = game["choices"][p1], game["choices"][p2]
            u1, u2 = game["usernames"][p1], game["usernames"][p2]

            result_text = (
                "🧠 <b>Rock Paper Scissors Result</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{u1}: {RPS_EMOJI[c1]}\n"
                f"{u2}: {RPS_EMOJI[c2]}\n"
                "━━━━━━━━━━━━━━━━━━━━━━━\n"
            )

            result = rps_result(c1, c2)
            if result == 0:
                result_text += "🤝 <b>It's a Draw!</b>"
            elif result == 1:
                result_text += f"🏆 <b>{u1} Wins!</b>"
            else:
                result_text += f"🏆 <b>{u2} Wins!</b>"

            await query.message.edit_text(result_text, parse_mode="html")
            active_rps_games.pop(chat_id, None)
        else:
            await query.answer("✅ Choice registered. Waiting for the other player.")
    except Exception as e:
        logging.exception("Error in RPS game")
        await query.answer("❌ An error occurred.", show_alert=True)
