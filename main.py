import random
from PIL import Image, ImageFilter, ImageEnhance

# --- 1. CONFIGURATION & REALISM VARIABLES ---

# Page Settings (A4 dimensions at ~150 DPI)
PAGE_WIDTH = 1240
PAGE_HEIGHT = 1754
MARGIN_TOP = 150
MARGIN_BOTTOM = 150
MARGIN_LEFT = 120
MARGIN_RIGHT = 120

# Spacing & Sizing
BASE_CHAR_SIZE = 45        # Base size to scale the 128x128 cells down to
LINE_HEIGHT = 80           # Vertical space between lines
WORD_SPACING = 35          # Space between words
CHAR_SPACING_BASE = -5     # Base space between letters (negative pulls them closer)

# Randomization / Imperfection Parameters
SIZE_VAR = 0.08            # Normal distribution: standard deviation for scaling (8%)
POS_X_VAR = 1.5            # Normal distribution: horizontal jitter (pixels)
POS_Y_VAR = 2.5            # Normal distribution: vertical baseline jitter (pixels)
ROTATION_RANGE = (-3, 3)   # Uniform distribution: min/max rotation (degrees)
BLUR_RANGE = (0.0, 0.0)    # Uniform distribution: Gaussian blur radius
OPACITY_RANGE = (0.6, 1.0) # Uniform distribution: Ink pressure/opacity (0.0 to 1.0)

# Sprite Sheet Info
CHARACTERS = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,?!-'()\"")
SAMPLES_PER_CHAR = 10
CELL_SIZE = 128

# --- 2. SCRIPT LOGIC ---

def load_spritesheet(path):
    """Loads the sprite sheet and returns a dictionary of character images."""
    try:
        sheet = Image.open(path).convert("RGBA")
    except FileNotFoundError:
        print(f"Error: Could not find '{path}'.")
        exit()

    sprites = {}
    for row, char in enumerate(CHARACTERS):
        sprites[char] = []
        for col in range(SAMPLES_PER_CHAR):
            left = col * CELL_SIZE
            top = row * CELL_SIZE
            # Crop the specific sample out of the grid
            img = sheet.crop((left, top, left + CELL_SIZE, top + CELL_SIZE))
            sprites[char].append(img)
    return sprites

def create_page():
    """Creates a blank white page."""
    return Image.new("RGBA", (PAGE_WIDTH, PAGE_HEIGHT), (255, 255, 255, 255))

def generate_document(text, spritesheet_path, output_prefix="output_page"):
    sprites = load_spritesheet(spritesheet_path)
    
    pages = []
    current_page = create_page()
    
    x, y = MARGIN_LEFT, MARGIN_TOP
    
    # Simple word-wrapping logic
    words = text.replace('\n', ' \n ').split(' ')
    
    for word in words:
        if word == '\n':
            x = MARGIN_LEFT
            y += LINE_HEIGHT
            continue
            
        # Estimate word length to check for line wrapping
        estimated_width = len(word) * (BASE_CHAR_SIZE + CHAR_SPACING_BASE)
        if x + estimated_width > PAGE_WIDTH - MARGIN_RIGHT:
            x = MARGIN_LEFT
            y += LINE_HEIGHT
            
            # Check for page wrapping
            if y > PAGE_HEIGHT - MARGIN_BOTTOM:
                pages.append(current_page)
                current_page = create_page()
                y = MARGIN_TOP

        for char in word:
            if char not in sprites:
                continue # Skip unsupported characters
                
            # Pick a random sample for this character
            char_img = random.choice(sprites[char]).copy()
            
            # --- APPLY REALISM ---
            
            # 1. Scale/Size (Normal Distribution)
            scale = random.gauss(1.0, SIZE_VAR)
            new_size = int(CELL_SIZE * (BASE_CHAR_SIZE / CELL_SIZE) * scale)
            char_img = char_img.resize((new_size, new_size), Image.Resampling.LANCZOS)
            
            # 2. Rotation (Uniform Range)
            angle = random.uniform(*ROTATION_RANGE)
            char_img = char_img.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
            
            # 3. Opacity / Ink Pressure
            alpha = char_img.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(random.uniform(*OPACITY_RANGE))
            char_img.putalpha(alpha)
            
            # 4. Blur
            blur_amount = random.uniform(*BLUR_RANGE)
            if blur_amount > 0:
                char_img = char_img.filter(ImageFilter.GaussianBlur(blur_amount))
                
            # 5. Position Jitter (Normal Distribution)
            jitter_x = random.gauss(0, POS_X_VAR)
            jitter_y = random.gauss(0, POS_Y_VAR)
            
            # Calculate final paste coordinates
            # Offset y by (BASE_CHAR_SIZE - new_size) to keep bottoms aligned
            paste_x = int(x + jitter_x)
            paste_y = int(y + jitter_y + (BASE_CHAR_SIZE - char_img.height) / 2)
            
            # Paste onto the page using the character's alpha channel as a mask
            current_page.paste(char_img, (paste_x, paste_y), char_img)
            
            # Advance X for the next character, adding slight random spacing
            x += new_size + CHAR_SPACING_BASE + random.gauss(0, 1.0)
            
        # Add space after word
        x += WORD_SPACING + random.gauss(0, 3.0)

    pages.append(current_page)
    
    # Save the pages
    for i, page in enumerate(pages):
        filename = f"{output_prefix}_{i+1}.png"
        # Convert back to RGB to save as standard PNG/JPG without transparency issues
        page.convert("RGB").save(filename)
        print(f"Saved {filename}")

# --- 3. RUN THE SCRIPT ---

sample_text = """Hello there! This is a test of the handwriting document generator.
It takes a sprite sheet, picks random samples, and applies Gaussian distributions to the layout.

Features include:
- Variable sizing and rotation.
- Simulated ink pressure.
- Micro-jitter on the X and Y axis.
- Very slight blurring for a natural, non-digital look!"""

if __name__ == "__main__":
    generate_document(sample_text, "handwriting_spritesheet.png")
