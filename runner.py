import drop_ai as dai
import os
import random
import glob
from pydub import AudioSegment
from datetime import datetime
from pathlib import Path, PureWindowsPath

now = datetime.now().strftime("%H-%M-%S")

now = str(now)

bpm = input("Please input the BPM you would like (default is 150): ")
key = input("Please input the key you would like (default is D): ")
length = input("Please input the length you would like in bars (default is 8): ")
times = input("Please input how many times you would like this program to run (default is 1): ")

if bpm == "":
    bpm = 150

if key == "":
    key = "D"

if length == "":
    length = 8

if times == "":
    times = 1

bpm = int(bpm)

length = int(length)

times = int(times)

kicks = dai.folder_search("Samples/kicks", "")
snares = dai.folder_search("Samples/snares", "")
basses = dai.folder_search("Samples/basses", key)
hats = dai.folder_search("Samples/hats", "")



for j in range(times):

    i = j + 1

    random.shuffle(basses)

    kick_stem = dai.kick_loop(random.choice(kicks), bpm, length)
    snare_stem = dai.snare_loop(random.choice(snares), bpm, length)

    sidechain = kick_stem[1].union(snare_stem[1])

    bass_stem = dai.bass_loop(sidechain, list(basses), bpm, length)
    hat_stem = dai.hat_loop(sidechain, random.choice(hats), bpm, length)

    kick_stem[0].export(PureWindowsPath(f"Test/{i} - {now}-kick_stem.wav"), "wav")
    print(f"Exported 'kick_stem-{i} {now}.wav' successfully!")

    snare_stem[0].export(PureWindowsPath(f"Test/{i} - {now}-snare_stem.wav"), "wav")
    print(f"Exported 'snare_stem-{i} {now}.wav' successfully!")

    bass_stem.export(PureWindowsPath(f"Test/{i} - {now}-bass_stem.wav"), "wav")
    print(f"Exported 'bass_stem-{i} {now}.wav' successfully!")

    hat_stem.export(PureWindowsPath(f"Test/{i} - {now}-hat_stem.wav"), "wav")
    print(f"Exported 'hat_stem-{i} {now}.wav' successfully!")
