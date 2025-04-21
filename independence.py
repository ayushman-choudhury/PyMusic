from resources import *

songFile = np.zeros(SAMPLE_RATE * 60 * 5)

firstChordFreqs = [
    notename_to_hertz('B-1'),
    notename_to_hertz('B-2'),
    notename_to_hertz('B-3'),
    notename_to_hertz('C#-4'),
    notename_to_hertz('E-4'),
    notename_to_hertz('F#-4'),
    notename_to_hertz('F#-5'),
    notename_to_hertz('G#-5'),
    notename_to_hertz('B-5'),
    notename_to_hertz('C#-6')]
firstChordVols = [1, 1, 0.9, 0.9, 0.9, 0.9, 0.3, 0.3, 0.3, 0.3]
chord = writeChord('sine', firstChordFreqs, firstChordVols, 30)
adsr = generate_adsr_envelope(len(chord), 'val', 2 * SAMPLE_RATE, 2 * SAMPLE_RATE, 0.99, 5 * SAMPLE_RATE)
songFile[0:len(chord)] += adsr * chord

life = sonify_morse_const_freq(morse_encrypt('life'), notename_to_hertz('B-5'), notename_to_hertz('B-5'), 0.1, 'square')
loc = 3 * SAMPLE_RATE
songFile[loc : (loc + len(life))] += life


# "The birds"
life_melody = ['B-3', 'C#-4', 'D-4', 'E-4', 'G-4', 'F#-4', 'B-3', 'C#-4', 'D-4', 'C#-4', 'A-3']
life_pitches = [notename_to_hertz(x) for x in life_melody]


life = sonify_morse_carousel_freq(morse_encrypt('life'), [i * 2 for i in life_pitches], 0.1, 'sine')
loc = 15 * SAMPLE_RATE
songFile[loc : (loc + len(life))] += life * 5
newLoc = int(loc + len(life) + 0.5 * SAMPLE_RATE)
songFile[(newLoc):(newLoc + len(life))] += life * 5

# Side birds
life = sonify_morse_carousel_freq(morse_encrypt('life'), life_pitches, 0.12, 'sine')
loc = int(16 * SAMPLE_RATE)
songFile[loc : (loc + len(life))] += life * 2

life = sonify_morse_carousel_freq(morse_encrypt('life'), life_pitches, 0.08, 'sine')
loc = int(16.2 * SAMPLE_RATE)
songFile[loc : (loc + len(life))] += life * 2

life = sonify_morse_carousel_freq(morse_encrypt('life'), [i * 4 for i in life_pitches], 0.12, 'sine')
loc = int(16.4 * SAMPLE_RATE)
songFile[loc : (loc + len(life))] += life

life = sonify_morse_carousel_freq(morse_encrypt('life'), [i * 1.5 for i in life_pitches], 0.07, 'sine')
loc = int(19.6 * SAMPLE_RATE)
songFile[loc : (loc + len(life))] += life * 2

life = sonify_morse_carousel_freq(morse_encrypt('life'), [i * 0.5 for i in life_pitches], 0.05, 'sine')
loc = int(19.8 * SAMPLE_RATE)
songFile[loc : (loc + len(life))] += life * 2

life = sonify_morse_carousel_freq(morse_encrypt('life'), [i for i in life_pitches], 0.06, 'sine')
loc = int(20 * SAMPLE_RATE)
songFile[loc : (loc + len(life))] += life




# Trumpet stabs
beat = bpm_to_beat_duration(144)
click = sonify_morse_const_freq((morse_encrypt('s')), notename_to_hertz('A-4'), notename_to_hertz('A-4'), beat / 2, 'square')
loc = 45 * SAMPLE_RATE
songFile[loc : (loc + len(click))] += 0.5 * click

def trumpet(freq, duration):
    waves = 0.7 * sawtoothWave(freq, duration) + 0.3 * squareWave(freq, duration)
    adsr = generate_adsr_envelope(len(waves), 'frac', 0.02, 0.1, 0.8, 0.3)
    return waves * adsr

note1 = trumpet(notename_to_hertz('A-5'), beat / 4)
note2 = trumpet(notename_to_hertz('E-5'), beat / 4)
note3 = trumpet(notename_to_hertz('C#-5'), beat / 4)
note4 = trumpet(notename_to_hertz('A-4'), beat / 4)
note5 = trumpet(notename_to_hertz('A-3'), beat / 4)
note6 = trumpet(notename_to_hertz('A-2'), beat / 4)
stab = note1 + note2 + note3 + note4 + note5 + note6

bassNote = sawtoothWave(notename_to_hertz('A-2'), 3 * beat / 4) + sawtoothWave(notename_to_hertz('A-1'), 3 * beat / 4)

loc = int(loc + (beat * 2) * SAMPLE_RATE)
songFile[loc : (loc + len(stab))] += 3 * stab
songFile[loc : (loc + len(bassNote))] += 3 * bassNote

loc = int(loc + (beat / 4) * SAMPLE_RATE)
songFile[loc : (loc + len(stab))] += 3 * stab

loc = int(loc + (beat / 4) * SAMPLE_RATE)
songFile[loc : (loc + len(stab))] += 3 * stab

note1 = trumpet(notename_to_hertz('B-5'), beat / 4)
note2 = trumpet(notename_to_hertz('F#-5'), beat / 4)
note3 = trumpet(notename_to_hertz('D-5'), beat / 4)
note4 = trumpet(notename_to_hertz('B-4'), beat / 4)
note5 = trumpet(notename_to_hertz('B-3'), beat / 4)
note6 = trumpet(notename_to_hertz('B-2'), beat / 4)
stab = note1 + note2 + note3 + note4 + note5 + note6

loc_19 = int(loc + (beat / 4) * SAMPLE_RATE)
songFile[loc_19 : (loc_19 + len(stab))] += 3 * stab

bassNote = sawtoothWave(notename_to_hertz('B-2'), 3 * beat / 4) + sawtoothWave(notename_to_hertz('B-1'), 3 * beat / 4)
songFile[loc_19 : (loc_19 + len(bassNote))] += 3 * bassNote

######
# loc_19 is a good checkpoint
print("measure 19 is at", loc_19 / SAMPLE_RATE)
######


# Life melody against liberty
life = sonify_morse_carousel_freq(morse_encrypt('life'), [i * 2 for i in life_pitches], beat / 2, 'sawtooth')
loc = loc_19

for i in range(6):
    songFile[loc : (loc + len(life))] += life
    loc += 3 * int(beat * SAMPLE_RATE)


# Out-of-sync morse codes
loc = loc_19 + SAMPLE_RATE
life = sonify_morse_carousel_freq(morse_encrypt('life'), [i * 2 for i in life_pitches], 0.1, 'sine')
rest = np.zeros(int(0.5 * SAMPLE_RATE))
life_concat = np.concatenate([life, rest, life, rest, life])
songFile[loc : (loc + len(life_concat))] += life_concat * 2

loc = loc_19 + 2 * SAMPLE_RATE
life = sonify_morse_carousel_freq(morse_encrypt('life'), life_pitches, 0.08, 'sine')
rest = np.zeros(int(0.2 * SAMPLE_RATE))
life_concat = np.concatenate([life, rest, life, rest, life])
songFile[loc : (loc + len(life_concat))] += life_concat * 2




# Cadential section
loc_29 = int(loc_19 + 10 * (3 * beat * SAMPLE_RATE))
print("measure 29 is at", loc_29 / SAMPLE_RATE)


cadenceFreqs = [
    notename_to_hertz('F#-2'),
    notename_to_hertz('G-2'),
    notename_to_hertz('F-2'),
    notename_to_hertz('F#-2'),
]
cadenceDurs = [beat, beat, beat, beat * 3]

adsr = generate_adsr_envelope(beat * SAMPLE_RATE, 'frac', 0.02, 0.1, 0.5, 0.3)
adsr_long = generate_adsr_envelope(beat * 3 * SAMPLE_RATE, 'frac', 0.02, 0.1, 0.5, 0.3)
cadence_adsr = np.concatenate([adsr, adsr, adsr, adsr_long])


cadence = writeMelody('sawtooth', [0.5 * i for i in cadenceFreqs], cadenceDurs) * cadence_adsr
cadence += writeMelody('sawtooth', cadenceFreqs, cadenceDurs) * cadence_adsr
loc = int(loc_29 + 3 * beat * SAMPLE_RATE)
songFile[loc : (loc + len(cadence))] += cadence * 2

cadence = writeMelody('sawtooth', [2 * i for i in cadenceFreqs], cadenceDurs) * cadence_adsr
cadence += writeMelody('sawtooth', [4 * i for i in cadenceFreqs], cadenceDurs) * cadence_adsr
loc = int(loc + 3 * beat * SAMPLE_RATE)
songFile[loc : (loc + len(cadence))] += cadence * 2

cadence_adsr = np.concatenate([adsr, adsr, adsr])
cadence = writeMelody('sawtooth', [8 * i for i in cadenceFreqs[:-1]], cadenceDurs[:-1]) * cadence_adsr
cadence += writeMelody('sawtooth', [16 * i for i in cadenceFreqs[:-1]], cadenceDurs[:-1]) * cadence_adsr
loc = int(loc + 3 * beat * SAMPLE_RATE)
songFile[loc : (loc + len(cadence))] += cadence * 2


chord1Freqs = [
    notename_to_hertz('F#-2'),
    notename_to_hertz('A#-2'),
    notename_to_hertz('C#-3'),
    notename_to_hertz('F#-3'),
    notename_to_hertz('A#-3'),
    notename_to_hertz('C#-4'),
    notename_to_hertz('F#-4'),
    notename_to_hertz('A#-4'),
    notename_to_hertz('C#-5'),
    notename_to_hertz('F#-6'),
]

chord1 = writeChord('sawtooth', chord1Freqs, [1] * len(chord1Freqs), beat) * adsr

chord2Freqs = [
    notename_to_hertz('G-2'),
    notename_to_hertz('B-2'),
    notename_to_hertz('D-3'),
    notename_to_hertz('G-3'),
    notename_to_hertz('B-3'),
    notename_to_hertz('D-4'),
    notename_to_hertz('G-4'),
    notename_to_hertz('B-4'),
    notename_to_hertz('D-5'),
    notename_to_hertz('G-6'),
]
chord2 = writeChord('sawtooth', chord2Freqs, [1] * len(chord2Freqs), beat) * adsr

chord3Freqs = [
    notename_to_hertz('F-2'),
    notename_to_hertz('F-3'),
    notename_to_hertz('G-3'),
    notename_to_hertz('B-3'),
    notename_to_hertz('C#-4'),
    notename_to_hertz('F-4'),
    notename_to_hertz('G-4'),
    notename_to_hertz('B-4'),
    notename_to_hertz('C#-5'),
    notename_to_hertz('F-5'),
]
chord3 = writeChord('sawtooth', chord3Freqs, [1] * len(chord3Freqs), beat) * adsr

adsr_long = generate_adsr_envelope(beat * 12 * SAMPLE_RATE, 'frac', 0.02, 0.1, 0.5, 0.3)
chord4 = writeChord('sawtooth', chord1Freqs, [1] * len(chord1Freqs), beat * 12) * adsr_long

loc = int(loc + 3 * beat * SAMPLE_RATE)
songFile[loc : (loc + len(chord1))] += chord1
loc += len(chord1)
songFile[loc : (loc + len(chord2))] += chord2
loc += len(chord2)
songFile[loc : (loc + len(chord3))] += chord3
loc += len(chord3)
songFile[loc : (loc + len(chord4))] += chord4
loc += len(chord4)


loc_35 = loc 

# Python gets the melody

life = 0.25 * sonify_morse_carousel_freq(morse_encrypt('life'), life_pitches, beat / 2, 'sine')
life += 0.25 * sonify_morse_carousel_freq(morse_encrypt('life'), life_pitches, beat / 2, 'sawtooth')
life += 0.25 * sonify_morse_carousel_freq(morse_encrypt('life'), [i * 2 for i in life_pitches], beat / 2, 'sine')
life += 0.25 * sonify_morse_carousel_freq(morse_encrypt('life'), [i * 2 for i in life_pitches], beat / 2, 'sawtooth')

# a bassoon?
bassoon = 0.6 * sonify_morse_carousel_freq(morse_encrypt('life'), [i / 2 for i in life_pitches], beat / 2, 'sine')
bassoon += 0.4 * sonify_morse_carousel_freq(morse_encrypt('life'), [i * 3 / 2 for i in life_pitches], beat / 2, 'sine')
bassoon += 0.2 * sonify_morse_carousel_freq(morse_encrypt('life'), [i * 5 / 2 for i in life_pitches], beat / 2, 'sine')
bassoon += 0.1 * sonify_morse_carousel_freq(morse_encrypt('life'), [i * 7 / 2 for i in life_pitches], beat / 2, 'sine')

loc = loc_35 + 3 * int(beat * SAMPLE_RATE)
songFile[loc : (loc + len(life))] += life + 2 * bassoon

loc_43 = loc_35 + 8 * 3 * int(beat * SAMPLE_RATE)
songFile[loc_43 : (loc_43 + len(life))] += life + 2 * bassoon




# B section: 1:30 - 4:00 (2.5 minutes total) (90 to 240, 150)



loc_50 = loc_43 + 7 * 3 * int(beat * SAMPLE_RATE)


# Time keeping
life_stretched = ['B-3'] * 3 + ['C#-4'] * 9 + ['D-4'] * 3 + ['E-4'] * 6 + ['G-4'] * 3 + ['F#-4'] * 6 + ['B-3'] * 3 + ['C#-4'] * 3 + ['D-4'] * 9 + ['C#-4'] * 6 + ['A-3'] * 2 + ['A#-3']
stretched_pitches = [notename_to_hertz(x) for x in life_stretched]
stretched_pedal = writeMelodicPedal(2 * 64 * 3, ['sine'], stretched_pitches, [beat])
adsr = generate_adsr_envelope((beat * SAMPLE_RATE), 'frac', 0.02, 0.02, 0.7, 0.3)
adsr_tiled = np.tile(adsr, 2 * 64 * 3)
#print('DEBUG: ', len(stretched_pedal), len(adsr_tiled))
songFile[loc_50 : (loc_50 + len(stretched_pedal))] += 5 * (stretched_pedal * adsr_tiled)
loc_section_C = loc_50 + len(stretched_pedal)


bass_notes = ['B-2', 'C#-3', 'D-3', 'E-3', 'F#-3', 'G-3', 'E-3', 'F#-3']
bass_pitches = 2 * [notename_to_hertz(x) for x in bass_notes]
bass = writeMelody('sawtooth', bass_pitches, [beat * 3 * 8] * len(bass_pitches)) + writeMelody('sawtooth', [0.5 * i for i in bass_pitches], [beat * 3 * 8] * len(bass_pitches))
adsr = generate_adsr_envelope(beat * 3 * 8 * SAMPLE_RATE, 'frac', 0.01, 0.01, 0.6, 0.9)
adsr_tiled = np.tile(adsr, 2 * 8)
songFile[loc_50 : (loc_50 + len(bass))] += 2 * bass * adsr_tiled



# Quotes

print('Start of B section: array length is', 90 * SAMPLE_RATE)
loc_quote = int(90 * SAMPLE_RATE)
quote_text = 'The history of the present King of Great Britain is a history of repeated injuries and usurpations, all having in direct object the establishment of an absolute Tyranny over these States.'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('B-4'), notename_to_hertz('C#-5'), 0.09, 'square')
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

print('Done with long quote')

loc_quote = int(120 * SAMPLE_RATE)
quote_text = 'He has refused his assent to laws'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('D-5'), notename_to_hertz('E-5'), 0.08, 'square')
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

loc_quote = int(130 * SAMPLE_RATE)
quote_text = 'He has obstructed the Administration of Justice'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('E-5'), notename_to_hertz('F#-5'), 0.085, 'square')
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

loc_quote = int(140 * SAMPLE_RATE)
quote_text = 'He has made Judges dependent on his Will alone'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('F#-5'), notename_to_hertz('G-5'), 0.075, 'square')
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

loc_quote = int(150 * SAMPLE_RATE)
quote_text = 'He has obstructed the Laws for Naturalization of Foreigners'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('G-5'), notename_to_hertz('A-5'), 0.08, 'square')
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

loc_quote = int(160 * SAMPLE_RATE)
quote_text = 'cutting off our Trade with all parts of the world'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('D-4'), notename_to_hertz('E-4'), 0.085, 'square')
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

loc_quote = int(170 * SAMPLE_RATE)
quote_text = 'transporting us beyond Seas to be tried for pretended offences'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('E-4'), notename_to_hertz('F#-4'), 0.075, 'square')
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

loc_quote = int(180 * SAMPLE_RATE)
quote_text = 'He has destroyed the lives of our people'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('F#-4'), notename_to_hertz('G-5'), 0.08, 'square')
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

loc_quote = int(190 * SAMPLE_RATE)
quote_text = 'He has excited domestic insurrections amongst us'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('G-4'), notename_to_hertz('A-4'), 0.085, 'square')
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified



# All at once, at the end
quote_text = 'He has refused his assent to laws'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('D-5'), notename_to_hertz('E-5'), 0.08, 'square')
loc_quote = loc_section_C - len(quote_sonified) - SAMPLE_RATE
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

quote_text = 'He has obstructed the Administration of Justice'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('E-5'), notename_to_hertz('F#-5'), 0.085, 'square')
loc_quote = loc_section_C - len(quote_sonified) - SAMPLE_RATE
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

quote_text = 'He has made Judges dependent on his Will alone'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('F#-5'), notename_to_hertz('G-5'), 0.075, 'square')
loc_quote = loc_section_C - len(quote_sonified) - SAMPLE_RATE
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

quote_text = 'He has obstructed the Laws for Naturalization of Foreigners'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('G-5'), notename_to_hertz('A-5'), 0.08, 'square')
loc_quote = loc_section_C - len(quote_sonified) - SAMPLE_RATE
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

quote_text = 'cutting off our Trade with all parts of the world'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('D-4'), notename_to_hertz('E-4'), 0.085, 'square')
loc_quote = loc_section_C - len(quote_sonified) - SAMPLE_RATE
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

quote_text = 'transporting us beyond Seas to be tried for pretended offences'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('E-4'), notename_to_hertz('F#-4'), 0.075, 'square')
loc_quote = loc_section_C - len(quote_sonified) - SAMPLE_RATE
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

quote_text = 'He has destroyed the lives of our people'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('F#-4'), notename_to_hertz('G-5'), 0.08, 'square')
loc_quote = loc_section_C - len(quote_sonified) - SAMPLE_RATE
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified

quote_text = 'He has excited domestic insurrections amongst us'
quote_sonified = sonify_morse_const_freq(morse_encrypt(quote_text), notename_to_hertz('G-4'), notename_to_hertz('A-4'), 0.085, 'square')
loc_quote = loc_section_C - len(quote_sonified) - SAMPLE_RATE
songFile[loc_quote : (loc_quote + len(quote_sonified))] += quote_sonified



print('Done with all quotes!')



# Conclusion
loc = loc_section_C

# END
# 11 notes . _ . . . . . . _ . . 
# If I end with America The Beautiful:
# good with bro ther hood
# from sea to shi ning sea
# If I end with Star Spangled Banner:
# (la)-and of the free
# and the home of the [long] brave

# Choosing Star Spangled Banner:
#end_melody = ['B-4', 'A-4', 'B-4', 'F#-4', 'F#-4', 'F#-4', 'G-4', 'B-4', 'F#-4', 'C#-5', 'B-4']
end_melody = ['C#-5', 'D-5', 'E-5', 'F#-5', 'B-4', 'C#-5', 'D-5', 'E-5', 'C#-5', 'F#-4', 'B-4']
end_pitches = [notename_to_hertz(x) for x in end_melody]
end_phrase = sonify_morse_carousel_freq(morse_encrypt('life'), end_pitches, beat / 1.5, 'sine')
num_seconds_end = len(end_phrase) / SAMPLE_RATE

chord = writeChord('sine', firstChordFreqs, firstChordVols, 18 * 3 * beat + 7 + num_seconds_end)
adsr = generate_adsr_envelope(len(chord), 'val', 2 * SAMPLE_RATE, 2 * SAMPLE_RATE, 0.99, 5 * SAMPLE_RATE)
songFile[loc : loc + len(chord)] += adsr * chord
loc += len(chord)
songFile[loc : loc + len(end_phrase)] += end_phrase



# Write
write('independence/independence.wav', SAMPLE_RATE, songFile * 10)