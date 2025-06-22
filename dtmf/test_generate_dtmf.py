import sys
from generate_dtmf import DTMFGenerator, play_tone, play_sequence


def display_menu():
    print("\n" + "="*50)
    print("DTMF Tone Generator Test")
    print("="*50)
    print("Choose an option:")
    print("1. Single digit test")
    print("2. Custom sequence")
    print("3. Audio test (all digits)")
    print("4. Acoustic coupling test")
    print("q. Quit")
    print("="*50)


def single_digit_test():
    """Test a single DTMF digit."""
    print("\nSingle Digit Test")
    print("Valid keys: 0-9, *, #")
    
    while True:
        digit = input("Enter digit to test (or 'back' to return): ").strip()
        
        if digit.lower() == 'back':
            break
        
        if len(digit) == 1 and digit in DTMFGenerator.get_supported_keys():
            print(f"Playing DTMF tone for '{digit}'...")
            play_tone(digit)
            print("Tone played successfully")
        else:
            print("Invalid digit. Use: 0-9, *, #")


def custom_sequence():
    """Allow user to input a custom sequence."""
    print("\nCustom Sequence Test")
    print("Enter a sequence of digits (e.g., '5551234' or '911')")
    
    while True:
        sequence = input("Enter sequence (or 'back' to return): ").strip()
        
        if sequence.lower() == 'back':
            break
        
        if not sequence:
            continue
            
        invalid_chars = [c for c in sequence if c not in DTMFGenerator.get_supported_keys()]
        if invalid_chars:
            print(f"Invalid characters: {', '.join(invalid_chars)}")
            print("Use only: 0-9, *, #")
            continue
        
        print(f"Playing sequence: {' → '.join(sequence)}")
        play_sequence(sequence)
        print("Sequence played successfully")


def audio_test():
    """Play all digits to test audio setup."""
    print("\nAudio Test - All Digits")
    print("This will play all keypad keys to test your audio setup")
    
    input("Press Enter to start audio test...")
    
    all_keys = "123456789*0#"
    dtmf = DTMFGenerator(tone_duration=0.4, silence_duration=0.2)
    
    print("Playing all keypad keys...")
    for key in all_keys:
        print(f"   {key}... ", end="", flush=True)
        dtmf.play_tone(key)
        print("")
    
    print("Audio test completed!")


def acoustic_coupling_test():
    """Test different settings for acoustic coupling (laptop speakers to phone)."""
    print("\nAcoustic Coupling Test")
    print("This test helps optimize DTMF recognition when playing from")
    print("laptop speakers to phone microphone")
    print()
    print("Setup instructions:")
    print("   1. Call a test number or voicemail system")
    print("   2. Hold phone microphone 2-3cm from laptop speakers")
    print("   3. Set laptop volume to maximum")
    print("   4. Test different tone durations below")
    print()
    
    durations = [0.8, 1.0, 1.5, 2.0]
    
    for duration in durations:
        input(f"Press Enter to test {duration}s tone duration...")
        print(f"🔊 Playing digit '2' for {duration} seconds...")
        
        dtmf = DTMFGenerator(tone_duration=duration, amplitude=0.9)
        dtmf.play_tone('2')
        
        response = input("Was this tone recognized? (y/n/q to quit): ").strip().lower()
        if response == 'y':
            print(f"{duration}s duration works! Use this setting.")
            break
        elif response == 'q':
            break
        else:
            print(f"{duration}s duration failed, trying longer...")

def main():
    """Main program loop."""
    print("DTMF Test Script")
    print("Using pygame for audio playback")
    
    while True:
        display_menu()
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q' or choice == 'quit':
            print("Goodbye!")
            break
        elif choice == '1':
            single_digit_test()
        elif choice == '2':
            custom_sequence()
        elif choice == '3':
            audio_test()
        elif choice == '4':
            acoustic_coupling_test()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting... Good luck with your test!")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
