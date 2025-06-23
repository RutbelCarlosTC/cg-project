import re
import yt_dlp
import os
from shutil import copyfile
import pandas as pd
from tqdm import tqdm

FOLDER = os.path.join("data", "videos")


def download_video(name, video_id, start_time, duration_time):
    """
    start and end have to be in the format mm:ss
    """
    file_path = os.path.join(FOLDER, name)
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'mp4[height<=720]/best[ext=mp4]',  # Prefer mp4 format, max 720p
        'outtmpl': os.path.join(FOLDER, '%(title)s.%(ext)s'),
        'quiet': True,  # Suppress yt-dlp output
        'no_warnings': True,
    }
    
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(video_url, download=False)
            
            # Check if info extraction was successful
            if not info or not isinstance(info, dict):
                print(f"Could not extract info for video {video_id}")
                return
            
            # Get video title safely
            video_title = info.get('title', f'video_{video_id}')
            if not video_title:
                video_title = f'video_{video_id}'
            
            # Clean the filename
            file_name = re.sub(r'[.;:,?!/\\<>:"|*]', "", str(video_title)) + ".mp4"
            full_video_path = os.path.join(FOLDER, file_name)
            
            # Download if not exists
            if not os.path.exists(full_video_path):
                try:
                    # Create a new ydl instance for downloading
                    download_opts = ydl_opts.copy()
                    download_opts['outtmpl'] = full_video_path.replace('.mp4', '.%(ext)s')
                    
                    with yt_dlp.YoutubeDL(download_opts) as download_ydl:
                        download_ydl.download([video_url])
                        
                    # Check if file was created with different extension
                    if not os.path.exists(full_video_path):
                        # Look for the downloaded file with any video extension
                        base_name = full_video_path.replace('.mp4', '')
                        for ext in ['.webm', '.mkv', '.mp4', '.avi']:
                            if os.path.exists(base_name + ext):
                                # Rename to .mp4 for consistency
                                os.rename(base_name + ext, full_video_path)
                                break
                except Exception as download_error:
                    print(f"Download failed for {video_id}: {download_error}")
                    return
            
            output_file = os.path.join(file_path, name + "-" + video_id + ".mp4")
            if os.path.exists(output_file):
                return

            # Handle video clipping
            if pd.isna(start_time) and pd.isna(duration_time):
                # Copy entire video if no time constraints
                if os.path.exists(full_video_path):
                    copyfile(src=full_video_path, dst=output_file)
            else:
                # Use ffmpeg to create clip
                if os.path.exists(full_video_path):
                    original_video = full_video_path
                    try:
                        if pd.notna(start_time) and pd.notna(duration_time):
                            # Both start and duration specified
                            os.system(
                                f'ffmpeg -hide_banner -loglevel error -ss {start_time} -i "{original_video}" -to {duration_time} -c copy "{output_file}"'
                            )
                        elif pd.notna(start_time):
                            # Only start time specified
                            os.system(
                                f'ffmpeg -hide_banner -loglevel error -ss {start_time} -i "{original_video}" -c copy "{output_file}"'
                            )
                        else:
                            # Only duration specified (from beginning)
                            os.system(
                                f'ffmpeg -hide_banner -loglevel error -i "{original_video}" -to {duration_time} -c copy "{output_file}"'
                            )
                    except Exception as ffmpeg_error:
                        print(f"FFmpeg error when processing {video_title}: {ffmpeg_error}")
                else:
                    print(f"Video file not found: {full_video_path}")
    
    except Exception as e:
        print(f"Error downloading video {video_id}: {e}")
        # Print more detailed error info for debugging
        import traceback
        print(f"Detailed error: {traceback.format_exc()}")


print("\nDownloading videos of signs from YouTube\n")

# Create data/videos folder if it doesn't exist
os.makedirs(FOLDER, exist_ok=True)

# Create the dataset based on yt_links.csv
df_links = pd.read_csv("yt_links.csv")
for idx, row in tqdm(df_links.iterrows(), total=df_links.shape[0]):
    download_video(*row)

# Delete the videos used to create the clips for the dataset
for file in os.listdir(FOLDER):
    if file.endswith(".mp4") and not os.path.isdir(os.path.join(FOLDER, file)):
        try:
            os.remove(os.path.join(FOLDER, file))
        except Exception as e:
            print(f"Could not delete {file}: {e}")