# Off-Momentum Lossmaps Simulation
This repository contains the basic tools and files to simulate off-momentum loss maps using SixTrack in two different scenarios:

  1) Off-momentum losses at the start of the ramp
  2) Off-momentum cleaning

In each scenario, there are two ways of performing the simulation:

  1) Using DYNK module for energy or RF frequency trim.
  2) Using a pencil beam directly sample at the momentum primary collimator.

## Files included in the repository

### Start of the ramp

  - clean_input: contains lattice related input
    - fort.2: actual lattice. Notice that accelerating cavities (elements acsca) are included and set with non-zero parameters. If cavities are not included in fort.2 the ramp or frequency trim would not work. If you need to include them you need to generate againg the file fort.2 from MADX including the "cavall" argument when executing the sixtrack conversion.
    - fort.3: the tracking option files. It must include the collimation block and the DYNK module for triming the parameters.
    - CollDB: Collimator Database
    - CollPositon: Collimator position file
    - Survey: Survey file.
    -
    
### Cleaning
