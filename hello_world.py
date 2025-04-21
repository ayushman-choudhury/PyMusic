from resources import *

total_length = 290 * SAMPLE_RATE
songFile = np.zeros(total_length)
songFile_L = np.zeros(total_length)
songFile_R = np.zeros(total_length)





# region 1: intro

loc = SAMPLE_RATE
note = sineWave(440, 5)
songFile[loc : loc + len(note)] += note

loc += len(note)
note = 0.3 * squareWave(440 / 1.5, 3)
songFile[loc : loc + len(note)] += note

loc += len(note)
note = 0.3 * sawtoothWave(440 / (1.5 ** 2), 11)
adsr = generate_adsr_envelope(len(note), 'val', 0, 0, 1, 5 * SAMPLE_RATE)
songFile[loc : loc + len(note)] += note * adsr

loc += SAMPLE_RATE
note = 0.3 * squareWave(440 / 1.5, 10)
adsr = generate_adsr_envelope(len(note), 'val', 0, 0, 1, 5 * SAMPLE_RATE)
songFile[loc : loc + len(note)] += note * adsr

loc += SAMPLE_RATE
note = sineWave(440, 9)
adsr = generate_adsr_envelope(len(note), 'val', 0, 0, 1, 5 * SAMPLE_RATE)
songFile[loc : loc + len(note)] += note * adsr

loc += SAMPLE_RATE
note = triangleWave(440 * 1.5, 8)
adsr = generate_adsr_envelope(len(note), 'val', 0, 0, 1, 5 * SAMPLE_RATE)
songFile[loc : loc + len(note)] += note * adsr



# At 15 seconds, fade in larger chord
loc = 15 * SAMPLE_RATE

# Square - uppers
chord_notes = [
    440 * 1.5,
    440, 
    440 / 1.5
]
chord = writeChord('sine', chord_notes, [1, 1, 1, 1.5, 2], 6)
adsr = generate_adsr_envelope(len(chord), 'val',
                              2 * SAMPLE_RATE, 0.1 * SAMPLE_RATE, 0.9, 2 * SAMPLE_RATE)
songFile[loc:(loc + len(chord))] += adsr * chord

# Sine - lowers
chord_notes = [
    440, 
    440 / 1.5,
    440 / (1.5 ** 2),
    440 / (1.5 ** 3),
    440 / (1.5 ** 4)
]
chord = writeChord('sine', chord_notes, [1, 1, 1, 1.5, 2], 10)
adsr = generate_adsr_envelope(len(chord), 'val',
                              5 * SAMPLE_RATE, 0.1 * SAMPLE_RATE, 0.9, 0)
songFile[loc:(loc + len(chord))] += adsr * chord

loc += len(chord)








# region 2: church
print('Church starts at', loc / SAMPLE_RATE)

# Chord progression

def organChord(chordNotes, chordLength):
    chordSine = 0.5 * writeChord('sine', chordNotes, [1] * len(chordNotes), chordLength)
    chordSawtooth = 0.3 * writeChord('sine', chordNotes, [1] * len(chordNotes), chordLength)
    chordTriangle = 0.2 * writeChord('sine', [i * 2 for i in chordNotes], [1] * len(chordNotes), chordLength)
    chordSquare = 0.1 * writeChord('sine', [i * 4 for i in chordNotes], [1] * len(chordNotes), chordLength)
    chord = chordSine + chordSawtooth + chordTriangle + chordSquare
    return 0.5 * chord

chord_notes = [
    notename_to_hertz('F-2'),
    notename_to_hertz('C-3'),
    notename_to_hertz('F-3'),
    notename_to_hertz('C-4'),
    notename_to_hertz('F-4'),
    notename_to_hertz('A-4'),
]
chord = organChord(chord_notes, 4)
songFile[loc : loc + len(chord)] += chord
loc += len(chord)

chord_notes = [
    notename_to_hertz('F-2'),
    notename_to_hertz('C#-3'),
    notename_to_hertz('F-3'),
    notename_to_hertz('C#-4'),
    notename_to_hertz('F-4'),
    notename_to_hertz('A-4'),
]
chord = organChord(chord_notes, 4)
songFile[loc : loc + len(chord)] += chord
loc += len(chord)

chord_notes = [
    notename_to_hertz('G-2'),
    notename_to_hertz('D-3'),
    notename_to_hertz('F-3'),
    notename_to_hertz('B-3'),
    notename_to_hertz('D-4'),
    notename_to_hertz('A-4'),
]
chord = organChord(chord_notes, 4)
songFile[loc : loc + len(chord)] += chord
loc += len(chord)

chord_notes = [
    notename_to_hertz('C-3'),
    notename_to_hertz('G-3'),
    notename_to_hertz('Bb-3'),
    notename_to_hertz('E-4'),
    notename_to_hertz('G-4')
]
chord = organChord(chord_notes, 4)
songFile[loc : loc + len(chord)] += chord

passing = 0.5 * writeMelody('sine', [notename_to_hertz('C-3'), notename_to_hertz('Bb-2'), notename_to_hertz('A-2')], [1, 1, 4])
passing_2 = 0.25 * writeMelody('square', [notename_to_hertz('C-3'), notename_to_hertz('Bb-2'), notename_to_hertz('A-2')], [1, 1, 4])
adsr = generate_adsr_envelope(len(passing), 'frac', 0.01, 0.01, 1, 0.6)
songFile[loc + 2 * SAMPLE_RATE: loc + 2 * SAMPLE_RATE + len(passing)] += adsr * (passing + passing_2)


loc += len(chord)


chord_notes = [
    notename_to_hertz('A-2'),
    notename_to_hertz('F-3'),
    notename_to_hertz('C-4'),
    notename_to_hertz('F-4'),
    notename_to_hertz('A-4')
]
chord = organChord(chord_notes, 4)
songFile[loc : loc + len(chord)] += chord
loc += len(chord)


chord_notes = [
    notename_to_hertz('C-3'),
    notename_to_hertz('A-3'),
    notename_to_hertz('C-4'),
    notename_to_hertz('F-4')
]
chord = organChord(chord_notes, 2)
songFile[loc : loc + len(chord)] += chord
loc += len(chord)


chord_notes = [
    notename_to_hertz('C-3'),
    notename_to_hertz('G-3'),
    notename_to_hertz('Bb-3'),
    notename_to_hertz('E-4')
]
chord = organChord(chord_notes, 2)
songFile[loc : loc + len(chord)] += chord
loc += len(chord)


chord_notes = [
    notename_to_hertz('F-2'),
    notename_to_hertz('C-3'),
    notename_to_hertz('F-3'),
    notename_to_hertz('A-3'),
    notename_to_hertz('C-4'),
    notename_to_hertz('F-4'),
]
chord = organChord(chord_notes, 8)
songFile[loc : loc + len(chord)] += chord

passing = 0.5 * writeMelody('sine', [notename_to_hertz('Bb-3'), 
                                     notename_to_hertz('A-3'), 
                                     notename_to_hertz('G-3'),
                                     notename_to_hertz('A-3')], [2, 1, 1, 4])
passing_2 = 0.25 * writeMelody('square', [notename_to_hertz('Bb-3'), 
                                     notename_to_hertz('A-3'), 
                                     notename_to_hertz('G-3'),
                                     notename_to_hertz('A-3')], [2, 1, 1, 4])
adsr = generate_adsr_envelope(len(passing), 'frac', 0.01, 0.01, 1, 0.5)
songFile[loc : loc + len(passing)] += adsr * (passing + passing_2)

loc += len(chord)


chord_notes = [
    notename_to_hertz('G-2'),
    notename_to_hertz('F-3'),
    notename_to_hertz('B-3'),
    notename_to_hertz('D-4'),
    notename_to_hertz('F-4'),
]
chord = organChord(chord_notes, 3)
songFile[loc : loc + len(chord)] += chord
loc += len(chord)


chord_notes = [
    notename_to_hertz('G-2'),
    notename_to_hertz('F-3'),
    notename_to_hertz('B-3'),
    notename_to_hertz('C#-4'),
    notename_to_hertz('F-4'),
]
chord = organChord(chord_notes, 3)
songFile[loc : loc + len(chord)] += chord
loc += len(chord)


chord_notes = [
    notename_to_hertz('F#-2'),
    notename_to_hertz('F#-2') * 2,
    notename_to_hertz('F#-2') * 4,
]
chord = organChord(chord_notes, 8)
songFile[loc : loc + len(chord)] += chord

chord_notes = [
    notename_to_hertz('B-3'),
    notename_to_hertz('D-4')
]
chord = organChord(chord_notes, 4)
songFile[loc : loc + len(chord)] += chord
loc += len(chord)

chord_notes = [
    notename_to_hertz('A#-3'),
    notename_to_hertz('C#-4')
]
chord = organChord(chord_notes, 4)
songFile[loc : loc + len(chord)] += chord
loc += len(chord)

print('- final volume before pop', np.max(chord))

breakBefore = int(0.5 * SAMPLE_RATE)
songFile[loc - breakBefore : loc] = np.zeros(breakBefore)












# region 3: pop section


loc_pop = loc
print('Pop starts at', loc_pop / SAMPLE_RATE)

bpm = 38
quarterNote = 60 / bpm
quarterLength = int(quarterNote * SAMPLE_RATE)



# Define functions for all instruments
def moogBass():
    freqs = [61.735, 73.416, 55]
    variation = 0.3

    note1 = sawtoothWave((freqs[0] - variation), quarterNote) + sawtoothWave((freqs[0] + variation), quarterNote)
    note2 = sawtoothWave((freqs[1] - variation), quarterNote) + sawtoothWave((freqs[1] + variation), quarterNote)
    note3 = sawtoothWave((freqs[2] - variation), 2 * quarterNote) + sawtoothWave((freqs[2] + variation), 2 * quarterNote)
    bassPattern = np.concatenate([note1, note2, note3])
    return moog_lowpass_filter(bassPattern, 500, 0, SAMPLE_RATE)

def padWave(freq, duration):
    normal = 0.7 * squareWave(freq, duration) + 0.2 * triangleWave(freq, duration)
    down_fourth = 0.7 * squareWave(freq * 3/4, duration) + 0.2 * triangleWave(freq * 3/4, duration)
    return normal + 0.8 * down_fourth

def songPad():
    quarterADSRpattern = generate_adsr_envelope(quarterNote * SAMPLE_RATE, 'frac', 0.2, 0.1, 0.8, 0.05)
    dottedHalfADSRpattern = generate_adsr_envelope(3 * quarterNote * SAMPLE_RATE, 'frac', 0.2 / 3, 0.1 / 3, 0.8, 0.05 / 3)
    line1 = np.concatenate([
        quarterADSRpattern * padWave(246.942, quarterNote),
        quarterADSRpattern * padWave(277.183, quarterNote),
        quarterADSRpattern * padWave(293.665, quarterNote),
        quarterADSRpattern * padWave(329.628, quarterNote)
    ])

    line2 = np.concatenate([
        dottedHalfADSRpattern * padWave(370, 3 * quarterNote),
        quarterADSRpattern * padWave(329.628, quarterNote)
    ])

    line3 = generate_adsr_envelope(4 * quarterNote * SAMPLE_RATE, 'frac', 0.2 / 4, 0.1 / 4, 0.8, 0.05 / 4) * padWave(440, 4 * quarterNote)

    line4 = np.concatenate([
        dottedHalfADSRpattern * padWave(587.33, 3 * quarterNote),
        quarterADSRpattern * padWave(554.365, quarterNote)
    ])

    minLength = min(len(line1), len(line2), len(line3), len(line4))
    padPattern = line1[:minLength] + line2[:minLength] + line3[:minLength] + line4[:minLength]

    return padPattern


def leadWave(freq, duration):
    triangle1 = triangleWave(freq - 0.05, duration)
    triangle2 = triangleWave(freq + 0.05, duration)
    triangle3 = 0.3 * triangleWave(2 * freq - 0.05, duration)
    triangle4 = 0.3 * triangleWave(2 * freq + 0.05, duration)
    sawtooth1 = 0.5 * sawtoothWave(freq - 0.05, duration)
    sawtooth2 = 0.5 * sawtoothWave(freq + 0.05, duration)
    sine = 0.25 * sineWave(freq - 0.1, duration)
    return triangle1 + triangle2 + sawtooth1 + sawtooth2 + sine + triangle3 + triangle4

def songLead():
    eighthNote = quarterNote / 2
    sixteenthNote = quarterNote / 4

    leadADSRpattern = generate_adsr_envelope(sixteenthNote * SAMPLE_RATE, 'frac', 0.05, 0.05, 0.7, 0.3)
    offsetADSRpattern = generate_adsr_envelope(eighthNote * SAMPLE_RATE, 'frac', 0.05, 0.05, 0.7, 0.3)

    freqs = [0, 740, 1480, 1480, 
            740, 1480, 1480, 740,
            740, 1480, 1480, 740,
            1109, 740, 880, 740]
    
    freq_odds = [0, 1480, 740, 1480, 740, 1480, 1109, 880]
    freq_evens = [740, 1480, 1480, 740, 1480, 740, 740, 740]

    line = []
    for freq in freqs:
        newNote = leadADSRpattern * leadWave(freq, sixteenthNote)
        line = np.concatenate([line, newNote])

    # Offset idea? 
    odd_line = []
    for freq in freq_odds:
        odd_line = np.concatenate([odd_line, offsetADSRpattern * leadWave(freq, eighthNote)])

    even_line = [0] * int(sixteenthNote * SAMPLE_RATE)
    for freq in freq_evens:
        even_line = np.concatenate([even_line, offsetADSRpattern * leadWave(freq, eighthNote)])

    full_line = odd_line + even_line[:len(odd_line)]

    filtered_line = moog_highpass_filter(full_line, 440, 0, SAMPLE_RATE)
    return filtered_line


def hihat():
    # Generate white noise wave
    seconds = quarterNote * 4
    white_noise_wave = whiteNoiseWave(seconds)


    # Customize volume
    hitFrequency = quarterNote / 8
    hitLength = 0.3 * hitFrequency
    adsrpattern = generate_adsr_envelope(hitLength * SAMPLE_RATE, 'frac', 
                                        0.05, 0.15, 0.35, 0.4)
    volumePattern = np.concatenate(
        [adsrpattern,
        [0] * int((hitFrequency - hitLength) * SAMPLE_RATE)]
    )
    numPatterns = int(np.floor(seconds*SAMPLE_RATE / len(volumePattern)))
    volumeVector = np.tile(volumePattern, numPatterns)

    shorterLength = len(white_noise_wave) if len(white_noise_wave) < len(volumeVector) else len(volumeVector)

    wave = white_noise_wave[:shorterLength] * volumeVector[:shorterLength]

    hihatPattern = moog_highpass_filter(wave, 440, 0, SAMPLE_RATE)
    
    return hihatPattern



moogAudio = 2 * moogBass()
padAudio = 0.3 * songPad()
leadAudio = 0.5 * songLead()
hatAudio = 0.08 * hihat()

print('- volumes of pop parts', np.max(moogAudio), np.max(padAudio), np.max(leadAudio), np.max(hatAudio))

unitLength = min(len(moogAudio), len(padAudio), len(leadAudio), len(hatAudio))

moogAudio = moogAudio[:unitLength]
padAudio = padAudio[:unitLength]
leadAudio = leadAudio[:unitLength]
hatAudio = hatAudio[:unitLength]


loc = loc_pop
for i in range(16):
    songFile[loc : loc + unitLength] += moogAudio

    if i == 3:
        songFile[loc : loc + unitLength] += np.linspace(0, 1, unitLength) * hatAudio

    if i > 3:
        songFile[loc : loc + unitLength] += hatAudio

    if i > 7:
        pan_up = np.linspace(0, 1, unitLength)
        if i % 2 == 0:
            songFile_L[loc : loc + unitLength] += 2 * leadAudio * (1 - pan_up)
            songFile_R[loc : loc + unitLength] += 2 * leadAudio * pan_up
        else:
            songFile_R[loc : loc + unitLength] += 2 * leadAudio * (1 - pan_up)
            songFile_L[loc : loc + unitLength] += 2 * leadAudio * pan_up

    if i > 11:
        # 12 --> 1 to 0.75
        # 13 --> 0.75
        # 14 --> 0.5
        # 15 --> 0.25
        y = 1 - 0.25 * (i - 12)
        songFile[loc : loc + unitLength] = np.linspace(y, y - 0.25, unitLength) * songFile[loc : loc + unitLength]
        songFile_L[loc : loc + unitLength] = np.linspace(y, y - 0.25, unitLength) * songFile_L[loc : loc + unitLength]
        songFile_R[loc : loc + unitLength] = np.linspace(y, y - 0.25, unitLength) * songFile_R[loc : loc + unitLength]

    # Don't fade out pad

    if i == 1:
        songFile[loc : loc + unitLength] += np.linspace(0, 1, unitLength) * padAudio
    if i > 1:
        songFile[loc : loc + unitLength] += padAudio
    

    loc += unitLength









# region 4:Steve Reich -esque
locAmbient = loc
print('Ambient starts at', locAmbient / SAMPLE_RATE)


def padDrone(notes, duration):
    drone = np.zeros(duration * SAMPLE_RATE)
    for note in notes:
        drone += 0.3 * padWave(notename_to_hertz(note), duration) + 0.5 * sineWave(notename_to_hertz(note), duration)
    return drone

drone = padDrone(['B-2', 'F#-3', 'A-3', 'C#-4', 'F#-4', 'B-4'], 30)
adsr = generate_adsr_envelope(len(drone), 'val', 0.25 * SAMPLE_RATE, 5 * SAMPLE_RATE, 0.5, 15 * SAMPLE_RATE)

songFile[locAmbient : locAmbient + len(drone)] += adsr * drone


duration = bpm_to_beat_duration(180)
riff1_notes = [notename_to_hertz('B-3'), 
               notename_to_hertz('F#-4'), 
               0,
               notename_to_hertz('E-4'),
               notename_to_hertz('C#-4'),
               0,
               notename_to_hertz('A-3'),
               0]
riff1 = 2 * writeMelody('sine', riff1_notes, [duration / 2] * len(riff1_notes))


riff2_notes = [0,
               notename_to_hertz('C#-5'), 
               notename_to_hertz('B-4'), 
               notename_to_hertz('A-4'), 
               0,
               notename_to_hertz('E-5'), 
               0,
               notename_to_hertz('C#-5')
               ]
riff2 = 2 * writeMelody('sine', riff2_notes, [duration / 2] * len(riff2_notes))


riff3_notes = [0, 0, 0, 0,
               notename_to_hertz('B-3'), notename_to_hertz('C#-4'), notename_to_hertz('E-4'), notename_to_hertz('F#-4'), 
               0, 0, 0, 0,
               notename_to_hertz('B-3'), notename_to_hertz('C#-4'), notename_to_hertz('E-4'), notename_to_hertz('F#-4')]
riff3 = writeMelody('square', [i * 2 for i in riff3_notes], [duration / 4] * len(riff3_notes))

riff3_alt_notes = [0, 0, 0, 0,
               notename_to_hertz('E-4'), notename_to_hertz('F#-4'), notename_to_hertz('A-4'), notename_to_hertz('B-4'), 
               0, 0, 0, 0,
               notename_to_hertz('E-4'), notename_to_hertz('F#-4'), notename_to_hertz('A-4'), notename_to_hertz('B-4')]
riff3_alt = writeMelody('square', [i * 2 for i in riff3_alt_notes], [duration / 4] * len(riff3_alt_notes))

riff4_notes = [notename_to_hertz('B-2'), 0, 0, notename_to_hertz('A-2'),
               0, 0, 0, 0]
riff4 = 2 * writeMelody('sawtooth', riff4_notes, [duration / 2] * len(riff4_notes))


a = anyWave('triangle', notename_to_hertz('B-2'), 2 * duration)
b = glissandoWave('triangle', notename_to_hertz('B-2'), notename_to_hertz('B-5'), 2 * duration)
c = anyWave('triangle', notename_to_hertz('B-5'), 4 * duration)

glissando_panup = np.concatenate([
    np.zeros(int(2 * duration * SAMPLE_RATE)),
    np.linspace(0, 1, int(2 * duration * SAMPLE_RATE)),
    np.ones(int(4 * duration * SAMPLE_RATE))
    ])
glissandoRiff = 2 * np.concatenate([a, b, c])

endRiff_notes = [notename_to_hertz('F#-2'), notename_to_hertz('E-2'), notename_to_hertz('D-2'), notename_to_hertz('C#-2'), notename_to_hertz('B-1')]
endRiff_durations = [duration, duration, duration, duration, 4 * duration]
endRiff = 2 * writeMelody('sawtooth', endRiff_notes, endRiff_durations) + writeMelody('sine', endRiff_notes, endRiff_durations)
endRiff_low = writeMelody('sawtooth', [0.5 * i for i in endRiff_notes], endRiff_durations) + 0.5 * writeMelody('sine', [0.5 * i for i in endRiff_notes], endRiff_durations)




loc = locAmbient + 15 * SAMPLE_RATE
riffLength = len(riff1)

songFile_L[loc : loc + riffLength] += riff1
loc += 4 * riffLength
songFile_R[loc : loc + riffLength] += riff1
loc += 4 * riffLength

for i in range(64):
    songFile_L[loc : loc + riffLength] += riff1

    if i >= 8:
        songFile_R[loc : loc + riffLength] += riff2

    if i >= 12 and i < 48:
        songFile_L[loc : loc + riffLength] += 0.6 * riff3
        songFile_R[loc : loc + riffLength] += 0.3 * riff3
    
    if i >= 48:
        songFile_L[loc : loc + riffLength] += 0.6 * riff3_alt
        songFile_R[loc : loc + riffLength] += 0.3 * riff3_alt

    if i >= 16:
        songFile_L[loc : loc + riffLength] += 0.3 * riff4
        songFile_R[loc : loc + riffLength] += 0.6 * riff4

    if i >= 32 and i % 2 == 0:
        songFile_L[loc : loc + 2 * riffLength] += glissando_panup * glissandoRiff
        songFile_R[loc : loc + 2 * riffLength] += (1 - glissando_panup) * glissandoRiff

    if i == 63:
        songFile[loc : loc + len(endRiff)] += endRiff + endRiff_low


    loc += riffLength

print("Final length:", (loc - riffLength + len(endRiff)) / SAMPLE_RATE)




# Combine everything, globally increase volume, write to .wav

song_stereo = 10 * np.column_stack((songFile_L + songFile, songFile_R + songFile))
write('hello_world/hello_world.wav', SAMPLE_RATE, song_stereo)