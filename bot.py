from pyrogram import Client, filters
import asyncio, json, os

# ========== CONFIG ==========
API_ID = 24203893
API_HASH = "6ba29d5fb7d359fe9afb138ea89873b4"
SESSION = "BAFxUnUAT9x61l0RT1tnOI7CiKRiUUtYpL7hxyoR5MlELoRWN8diwKefEvqh_TGdngltRTovxh3ngMbYFryG5yviJEDPXsVKJVugzkZcXCbFr8AVNqL_oLhSluUarbXR4C7jOpld5q6VwV2Rql0CruHtLGObiNmnxT9nro0dmaea4owI6nGbKb6X5AtDeibwS_BWxmVLc8VYuyAAcXbQwpTvEPgtVOBSi3sKwSml7H7CpwnVHwlG9JS-4SX9_xg8Uq2rnVd89m4M0_IgOHSDQoWSTVfSyCFdIu4GBWXudul7aWwZUZQShLSjzQtqRURP8pSLhXi0ZJR4p-yFJRzdoikxRzYhpwAAAAG243VNAA"

SOURCE_CHANNEL = -1002987979422   # Channel A (source)
DEST_CHANNEL = -1002860886608     # Channel B (destination)
PROGRESS_FILE = "progress.json"   # Resume ke liye
# ============================

app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)


# -------- Helper Functions ----------
def save_progress(msg_id: int):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"last_msg_id": msg_id}, f)


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f).get("last_msg_id", None)
    return None
# -----------------------------------


@app.on_message(filters.command("forward", prefixes="/") & filters.me)
async def forward_all(client, message):
    await message.edit("📤 Forwarding videos start ho raha hai...")

    last_id = load_progress()
    count = 0

    try:
        async for msg in client.get_chat_history(SOURCE_CHANNEL, offset_id=last_id):
            if msg.video:  # sirf videos forward karna
                try:
                    await msg.forward(DEST_CHANNEL)
                    save_progress(msg.id)
                    count += 1

                    # Har 50 video par progress update
                    if count % 50 == 0:
                        await message.edit(f"✅ {count} videos forward ho gayi...")

                    await asyncio.sleep(1)  # floodwait safe
                except Exception as e:
                    print("❌ Error:", e)
                    await asyncio.sleep(5)

        await message.edit(f"🎉 Forward complete! Total {count} videos bhej di gayi ✅")

    except Exception as e:
        await message.edit(f"⚠️ Error: {str(e)}")


print("🚀 Bot started. Telegram me /forward bhejna (apne account se).")
app.run()
