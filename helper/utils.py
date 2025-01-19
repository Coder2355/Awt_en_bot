import asyncio
import math, time
from . import *
from datetime import datetime as dt
import sys
import shutil
import signal
import os
import re
from pathlib import Path
from datetime import datetime
import psutil
from pathlib import Path
from pytz import timezone
from config import Config
import subprocess
from math import floor
from script import Txt
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto


QUEUE = []

user_operations = {}


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "{0}{1}".format(
            ''.join(["⬢" for i in range(math.floor(percentage / 5))]),
            ''.join(["⬡" for i in range(20 - math.floor(percentage / 5))])
        )
        tmp = progress + Txt.PROGRESS_BAR.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )

        try:
            # Store the operation in the user_operations dictionary
            user_operations[message.chat.id] = message

            # Update the progress message
            await message.edit(
                text=f"{ud_type}\n\n{tmp}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data=f"close-{message.chat.id}")]]
                )
            )
        except Exception as e:
            print(e)
            pass

def humanbytes(size):    
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
        ((str(hours) + "ʜ, ") if hours else "") + \
        ((str(minutes) + "ᴍ, ") if minutes else "") + \
        ((str(seconds) + "ꜱ, ") if seconds else "") + \
        ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    return tmp[:-2] 

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def ts(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]


async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        botusername = await b.get_me()
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')
        await b.send_message(
            Config.LOG_CHANNEL,
            f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\nUꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\nDᴀᴛᴇ: {date}\nTɪᴍᴇ: {time}\n\nBy: @{botusername.username}"
        )
        

def Filename(filename, mime_type):
    if filename.split('.')[-1] in ['mkv', 'mp4', 'mp3', 'mov']:

        return filename

    else:
        if mime_type.split('/')[1] in ['pdf', 'mkv', 'mp4', 'mp3']:
            return f"{filename}.{mime_type.split('/')[1]}"
        
        elif mime_type.split('/')[0] == "audio":
            return f"{filename}.mp3"

        else:
            return f"{filename}.mkv"
            
async def CANT_CONFIG_GROUP_MSG(client, message):
    botusername = await client.get_me()
    btn = [
        [InlineKeyboardButton(text='Bᴏᴛ Pᴍ', url=f'https://t.me/{botusername.username}')]
    ]
    ms = await message.reply_text(text="Sᴏʀʀʏ Yᴏᴜ Cᴀɴ'ᴛ Cᴏɴғɪɢ Yᴏᴜʀ Sᴇᴛᴛɪɴɢs\n\nFɪʀsᴛ sᴛᴀʀᴛ ᴍᴇ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍʏ ғᴇᴀᴛᴜᴇʀs ɪɴ ɢʀᴏᴜᴘ", reply_to_message_id = message.id, reply_markup=InlineKeyboardMarkup(btn))

    await asyncio.sleep(10)
    await ms.delete()


import math
import time


def format_time(seconds):
    """Convert seconds into a human-readable format."""
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    if hours > 0:
        return f"{hours}h {mins}m {secs}s"
    elif mins > 0:
        return f"{mins}m {secs}s"
    else:
        return f"{secs}s"


def progress_bar(completed, total, length=20):
    """Generate a progress bar."""
    progress = math.floor(length * completed / total)
    bar = "█" * progress + "░" * (length - progress)
    return f"[{bar}]"




async def Compress_Stats(e, userid):
    if int(userid) not in [e.from_user.id, 0]:
        return await e.answer(
            f"⚠️ Hᴇʏ {e.from_user.first_name}\nYᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇ sᴛᴀᴛᴜs ᴀs ᴛʜɪs ɪs ɴᴏᴛ ʏᴏᴜʀ ғɪʟᴇ", 
            show_alert=True
        )

    # Input and output paths
    input_folder = f"ffmpeg/{e.from_user.id}/"
    output_folder = f"encode/{e.from_user.id}/"
    inp = os.path.join(input_folder, os.listdir(input_folder)[0])
    outp = os.path.join(output_folder, os.listdir(output_folder)[0])

    try:
        # Get input file size
        input_size = Path(inp).stat().st_size
        
        # Check if output file exists before encoding starts
        output_size_before = Path(outp).stat().st_size if Path(outp).exists() else 0
        
        # Calculate progress for compressed file
        # If output file exists, calculate progress
        output_size = Path(outp).stat().st_size if Path(outp).exists() else 0
        percentage = (output_size / input_size) * 100 if input_size > 0 else 0
        bar = progress_bar(output_size, input_size)

        # Encoding speed (calculating based on elapsed time)
        start_time = e.message.date.timestamp()
        elapsed_time = time.time() - start_time
        encoding_speed = output_size / elapsed_time if elapsed_time > 0 else 0  # Bytes per second
        encoding_speed_human = humanbytes(encoding_speed) + "/s"

        # Time left (remaining size / encoding speed)
        remaining_size = input_size - output_size
        time_left = remaining_size / encoding_speed if encoding_speed > 0 else 0
        time_left_formatted = TimeFormatter(time_left)

        # Formatting output values
        compressed_size = humanbytes(output_size)
        original_size = humanbytes(input_size)
        output_size_before_human = humanbytes(output_size_before)

        # Estimate the compressed size if the process isn't finished
        estimated_compressed_size = humanbytes(output_size_before)  # Before encoding starts

        ans = (
            f"**Encoding Status:**\n"
            f"**File**: `{inp.replace(f'ffmpeg/{userid}/', '').replace('_', '')}`\n"
            f"**Progress**: `{percentage:.2f}%`\n"
            f"{bar}\n\n"
            f"**Compressed Size Before Encoding**: `{output_size_before_human}`\n"
            f"**Compressed Size Now**: `{compressed_size}`\n"
            f"**Original Size**: `{original_size}`\n"
            f"**Estimated Compressed Size**: `{estimated_compressed_size}`\n"
            f"**Encoding Speed**: `{encoding_speed_human}`\n"
            f"**Estimated Time Left**: `{time_left_formatted}`"
        )

        # Ensure the message length is within limits
        if len(ans) > 200:
            ans = ans[:197] + "..."

        await e.answer(ans, cache_time=0, show_alert=True)

    except Exception as er:
        print(er)
        await e.answer(
            "Something went wrong. Please send the media again.", cache_time=0, show_alert=True
        )




async def skip(e, userid):

    if int(userid) not in [e.from_user.id, 0]:
        return await e.answer(f"⚠️ Hᴇʏ {e.from_user.first_name}\nYᴏᴜ ᴄᴀɴ'ᴛ ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇss ᴀs ʏᴏᴜ ᴅɪᴅɴ'ᴛ sᴛᴀʀᴛ ɪᴛ", show_alert=True)
    try:
        await e.message.delete()
        os.system(f"rm -rf ffmpeg/{userid}*")
        os.system(f"rm -rf encode/{userid}*")
        for proc in psutil.process_iter():
            processName = proc.name()
            processID = proc.pid
            print(processName , ' - ', processID)
            if(processName == "ffmpeg"):
             os.kill(processID,signal.SIGKILL)
    except Exception as e:
        pass
    try:
        shutil.rmtree(f'ffmpeg' + '/' + str(userid))
        shutil.rmtree(f'encode' + '/' + str(userid))
    except Exception as e:
        pass
    
    return


async def update_progress_bar(ms, progress, size_done, size_total, estimated_size, speed, elapsed, time_left):
    """
    Updates the encoding progress dynamically every 3 seconds.
    """
    progress_bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
    new_content = (
        f"⚠️ **Encoding...**\n"
        f"Progress: [{progress_bar}] {progress:.2f}%\n\n"
        f"📦 **Size:** {size_done:.2f} MB out of ~ {estimated_size:.2f} MB\n"
        f"⚡ **Speed:** {speed:.2f} KB/s\n"
        f"⏳ **Time Elapsed:** {elapsed:.2f}s\n"
        f"⏱️ **Time Left:** {time_left:.2f}s\n"
        f"📦 **Total Input Size:** {size_total:.2f} MB"
    )

    if ms.text.strip() != new_content.strip():
        await ms.edit(new_content)


async def process_ffmpeg_progress(process, ms, start_time, total_size):
    """
    Parses FFmpeg progress logs and updates the progress bar every 3 seconds.
    """
    size_done = 0
    last_update_time = time.time()

    while True:
        line = await process.stdout.readline()
        if not line:
            break

        decoded_line = line.decode("utf-8").strip()
        time_match = re.search(r"out_time_ms=(\d+)", decoded_line)
        size_match = re.search(r"total_size=(\d+)", decoded_line)
        speed_match = re.search(r"speed=([\d\.]+)x", decoded_line)

        elapsed = 0
        progress = 0
        speed = 0
        estimated_size = total_size * 0.85  # Estimate output size as 85% of input size

        if time_match:
            elapsed = int(time_match.group(1)) / 1_000_000  # Convert to seconds
            progress = min((elapsed / (elapsed + 1)) * 100, 100)  # Example percentage logic

        if size_match:
            size_done = int(size_match.group(1)) / (1024 * 1024)  # Convert bytes to MB

        if speed_match:
            speed = float(speed_match.group(1)) * total_size  # Approximate speed in KB/s

        time_left = (estimated_size - size_done) / (speed / 1024) if speed > 0 else 0

        # Update the progress bar only if 3 seconds have passed
        current_time = time.time()
        if current_time - last_update_time >= 3:  # 3-second interval
            last_update_time = current_time
            await update_progress_bar(ms, progress, size_done, total_size, estimated_size, speed, elapsed, time_left)


async def quality_encode(bot, query, c_thumb):
    UID = query.from_user.id
    ms = await query.message.edit('Pʟᴇᴀsᴇ Wᴀɪᴛ...\n\n**Fᴇᴛᴄʜɪɴɢ Qᴜᴇᴜᴇ 👥**')
    
    if os.path.isdir(f'ffmpeg/{UID}') and os.path.isdir(f'encode/{UID}'):
        return await ms.edit("**⚠️ Yᴏᴜ ᴄᴀɴ ᴄᴏᴍᴘʀᴇss ᴏɴʟʏ ᴏɴᴇ ғɪʟᴇ ᴀᴛ ᴀ ᴛɪᴍᴇ\n\nAs ᴛʜɪs ʜᴇʟᴘs ʀᴇᴅᴜᴄᴇ sᴇʀᴠᴇʀ ʟᴏᴀᴅ.**")

    try:
        # Set up directories
        media = query.message.reply_to_message
        file = getattr(media, media.media.value)
        filename = str(file.file_name)
        Download_DIR = f"ffmpeg/{UID}"
        Output_DIR = f"encode/{UID}"
        File_Path = f"{Download_DIR}/{filename}"
        
        if not os.path.isdir(Download_DIR):
            os.makedirs(Download_DIR)
        if not os.path.isdir(Output_DIR):
            os.makedirs(Output_DIR)

        # Download the file
        await ms.edit('⚠️__**Please wait...**__\n**Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ....**')
        dl = await bot.download_media(
            message=file,
            file_name=File_Path,
            progress=progress_for_pyrogram,
            progress_args=("\n⚠️__**Please wait...**__\n\n☃️ **Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
        )

        resolutions = {
            "480p": "-vf scale=144:144 -crf 30",
            "720p": "-vf scale=240:240 -crf 30",
            "1080p": "-vf scale=360:360 -crf 30"
        }

        for res, ffmpegcode in resolutions.items():
            output_path = f"{Output_DIR}/{res}_{filename}"

            # Encoding
            await ms.edit(f"**🗜 Compressing to {res}...**")
            cmd = f"""ffmpeg -i "{dl}" {ffmpegcode} "{output_path}" -y"""

            process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            total_duration = None
            progress_message = None

            while True:
                line = await process.stderr.readline()
                if not line:
                    break

                line = line.decode("utf-8").strip()
                
                # Extract duration from ffmpeg's output
                if total_duration is None:
                    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", line)
                    if match:
                        hours, minutes, seconds = map(float, match.groups())
                        total_duration = hours * 3600 + minutes * 60 + seconds

                # Extract progress
                match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
                if match and total_duration:
                    hours, minutes, seconds = map(float, match.groups())
                    elapsed_time = hours * 3600 + minutes * 60 + seconds
                    progress = (elapsed_time / total_duration) * 100

                    # Update progress message
                    progress_message = f"Encoding {res}: {progress:.2f}%"
                    await ms.edit(progress_message)

            await process.wait()

            if process.returncode != 0:
                await ms.edit(f"Error during {res} compression.")
                return

            # Uploading
            if (file.thumbs or c_thumb):
                if c_thumb:
                    ph_path = await bot.download_media(c_thumb)
                else:
                    ph_path = await bot.download_media(file.thumbs[0].file_id)

            await ms.edit(f"⚠️__**Please wait...**__\n**Uploading {res} file...**")
            org = int(Path(File_Path).stat().st_size)
            com = int(Path(output_path).stat().st_size)
            pe = 100 - ((com / org) * 100)
            per = f"{pe:.2f}%"
            eees = dt.now()
            x = dtime
            xx = ts(int((ees - es).seconds) * 1000)
            xxx = ts(int((eees - ees).seconds) * 1000)

            await bot.send_document(
                    UID,
                    document=output_path,
                    thumb=ph_path,
                    caption="output file",
                    progress=progress_for_pyrogram,
                    progress_args=("⚠️__**Please wait...**__\n🌨️ **Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
        

        # Final Cleanup
        await ms.edit("All files uploaded successfully. Cleaning up...")
        shutil.rmtree(f"ffmpeg/{UID}")
        shutil.rmtree(f"encode/{UID}")

    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        if os.path.isdir(f"ffmpeg/{UID}"):
            shutil.rmtree(f"ffmpeg/{UID}")
        if os.path.isdir(f"encode/{UID}"):
            shutil.rmtree(f"encode/{UID}")            
            
            

async def CompressVideo(bot, query, ffmpegcode, c_thumb):
    UID = query.from_user.id
    ms = await query.message.edit('Pʟᴇᴀsᴇ Wᴀɪᴛ...\n\n**Fᴇᴛᴄʜɪɴɢ Qᴜᴇᴜᴇ 👥**')
    

    if os.path.isdir(f'ffmpeg/{UID}') and os.path.isdir(f'encode/{UID}'):
        return await ms.edit("**⚠️ Yᴏᴜ ᴄᴀɴ ᴄᴏᴍᴘʀᴇss ᴏɴʟʏ ᴏɴᴇ ғɪʟᴇ ᴀᴛ ᴀ ᴛɪᴍᴇ\n\nAs ᴛʜɪs ʜᴇʟᴘs ʀᴇᴅᴜᴄᴇ sᴇʀᴠᴇʀ ʟᴏᴀᴅ.**")

    try:
        media = query.message.reply_to_message
        file = getattr(media , media.media.value)
        filename = Filename(filename=str(file.file_name), mime_type=str(file.mime_type))
        Download_DIR = f"ffmpeg/{UID}"
        Output_DIR = f"encode/{UID}"
        File_Path = f"ffmpeg/{UID}/{filename}"
        Output_Path = f"encode/{UID}/{filename}"
        
        
        await ms.edit('⚠️__**Please wait...**__\n**Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ....**')
        s = dt.now()
        try:
            if not os.path.isdir(Download_DIR) and not os.path.isdir(Output_DIR):
                os.makedirs(Download_DIR)
                os.makedirs(Output_DIR)

                dl = await bot.download_media(
                    message=file,
                    file_name=File_Path,
                    progress=progress_for_pyrogram,
                    progress_args=("\n⚠️__**Please wait...**__\n\n☃️ **Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
                )
        except Exception as e:
            return await ms.edit(str(e))
        
        es = dt.now()
        dtime = ts(int((es - s).seconds) * 1000)

        await ms.edit(
            "**🗜 Compressing...**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Sᴛᴀᴛs', callback_data=f'stats-{UID}')],
                [InlineKeyboardButton(text='Cᴀɴᴄᴇʟ', callback_data=f'skip-{UID}')]
            ])
        )
        
        cmd = f"""ffmpeg -i "{dl}" {ffmpegcode} "{Output_Path}" -y"""

        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        

        stdout, stderr = await process.communicate()
        er = stderr.decode()

        try:
            if er:
                await ms.edit(str(er) + "\n\n**Error**")
                shutil.rmtree(f"ffmpeg/{UID}")
                shutil.rmtree(f"encode/{UID}")
                return
        except BaseException:
            pass
        

        # Clean up resources
        # Now Uploading to the User
        ees = dt.now()
        
        if (file.thumbs or c_thumb):
            if c_thumb:
                ph_path = await bot.download_media(c_thumb)
            else:
                ph_path = await bot.download_media(file.thumbs[0].file_id)

        org = int(Path(File_Path).stat().st_size)
        com = int((Path(Output_Path).stat().st_size))
        pe = 100 - ((com / org) * 100)
        per = str(f"{pe:.2f}")  + "%"
        eees = dt.now()
        x = dtime
        xx = ts(int((ees - es).seconds) * 1000)
        xxx = ts(int((eees - ees).seconds) * 1000)
        await ms.edit("⚠️__**Please wait...**__\n**Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....**")
        await bot.send_document(
                UID,
                document=Output_Path,
                thumb=ph_path,
                caption=Config.caption.format(filename, humanbytes(org), humanbytes(com) , per, x, xx, xxx),
                progress=progress_for_pyrogram,
                progress_args=("⚠️__**Please wait...**__\n🌨️ **Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
        
        if query.message.chat.type == enums.ChatType.SUPERGROUP:
            botusername = await bot.get_me()
            await ms.edit(f"Hey {query.from_user.mention},\n\nI Have Send Compressed File To Your Pm", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Bᴏᴛ Pᴍ", url=f'https://t.me/{botusername.username}')]]))
            
        else:
            await ms.delete()

        try:
            shutil.rmtree(f"ffmpeg/{UID}")
            shutil.rmtree(f"encode/{UID}")
            os.remove(ph_path)
        except BaseException:
            os.remove(f"ffmpeg/{UID}")
            os.remove(f"ffmpeg/{UID}")

        
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
