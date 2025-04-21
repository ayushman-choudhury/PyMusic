print('Initializing resources...')

# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy import signal

print('... packages imported!')

# The sampling rate of modern audio is 44,100 samples per second
SAMPLE_RATE = 44100


# region 1. Basic Wave Functions

def sineWave(freq, duration):
    """
    Generate a sine wave, at a particular frequency, for a particular duration
        e.g. an A for one second is sineWave(440, 1)

    Parameters:
        freq: Frequency of note
        duration: Length of note as a fraction of a second. E.g. 0.5 = half a second

    Returns a np.array
    """
    x = np.linspace(0, duration, int(duration * SAMPLE_RATE))
    return 0.01 * np.sin(2 * np.pi * freq * x)


def sawtoothWave(freq, duration):
    """
    Generate a sawtooth wave, at a particular frequency, for a particular duration
        e.g. an A for one second is sawtoothWave(440, 1)

    Parameters:
        freq: Frequency of note
        duration: Length of note as a fraction of a second. E.g. 0.5 = half a second

    Returns a np.array
    """
    x = np.linspace(0, duration, int(duration * SAMPLE_RATE))
    return 0.01 * signal.sawtooth(2 * np.pi * freq * x)


def squareWave(freq, duration):
    """
    Generate a square wave, at a particular frequency, for a particular duration
        e.g. an A for one second is squareWave(440, 1)

    Parameters:
        freq: Frequency of note
        duration: Length of note as a fraction of a second. E.g. 0.5 = half a second

    Returns a np.array
    """
    x = np.linspace(0, duration, int(duration * SAMPLE_RATE))
    return 0.01 * np.sign(np.sin(2 * np.pi * freq * x))

def triangleWave(freq, duration):
    """
    Generate a triangle wave, at a particular frequency, for a particular duration
        e.g. an A for one second is triangleWave(440, 1)

    Parameters:
        freq: Frequency of note
        duration: Length of note as a fraction of a second. E.g. 0.5 = half a second

    Returns a np.array
    """
    x = np.linspace(0, duration, int(duration * SAMPLE_RATE))
    return 0.01 * (2 * np.abs(2 * (x * freq % 1) - 1) - 1)


def whiteNoiseWave(duration):
    """
    Generate a burst of white noise for a particular duration
        e.g. one second of white noise is whiteNoiseWave(1)

    Parameters:
        duration: Length of burst as a fraction of a second. E.g. 0.5 = half a second

    Returns a np.array
    """
    gauss = np.random.normal(0, 1, size= int(duration * SAMPLE_RATE))
    return 0.1 * np.sin(2 * np.pi * gauss)


def anyWave(waveType, freq, duration):
    """
    Generate any wave, at a particular frequency, for a particular duration
        e.g. a sine A for one second is anyWave('sine', 440, 1)

    Parameters:
        waveType: 'sine', 'square', 'triangle', 'sawtooth', 'whiteNoise'
        freq: Frequency of note
        duration: Length of note as a fraction of a second. E.g. 0.5 = half a second

    Returns a np.array
    """
    if waveType == 'sine':
        return sineWave(freq, duration)
    elif waveType == 'square':
        return squareWave(freq, duration)
    elif waveType == 'triangle':
        return triangleWave(freq, duration)
    elif waveType == 'sawtooth':
        return sawtoothWave(freq, duration)
    elif waveType == 'whiteNoise':
        return whiteNoiseWave(duration)
    else:
        raise Exception('Did not expect that wave type')





# region 2. Basic music functionality

def glissandoWave(waveType, startFreq, endFreq, duration):
    """
    Generate a glissando between two pitches

    Parameters:
        waveType: 'sine', 'square', 'triangle', 'sawtooth'
        startFreq: starting frequency
        endFreq: ending frequency
        duration: Length of note as a fraction of a second. E.g. 0.5 = half a second

    Returns a np.array
    """
    # Correct for phase shifting:
    if endFreq != startFreq:
        endFreq = (startFreq + endFreq) / 2

    freqArr = np.linspace(startFreq, endFreq, int(duration * SAMPLE_RATE))

    return anyWave(waveType, freqArr, duration)



def glissandoMelody(waveType, noteFreqs, noteDurations):
    """
    Compiles a series of glissandos into a melody

    Parameters:
        waveType: 'sine', 'square', 'triangle', or 'sawtooth'
        noteFreqs: a list of pitch frequencies for the notes
        noteDurations: a list of durations (fractions of seconds)

    Returns: a np.array
    """
    if len(noteFreqs) != len(noteDurations):
            raise Exception('Frequencies and Durations must have the same length!')
        
    melody = np.array([])

    for index in range(len(noteFreqs) - 1):
        melody = np.concatenate([melody, 
            glissandoWave(waveType, noteFreqs[index], noteFreqs[index + 1], noteDurations[index])])
    
    return melody



def writeMelody(waveType, noteFreqs, noteDurations):
    """
    Writes a melody for a given wave type
        e.g. a sine octave at half-second intervals is:
        writeMelody('sine', [440, 880], [0.5, 0.5])

    Parameters:
        waveType: 'sine', 'square', 'triangle', or 'sawtooth'
        noteFreqs: a list of pitch frequencies for the notes
        noteDurations: a list of durations (fractions of seconds)

    Returns: a np.array
    """
    if len(noteFreqs) != len(noteDurations):
        raise Exception('Frequencies and Durations must have the same length!')
    
    melody = np.array([])

    for freq, dur in zip(noteFreqs, noteDurations):
        melody = np.concatenate([melody, anyWave(waveType, freq, dur)])
    
    return melody



def writeMelodicPedal(numNotes, waveTypes, noteFreqs, noteDurations):
    """
    Writes a melodic pedal for some number of notes. 

    Parameters:
        numNotes: an integer number of notes for the pedal
        waveTypes: a list of the wave types to be repeated. 'sine', 'square', 'triangle', or 'sawtooth'
        noteFreqs: a list of the pitch frequencies to be repeated
        noteDurations: a list of the durations (fractions of a second) to be repeated

    Returns: a np.array
    """
    lenWavePedal = len(waveTypes)
    lenNotePedal = len(noteFreqs)
    lenDurationPedal = len(noteDurations)

    melody = np.array([])

    for i in range(numNotes):
        newNote = anyWave(waveTypes[i % lenWavePedal], 
                          noteFreqs[i % lenNotePedal], 
                          noteDurations[i % lenDurationPedal])
        melody = np.concatenate([melody, newNote])
    
    return melody



def writeChord(waveType, noteFreqs, noteVols, duration):
    """
    Writes a chord for a given wave type
        e.g. a sawtooth A power-chord for one second is:
        writeChord('sawtooth', [110, 165, 220,], [3, 2, 2], 1)

    Parameters:
        waveType: 'sine', 'square', 'triangle', or 'sawtooth'
        noteFreqs: a list of pitch frequencies for the notes
        noteVols: a list of volumes for the notes
        duration: the duration of the chord (fractions of seconds)

    Returns: a np.array
    """
    chord = np.zeros(int(SAMPLE_RATE * duration))

    for freq, vol in zip(noteFreqs, noteVols):
        thisWave = anyWave(waveType, freq, duration)
        chord += vol * thisWave

    return chord
        


def bpm_to_beat_duration(bpm):
    """
    Converts bpm to beat_duration
        Ex. 120 bpm --> 0.5 seconds / beat

    Parameters: 
        bpm: beats per minute, the standard tempo indicator
    
    Returns: a number
    """
    return 60 / bpm



def generate_adsr_envelope(totalLength, adsrMode, attack, decay, sustainVol, release):
    """
    Generates an ADSR envelope

    Parameters:
        totalLength: array length of desired envelope
        adsrMode: 'frac' or 'val' for whether ADSR sections are fractions or values
        attack: rise from 0 to 1
        decay: fall from 1 to sustainVol
        sustainVol: volume of middle part of sound
        release: fall from sustainVol to 0
    
    Returns: a np.array
    """

    if adsrMode == 'frac':
        # Calculate lengths of each phase
        attack_length = int(totalLength * attack)
        decay_length = int(totalLength * decay)
        release_length = int(totalLength * release)
    elif adsrMode == 'val':
        attack_length = int(attack)
        decay_length = int(decay)
        release_length = int(release)
    else:
        raise Exception('Did not expect that adsr type')

    # Calculate sustain based on these
    sustain_length = int(totalLength) - (attack_length + decay_length + release_length)

    # Generate the phases
    attack_phase = np.linspace(0, 1, attack_length)
    decay_phase = np.linspace(1, sustainVol, decay_length)
    sustain_phase = np.full(sustain_length, sustainVol)
    release_phase = np.linspace(sustainVol, 0, release_length)

    # Combine all phases
    return np.concatenate([attack_phase, decay_phase, sustain_phase, release_phase])



def lfo(freq, duration, phase=0):
    """
    Generates a low-frequency oscillator

    Parameters:
        freq: Frequency of note
        duration: Length of note as a fraction of a second. E.g. 0.5 = half a second
        phase: Starting phase of oscillation
    
    Returns: a np.array
    """
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return np.sin(2 * np.pi * freq * t + phase)





# region 3. Morse Code (text)

# Credit to "geeksforgeeks.org"
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 
                    'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 
                    'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', 
                    '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', 
                    '.':'.-.-.-', ',':'--..--', '?':'..--..', ':':'---...', ';':'_._._.',
                    '-':'-....-', '/':'-..-.', '!': '-.-.--', '(':'-.--.', ')':'-.--.-'
}

def morse_encrypt(message: str):
    """
    Converts a string message to a Python list of Morse representations of each char
        Spaces and invalid characters become list items of ''

    Parameters:
        message: a string

    Returns: a Python list
    """
    message = message.upper()
    cipher = []
    for letter in message:
        if letter == '':
            cipher.append('')
        elif letter in MORSE_CODE_DICT:
            cipher.append(MORSE_CODE_DICT[letter])
        else:
            cipher.append('')
 
    return cipher



def sonify_morse_const_freq(morse, dotFreq, dashFreq, dotDuration, waveType):
    """
    Writes a melody for a given Morse list

    Parameters:
        morse: the list built in morse_encrypt()
        dotFreq: the pitch of dots
        dashFreq: the pitch of dashes
        dotDuration: the length of a dot, in seconds
        waveType: 'sine', 'square', 'triangle', or 'sawtooth'

    Returns: a np.array
    """
    
    # To call writeMelody, we need noteFreqs, noteDurations
    noteFreqs = []
    noteDurations = []
    
    #Spacing rules:
    # - Within a letter, after each dot or dash: 1 dot-worth of space
    # - After a letter: 3 dot-worth of space (2 more than normally after a symbol)
    # - After a word: 7 dot-worth of space (4 more than normally after a letter)
    for letter in morse:
        if letter == '':
            noteFreqs.append(0)
            noteDurations.append(4 * dotDuration)
        else:
            for symbol in letter:
                if symbol == '.':
                    noteFreqs.append(dotFreq)
                    noteDurations.append(dotDuration)
                elif symbol == '-':
                    noteFreqs.append(dashFreq)
                    noteDurations.append(3 * dotDuration)
                else:
                    raise Exception('Not supposed to be anything besides . and -')
                noteFreqs.append(0)
                noteDurations.append(dotDuration)
            
            noteFreqs.append(0)
            noteDurations.append(2 * dotDuration)

    melody = writeMelody(waveType, noteFreqs, noteDurations)
    return melody



def sonify_morse_carousel_freq(morse, carouselFreq, dotDuration, waveType):
    """
    Writes a melody for a given Morse list

    Parameters:
        morse: the list built in morse_encrypt()
        carouselFreq: a list of frequencies, that can be repeated
        dotDuration: the length of a dot, in seconds
        waveType: 'sine', 'square', 'triangle', or 'sawtooth'

    Returns: a np.array
    """
    i = 0
    
    # To call writeMelody, we need noteFreqs, noteDurations
    noteFreqs = []
    noteDurations = []
    
    #Spacing rules:
    # - Within a letter, after each dot or dash: 1 dot-worth of space
    # - After a letter: 3 dot-worth of space (2 more than normally after a symbol)
    # - After a word: 7 dot-worth of space (4 more than normally after a letter)
    for letter in morse:
        if letter == '':
            noteFreqs.append(0)
            noteDurations.append(4 * dotDuration)
        else:
            for symbol in letter:
                noteFreqs.append(carouselFreq[i % len(carouselFreq)])
                i += 1
                if symbol == '.':
                    noteDurations.append(dotDuration)
                elif symbol == '-':
                    noteDurations.append(3 * dotDuration)
                else:
                    raise Exception('Not supposed to be anything besides . and -')
                noteFreqs.append(0)
                noteDurations.append(dotDuration)
            
            noteFreqs.append(0)
            noteDurations.append(2 * dotDuration)

    melody = writeMelody(waveType, noteFreqs, noteDurations)
    return melody





# region 4. Equal Temperament

NOTE_DICT = {'C':0, 'C#':1, 'Db':1,
             'D':2, 'D#':3, 'Eb':3,
             'E':4, 'F':5, 'F#':6, 'Gb':6,
             'G':7, 'G#':8, 'Ab':8,
             'A':9, 'A#':10, 'Bb':10, 'B':11}



def notename_to_hertz(notename: str):
    """
    Inputs a string of a notename, outputs the hertz value
        ex. A-4 --> 440, or A 4 --> 440

    Parameters:
        notename: a string, of a note and a hyphen, separated by a space or hyphen

    Returns: a number
    """
    substrings = notename.replace('-', ' ').split(' ')
    note_num = NOTE_DICT[substrings[0]]
    octave_num = float(substrings[1])

    c_hertz = 32.7032 * (2 ** (octave_num-1))
    hertz = c_hertz * (2 ** (note_num / 12))

    return int(hertz * 1000) / 1000.0





# region 5. fun filters

def moog_lowpass_filter(input_signal, cutoff, resonance, sample_rate):
    """
    Simulates a Moog 4-pole resonant low-pass filter.
    
    Parameters:
        input_signal (np.array): The audio input signal.
        cutoff (float): Cutoff frequency in Hz.
        resonance (float): Resonance (0 to 4, where 4 is self-oscillating).
        sample_rate (int): The sample rate of the audio signal.

    Returns:
        np.array: The filtered audio signal.
    """
    # Clamp resonance to the 0-4 range
    resonance = max(0, min(resonance, 4))
    
    # Calculate filter coefficients
    fc = cutoff / sample_rate
    g = 4.0 * (1.0 - np.exp(-2.0 * np.pi * fc))
    
    # Filter state
    z = [0.0, 0.0, 0.0, 0.0]  # 4 filter stages
    
    # Output signal
    output = np.zeros_like(input_signal)
    
    # Main filter loop
    for n, x in enumerate(input_signal):
        # Input with resonance feedback
        x_feedback = x - resonance * z[3]
        
        # Process through each pole (4 stages)
        z[0] += g * (np.tanh(x_feedback) - np.tanh(z[0]))
        z[1] += g * (np.tanh(z[0]) - np.tanh(z[1]))
        z[2] += g * (np.tanh(z[1]) - np.tanh(z[2]))
        z[3] += g * (np.tanh(z[2]) - np.tanh(z[3]))
        
        # Output is the final stage
        output[n] = z[3]
    
    return output




def moog_highpass_filter(input_signal, cutoff, resonance, sample_rate):
    """
    Simulates a Moog 4-pole resonant high-pass filter.
    
    Parameters:
        input_signal (np.array): The audio input signal.
        cutoff (float): Cutoff frequency in Hz.
        resonance (float): Resonance (0 to 4, where 4 is self-oscillating).
        sample_rate (int): The sample rate of the audio signal.
    
    Returns:
        np.array: The filtered audio signal.
    """
    # Clamp resonance to the 0-4 range
    resonance = max(0, min(resonance, 4))
    
    # Calculate filter coefficients
    fc = cutoff / sample_rate
    g = 4.0 * (1.0 - np.exp(-2.0 * np.pi * fc))
    
    # Filter state
    z = [0.0, 0.0, 0.0, 0.0]  # 4 filter stages
    
    # Output signal
    output = np.zeros_like(input_signal)
    
    # Main filter loop
    for n, x in enumerate(input_signal):
        # Input with resonance feedback
        x_feedback = x - resonance * z[3]
        
        # Process through each low-pass stage
        z[0] += g * (np.tanh(x_feedback) - np.tanh(z[0]))
        z[1] += g * (np.tanh(z[0]) - np.tanh(z[1]))
        z[2] += g * (np.tanh(z[1]) - np.tanh(z[2]))
        z[3] += g * (np.tanh(z[2]) - np.tanh(z[3]))
        
        # Subtract low-pass output from the input to get high-pass
        output[n] = x - z[3]
    
    return output






print('... resources initialized!')