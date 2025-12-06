"""
Color Tester for Inverted Trust Game
=====================================
Click elements to select | Drag RGB sliders | H=HEX | P=Print | ESC=Quit
"""
from psychopy import visual, core, event
import os

# --- Config ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COIN_PATH = os.path.join(SCRIPT_DIR, 'img', 'Coins')

# Layout
TOKEN_SIZE, TOKEN_SPACING = 30, 5
TOTAL_TOKENS, HIGH_COUNT = 20, 12
SLIDER_WIDTH, SLIDER_HEIGHT = 200, 25

# --- Colors ---
def hex_to_rgb(h): return [int(h.lstrip('#')[i:i+2], 16) for i in (0,2,4)]
def rgb_to_hex(r,g,b): return f'#{r:02x}{g:02x}{b:02x}'

colors = {
    'high': hex_to_rgb('#004aa9'),  # Blue
    'low': hex_to_rgb('#a68400'),   # Gold
    'yes': hex_to_rgb('#480069'),   # Purple
    'no': hex_to_rgb('#554643'),    # Brown/gray
}
btn_text = 'white'
selected = 'high'

NAMES = {'high': 'HIGH Squares', 'low': 'LOW Squares', 'yes': 'YES Button', 'no': 'NO Button', 'text': 'Button Text'}

def get_hex(): return {k: rgb_to_hex(*v) for k,v in colors.items()} | {'text': btn_text}

def load_coin(win, n, x, y):
    path = os.path.join(COIN_PATH, f'Coins_{n}.jpg')
    if not os.path.exists(path): return None
    img = visual.ImageStim(win, image=path, units='pix')
    scale = 115 / img.size[1]
    img.size = (img.size[0] * scale, 115)
    img.pos = (x, y + 57.5)
    return img

def draw_sliders(win, mouse_pos, slider_x):
    rgb = colors[selected]
    visual.TextStim(win, f"Edit: {NAMES[selected]}", color='white', height=18, pos=[slider_x, 240], bold=True).draw()

    for i, (ch, col) in enumerate(zip('RGB', ['red','green','blue'])):
        y = 200 - i*40
        bounds = (slider_x - SLIDER_WIDTH/2, slider_x + SLIDER_WIDTH/2, y - SLIDER_HEIGHT/2, y + SLIDER_HEIGHT/2)

        visual.Rect(win, width=SLIDER_WIDTH, height=SLIDER_HEIGHT, fillColor='#333', lineColor='white', pos=[slider_x, y]).draw()
        fill_w = (rgb[i]/255) * SLIDER_WIDTH
        if fill_w > 0:
            visual.Rect(win, width=fill_w, height=SLIDER_HEIGHT-4, fillColor=col, pos=[slider_x - SLIDER_WIDTH/2 + fill_w/2, y]).draw()
        visual.Rect(win, width=4, height=SLIDER_HEIGHT+2, fillColor='white', pos=[slider_x - SLIDER_WIDTH/2 + fill_w, y]).draw()
        visual.TextStim(win, f"{ch}:", color='white', height=16, pos=[slider_x - SLIDER_WIDTH/2 - 25, y]).draw()
        visual.TextStim(win, f"{rgb[i]}", color='white', height=16, pos=[slider_x + SLIDER_WIDTH/2 + 30, y]).draw()

    visual.TextStim(win, f"HEX: {rgb_to_hex(*rgb)}", color='cyan', height=16, pos=[slider_x, 80]).draw()
    return [(slider_x - SLIDER_WIDTH/2, slider_x + SLIDER_WIDTH/2, 200-i*40 - SLIDER_HEIGHT/2, 200-i*40 + SLIDER_HEIGHT/2) for i in range(3)]

def draw_display(win, mouse_pos, center_x, bounds):
    hex_cols = get_hex()

    # Token positions
    total_w = TOTAL_TOKENS * (TOKEN_SIZE + TOKEN_SPACING)
    positions = [center_x - total_w/2 + TOKEN_SIZE/2 + i*(TOKEN_SIZE + TOKEN_SPACING) for i in range(TOTAL_TOKENS)]
    high_pos, low_pos = positions[:HIGH_COUNT], positions[HIGH_COUNT:]
    high_cx, low_cx = sum(high_pos)/len(high_pos), sum(low_pos)/len(low_pos)

    squares_y, label_y, coin_y = -50, 5, 30

    # Bounds for click detection
    bounds['high'] = (high_pos[0]-TOKEN_SIZE, high_pos[-1]+TOKEN_SIZE, squares_y-TOKEN_SIZE, coin_y+115)
    bounds['low'] = (low_pos[0]-TOKEN_SIZE, low_pos[-1]+TOKEN_SIZE, squares_y-TOKEN_SIZE, coin_y+115)

    # Draw HIGH section
    coin = load_coin(win, 18, high_cx, coin_y)
    if coin: coin.draw()
    box_col = 'yellow' if selected=='high' else hex_cols['high']
    visual.Rect(win, width=100, height=35, fillColor='black', lineColor=box_col, lineWidth=4 if selected=='high' else 3, pos=[high_cx, label_y]).draw()
    visual.TextStim(win, "18 tokens", color='white', height=24, pos=[high_cx, label_y]).draw()
    for x in high_pos:
        visual.Rect(win, width=TOKEN_SIZE, height=TOKEN_SIZE, fillColor=hex_cols['high'], pos=[x, squares_y]).draw()
    visual.TextStim(win, "HIGH", color='yellow' if selected=='high' else hex_cols['high'], height=14, pos=[high_cx, coin_y+125]).draw()

    # Draw LOW section
    coin = load_coin(win, 5, low_cx, coin_y)
    if coin: coin.draw()
    box_col = 'yellow' if selected=='low' else hex_cols['low']
    visual.Rect(win, width=100, height=35, fillColor='black', lineColor=box_col, lineWidth=4 if selected=='low' else 3, pos=[low_cx, label_y]).draw()
    visual.TextStim(win, "5 tokens", color='white', height=24, pos=[low_cx, label_y]).draw()
    for x in low_pos:
        visual.Rect(win, width=TOKEN_SIZE, height=TOKEN_SIZE, fillColor=hex_cols['low'], pos=[x, squares_y]).draw()
    visual.TextStim(win, "LOW", color='yellow' if selected=='low' else hex_cols['low'], height=14, pos=[low_cx, coin_y+125]).draw()

    # Buttons
    btn_y, btn_w, btn_h = -220, 140, 55
    bounds['yes'] = (center_x-120-btn_w/2, center_x-120+btn_w/2, btn_y-btn_h/2-20, btn_y+btn_h/2+20)
    bounds['no'] = (center_x+120-btn_w/2, center_x+120+btn_w/2, btn_y-btn_h/2-20, btn_y+btn_h/2+20)

    for name, bx in [('yes', center_x-120), ('no', center_x+120)]:
        sel = selected == name
        visual.Rect(win, width=btn_w, height=btn_h, fillColor=hex_cols[name], lineColor='yellow' if sel else None, lineWidth=3 if sel else 0, pos=[bx, btn_y]).draw()
        visual.TextStim(win, name.capitalize(), color=hex_cols['text'], height=22, pos=[bx, btn_y]).draw()
        visual.TextStim(win, name.upper(), color='yellow' if sel else hex_cols[name], height=13, pos=[bx, btn_y-45]).draw()

    # Text toggle
    toggle_y = btn_y - 80
    bounds['text'] = (center_x-60, center_x+60, toggle_y-15, toggle_y+15)
    visual.Rect(win, width=120, height=30, fillColor='#222', lineColor='yellow' if selected=='text' else 'gray', pos=[center_x, toggle_y]).draw()
    visual.TextStim(win, f"Text: {hex_cols['text'].upper()}", color='yellow' if selected=='text' else 'white', height=14, pos=[center_x, toggle_y]).draw()

def print_colors():
    c = get_hex()
    print(f"\n{'='*60}\nCOLORS for style_config.py:\n{'='*60}")
    print(f"'token_schemes': [\n  {{'high': '{c['high']}', 'low': '{c['low']}'}},\n  {{'high': '{c['low']}', 'low': '{c['high']}'}}\n],")
    print(f"'button_yes': '{c['yes']}',\n'button_no': '{c['no']}',\n# text: '{c['text']}'\n{'='*60}\n")

def hex_input(win):
    txt = ""
    while True:
        visual.Rect(win, width=300, height=80, fillColor='#222', lineColor='white', lineWidth=2, pos=[0,0]).draw()
        visual.TextStim(win, "Enter HEX (e.g. ff0000):", color='white', height=16, pos=[0, 20]).draw()
        visual.TextStim(win, f"#{txt}_", color='cyan', height=20, pos=[0, -10]).draw()
        win.flip()
        for k in event.waitKeys():
            if k == 'escape': return None
            if k == 'return' and len(txt) == 6:
                try: int(txt, 16); return f"#{txt}"
                except: pass
            if k == 'backspace': txt = txt[:-1]
            elif len(k) == 1 and k in '0123456789abcdef' and len(txt) < 6: txt += k

def main():
    global selected, btn_text

    win = visual.Window(fullscr=True, color='black', units='pix', allowGUI=True)
    mouse = event.Mouse(visible=True, win=win)
    h = win.size[1]

    center_x, slider_x = -150, 450
    bounds = {}
    was_pressed = False

    print(f"\n{'='*40}\nCOLOR TESTER\nClick elements | Drag sliders | H=HEX | P=Print | ESC=Quit\n{'='*40}\n")

    while True:
        pos = mouse.getPos()
        pressed = mouse.getPressed()[0]

        # Click detection
        if was_pressed and not pressed:
            for name, (l,r,b,t) in bounds.items():
                if l <= pos[0] <= r and b <= pos[1] <= t:
                    if name == 'text':
                        btn_text = 'black' if btn_text == 'white' else 'white'
                    else:
                        selected = name
                    break

        # Slider drag
        if pressed:
            for i in range(3):
                y = 200 - i*40
                if slider_x - SLIDER_WIDTH/2 <= pos[0] <= slider_x + SLIDER_WIDTH/2 and y - SLIDER_HEIGHT/2 <= pos[1] <= y + SLIDER_HEIGHT/2:
                    colors[selected][i] = int(max(0, min(255, (pos[0] - (slider_x - SLIDER_WIDTH/2)) / SLIDER_WIDTH * 255)))

        was_pressed = pressed

        # Draw
        visual.TextStim(win, "COLOR TESTER", color='white', height=24, pos=[0, h/2-40], bold=True).draw()
        visual.TextStim(win, "Click element | H=HEX | P=Print | ESC=Quit", color='gray', height=13, pos=[0, h/2-70]).draw()

        draw_display(win, pos, center_x, bounds)
        draw_sliders(win, pos, slider_x)

        # Recap bar with color swatches (fixed position below buttons)
        c = get_hex()
        recap_y = -380  # Fixed position below the text toggle
        visual.Rect(win, width=920, height=50, fillColor='#222', lineColor='white', lineWidth=2, pos=[center_x, recap_y]).draw()

        # Draw color swatches with labels
        swatch_size = 22
        items = [('HIGH', c['high']), ('LOW', c['low']), ('YES', c['yes']), ('NO', c['no'])]
        spacing = 170
        start_x = center_x - 280
        for i, (label, hex_col) in enumerate(items):
            x = start_x + i * spacing
            visual.Rect(win, width=swatch_size, height=swatch_size, fillColor=hex_col, lineColor='white', pos=[x - 35, recap_y]).draw()
            visual.TextStim(win, f"{label}: {hex_col}", color='white', height=13, pos=[x + 25, recap_y]).draw()
        # Text color at the end
        visual.TextStim(win, f"Text: {c['text']}", color='white', height=13, pos=[start_x + 4 * spacing + 20, recap_y]).draw()

        win.flip()

        # Keys
        for k in event.getKeys():
            if k == 'escape':
                print_colors()
                win.close()
                core.quit()
            elif k == 'h':
                new = hex_input(win)
                if new: colors[selected] = hex_to_rgb(new)
            elif k == 'p':
                print_colors()

        core.wait(0.016)

if __name__ == '__main__':
    main()
