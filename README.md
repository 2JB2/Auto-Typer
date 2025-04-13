# Auto Typer

![image](https://github.com/user-attachments/assets/1e37494c-866c-438c-8d12-71cfff659709)

## Overview

Auto Typer is a powerful, customizable tool designed to simulate realistic human typing behavior. It allows you to automatically type text from files or the built-in editor into any application with adjustable typing characteristics like speed, typos, and natural pauses.

## Features

- **Realistic Typing Simulation**: Adjustable typing speed, typo correction, pausing, and deletion behavior
- **Intuitive Interface**: Clean, modern UI with both light and dark modes
- **Built-in Text Editor**: Edit your content directly within the application
- **Preview Mode**: Test your typing settings before deploying them
- **Configurable Hotkeys**: Customize keyboard shortcuts for common actions
- **Session Statistics**: View performance metrics after each typing session
- **Typing Behavior Presets**: Choose from pre-configured typing behaviors or create custom ones

## Installation

### Requirements
- Python 3.6 or higher
- Required Python packages:
  - pyautogui
  - keyboard
  - Pillow (PIL)

### Setup Instructions

1. Clone or download this repository
2. Install required packages:
   ```
   pip install pyautogui keyboard pillow
   ```
3. Run the application:
   ```
   python autotyper.py
   ```

## Usage Guide

### Getting Started

1. Launch Auto Typer
2. Load text content using one of these methods:
   - Type directly in the editor
   - Click "Browse" to load from a text file
3. Adjust typing behavior settings in the "Options" tab
4. Click "Preview Typing" to test your settings
5. When ready, click "Start Typing"
6. Focus on your target application within 3 seconds
7. Press the configured hotkey (default: ESC) to stop typing

### Typing Behavior Settings

| Setting | Description |
|---------|-------------|
| Delay between words | Time between typing each word (in seconds) |
| Typo Chance | Probability of making and correcting typos |
| Delete Chance | Probability of deleting and retyping text |
| Pause Chance | Probability of natural pauses during typing |
| Stop Hotkey | Key to stop typing (e.g., 'esc', 'f1') |

### Presets

Choose from built-in typing behavior presets:
- **Fast Typist**: Quick typing with minimal errors
- **Beginner**: Slower typing with frequent corrections
- **Professional**: Moderate speed with occasional corrections
- **Custom**: Your custom settings

### Keyboard Shortcuts

| Action | Default Shortcut |
|--------|------------------|
| Save File | Ctrl+S |
| Open File | Ctrl+O |
| Clear Editor | Ctrl+N |
| Stop Typing | ESC (configurable) |

## Best Practices

- Open the target application before starting Auto Typer
- Position your cursor correctly before initiating typing
- Break long texts into smaller sections for better control
- Use the Preview feature to test settings before actual use
- Save frequently used configurations

## Important Notes

⚠️ **Use Responsibly**: Auto Typer is designed for legitimate purposes. Misuse for spamming, circumventing anti-cheat systems, or any unauthorized automation may violate terms of service agreements.

## Troubleshooting

- **Typing not working**: Ensure target application is in focus and accepting text input
- **Hot keys not responding**: Verify there are no conflicts with other applications
- **Unexpected behavior**: Try resetting to default settings in the Options tab

## License
Made By the one and only Jfreaky
