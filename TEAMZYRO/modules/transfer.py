from pyrogram import Client, filters
from pyrogram.types import Message
from TEAMZYRO import app as Client, user_collection, OWNER_ID


@Client.on_message(filters.command("transfer"))
async def transfer_collection(client: Client, message: Message):
    sender_id = message.from_user.id

    if sender_id not in OWNER_ID:
        await message.reply_text("❌ You don't have permission to use this command.")
        return

    try:
        args = message.command[1:]  # Skip the command itself
        if len(args) != 2:
            await message.reply_text('❌ Incorrect format.\nUse: `/transfer user_id owner_id`', quote=True)
            return

        user_id = int(args[0])
        owner_id = int(args[1])

        # Fetch both user and owner from the database
        user = await user_collection.find_one({'id': user_id})
        owner = await user_collection.find_one({'id': owner_id})

        if not user:
            await message.reply_text('❌ User not found.')
            return
        if not owner:
            await message.reply_text('❌ Owner not found.')
            return

        user_characters = user.get('characters', [])
        owner_characters = owner.get('characters', [])

        if user_characters:
            # Transfer from user to owner
            await user_collection.update_one(
                {'id': owner_id},
                {'$push': {'characters': {'$each': user_characters}}}
            )
            await user_collection.update_one(
                {'id': user_id},
                {'$set': {'characters': []}}
            )
            await message.reply_text(
                f"✅ Transferred {len(user_characters)} characters from user `{user_id}` to owner `{owner_id}`."
            )

        elif owner_characters:
            # Transfer from owner to user
            await user_collection.update_one(
                {'id': user_id},
                {'$push': {'characters': {'$each': owner_characters}}}
            )
            await user_collection.update_one(
                {'id': owner_id},
                {'$set': {'characters': []}}
            )
            await message.reply_text(
                f"✅ Transferred {len(owner_characters)} characters from owner `{owner_id}` to user `{user_id}`."
            )

        else:
            await message.reply_text("⚠️ Neither the user nor the owner have characters to transfer.")

    except Exception as e:
        await message.reply_text(f"❌ An error occurred:\n`{str(e)}`")
