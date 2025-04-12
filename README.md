# Auto Typer

## Overview
Auto Typer is a desktop application that simulates realistic human typing behavior. It lets you automatically type text content into any application while mimicking natural typing patterns including random pauses, occasional typos, and text revisions.

![image](https://github.com/user-attachments/assets/f8782c00-bde1-45ab-9537-5adcdc684fc4)


## Features
- **Realistic Typing Simulation**: Mimics human typing with customizable delays, typos, and editing behavior
- **Text Editor**: Built-in editor for creating or modifying text to be typed
- **File Management**: Open and save text files directly within the application
- **Customizable Settings**: Adjust typing speed, typo frequency, deletion chance, and pause behavior
- **Modern UI**: Clean, intuitive interface with tabbed organization
- **Emergency Stop**: Press ESC at any time to abort the typing process

## Installation

### Requirements
- Python 3.6 or higher
- Required Python packages:
  - pyautogui
  - Pillow (PIL)
  - keyboard

### Setup
1. Clone or download this repository
2. Install required packages:
   ```
   pip install pyautogui pillow keyboard
   ```
3. Run the application:
   ```
   python auto_typer.py
   ```

## Usage

### Basic Operation
1. Open the application
2. Either load a text file using the "Browse" button or type content directly in the editor
3. Click "Start Typing"
4. Quickly click into your target application (e.g., Word, Notepad, browser)
5. The application will automatically type the text with realistic human behavior
6. Press ESC at any time to stop the typing process

### Customizing Typing Behavior
Navigate to the "Options" tab to adjust:
- **Delay between words**: Controls typing speed (0.1-2.0 seconds)
- **Typo Chance**: Controls how often a typo is made and then corrected (0-20%)
- **Delete Chance**: Controls how often text is deleted and retyped (0-30%)
- **Pause Chance**: Controls frequency of natural pauses in typing (0-30%)

## Tips for Best Results
- Always have your target application open and focused before starting the typing process
- For longer texts, consider breaking them into smaller chunks
- Test with shorter texts first to find your preferred settings
- Make sure your cursor is correctly positioned in the target application
- Use the ESC key to stop typing at any time

## Keyboard Shortcuts
- **ESC**: Stop the typing process
- **Ctrl+S**: Save the current text
- **Ctrl+O**: Open a file
- **Ctrl+N**: Clear the editor

## Troubleshooting
- If typing doesn't start, make sure you clicked into the target application within the 3-second countdown
- If typing appears erratic, try reducing the typing speed by increasing the delay value
- Make sure the target application can receive text input and is not in protected or read-only mode

## License
This software is provided "as is" without warranty of any kind.

## Credits
Developed by Jfreaky
