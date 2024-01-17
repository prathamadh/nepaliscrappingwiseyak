import pandas as pd
from glob import glob
import gc
import os


def spliiter():
    vocal_df=pd.read_csv('vocalsplit_status.csv')
    for idx,row in vocal_df.iterrows():
        if row["vocalsepstatus"] ==2 :
            print("already")
            continue
        elif row["vocalsepstatus"] == 1:
            # delete all the vocals for broken pieces
            continue
        #code to change the audio into processable segment
        link=row['filelocation']
        vocal_df.loc[idx,'vocalsepstatus'] = 1
        vocal_df.to_csv("vocalsplit_status.csv",index=False)
        command1=f'python -m spleeter separate -p spleeter:2stems -o "splitvocal" -i "{link}"'
        os.system(command1)
        vocal_df.loc[idx,'vocalsepstatus'] = 2

        vocal_df.to_csv("vocalsplit_status.csv",index=False)
        gc.collect()


if __name__ == "__main__":
    links=glob("segments\*.wav")
    
    data = {'filelocation': links}
    data_df = pd.DataFrame(data)
    data_df['vocalsepstatus']=0
    # segment_df=pd.concat([segment_df,data_df],ignore_index=True)
    data_df.to_csv("./vocalsplit_status.csv",index=False)
#----------------------------above is code for making csv run only once ----------
    spliiter()