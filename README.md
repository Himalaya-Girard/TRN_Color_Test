# TRN_Color_Test

## Color Tester - Inverted Trust Game

Interactive to test colors for the experiment.

## Requirements

```bash
pip install psychopy
```

## Usage

```bash
python run_color_test.py
```

## Controls

- **Click** on element to select it
- **Drag** RGB sliders to change color
- **H** = Enter HEX code directly
- **P** = Print colors to console
- **ESC** = Quit

## Output

Press P to get code for `style_config.py`:

```python
'token_schemes': [
  {'high': '#xxxxxx', 'low': '#xxxxxx'},
  {'high': '#xxxxxx', 'low': '#xxxxxx'}
],
'button_yes': '#xxxxxx',
'button_no': '#xxxxxx',
```

## Files

```
ColorTester_Standalone/
├── run_color_test.py
├── README.md
└── img/Coins/
    ├── Coins_5.jpg
    └── Coins_18.jpg
```
