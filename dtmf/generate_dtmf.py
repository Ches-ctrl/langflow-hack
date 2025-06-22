import math
import pygame
import numpy as np
from typing import List


class DTMFGenerator:
    FREQ_MAP = {
        "1": (697.0, 1209.0), "2": (697.0, 1336.0), "3": (697.0, 1477.0),
        "4": (770.0, 1209.0), "5": (770.0, 1336.0), "6": (770.0, 1477.0), 
        "7": (852.0, 1209.0), "8": (852.0, 1336.0), "9": (852.0, 1477.0),
        "*": (941.0, 1209.0), "0": (941.0, 1336.0), "#": (941.0, 1477.0),
        "A": (697.0, 1633.0), "B": (770.0, 1633.0), 
        "C": (852.0, 1633.0), "D": (941.0, 1633.0)
    }
    
    def __init__(self, 
                 sample_rate: int = 8000,
                 tone_duration: float = 0.8,
                 silence_duration: float = 0.2,
                 amplitude: float = 0.8):
        self.sample_rate = sample_rate
        self.tone_duration = tone_duration
        self.silence_duration = silence_duration
        self.amplitude = amplitude
        
        pygame.mixer.pre_init(frequency=sample_rate, size=-16, channels=1, buffer=512)
        pygame.mixer.init()
    
    def generate_tone(self, key: str) -> List[float]:
        """
        Generate DTMF tone audio samples for a single key.
        """
        if key not in self.FREQ_MAP:
            raise ValueError(f"Invalid DTMF key: {key}")
        
        low_freq, high_freq = self.FREQ_MAP[key]
        num_samples = int(self.tone_duration * self.sample_rate)
        
        samples = []
        for i in range(num_samples):
            t = i / self.sample_rate
            low_tone = math.sin(2 * math.pi * low_freq * t)
            high_tone = math.sin(2 * math.pi * high_freq * t)
            combined = (low_tone + high_tone) * self.amplitude * 0.5
            samples.append(combined)
        
        return samples
    
    def generate_sequence(self, keys: str, include_silence: bool = True) -> List[float]:
        """
        Generate DTMF sequence for multiple keys.
        """
        audio_data = []
        silence_samples = self._generate_silence() if include_silence else []
        
        for i, key in enumerate(keys):
            tone_samples = self.generate_tone(key)
            audio_data.extend(tone_samples)
            
            if include_silence and i < len(keys) - 1:
                audio_data.extend(silence_samples)
        
        return audio_data
    
    def _generate_silence(self) -> List[float]:
        """Generate silence samples."""
        num_samples = int(self.silence_duration * self.sample_rate)
        return [0.0] * num_samples
    
    def play_tone(self, key: str) -> None:
        """
        Generate and play a single DTMF tone.
        """
        audio_data = self.generate_tone(key)
        self._play_audio(audio_data)
    
    def play_sequence(self, keys: str, include_silence: bool = True) -> None:
        """
        Generate and play a sequence of DTMF tones.
        """
        audio_data = self.generate_sequence(keys, include_silence)
        self._play_audio(audio_data)
    
    def _play_audio(self, audio_data: List[float]) -> None:
        """
        Play audio data using pygame.
        """
        # Convert to numpy array and scale to 16-bit
        audio_array = np.array(audio_data) * 32767
        audio_array = audio_array.astype(np.int16)
        
        sound = pygame.sndarray.make_sound(audio_array)
        sound.play()
        
        while pygame.mixer.get_busy():
            pygame.time.wait(10)
    
    def cleanup(self) -> None:
        """Clean up pygame mixer resources."""
        pygame.mixer.quit()
    
    @classmethod
    def get_supported_keys(cls) -> List[str]:
        """Get list of all supported DTMF keys."""
        return list(cls.FREQ_MAP.keys())
    
    @classmethod
    def is_valid_key(cls, key: str) -> bool:
        """Check if a key is valid for DTMF generation."""
        return key in cls.FREQ_MAP


def generate_tone(key: str, 
                 sample_rate: int = 8000,
                 duration: float = 0.8,
                 amplitude: float = 0.8) -> List[float]:
    """
    Generate a single DTMF tone.
    """
    generator = DTMFGenerator(sample_rate=sample_rate, 
                             tone_duration=duration,
                             amplitude=amplitude)
    tone_data = generator.generate_tone(key)
    return tone_data


def play_tone(key: str,
              sample_rate: int = 8000,
              duration: float = 0.8,
              amplitude: float = 0.8) -> None:
    """
    Generate and play a single DTMF tone.
    """
    generator = DTMFGenerator(sample_rate=sample_rate,
                             tone_duration=duration,
                             amplitude=amplitude)
    generator.play_tone(key)


def play_sequence(keys: str,
                 sample_rate: int = 8000,
                 tone_duration: float = 0.8,
                 silence_duration: float = 0.2,
                 amplitude: float = 0.8) -> None:
    """
    Generate and play a sequence of DTMF tones.
    """
    generator = DTMFGenerator(sample_rate=sample_rate,
                             tone_duration=tone_duration,
                             silence_duration=silence_duration,
                             amplitude=amplitude)
    generator.play_sequence(keys)
