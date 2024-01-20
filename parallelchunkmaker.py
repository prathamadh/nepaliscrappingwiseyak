from concurrent.futures import ThreadPoolExecutor

def process_file(filename):
    path_parts = filename.split('/')

# Get the segment identifier from the path
    segment= path_parts[-2]
    print(f"Processing File : {segment}")
    sound_file = AudioSegment.from_wav(filename)
    audio_chunks = split_on_silence(sound_file,
                                    min_silence_len=500,
                                    silence_thresh=-50)



    os.makedirs(f"/content/audiochunks/{segment}", exist_ok=True)
    target_length = 10 * 1000
    output_chunks = [audio_chunks[0]]

    for chunk in audio_chunks[1:]:
        if len(output_chunks[-1]) < target_length:
            output_chunks[-1] += chunk
            print("combined",segment)
        else:
            output_chunks.append(chunk)



    for i, chunk in enumerate(output_chunks):
        out_file = "/content/audiochunks/{0}/{0}_{1}.wav".format(segment, i)
        print(out_file)

        samples = np.array(chunk.get_array_of_samples())
        samples = samples.reshape(1, -1)
        torsamples = torch.from_numpy(samples).float()
        data = {"waveform": torsamples, "sample_rate": 16000}
        osd = pipeline(data)

        if len(osd) > 1:
            print("not saved")
            print(out_file)
            print(osd)
            continue

        chunk.export(out_file, format="wav")




vocallinks = glob("/content/vocalsplitted/*/vocals.wav")
print(vocallinks)
# Specify the number of threads you want to run concurrently
num_threads =7

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    result=executor.map(process_file, vocallinks)