#  Assessing the Impacts of Falling Ice Radiative Effects (FIREs) on the Seasonal Variation of Land Surface Properties Replication code

This repository contains replication code for [Kisembe et al. (2024)](https://doi.org/10.1029/2024JD040991) in the *Journal of Geophysical Research: Atmospheres*

This includes the code necessary to reproduce all main text and supplementary figures. This code is to be used in conjunction with the replication data at [doi.org/10.5281/zenodo.8092600](https://zenodo.org/records/10476872).


# Motivation

Coupled global climate models (GCMs) are widely used to study interactions between the atmosphere and the land surface. However, uncertainties remain in how these models represent clouds and frozen hydrometeors, including cloud fraction, cloud hydrometeor mass, falling hydrometeors (e.g., snow), and their radiative impacts on surface energy and hydrological processes.

Previous studies have shown that most models participating in the Coupled Model Intercomparison Project Phase 5 (CMIP5) did not include the radiative effects of falling ice (FIREs). Instead, these models accounted only for the radiative effects of cloud ice. In reality, however, radiation interacts with all frozen hydrometeors, including falling snow. 

The omission of FIREs in climate models may influence the simulated surface radiative budget and, consequently, affect land surface temperature and other surface processes. Such discrepancies in present-day simulations may also influence the reliability of future climate projections.

Following previous work by [Li et al. (2016)](https://doi.org/10.1002/2016JD025175), we investigate the impacts of FIREs on land surface properties using a pair of sensitivity experiments using the National Center for Atmospheric Research (NCAR) Community Earth System Model Version 1 (CESM1) in fully coupled modes with FIREs turned on and off.

The schematic below illustrates cloud-precipitation-radiation interactions in the **REAL WORLD** compared to their representation in **CLIMATE MODELS**.

![FIRE schematic](FIRES_Schemantic.jpg)


## Other Notes
For questions, please reach out to @jessekisembe Jesse Kisembe.
