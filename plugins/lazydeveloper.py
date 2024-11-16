import asyncio
from pyrogram import filters, Client
from config import *
from helpo.database import db 
from asyncio.exceptions import TimeoutError

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)
# user_forward_data = {}
St_Session = {}
handler = {}

def manager(id, value):
    global handler
    handler[id] = value
    return handler

def get_manager():
    global handler
    return handler


PHONE_NUMBER_TEXT = (
    "📞__ Now send your Phone number to Continue"
    " include Country code.__\n**Eg:** `+13124562345`\n\n"
    "Press /cancel to Cancel."
)


@Client.on_message(filters.private & filters.command("connect"))
async def generate_str(c, m):

    user_id = m.from_user.id

    # Check if the user is allowed to use the bot
    if not await verify_user(user_id):
        return await m.reply("⛔ You are not authorized to use this bot.")
    
    if user_id in St_Session:
        # Check if session already exists for this user
        return await m.reply("String session already connected! Use /rename")
    
    try:
        client = Client(":memory:", api_id=API_ID, api_hash=API_HASH)
    except Exception as e:
        return await c.send_message(m.chat.id ,f"**🛑 ERROR: 🛑** {str(e)}\nPress /login to create again.")

    try:
        await client.connect()
    except ConnectionError:
        await client.disconnect()
        await client.connect()

    while True:
        get_phone_number = await c.ask(
            chat_id=m.chat.id,
            text=PHONE_NUMBER_TEXT
        )
        phone_number = get_phone_number.text
        if await is_cancel(m, phone_number):
            return
        await get_phone_number.delete()
        await get_phone_number.request.delete()

        confirm = await c.ask(
            chat_id=m.chat.id,
            text=f'🤔 Is {phone_number} correct? (y/n): \n\ntype: y (If Yes)\ntype: n (If No)'
        )
        if await is_cancel(m, confirm.text):
            return
        if "y" in confirm.text.lower():
            await confirm.delete()
            await confirm.request.delete()
            break
    try:
        code = await client.send_code(phone_number)
        await asyncio.sleep(1)
    except FloodWait as e:
        return await m.reply(f"__Sorry to say you that you have floodwait of {e.x} Seconds 😞__")
    except ApiIdInvalid:
        return await m.reply("🕵‍♂ The API ID or API HASH is Invalid.\n\nPress /login to create again.")
    except PhoneNumberInvalid:
        return await m.reply("☎ Your Phone Number is Invalid.\n\nPress /login to create again.")

    try:
        # sent_type = {"app": "Telegram App 💌",
        #     "sms": "SMS 💬",
        #     "call": "Phone call 📱",
        #     "flash_call": "phone flash call 📲"
        # }[code.type]
        otp = await c.ask(
            chat_id=m.chat.id,
            text=(f"I had sent an OTP to the number {phone_number} through\n\n"
                  "Please enter the OTP in the format 1 2 3 4 5 __(provied white space between numbers)__\n\n"
                  "If Bot not sending OTP then try /start the Bot.\n"
                  "Press /cancel to Cancel."), timeout=300)
    except TimeoutError:
        return await m.reply("**⏰ TimeOut Error:** You reached Time limit of 5 min.\nPress /start to create again.")
    if await is_cancel(m, otp.text):
        return
    otp_code = otp.text
    await otp.delete()
    await otp.request.delete()
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code=' '.join(str(otp_code)))
    except PhoneCodeInvalid:
        return await m.reply("**📵 Invalid Code**\n\nPress /start to create again.") 
    except PhoneCodeExpired:
        return await m.reply("**⌚ Code is Expired**\n\nPress /start to create again.")
    except SessionPasswordNeeded:
        try:
            two_step_code = await c.ask(
                chat_id=m.chat.id, 
                text="🔐 This account have two-step verification code.\nPlease enter your second factor authentication code.\nPress /cancel to Cancel.",
                timeout=300
            )
        except TimeoutError:
            return await m.reply("**⏰ TimeOut Error:** You reached Time limit of 5 min.\nPress /start to create again.")
        if await is_cancel(m, two_step_code.text):
            return
        new_code = two_step_code.text
        await two_step_code.delete()
        await two_step_code.request.delete()
        try:
            await client.check_password(new_code)
        except Exception as e:
            return await m.reply(f"**⚠️ ERROR:** {str(e)}")
    except Exception as e:
        return await c.send_message(m.chat.id ,f"**⚠️ ERROR:** {str(e)}")
    try:
        session_string = await client.export_session_string()
        St_Session[m.from_user.id] = session_string 
        await client.send_message("me", f"**Your String Session 👇**\n\n{session_string}\n\nThanks For using {(await c.get_me()).mention(style='md')}")
        text = "✅ Successfully Generated Your String Session and sent to you saved messages.\nCheck your saved messages or Click on Below Button."
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="String Session ↗️", url=f"tg://openmessage?user_id={m.chat.id}")]]
        )
        await c.send_message(m.chat.id, text, reply_markup=reply_markup)
    except Exception as e:
        return await c.send_message(m.chat.id ,f"**⚠️ ERROR:** {str(e)}")
    try:
        await client.stop()
    except:
        pass

@Client.on_message(filters.private & filters.command("logout"))
async def logout_user(c, m):
    user_id = m.from_user.id
    # Check if the user is allowed to use the bot
    if not await verify_user(user_id):
        return await m.reply("⛔ You are not authorized to use this bot.")
    
    # Check if the user has an active session @LazyDeveloperr
    if user_id in St_Session:
        try:

            # Clear the user's session from St_Session @LazyDeveloperr
            del St_Session[user_id]

            # Send a confirmation message to the user @LazyDeveloperr
            await c.send_message(m.chat.id, "🟢 You have been successfully logged out.")
        
        except Exception as e:
            # Handle any errors during logout @LazyDeveloperr
            await c.send_message(m.chat.id, f"⚠️ Error during logout: {str(e)}")
    else:
        # If no active session is found, notify the user @LazyDeveloperr
        await c.send_message(m.chat.id, "🛑 No active session found to log out.")


@Client.on_message(filters.command("rename"))
async def rename(client, message):
    user_id = message.from_user.id
    # Check if the user is allowed to use the bot
    if not await verify_user(user_id):
        return await message.reply("⛔ You are not authorized to use this bot.")
    
    if message.from_user.id in St_Session:
        try:
            String_Session = St_Session[message.from_user.id]
            ubot = Client("Urenamer", session_string=String_Session, api_id=API_ID, api_hash=API_HASH)
            print("Ubot Connected")
        except Exception as e:
            print(e)
            return await message.reply("String Session Not Connected! Use /connect")
    else:
        return await message.reply("String Session Not Connected! Use /connect")

    await ubot.start()
 

    if not ubot:
        return  # Stop if ubot could not be connected

    chat_id = await client.ask(
        text="Send Channel Id From Where You Want To Forward in `-100XXXX` Format ",
        chat_id=message.chat.id
    )
    target_chat_id = int(chat_id.text)
    
    print(f'✅Set target chat => {target_chat_id}' )
    try:
        chat_info = await client.get_chat(target_chat_id)
        print(f"Got Chat info")
    except Exception as e:
        await client.send_message(message.chat.id, f"Something went wrong while accessing chat : {chat_info}")
        print(f"Error accessing chat: {e}")
    # Handle the exception appropriately

    Forward = await client.ask(
        text="Send Channel Id In Which You Want Renamed Files To Be Sent in `-100XXXX` Format ",
        chat_id=message.chat.id
    )
    Forward = int(Forward.text)
    print(f'🔥Set destination chat => {target_chat_id}' )


    await db.set_forward(message.from_user.id, Forward)

    print(f"Starting to forward files from channel {target_chat_id} to {BOT_USERNAME}.")

    # Using `ubot` to iterate through chat history in target chat
    file_count = 0
    
    async for msg in ubot.get_chat_history(target_chat_id):
        try:
            # Check if message has any file type (document, audio, video, etc.)
            if msg.document or msg.audio or msg.video:
                print("Found media message, copying to target...")
                await msg.copy(BOT_USERNAME)  # Send to target chat or bot PM
                await asyncio.sleep(3)  # Delay between each file sent
                print("Message forwarded successfully!")

                # Delete message after forwarding
                await ubot.delete_messages(target_chat_id, msg.id)
                print(f"Message {msg.id} deleted from target channel.")
                
                file_count += 1  # Increment the file_count

                if file_count == 10:
                    confirm = await client.ask(
                        chat_id=message.chat.id,
                        text=f'Completed 10 tasks! Do you want to continue forwarding? (y/n):\n\n'
                             'Type: `y` (If Yes)\nType: `n` (If No)'
                    )

                    if "n" in confirm.text.lower():  # If user wants to stop
                        await confirm.delete()
                        file_count = 0
                        break  # Stop forwarding
                    await confirm.delete()
                    file_count = 0

        except Exception as e:
            print(f"Error processing message {msg.id}: {e}")
            continue  # Move to next message on error

    await ubot.stop()
    print("Finished forwarding and deleting all files.")


async def is_cancel(msg: Message, text: str):
    if text.startswith("/cancel"):
        await msg.reply("⛔ Process Cancelled.")
        return True
    return False

async def verify_user(user_id: int):
    return user_id in ADMIN


