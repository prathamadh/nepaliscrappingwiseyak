from pytube import YouTube
from pydub import AudioSegment
import pandas as pd
import os
#code for making csv



# Create a DataFrame with the desired columns and data
data = {'filelink': ['https://www.youtube.com/watch?v=WatXucJcTgY',
                     'https://www.youtube.com/watch?v=PI_HD5_gz6E'
                    #  'https://www.youtube.com/watch?v=j-I2ipptuZA',
                    #  'https://www.youtube.com/watch?v=HiRrXN9u40Y',
                    #  'https://www.youtube.com/watch?v=XJshM7iB-5Y'
                     ],
        'dnldstatus': [0,0],
        'filename' :["n","n"]
        }

download_df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
download_df.to_csv('download_status.csv', index=False)

def convert_audio(audio_file):
    """
    Corrects the channels, sample rate, and sample width of the audios.
    Replaces the original audio file with the one generated.
    """
    print(audio_file)
    sound = AudioSegment.from_file(audio_file)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)
    sound = sound.set_sample_width(2)
    temfilename=audio_file[:-3]+"wav"
    sound.export(temfilename, format ="wav")
    os.remove(audio_file)
    return temfilename

def download_audio(youtube_url, output_path='./'):
    try:
        # Create a YouTube object
        yt = YouTube(youtube_url)

        # Get the highest resolution stream (for videos) or audio stream (for audio-only)
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio stream
        name=audio_stream.download(output_path)

        print("Audio download completed.",name)

    except Exception as e:
        print(f"Error: {str(e)}")

    return name

from datetime import datetime

def split_wav(input_file, output_prefix, segment_length=5 * 60 * 1000):
    # Load the input audio file
    audio = AudioSegment.from_file(input_file, format="wav")

    # Calculate the number of segments
    num_segments = len(audio) // segment_length + 1
    os.makedirs(output_prefix,exist_ok=True)
    for i in range(num_segments):
        # Calculate start and end time for each segment
        start_time = i * segment_length
        end_time = (i + 1) * segment_length
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        # Extract the segment
        segment = audio[start_time:end_time]

        # Create output file name
        output_file = f"{output_prefix}/segment_{i + 1}_t_{timestamp}.wav"

        # Export the segment to a new WAV file
        segment.export(output_file, format="wav")

if __name__ == "__main__":
    
    #making df
    data = {'filelink': ['https://www.youtube.com/watch?v=WatXucJcTgY',
                     'https://www.youtube.com/watch?v=PI_HD5_gz6E'
                    #  'https://www.youtube.com/watch?v=j-I2ipptuZA',
                    #  'https://www.youtube.com/watch?v=HiRrXN9u40Y',
                    #  'https://www.youtube.com/watch?v=XJshM7iB-5Y'
                     ],
        'dnldstatus': [0,0],
        'filename' :["n","n"]
        }

    download_df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    download_df.to_csv('./download_status.csv', index=False)

    download_df=pd.read_csv("./download_status.csv")
    for idx,row in download_df.iterrows():
        filename=download_audio(row['filelink'], output_path='ytdownloaded')
        download_df.loc[idx, 'dnldstatus'] = 1
        download_df.loc[idx, 'filename']=filename
        print("____________________________",filename)
        filename=convert_audio(filename)
        split_wav(filename, './segments')
        download_df.to_csv("./download_status.csv", index=False)