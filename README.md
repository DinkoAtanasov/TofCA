# Time of Flight calibrator/analyser (*TofCA*)

The **TofCA** software is a Python tool which can be used 
to calibrate and do a basic plotting of spectra collected (or to be collected) 
with Multi Reflection Tim of Flight spectrometers.

Supported Acquisition data formats

1. **P7887**:

    + MCDWIN = \*.csv (parameters saved in \*.887)
    + MCDWIN = \*.asc (parameters saved in \*.887)

2. **MCS6A**

    + MPANT  = \*.mpa (parameters saved in \*.mpa)

3. **CSV (Two columns separated with a comma)**:

    + TextFile = \*.csv (first line is skipped)

4. **JYFL (Special export of ToF projection by JYFLTRAP)**:

    + JYFL = \*.txt 
## Dependencies

+ Python3\.X
+ Qt5 (installed through your python version as PyQt5)
+ pyqtgraph (for visualisation)

Checkout the GitLab repository for dEval using your CERN credentials:

```bash
cd /to/your/working/directory/
git clone https://github.com/DinkoAtanasov/TofCA
cd TofCA/
```

### Prerequisites

The software's python dependencies are summarized 
in *requirements.txt* file.
You can execute the following command to install them

```bash
python3 -m pip install -U -r requirements.txt
```

### ToF calculation/calibration
The file etc/constants.py defines the specific configuration 
for Time of Flight calculation. Adapt it to your needs. 

## Authors

Dinko Atanasov
