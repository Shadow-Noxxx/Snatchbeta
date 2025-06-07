from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from TEAMZYRO import app, db, OWNER_ID

sudo_users = db['sudo_users']

ALL_POWERS = [
    "add_character",
    "delete_character",
    "update_character",
    "approve_request",
    "approve_inventory_request",
    "VIP"
]

def is_owner(user_id):
    return user_id in OWNER_ID


@app.on_message(filters.command("saddsudo") & filters.reply)
async def add_sudo(client, message):
    if not is_owner(message.from_user.id):
        await message.reply("❌ You don't have permission.")
        return

    replied_user_id = message.reply_to_message.from_user.id
    existing_user = await sudo_users.find_one({"_id": replied_user_id})
    if existing_user:
        await message.reply_text(f"User `{replied_user_id}` is already a sudo.")
        return

    await sudo_users.update_one(
        {"_id": replied_user_id},
        {"$set": {"powers": {"add_character": True}}},
        upsert=True
    )
    await message.reply_text(f"✅ User `{replied_user_id}` added as sudo with 'add_character' power.")


@app.on_message(filters.command("sremovesudo"))
async def remove_sudo(client, message):
    if not is_owner(message.from_user.id):
        await message.reply("❌ You don't have permission.")
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1 and message.command[1].isdigit():
        user_id = int(message.command[1])
    else:
        await message.reply_text("❌ Please reply to a user or provide a valid user ID.")
        return

    existing_user = await sudo_users.find_one({"_id": user_id})
    if not existing_user:
        await message.reply_text(f"⚠️ User `{user_id}` is not a sudo.")
        return

    await sudo_users.delete_one({"_id": user_id})
    await message.reply_text(f"✅ User [{user_id}](tg://user?id={user_id}) removed from sudo.", disable_web_page_preview=True)


@app.on_message(filters.command("seditsudo") & filters.reply)
async def edit_sudo(client, message):
    if not is_owner(message.from_user.id):
        await message.reply("❌ You don't have permission.")
        return

    replied_user_id = message.reply_to_message.from_user.id
    user_data = await sudo_users.find_one({"_id": replied_user_id})
    if not user_data:
        await message.reply_text("❌ This user is not a sudo.")
        return

    powers = user_data.get("powers", {})
    buttons = []
    for power in ALL_POWERS:
        status = "Yes" if powers.get(power, False) else "No"
        buttons.append([
            InlineKeyboardButton(f"{power}", callback_data="noop"),
            InlineKeyboardButton(f"{status}", callback_data=f"toggle_{replied_user_id}_{power}")
        ])
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="close_keyboard")])

    await message.reply_text(
        f"🛠 Edit powers for `{replied_user_id}`:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(r"^toggle_(\d+)_(\w+)$"))
async def toggle_power(client, callback_query: CallbackQuery):
    if not is_owner(callback_query.from_user.id):
        await callback_query.answer("❌ You don't have permission.", show_alert=True)
        return

    user_id = int(callback_query.matches[0].group(1))
    power = callback_query.matches[0].group(2)

    user_data = await sudo_users.find_one({"_id": user_id})
    if not user_data:
        await callback_query.answer("❌ User not found.", show_alert=True)
        return

    new_status = not user_data.get("powers", {}).get(power, False)
    await sudo_users.update_one(
        {"_id": user_id},
        {"$set": {f"powers.{power}": new_status}}
    )
    await callback_query.answer(f"Power '{power}' set to {'Yes' if new_status else 'No'}.", show_alert=True)

    updated = await sudo_users.find_one({"_id": user_id})
    powers = updated.get("powers", {})
    buttons = []
    for p in ALL_POWERS:
        status = "Yes" if powers.get(p, False) else "No"
        buttons.append([
            InlineKeyboardButton(f"{p}", callback_data="noop"),
            InlineKeyboardButton(f"{status}", callback_data=f"toggle_{user_id}_{p}")
        ])
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="close_keyboard")])

    await callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(r"^close_keyboard$"))
async def close_keyboard(client, callback_query: CallbackQuery):
    if not is_owner(callback_query.from_user.id):
        await callback_query.answer("❌ You don't have permission.", show_alert=True)
        return

    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer("Closed!", show_alert=True)


@app.on_message(filters.command("sudolist"))
async def sudo_list(client, message):
    if not is_owner(message.from_user.id):
        await message.reply("❌ You don't have permission.")
        return

    users = await sudo_users.find().to_list(length=None)
    if not users:
        await message.reply_text("There are no sudo users.")
        return

    text = "🛠 **Sudo Users List:**\n\n"
    for user in users:
        uid = user["_id"]
        try:
            info = await client.get_users(uid)
            name = info.first_name
        except:
            name = "Unknown"
        text += f"➤ [{name}](tg://user?id={uid}) (`{uid}`)\n"

    await message.reply_text(text, disable_web_page_preview=True)
