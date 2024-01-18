
# nepaliscrappingwiseyak


## file system
# Project Directory Structure

# Project Directory Structure

- **mainfolder/:**
  - **audiochunks/:**
  
  - **segments/:**
  
  - **splitvocal/:**
  
  - **ytdownloaded/:**
  
  - **download_status.csv:**
  
  - **filechunk_status.csv:**
  
  - **vocalsplit_status.csv:**
  
  - **download.py:**
  
  - **vocalsplit.py:**
  
  - **chunkmaker.py:**
# make the first four folders using mkdir

put path of ffmpeg in your env variables
ffmpeg can be downloaded from here https://www.gyan.dev/ffmpeg/builds/

install python 3.6.0 
python -m virtualenv -p python3.6 venv
pip install spleeter


steps to run each code :

1)download.py
install pytube and pydub 
make a csv of data make folders and then run the code 

2)vocal_split.py
install spleeter 
make a csv from segments of downloaded audio 
then run code os it splits into vocals.wav and acc...wav in file splitvocal 

3)chunk maker.py
install pyannote 
install torch 
make a csv for the first time then run the code 


if code fails then just delete the csv generating code and rerun the code the code should work from where we left . thank you

