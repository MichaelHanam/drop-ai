import glob
import random
from pydub import AudioSegment
from pydub import effects
from pydub.playback import play



def folder_search(item, key):

    """
    Returns a list containing all audio in a given key in a given folder.
    """
    if key == "":

        items = glob.glob(f"{item.lower()}\*.wav")

        print(f"Found {len(items)} {item} without a key.")
        return items

    items = glob.glob(f"{item.lower()}\*{key.upper()}.wav")

    print(f"Found {len(items)} {item} with the key of {key.upper()}.")
    return items

def kick_loop(sample, bpm = 150, length = 8):

    """
    Creates an audio file containing a loop of kick samples played in a 
    given BPM.
    """
    sidechain = set()
    stem = AudioSegment.empty()

    sample = AudioSegment.from_wav(sample)
    beat = 60/bpm*1000/2
    length = length*2

    snare_hits = range(2, length, 4)

    for bar in range(length):
        if bar not in snare_hits:
            if random.random() > 0.5:
                stem += sample[:beat].fade_out(5)
                stem += AudioSegment.silent()[:beat]
                sidechain.add(bar)
                continue
                
        stem += AudioSegment.silent()[:beat]
        stem += AudioSegment.silent()[:beat]

    return (stem, sidechain)

def snare_loop(sample, bpm = 150, length = 8):

    """
    Creates an audio file containing a loop of snare samples played in a 
    given BPM.
    """
    sidechain = set()
    stem = AudioSegment.empty()

    sample = AudioSegment.from_wav(sample)
    beat = 60/bpm*1000/2
    length = length*2

    snare_hits = range(2, length, 4)

    for bar in range(length):
        if bar in snare_hits:
            stem += sample[:beat].fade_out(5)
            stem += AudioSegment.silent()[:beat]
            sidechain.add(bar)
            continue
  
        stem += AudioSegment.silent()[:beat]
        stem += AudioSegment.silent()[:beat]

    return (stem, sidechain)

def hat_loop(sidechain, sample, bpm = 150, length = 8):

    """
    Creates an audio file containing a loop of hat samples played in a 
    given BPM.
    """
    stem = AudioSegment.empty()

    sample = AudioSegment.from_wav(sample)
    beat = 60/bpm*1000/2
    length = length*2

    for bar in range(length):
        if bar in sidechain:
            stem += sample[:beat].fade_in(beat/3)
            stem += AudioSegment.silent()[:beat].fade_out(30)
            continue
        stem += sample[:beat]
        stem += AudioSegment.silent()[:beat].fade_out(30)
    return stem

def bass_loop(sidechain, samples, bpm = 150, length = 8):

    stem = AudioSegment.empty()

    bass_1 = AudioSegment.from_wav(samples.pop())
    bass_2 = AudioSegment.from_wav(samples.pop())
    bass_3 = AudioSegment.from_wav(samples.pop())

    sample = bass_1
    beat = 60/bpm*1000/2
    length = length*2

    calls = range(0, length, 4)

    delay_length = random.randrange(int(beat/1.6), int(beat/1.2))

    pattern_temp = []
    for i in range(4):
        if pattern_temp != []:
            if random.random() > 0.5:
                pattern_temp.append(not pattern_temp[-1])
            else:
                pattern_temp.append(random.choice([True, False]))
        else: 
            if random.random() > 0.25:
                pattern_temp.append(False)
            else:
                pattern_temp.append(True)

    pattern = []
    count = 0

    for bar in range(length):
        if bar in range(0, length, 4):
            for item in pattern_temp:
                count += 1
                if count in range(8, length+1, 8):
                    pattern.append(not item)
                else:
                    pattern.append(item)

    print(pattern)

    for bar in range(length):

        if pattern[bar]:
            delay = delay_length
        else:
            delay = 0

        if bar in calls: 
            sample = bass_1
        
        elif delay > 0:
            sample = bass_2

        if bar in sidechain and delay == 0:
            stem += sample[:beat].fade_in(beat/3).fade_out(50)
            stem += AudioSegment.silent()[:beat]
            continue

        elif delay > 0:
            if random.random() > 0.7:
                stem += AudioSegment.silent()[:delay/2]
                stem += sample[:(beat*2-delay)/5*2.5].fade_out(80)
                stem += sample[:(beat*2-delay)].fade_out(30)
                print((bar+1)*(beat*4)/2)
                stem = stem[:(bar+1)*(beat*4)/2]
            else:
                stem += AudioSegment.silent()[:delay]
                stem += sample[:beat*2-delay].fade_out(100)
            continue
        
        elif bar not in sidechain and delay == 0:
            stem += sample[:beat].fade_out(50)

        if random.random() > 0.25 and delay == 0 or bar == length-1:
            stem += AudioSegment.silent()[:delay*1.5]
            stem += bass_3[:beat-delay*1.5].fade_out(10)
        else: 
            stem += AudioSegment.silent()[:beat]

        
    return stem