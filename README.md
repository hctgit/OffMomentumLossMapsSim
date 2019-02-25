# Off-Momentum Lossmaps Simulation
This repository contains the basic tools and files to simulate off-momentum loss maps using SixTrack in two different scenarios:

  1) Off-momentum losses at the start of the ramp
  2) Off-momentum cleaning

In each scenario, there are two ways of performing the simulation:

  1) Using DYNK module for energy or RF frequency trim.
  2) Using a pencil beam directly sample at the momentum primary collimator.

## Files included in the repositories

  - clean_input: contains lattice related input
    - fort.2: actual lattice. Notice that accelerating cavities (elements acsca) are included and set with non-zero parameters. If cavities are not included in fort.2 the ramp or frequency trim would not work. If you need to include them you need to generate againg the file fort.2 from MADX including the "cavall" argument when executing the sixtrack conversion.
    - fort.3: the tracking option files. It must include the collimation block and the DYNK module for triming the parameters.
    - CollDB: Collimator Database
    - CollPositon: Collimator position file
    - Survey: Survey file.
  - analysis: contains the basic analysis Python scripts for postprocessing and generating the lossmaps 
    - lossmap.py: generates the loss map.
    - LMevo.py: plots the evolution of losses in both TCPs (IR3 and IR7) as a function of the frequency shift.
  - sixtrack_batch.sh: submission script
  - htcondor.sub: submission script options

## Instructions for running simulations in different scenarios

### 1.1 Start of the ramp using DYNK
  - Clone StartRamp directory
  -
### 1.2 Start of the ramp using pencil beam

  - In order to perform the simulation correctly, the beam distribution must be sampled directly a the IR3 primary collimator. To do that one can cycle the optics to obtain a fort.2 with TCP.6 first element.
  - The beam distribution is externaly generated (script included) and the energy of the reference particle must be adjusted so the impact parameter on the TCP is about 1um.
  - Run the simulations normally as regular collimation simulations.
  - The analysis script is cycled in such a way that the lossmap starts at the usual location (IP1).

### 2.1 Off-momentum cleaning using DYNK

### 2.2 Off-momentum cleaning using pencil beam

  - In order to perform the simulation correctly, the beam distribution must be sampled directly a the IR3 primary collimator. To do that one can cycle the optics to obtain a fort.2 with TCP.6 first element.
  - The beam distribution is externaly generated (script included) and the energy of the reference particle must be adjusted so the impact parameter on the TCP is about 1um.
  - Run the simulations normally as regular collimation simulations.
  - The analysis script is cycled in such a way that the lossmap starts at the usual location (IP1).
