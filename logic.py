# 𝖥𝗂𝗅𝖾: 𝗅𝗈𝗀𝗂𝖼.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import os
import time
import asyncio
import subprocess
from datetime import datetime

class MegaLogic:
    def __init__(self, input_path, output_path=None):
        self.input_path = input_path
        self.output_path = output_path or f"{input_path}_processed.mp4"
        self.start_time = time.time()

    async def get_video_info(self):
        """ভিডিওর ডিটেইল মেটাডেটা অ্যানালাইসিস করার জন্য"""
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", "-show_streams", self.input_path
        ]
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        import json
        return json.loads(stdout)

    async def encode_video(self, quality, progress_callback=None):
        """
        জিৎ, এখানে তোমার সব কমান্ডের (144p to 2160p) 
        ইন্ডাস্ট্রিয়াল লেভেল এনকোডিং লজিক দেওয়া হয়েছে।
        """
        mapping = {
            "144p":  {"scale": "256:144",   "bitrate": "150k",  "crf": "28"},
            "360p":  {"scale": "640:360",   "bitrate": "400k",  "crf": "26"},
            "480p":  {"scale": "854:480",   "bitrate": "800k",  "crf": "24"},
            "720p":  {"scale": "1280:720",  "bitrate": "1800k", "crf": "22"},
            "1080p": {"scale": "1920:1080", "bitrate": "3500k", "crf": "20"},
            "2160p": {"scale": "3840:2160", "bitrate": "9000k", "crf": "18"}
        }

        q_set = mapping.get(quality, mapping["480p"])
        
        # 𝖠𝖽𝗏𝖺𝗇𝖼𝖾𝖽 𝖥𝖥𝗆𝗉𝖾𝗀 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖿𝗈𝗋 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖰𝗎𝖺𝗅𝗂𝗍𝗒
        cmd = [
            "ffmpeg", "-i", self.input_path,
            "-vf", f"scale={q_set['scale']}",
            "-c:v", "libx264", "-crf", q_set['crf'],
            "-b:v", q_set['bitrate'],
            "-preset", "fast", "-c:a", "aac", "-b:a", "128k",
            "-y", self.output_path
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        
        # 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌 𝖲𝗒𝗇𝖼 (এটি তোমার UI-এর সাথে কানেক্ট হবে)
        await process.wait()
        return self.output_path if process.returncode == 0 else None

    async def cut_video(self, start_time, duration):
        """/cut কমান্ডের জন্য প্রিসাইজ ট্রিমিং লজিক"""
        cmd = [
            "ffmpeg", "-ss", start_time, "-i", self.input_path,
            "-t", duration, "-c", "copy", "-y", self.output_path
        ]
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()
        return self.output_path

    async def merge_videos(self, video_list):
        """/merge কমান্ডের জন্য লজিক"""
        with open("concat.txt", "w") as f:
            for v in video_list:
                f.write(f"file '{v}'\n")
        
        cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-c", "copy", "-y", self.output_path]
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()
        os.remove("concat.txt")
        return self.output_path

    async def change_metadata(self, title, author):
        """/metadata কমান্ডের জন্য মেটাডেটা ইঞ্জেকশন"""
        cmd = [
            "ffmpeg", "-i", self.input_path,
            "-metadata", f"title={title}",
            "-metadata", f"artist={author}",
            "-c", "copy", "-y", self.output_path
        ]
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()
        return self.output_path

    async def extract_audio(self):
        """/extract_audio কমান্ডের লজিক"""
        audio_path = self.input_path.rsplit(".", 1)[0] + ".mp3"
        cmd = ["ffmpeg", "-i", self.input_path, "-vn", "-acodec", "libmp3lame", "-y", audio_path]
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()
        return audio_path

