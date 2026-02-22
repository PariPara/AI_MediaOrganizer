```markdown
# 📂 Local AI-Media-Organizer (Vision Edition)

An automated, privacy-first tool that uses **Local Vision LLMs** to intelligently rename, categorize, and backup your digital clutter. It "looks" at your images, PDFs, and even video clips to determine the most descriptive filename.

## ✨ Key Features

* **Local & Private:** No data leaves your machine. Your personal files stay private.
* **Turbo Speed:** Powered by **Moondream**, a lightweight vision model optimized for speed on Apple Silicon and consumer hardware.
* **Multi-Media Support:** * **Images:** PNG (with transparency fix), JPG, WebP.
    * **Videos:** MP4, MOV, AVI (extracts frames at the 1-second mark).
    * **Documents:** PDFs (analyzes the first page).
* **Smart Constraints:** Filenames are sanitized and capped at **40 characters** for clean file systems.
* **Flexible Organization:** Choose between in-place renaming or automatic folder sorting using the `--folder` flag.
* **Safety First:** Automatic original file backups and a **Dry Run** mode.
* **Audit Trail:** Generates a `rename_log.csv` for easy tracking.

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.9+
* **Ollama** installed and running.
* **Download the Model:**
    ```bash
    ollama pull moondream
    ```

### 2. Installation
```bash
pip install ollama pydantic PyMuPDF Pillow opencv-python

```

### 3. Usage

**Perform a Dry Run (Recommended):**
See what the AI suggests without changing anything.

```bash
python3 organizer.py ./my_files

```

**Live Rename (In-Place):**
Renames files in their current folder and creates a backup of the originals.

```bash
python3 organizer.py ./my_files --live

```

**Live Rename + Folder Organization:**
Renames files and moves them into AI-generated category folders.

```bash
python3 organizer.py ./my_files --live --folder

```

---

## 🛠️ Command Line Arguments

| Argument | Description | Default |
| --- | --- | --- |
| `directory` | The target folder to process | (Required) |
| `--live` | Execute actual file moves/renames | `False` |
| `--folder` | Organize files into category subfolders | `False` |
| `--model` | Specify the Ollama model to use | `moondream` |

---

## 📁 Folder Structure After Execution (with --folder)

```text
/my_files
├── rename_log.csv           <-- Map of old names to new names
├── original_backups/        <-- Your untouched original files
├── Education/               <-- AI-created category
│   └── activate_office_steps.mp4
└── Lifestyle/               <-- AI-created category
    └── shoe_organization_tips.mp4

```

---

## ⚠️ Technical Notes

* **Video Processing:** Uses OpenCV to jump 1 second into a video to bypass black intro frames/fades.
* **PNG Handling:** Handles RGBA transparency by flattening images onto a white background.
* **Sanitization:** Automatically removes illegal characters (`?`, `:`, `*`, etc.) and replaces spaces with underscores.
* **Limits:** Filenames are strictly truncated to **40 characters** before the extension.

---

## 🛠️ Troubleshooting

### 1. "Ollama not found" or Connection Errors

* **The Fix:** Ensure the Ollama application is running. You should see the sheep icon in your menu bar (macOS).
* **Model Check:** Run `ollama list` to verify `moondream` is downloaded.

### 2. OpenCV Errors (cv2)

* **Linux Fix:** `sudo apt-get update && sudo apt-get install libgl1`
* **Mac Users:** If you get a "Camera Access" popup, it's just macOS reacting to the library. The script does **not** use your webcam.

### 3. "File temp_fast_preview.jpg does not exist"

* **The Cause:** Failure to extract a frame from a video or page from a PDF.
* **The Fix:** Ensure the file isn't corrupted and is at least 1 second long.

### 4. Slow Performance

* **Memory:** Close heavy apps (like Chrome) to free up **Unified Memory**.
* **Power:** MacBooks run AI models significantly faster when **plugged into power**.

---

## 🌟 Pro-Tip

To see what the AI "sees," look for the `temp_fast_preview.jpg` that appears briefly during analysis. You can comment out `os.remove(temp_image)` in the script to keep the file for inspection.

## ⚖️ License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

```

---

### How to use this:
1.  Open your code editor (VS Code, TextEdit, etc.).
2.  Create a new file and name it exactly `README.md`.
3.  Paste the code block above into it.
4.  When you upload this to GitHub, it will automatically render with beautiful headers, bold text, and code boxes.

Would you like me to help you set up a `.gitignore` file next so you don't accidentally upload your private backups to the public?

```
