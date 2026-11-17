# Flash Project Extractor
Simple Python script to pull .swf files out of Flash Projector .exe binaries.
## How It Works

Standard Flash Projectors bundle the Flash Player runtime and your `.swf` movie together by appending the raw SWF bytes and an 8-byte footer (`0xFA123456` + file size) to the end of the executable. This script looks for that signature, verifies the SWF header (`FWS`, `CWS`, or `ZWS`), and extracts the clean `.swf` payload—even if the `.exe` was digitally signed afterward.

## Requirements

* Python 3.8+

## Usage

1. Download `extract.py` and drop it into the folder containing your Flash Projector `.exe` files.
2. Open a terminal in that folder and run: `python extract.py` or `python3 extract.py` on Linux and macOS.
