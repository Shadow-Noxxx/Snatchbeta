import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)

# Replace 'TEAMZYRO' and related variables accordingly
from TEAMZYRO import ZYRO as app

active_xo_games = {}

def check_xo_winner(board):
    for i in range(3):
        if board[i][0] != " " and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] != " " and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
    if board[0][0] != " " and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] != " " and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None

def create_board_markup(board):
    keyboard = []
    for i in range(3):
        row = []
        for j in range(3):
            cell = board[i][j]
            text = cell if cell != " " else "⬜️"
            data = f"xo_move:{i}:{j}" if cell == " " else "none"
            row.append(InlineKeyboardButton(text, callback_data=data))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

async def show_xo_board(client, chat_id, game, edit=False):
    board = game["board"]
    markup = create_board_markup(board)
    turn_user_id = game["players"][game["turn"]]
    text = f"<b>Tic-Tac-Toe</b>\nTurn: {game['usernames'][turn_user_id]} ({game['symbols'][turn_user_id]})\nTap a cell to play."
    try:
        if edit and game.get("message_id"):
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=game["message_id"],
                text=text,
                reply_markup=markup,
                parse_mode="html"
            )
        else:
            msg = await client.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=markup,
                parse_mode="html"
            )
            game["message_id"] = msg.id
    except Exception as e:
        logging.error(f"Error in show_xo_board: {e}")

@app.on_message(filters.command("xo"))
async def xo_start(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in active_xo_games:
        await message.reply_text("❗️A game is already active in this chat!")
        return

    active_xo_games[chat_id] = {
        "players": [message.from_user.id],
        "symbols": {},
        "board": [[" " for _ in range(3)] for _ in range(3)],
        "turn": 0,
        "started": False,
        "usernames": {message.from_user.id: message.from_user.first_name},
        "message_id": None
    }

    msg = await message.reply_text("✅ Waiting for a second player. Use /joinxo to join.")
    active_xo_games[chat_id]["message_id"] = msg.id

@app.on_message(filters.command("joinxo"))
async def join_xo(client: Client, message: Message):
    chat_id = message.chat.id
    user = message.from_user
    game = active_xo_games.get(chat_id)

    if not game:
        await message.reply_text("❌ No game found. Start one using /xo.")
        return
    if len(game["players"]) >= 2:
        await message.reply_text("❌ Already two players in the game!")
        return
    if user.id in game["players"]:
        await message.reply_text("❗️You already joined the game!")
        return

    game["players"].append(user.id)
    game["usernames"][user.id] = user.first_name
    game["symbols"] = {
        game["players"][0]: "❌",
        game["players"][1]: "⭕️"
    }
    game["started"] = True

    msg_id = game.get("message_id")
    start_msg = (
        f"🎲 Tic-Tac-Toe Started!\n"
        f"{game['usernames'][game['players'][0]]} is ❌\n"
        f"{game['usernames'][game['players'][1]]} is ⭕️\n"
        f"{game['usernames'][game['players'][0]]} goes first.\n"
    )

    if msg_id:
        await client.edit_message_text(chat_id, msg_id, start_msg)
    else:
        msg = await message.reply_text(start_msg)
        game["message_id"] = msg.id

    await show_xo_board(client, chat_id, game, edit=True)

@app.on_callback_query(filters.regex(r"^xo_move:\d+:\d+$"))
async def xo_move_handler(client: Client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user = callback_query.from_user
    game = active_xo_games.get(chat_id)

    if not game or not game["started"]:
        await callback_query.answer("❌ No active game.", show_alert=True)
        return

    if user.id not in game["players"]:
        await callback_query.answer("❌ You're not part of this game!", show_alert=True)
        return

    if game["players"][game["turn"]] != user.id:
        await callback_query.answer("⏳ Not your turn yet!", show_alert=True)
        return

    _, row, col = callback_query.data.split(":")
    row, col = int(row), int(col)

    if game["board"][row][col] != " ":
        await callback_query.answer("❌ Cell already taken!", show_alert=True)
        return

    symbol = game["symbols"][user.id]
    game["board"][row][col] = symbol

    winner = check_xo_winner(game["board"])
    is_draw = all(cell != " " for r in game["board"] for cell in r)
    msg_id = game.get("message_id")

    if winner:
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=f"🏆 {game['usernames'][user.id]} ({symbol}) wins! Congratulations!",
            parse_mode="html"
        )
        active_xo_games.pop(chat_id, None)
        return

    if is_draw:
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text="🤝 It's a draw! Good game!",
            parse_mode="html"
        )
        active_xo_games.pop(chat_id, None)
        return

    game["turn"] = 1 - game["turn"]
    await show_xo_board(client, chat_id, game, edit=True)
    await callback_query.answer()

@app.on_message(filters.command("cancelxo"))
async def cancel_xo(client: Client, message: Message):
    chat_id = message.chat.id
    game = active_xo_games.pop(chat_id, None)

    if game and game.get("message_id"):
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=game["message_id"],
            text="❌ The game has been cancelled."
        )
    else:
        await message.reply_text("No active game to cancel.")
