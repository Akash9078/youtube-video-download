import os
import yt_dlp
import logging
from moviepy.editor import VideoFileClip, AudioFileClip

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directory to save downloaded videos
output_dir = "downloads"
os.makedirs(output_dir, exist_ok=True)

def download_youtube_content(video_url):
    try:
        logging.info(f"Downloading video: {video_url}")
        
        # First, get video info to get the title
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title', 'downloaded_video')
            # Sanitize the filename
            video_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
        # Download best quality video only
        video_opts = {
            'format': 'bestvideo/best',
            'outtmpl': os.path.join(output_dir, 'video.mp4'),
            'merge_output_format': 'mp4'
        }
        
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.download([video_url])
            
        logging.info("Video download completed")
        
        # Download audio only
        audio_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, 'audio.mp3'),
            'postprocessor_args': ['-acodec', 'mp3'],
            'keepvideo': False,
            'merge_output_format': 'mp3'
        }
        
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([video_url])
            
        logging.info("Audio download completed")

        # Set paths for files
        video_path = os.path.join(output_dir, 'video.mp4')
        audio_path = os.path.join(output_dir, 'audio.mp3')
        final_output_file = os.path.join(output_dir, f"{video_title}.mp4")

        # Merge video and audio using moviepy
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(final_output_file, codec='libx264', audio_codec='aac')
        
        # Close clips
        video_clip.close()
        audio_clip.close()
        final_clip.close()

        logging.info(f"Successfully merged video and audio into: {final_output_file}")

        # Delete temporary files
        os.remove(video_path)
        os.remove(audio_path)
        logging.info("Deleted temporary video and audio files")

        return final_output_file

    except Exception as e:
        logging.error(f"Error processing {video_url}: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    video_url = input("Enter the YouTube video URL: ")
    download_youtube_content(video_url)