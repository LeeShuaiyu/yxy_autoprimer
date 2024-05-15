
# Primer Design Tool

## Introduction

**Primer Design Tool** is a small tool for designing PCR primers. Users can input a DNA sequence and set primer design parameters. The tool will automatically generate primers that meet the specified conditions and display the results in a text box. The generated primers will also be highlighted in the input DNA sequence.

This tool was developed by **yangxinyue** and **lsy**, inspired by the Nature article [Self-driving laboratories to autonomously navigate the protein fitness landscape](https://www.nature.com/articles/s41586-019-1405-3). While this tool is far from achieving fully automated experimental design, it is a good starting point.

## Installation

Make sure your system has Python 3 and pip installed. Then follow these steps:

1. Clone or download this project.
2. Navigate to the project root directory.
3. Create and activate a virtual environment (optional but recommended).

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4. Install the required dependencies.

```bash
pip install -r requirements.txt
```

5. Use PyInstaller to package the script as an executable file.

```bash
pyinstaller --onefile --windowed --noconfirm maker.py
```

The generated EXE file will be located in the `dist` directory.

## Usage

1. Run `maker.exe`.
2. Enter your DNA sequence in the "Enter Sequence" text box.
3. Enter or keep the default parameter values:
   - `PRIMER_MAX_POLY_X`: Maximum allowable consecutive identical bases (default: 2).
   - `PRIMER_OPT_SIZE`: Optimal primer length (default: 20).
4. Click the "Submit" button.
5. The tool will automatically design primers and display them in the results box. When you drag to select the generated primer content, the corresponding content in the input template will also be selected and highlighted.

## Parameter Description

- `PRIMER_OPT_SIZE`: Optimal primer length, default is 20. Typically between 18 and 25 bases; too short or too long can affect PCR efficiency.
- `PRIMER_PICK_INTERNAL_OLIGO`: Whether to pick internal oligos, 0 means no, default is 0.
- `PRIMER_INTERNAL_OPT_SIZE`: Optimal length of internal primers, default is 20.
- `PRIMER_INTERNAL_MIN_SIZE`: Minimum length of internal primers, default is 18.
- `PRIMER_INTERNAL_MAX_SIZE`: Maximum length of internal primers, default is 25.
- `PRIMER_INTERNAL_OPT_TM`: Optimal annealing temperature of internal primers, default is 60.0°C.
- `PRIMER_INTERNAL_MIN_TM`: Minimum annealing temperature of internal primers, default is 57.0°C.
- `PRIMER_INTERNAL_MAX_TM`: Maximum annealing temperature of internal primers, default is 63.0°C.
- `PRIMER_INTERNAL_MAX_SELF_END`: Maximum self-complementary end of internal primers, default is 8.
- `PRIMER_MIN_SIZE`: Minimum primer length, default is 18.
- `PRIMER_MAX_SIZE`: Maximum primer length, default is 25.
- `PRIMER_OPT_TM`: Optimal annealing temperature of primers, default is 60.0°C.
- `PRIMER_MIN_TM`: Minimum annealing temperature of primers, default is 57.0°C.
- `PRIMER_MAX_TM`: Maximum annealing temperature of primers, default is 63.0°C.
- `PRIMER_MAX_POLY_X`: Maximum allowable consecutive identical bases, default is 2. Long runs of identical bases can lead to secondary structure and non-specific binding.
- `PRIMER_SALT_MONOVALENT`: Monovalent salt concentration, default is 50.0 mM.
- `PRIMER_DNA_CONC`: DNA concentration, default is 50.0 nM.
- `PRIMER_PRODUCT_SIZE_RANGE`: Product size range, default is [[100, 300]].

## Developers

This tool was developed by **yangxinyue** and **lsy**, inspired by the Nature article [Self-driving laboratories to autonomously navigate the protein fitness landscape](https://www.nature.com/articles/s41586-019-1405-3). While this tool is far from achieving fully automated experimental design, it is a good starting point.

## License

This project is licensed under the MIT License. For more details, please refer to the LICENSE file.
