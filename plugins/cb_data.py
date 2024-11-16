from helpo.utils import progress_for_pyrogram, convert
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helpo.database import db
import os
import humanize
from PIL import Image
import time
from config import *

@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
    except:
        return

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    user_id = update.message.chat.id
    date = update.message.date
    await update.message.delete()
    await update.message.reply_text("__𝙿𝚕𝚎𝚊𝚜𝚎 𝙴𝚗𝚝𝚎𝚛 𝙽𝚎𝚠 𝙵𝚒𝚕𝚎𝙽𝚊𝚖𝚎...__",
                                    reply_to_message_id=update.message.reply_to_message.id,
                                    reply_markup=ForceReply(True))

handler = {}

def manager(id, value):
    global handlers
    handler[id] = value
    return handler


def get_manager():
    global handler
    return handler

@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    print(f"This is user id {update.from_user.id}")
    manager(update.from_user.id, True)

    type = update.data.split("_")[1]
    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file_path = f"downloads/{new_filename}"
    file = update.message.reply_to_message
    org_file = file
    ms = await update.message.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳...")
    c_time = time.time()
    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram,
                                        progress_args=("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳....", ms, c_time))
    except Exception as e:
        await ms.edit(e)
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    except:
        pass
    user_id = int(update.message.chat.id)
    ph_path = None
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.chat.id)
    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(media.file_size),
                                       duration=convert(duration))
        except Exception as e:
            await ms.edit(text=f"Your caption Error unexpected keyword ●> ({e})")
            return
    else:
        caption = f"**{new_filename}**"
    if (media.thumbs or c_thumb):
        if c_thumb:
            ph_path = await bot.download_media(c_thumb)
        else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
    await ms.edit("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....")
    c_time = time.time()
    print(f" Before getting forward This is user id {update.from_user.id}")
    try:
        forward_id = await db.get_forward(update.from_user.id)
    except Exception as e:
        print(e)
        pass
    if String_Session !="None":
        try:
            zbot = Client("Z4renamer", session_string=String_Session, api_id=API_ID, api_hash=API_HASH)
            print("Ubot Connected")
        except Exception as e:
            print(e)
        await zbot.start()
        try:
            if type == "document":
                suc = await zbot.send_document(
                    int(Permanent_4gb),
                    document=file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....", ms, c_time)
                )
            elif type == "video":
                suc = await zbot.send_video(
                    int(Permanent_4gb),
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....", ms, c_time)
                )
            elif type == "audio":
                suc = await zbot.send_audio(
                    int(Permanent_4gb),
                    audio=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....", ms, c_time)
                )
            try:
                await bot.copy_message(chat_id = update.message.chat.id, from_chat_id = int(Permanent_4gb),message_id = suc.id)
            except Exception as e:
                pass
            try:
                await bot.copy_message(chat_id = forward_id, from_chat_id = int(Permanent_4gb),message_id = suc.id)
            except Exception as e:
                pass
        except Exception as e:
            await ms.edit(f" Erro {e}")

            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            return
        
        # Delete the original file message in the bot's PM @LazyDeveloperr
        try:
            await file.delete()
            await suc.delete()
        except Exception as e:
            print(f"Error deleting original file message: {e}")
        
        await ms.delete()
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
    else:
        try:
            if type == "document":
                suc = await bot.send_document(
                    update.message.chat.id,
                    document=file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....", ms, c_time)
                )
            elif type == "video":
                suc = await bot.send_video(
                    update.message.chat.id,
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....", ms, c_time)
                )
            elif type == "audio":
                suc = await bot.send_audio(
                    update.message.chat.id,
                    audio=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("𝚃𝚁𝚈𝙸𝙽𝙶 𝚃𝙾 𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶....", ms, c_time)
                )
            try:
                await suc.copy(forward_id)
            except Exception as e:
                pass
        except Exception as e:
            await ms.edit(f" Erro {e}")
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            return
        
        # Delete the original file message in the bot's PM => @LazyDeveloperr
        try:
            await file.delete()
            await suc.delete()
        except Exception as e:
            print(f"Error deleting original file message: {e}")
        
        await ms.delete()
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)

    
    
