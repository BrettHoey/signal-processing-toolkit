# Signal Processing Toolkit

An interactive Python tool for generating, filtering, and analyzing signals.
Includes a GUI (Tkinter) and command-line version.

## Features
- Synthetic signal generation (sine waves + noise)
- Moving average and Butterworth filtering
- FFT spectrum analysis
- Interactive GUI with parameter inputs
- Automatic graph saving with timestamps

## How to Run
1. Clone the repo:

git clone https://github.com/bretthoey/signal-processing-toolkit.git


2. Create a virtual environment:
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows

3. Install dependencies:
pip install numpy matplotlib scipy

4. Run the GUI:
python signal_gui.py


## Example Outputs
Graphs are saved automatically to the `plots/` folder.