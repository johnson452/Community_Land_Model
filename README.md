# Community_Land_Model

Contributors: Kevin, Harry, Grant Date: 11/09/2022

# Code Documentation:

Preferred: RTD_Community_Land_Model.pdf

(Some issues with the website:
https://community-land-model.readthedocs.io/en/latest/DIAGNOSTICS.html)

# Run a sample script and diagnostics

Download the code:

> > git clone https://github.com/johnson452/Community_Land_Model

Then run the following code:

> > python3 EXAMPLES/input_script.py > OUTPUT/a.out

Running diagnostics

> > python3 DIAGNOSTICS/diagnostics.py > OUTPUT/b.out

this will save the plot outputs in the folder OUTPUT/PLOTS

Check the code successfully ran with

> > vim OUTPUT/a.out

# Verify a commit before pushing

Manual checks before committing

> > nox -s tests

and

> > pre-commit run -a
