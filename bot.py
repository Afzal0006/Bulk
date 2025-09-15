from pyrogram import Client
import asyncio

# ================= CONFIG =================
API_ID = 24203893       # my.telegram.org se lo
API_HASH = "6ba29d5fb7d359fe9afb138ea89873b4"
SESSION = "BAFxUnUAT9x61l0RT1tnOI7CiKRiUUtYpL7hxyoR5MlELoRWN8diwKefEvqh_TGdngltRTovxh3ngMbYFryG5yviJEDPXsVKJVugzkZcXCbFr8AVNqL_oLhSluUarbXR4C7jOpld5q6VwV2Rql0CruHtLGObiNmnxT9nro0dmaea4owI6nGbKb6X5AtDeibwS_BWxmVLc8VYuyAAcXbQwpTvEPgtVOBSi3sKwSml7H7CpwnVHwlG9JS-4SX9_xg8Uq2rnVd89m4M0_IgOHSDQoWSTVfSyCFdIu4GBWXudul7aWwZUZQShLSjzQtqRURP8pSLhXi0ZJR4p-yFJRzdoikxRzYhpwAAAAG243VNAA"  # Pyrogram session string ya file
SOURCE_CHANNEL = -1002987979422  # Channel A ka ID
DEST_CHANNEL = -1002860886608    # Channel B ka ID
# ===========================================

app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("forward", prefixes="/") & filters.me)
async def forward_all(client, message):
    await message.edit("📤 Forwarding all videos...")

    async for msg in client.get_chat_history(SOURCE_CHANNEL):
        if msg.video:  # sirf video wale messages
            try:
                await msg.forward(DEST_CHANNEL)
                await asyncio.sleep(1)  # floodwait se bachne ke liye
            except Exception as e:
                print("Error:", e)
                await asyncio.sleep(5)

    await message.edit("✅ Saare videos forward ho gaye!")

app.run()
