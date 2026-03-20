# 🖋️ YOWO: You Only Write Once

**YOWO** is a handwriting synthesis tool built for people who hate manual paperwork. By providing just **10 samples per character**, you can generate realistic, lifelike handwritten documents from any digital text. Stop the repetitive strain and let your samples do the heavy lifting.

---

## 🚀 Quick Start

### 1. Install Dependencies
This project uses **Pillow** for image processing. You can install it via `pip` or use `uv` for faster dependency management.

```bash
# Using pip
pip install pillow==12.1.1

# Or using uv (recommended)
uv sync
```

### 2. Configure Your Environment
Add the following to your shell configuration file (`~/.bashrc` or `~/.zshrc`) to run the generator from anywhere:

```bash
# Path to the cloned repository
export HAND_GEN_DIR="$HOME/<PATH TO PROJECT>"

# Alias for easy access (Choose one)
alias handwriting_gen="uv run --project $HAND_GEN_DIR $HAND_GEN_DIR/main.py"
# OR
alias handwriting_gen="python $HAND_GEN_DIR/main.py"
```

---

## 🛠️ Usage

To generate a handwritten document, point the script to your **character spritesheet** and the **text file** you want to "write."

```bash
handwriting_gen --sheet $HAND_GEN_DIR/handwriting_spritesheet00.png <input.txt>
```

### Spritesheet Requirements
* **Variety:** Ensure you have 10 versions of each character for natural-looking variance.
* **Format:** Transparent PNGs generally work best for layering on digital "paper" backgrounds.

---

## 💡 Why YOWO?
* **Authentic Variance:** By cycling through 10 unique samples per letter, YOWO avoids the "robotic" look of standard handwriting fonts.
* **Efficiency:** You provide the DNA of your handwriting once; the tool clones it forever.
* **Minimalist:** No heavy machine learning frameworks—just clean image processing.

---

**Would you like me to create a "Tips for Best Results" section to explain how users should format their spritesheet?**
