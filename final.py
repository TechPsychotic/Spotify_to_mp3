import pandas as pd
from py_youtube import Search
from pytube import YouTube


def download_youtube_video(video_id, save_path='.', video_title=''):
    try:
        # Construct the complete YouTube video URL
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        
        # Create a YouTube object
        yt = YouTube(video_url)
        
        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio to the specified path
        audio_stream.download(output_path=save_path)
        

    except Exception as e:
        print(f"An error occurred: {e}")
# Perform a search for the video
def video(name):
    try:
        videos = Search(name, limit=1).videos()
        video_id = videos[0]['id']
        video_title = videos[0]['title']
        return video_id, video_title
    except Exception as e:
        videos = Search(name, limit=3).videos()
        video_id = videos[0]['id']
        video_title = videos[0]['title']
        return video_id, video_title



def format_song_data(csv_file_path):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Create a new column combining artist and songname
        df['formatted'] = df.apply(lambda row: f'{row["Track Name"]} - {row["Artist Name(s)"]}', axis=1)
        
        # Convert the 'formatted' column to a list of strings
        formatted_list = df['formatted'].tolist()

        return formatted_list
    except Exception as e:
        return f"An error occurred: {e}"

# Example: Provide the path to your CSV file
csv_file_path = 'metadata.csv'
result = format_song_data(csv_file_path)

if result and isinstance(result, list):
    for name in result:
        print(video(name))
        id = video(name)[0]
        title = video(name)[1] 
        print("downloading: ", title)
        download_youtube_video(id, save_path='./downloads', video_title=title)
        print("downloaded: ", title)
else:
    print(result)
