from glob import glob
import pandas as pd
from pydub import AudioSegment
import numpy as np
from pydub.silence import split_on_silence
import os
from pyannote.audio import Model
from pyannote.audio.pipelines import OverlappedSpeechDetection





def make_chunks():
    chunk_df=pd.read_csv("filechunk_status.csv")
    for idx,row in chunk_df.iterrows():
            if row["chunkstatus"] ==2 :
                print("already")
                continue
            elif row["chunkstatus"] == 1:
                # delete all the vocals for broken pieces
                continue
                    # give link to all the vocals.wav file

            link_num=idx
            # Step 4: Split into smaller parts
            filename=row['vocalfilelink']
            sound_file = AudioSegment.from_wav(filename)
            audio_chunks = split_on_silence(sound_file,
                # must be silent for at least half a second
                min_silence_len=500,

                # consider it silent if quieter than -16 dBFS
                silence_thresh=-50
            )
            print ("exporting files for link number: ",link_num)

            os.makedirs(f"audiochunks/{link_num}",exist_ok=True)
            #combining chunks if small and making it splited if big
            target_length = 10 * 1000
            output_chunks = [audio_chunks[0]]
            for chunk in audio_chunks[1:]:
                if len(output_chunks[-1]) < target_length:
                    output_chunks[-1] += chunk
                    print("combined")
                else:
                    # if the last output chunk is longer than the target length,
                    # we can start a new one

                    output_chunks.append(chunk)
            chunk_df.loc[idx,'chunkstatus'] = 1
            chunk_df.to_csv("filechunk_status.csv", index=False)
            # making folder named after link number we are processing
            for i, chunk in enumerate(output_chunks):
                out_file = "/content/audiochunks/{0}/{0}_{1}.wav".format(link_num, i)
                #code to check if it has overlapping sound
                samples = np.array(chunk.get_array_of_samples())
                samples=samples.reshape(1,-1)
                torsamples=torch.from_numpy(samples).float()
                data={"waveform": torsamples, "sample_rate": 16000}
                osd = pipeline(data)
                if len(osd)>1:
                    print("not saved")
                    print(out_file)
                    print(osd)
                    continue


                chunk.export(out_file, format="wav")
            chunk_df.loc[idx,'chunkstatus']=2
            chunk_df.to_csv("filechunk_status.csv", index=False)

if __name__ == "__main__":
    #_______________do once_________________________
    print('hello')
    vocallinks=glob("splitvocal/*/vocals.wav")
    # chunk_df=pd.read_csv("/content/filechunk_status.csv")
    data = {'vocalfilelink': vocallinks}
    chunk_df = pd.DataFrame(data)
    chunk_df['chunkstatus']=0
    chunk_df.to_csv("filechunk_status.csv", index=False)
    
#_____________________________do once ________________
    
    model = Model.from_pretrained("pyannote/segmentation",use_auth_token='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' )
    HYPER_PARAMETERS = {
    # onset/offset activation thresholds
    "onset": 0.4, "offset": 0.4,
    # remove speech regions shorter than that many seconds.
    "min_duration_on": 0.7,
    # fill non-speech regions shorter than that many seconds.
    "min_duration_off": 0.0
    }
   
    pipeline = OverlappedSpeechDetection(segmentation=model)
    pipeline.instantiate(HYPER_PARAMETERS)
    make_chunks()

