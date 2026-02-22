📂 Local AI-Media-Organizer (Vision Edition)
An automated, privacy-first tool that uses Local Vision LLMs to intelligently rename, categorize, and backup your digital clutter. It "looks" at your images, PDFs, and even video clips to determine the most descriptive filename.

✨ Key Features
Local & Private: No data leaves your machine. Your personal files stay private.

Turbo Speed: Now powered by Moondream, a lightweight vision model optimized for speed on Apple Silicon and consumer hardware.

Multi-Media Support: - Images: PNG (with transparency fix), JPG, WebP.

Videos: MP4, MOV, AVI (extracts frames at the 1-second mark).

Documents: PDFs (analyzes the first page).

Smart Constraints: Filenames are sanitized and capped at 40 characters for clean file systems.

Flexible Organization: Choose between in-place renaming or automatic folder sorting using the --folder flag.

Safety First: Automatic original file backups and a Dry Run mode.

Audit Trail: Generates a rename_log.csv for easy tracking.

🚀 Getting Started

1. Prerequisites
   Python 3.9+

Ollama installed and running.

Download the Model:

2. Installation
3. Usage
   Perform a Dry Run (Recommended):
   See what the AI suggests without changing anything.

Live Rename (In-Place):
Renames files in their current folder and creates a backup of the originals.

Live Rename + Folder Organization:
Renames files and moves them into AI-generated category folders (e.g., /Finance, /Gaming).

🛠️ Command Line Arguments
📁 Folder Structure After Execution (with --folder)
⚠️ Technical Notes
Video Processing: The script uses OpenCV to jump 1 second into a video to bypass black intro frames/fades.

PNG Handling: Specifically handles RGBA transparency by flattening images onto a white background to prevent AI processing errors.

Sanitization: Automatically removes illegal characters (?, :, \*, etc.) and replaces spaces with underscores.

Limits: The filename is strictly truncated to 40 characters before the extension to ensure compatibility with all OS environments.

🛠️ Troubleshooting
If you encounter issues while running the organizer, check these common solutions:

1. "Ollama not found" or Connection Errors
   The Fix: Ensure the Ollama application is running. You should see the sheep icon in your menu bar (macOS).

Model Check: Run ollama list in your terminal to verify moondream is downloaded. If not, run ollama pull moondream.

2. OpenCV Errors (cv2)
   Error: ImportError: libGL.so.1: cannot open shared object file

The Fix: This usually happens on Linux. Install the additional dependencies:

Mac Users: If you get a "Camera Access" popup, it is just macOS reacting to the OpenCV library. The script only reads file data, it does not use your webcam.

3. "File temp_fast_preview.jpg does not exist"
   The Cause: This happens if the script fails to extract a frame from a video or page from a PDF.

The Fix: Ensure your video isn't corrupted and can play in a standard player (like VLC or QuickTime). If the video is extremely short (under 1 second), the script might miss the frame.

4. Slow Performance
   Memory: Ensure you aren't running heavy apps (like 50+ Chrome tabs) while processing. Local AI uses Unified Memory on Mac.

Power: On MacBooks, performance is significantly faster when the laptop is plugged into power.

🌟 Pro-Tip for Peering into the "Brain"
If you want to see exactly what the AI is seeing when it makes a mistake, look for the temp_fast_preview.jpg that appears briefly in your folder during the "Analyzing" step. You can comment out the line os.remove(temp_image) in the script to keep that file and inspect it.

⚖️ License
This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the LICENSE file for details.
