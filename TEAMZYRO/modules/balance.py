import html
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from TEAMZYRO import app, user_collection

OWNER_ID = [6138142369, 7819315360]  # Replace with actual owner Telegram user IDs

async def get_balance(user_id):
    user_data = await user_collection.find_one({'id': user_id}, {'balance': 1, 'tokens': 1})
    if user_data:
        return user_data.get('balance', 0), user_data.get('tokens', 0)
    return 0, 0

@app.on_message(filters.command("balance"))
async def balance(client: Client, message: Message):
    user_id = message.from_user.id
    user_balance, user_tokens = await get_balance(user_id)
    response = (
        f"{message.from_user.first_name} \n◈⌠ {user_balance} coins⌡\n"
        f"◈ ⌠ {user_tokens} Tokens⌡"
    )
    await message.reply_text(response, reply_to_message_id=False)

@app.on_message(filters.command("pay"))
async def pay(client: Client, message: Message):
    sender_id = message.from_user.id
    args = message.command

    if len(args) < 2:
        await message.reply_text("Usage: /pay <amount> [@username/user_id] or reply to a user.")
        return

    try:
        amount = int(args[1])
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.reply_text("Invalid amount. Please enter a positive number.")
        return

    recipient_id = None
    recipient_username = None

    if message.reply_to_message:
        recipient_id = message.reply_to_message.from_user.id
        recipient_username = message.reply_to_message.from_user.username
    elif len(args) > 2:
        try:
            recipient_id = int(args[2])
        except ValueError:
            recipient_username = args[2]
            user_data = await user_collection.find_one({'username': recipient_username}, {'id': 1})
            if user_data:
                recipient_id = user_data['id']

    if not recipient_id:
        await message.reply_text("Recipient not found. Reply to a user or provide a valid user ID/username.")
        return

    sender_balance, _ = await get_balance(sender_id)
    if sender_balance < amount:
        await message.reply_text("Insufficient balance.")
        return

    await user_collection.update_one({'id': sender_id}, {'$inc': {'balance': -amount}})
    await user_collection.update_one({'id': recipient_id}, {'$inc': {'balance': amount}})

    updated_sender_balance, _ = await get_balance(sender_id)
    updated_recipient_balance, _ = await get_balance(recipient_id)

    await message.reply_text(
        f"✅ You paid {amount} coins to @{html.escape(recipient_username or str(recipient_id))}."
        f"\n💰 Your New Balance: {updated_sender_balance} coins"
    )

    await client.send_message(
        chat_id=recipient_id,
        text=f"🎉 You received {amount} coins from @{message.from_user.username}!"
        f"\n💰 Your New Balance: {updated_recipient_balance} coins"
    )

@app.on_message(filters.command("kill"))
async def kill_handler(client: Client, message: Message):
    if message.from_user.id not in OWNER_ID:
        await message.reply_text("❌ Only the owner can use this command.")
        return

    if not message.reply_to_message:
        await message.reply_text("❌ Please reply to a user's message to use the /kill command.")
        return

    user_id = message.reply_to_message.from_user.id
    command_args = message.text.split()

    if len(command_args) < 2:
        await message.reply_text("Please specify an option: `c` to delete character, `f` to delete full data, or `b` to delete balance.")
        return

    option = command_args[1]

    try:
        if option == 'f':
            await user_collection.delete_one({"id": user_id})
            await message.reply_text("✅ Full data of the user has been deleted.")

        elif option == 'c':
            if len(command_args) < 3:
                await message.reply_text("Please specify a character ID to remove.")
                return

            char_id = command_args[2]
            user = await user_collection.find_one({"id": user_id})

            if user and 'characters' in user:
                characters = user['characters']
                updated_characters = [c for c in characters if c.get('id') != char_id]

                if len(updated_characters) == len(characters):
                    await message.reply_text(f"No character with ID {char_id} found.")
                    return

                await user_collection.update_one({"id": user_id}, {"$set": {"characters": updated_characters}})
                await message.reply_text(f"✅ Character with ID {char_id} removed.")

            else:
                await message.reply_text("❌ No characters found for this user.")

        elif option == 'b':
            if len(command_args) < 3:
                await message.reply_text("Please specify an amount to deduct from balance.")
                return

            try:
                amount = int(command_args[2])
            except ValueError:
                await message.reply_text("Invalid amount.")
                return

            user_data = await user_collection.find_one({"id": user_id}, {"balance": 1})
            if user_data and "balance" in user_data:
                new_balance = max(0, user_data["balance"] - amount)
                await user_collection.update_one({"id": user_id}, {"$set": {"balance": new_balance}})
                await message.reply_text(f"✅ {amount} coins deducted. New balance: {new_balance}")
            else:
                await message.reply_text("❌ User has no balance.")

        else:
            await message.reply_text("Invalid option. Use `c` for character, `f` for full data, or `b {amount}` to deduct balance.")

    except Exception as e:
        print(f"Error in /kill: {e}")
        await message.reply_text("An unexpected error occurred.")
