# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based Instagram Reels video editor built with Streamlit. The application provides a web interface for creating 9:16 aspect ratio videos by combining background images, logos, overlays, scrolling captions, and audio.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Start the Streamlit development server
streamlit run video_editor.py
```

The application will automatically open in your browser at `http://localhost:8501`.

### Testing
This project currently has no automated test suite. Testing is done manually through the web interface.

## Architecture

The application is structured as a single-file Streamlit app (`video_editor.py`) with the following key components:

### Core Functions
- `create_base_clip()`: Creates the base video from background images with looping support
- `add_overlay_image()`: Adds logo and overlay images with positioning and opacity controls
- `add_scrolling_caption()`: Implements scrolling text effect for captions
- `add_static_caption_for_preview()`: Static caption rendering for preview
- `generate_final_video()`: Main orchestration function that combines all elements
- `generate_preview_frame()`: Creates real-time preview frames

### UI Layout
The interface uses a three-column layout:
1. **Left Column**: File uploads and controls
2. **Middle Column**: Configuration panels (expandable sections)
3. **Right Column**: Real-time preview

### Key Features
- **Numerical Image Sorting**: Images are automatically sorted by numeric prefixes (01-, 02-, etc.)
- **Reactive Preview**: Preview updates automatically when controls are modified
- **Multi-format Support**: Handles JPG/PNG images, MP3/WAV audio, and PNG overlays
- **Video Looping**: Automatically loops image sequences to match total duration

### Dependencies
- `streamlit`: Web UI framework
- `moviepy==1.0.3`: Video processing (pinned version for stability)
- `Pillow`: Image manipulation
- `numpy`: Numerical operations

## File Structure
```
instagram_reels_editor/
├── video_editor.py        # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .venv/                # Virtual environment
└── *.mp4                # Generated video files
```

## Development Notes

- The application uses MoviePy 1.0.3 specifically for stability
- Preview uses 0.5x scale for performance optimization
- Default font is hardcoded to 'Liberation-Sans-Bold' for caption consistency
- Video output format is MP4 with libx264 codec and AAC audio
- The UI state is managed through Streamlit's session state for filename persistence