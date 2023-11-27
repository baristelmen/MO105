<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Tensile test practical work (TP)</h3>

  <p align="center">
    Python scripts for controlling the machine and post-treatment of video data
    <br />
    <a href="https://github.com/baristelmen/TP-Traction-2023/archive/refs/heads/main.zip">Download</a>
    ·
    <a href="https://github.com/baristelmen/TP-Traction-2023/tree/main/examples">View Demo</a>
    ·
    <a href="https://github.com/baristelmen/TP-Traction-2023/issues">Report Bug</a>
    ·
    <a href="https://github.com/baristelmen/TP-Traction-2023/issues">Request Feature</a>
  </p>
</div>



# About this repository
This repo contains python scripts to assist you through your practical course. Currently, two main scripts are available.

| Name            | Definition                                                                                                                                                                                   |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| control_machine | This script will be used to control machine's cross-head displacement during tensile testing. It's a graphical user interface to control the machine using an Arduino based micro-controller |
| point_tracking  | This script can be used for post-treatment of recorded video during the tensile testing to obtain deformation on given points.                                                               |

As it's current state, it has been tested under Windows and Linux. **On MacOS, the GUI known to be buggy.**

---
<!-- GETTING STARTED -->
# Getting Started

The scripts for controlling the machine and post-treatment of video files requires a valid python installation and availability of python libraries. To facilitate the installation process and unifying the functionality, it's recommended to use **conda**.

Conda is an open source package management system and environment management system that runs on Windows, macOS, and Linux. Conda quickly installs, runs and updates packages and their dependencies. If you need a package that requires a different version of Python, you do not need to switch to a different environment manager, because conda is also an environment manager.

Conda is widely used in the scientific computing and data science communities due to its extensive package availability, environment management capabilities, and robust dependency resolution. It simplifies the process of setting up and managing software environments, making it easier to work on Python projects with different dependencies and configurations.

Anaconda contains huge pack of default libraries which we don't require at the moment. Therefore, we will install **miniconda** instead. Miniconda is a lightweight installer for Conda that includes only the essential components needed to run Conda. It provides a smaller footprint compared to the full Anaconda distribution, making it faster to download and install. Miniconda allows you to create and manage Python environments and install packages using the Conda package manager.

With Miniconda, you have the flexibility to set up custom Python environments tailored to your specific project requirements. You can create isolated environments with different versions of Python and install packages using Conda or pip, depending on your preference.

Miniconda provides the core functionality of Conda, including package management, dependency resolution, and environment management. It's a popular choice for those who prefer a lightweight installation and want more control over the packages and dependencies in their Python environments.

---

# Prerequisites

**Before going any further, please follow the instructions below to install and configure your environment**

To obtain miniconda, follow the instructions below;

1. Visit the Miniconda website at [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html).
2. Download the installer appropriate for your operating system.
3. Run the installer and follow the prompts to complete the installation.

### For Windows 10/11
It's recommended to use `Anaconda Powershell Prompt` or `Anaconda Prompt` to access `conda` functions. By default, if it's not added on the PATH, the system can't recognize the where to find `conda`. 

To verify the installation is passed correctly, open `Anaconda Powershell Prompt` or `Anaconda Prompt` run the following command:

`conda --version`

If the installation was successful, you should see the version of Conda installed on your system. 

Inside the repository, there is a file which is called `traction.yaml`. This file contains all the necessary libraries that is required to run scripts for both `control_machine` and `point_tracking`. Therefore, access `Anaconda Powershell Prompt` or `Anaconda Prompt` and type the following code for automatic installation of packages.

`conda env create --name traction-tp --file environment.yml`

By default, this file will create an environment which is called `traction-tp`. To run these scripts, these environment has to be activated. To do that, access `Anaconda Powershell Prompt` or `Anaconda Prompt` and type the following 

`conda activate traction-tp`

In case if you encounter any error, follow the `Manual installation instructions`

### For Linux (Ubuntu, Arch, Fedora, Centos etc.)
Once the miniconda is installed, if it's added to the path, it's automatically activated. Therefore, open a terminal and verify the accessibility and installation using;

`conda --version`

If the installation was successful, you should see the version of Conda installed on your system. 

Inside the repository, there is a file which is called `traction.yaml`. This file contains all the necessary libraries that is required to run scripts for both `control_machine` and `point_tracking`. Therefore, access `Anaconda Powershell Prompt` or `Anaconda Prompt` and type the following code for automatic installation of packages.

`conda env create --name traction --file environment.yml`

By default, this file will create an environment which is called `traction-tp`. To run these scripts, these environment has to be activated. To do that, access `Anaconda Powershell Prompt` or `Anaconda Prompt` and type the following 

`conda activate traction-tp`

In case if you encounter any error, follow the `Manual installation instructions`

### For MacOS (Including Intel and ARM based chips)

For MacOS, Once the miniconda is installed, if it's added to the path, it's automatically activated. Therefore, open a terminal and verify the accessibility and installation using;

`conda --version`

If the installation was successful, you should see the version of Conda installed on your system. Unfortunately, the automatic installation through `traction.yaml` file is known to be not working. Therefore, follow the manual installation below.

### Manual installation instructions

At some point, some configurations might require elevated prompt or some other interventions. Therefore, it's necessary to install everything from scratch manually. For each system (Windows, Linux or MacOS), open the terminal which has an access to `conda` and type the following;

* conda create -n traction-tp
* conda activate traction-tp
* conda install -c conda-forge pyserial opencv matplotlib pandas numpy scipy

These packages should be sufficient to run the programs. 

---
<!-- USAGE EXAMPLES -->
# Usage
To use the programs, inside the activated environment of conda type the following:

| Name            | Definition                                                                                                                                                                                   |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| control_machine | python combine_frames.py |
| point_tracking  | python Tracking_Video_ZNCC.py                                                               |

---



## Quick introduction to tensile testing
Tensile Testing is a form of tension testing and is a destructive engineering and materials science test whereby controlled tension is applied to a sample until it fully fails. It is widely used for material characterization and quality control in various industries, including engineering, manufacturing, and materials science.

A test sample is loaded in tension when it experiences opposing forces acting upon opposite faces both located on the same axis that attempt to pull the specimen apart. The test involves applying an axial force or axial displacement to a specimen while measuring its response in terms of;

* Force
* Displacement
* Strain (if an extensometer is used)

The setup for a tensile test consists of a specialized machine called a universal testing machine (UTM) or a tensile testing machine. This machine consists of a load frame, grips to hold the specimen, and a load cell or load sensor to measure the applied force. The grips securely hold the specimen, ensuring that it doesn't slip during the test.

To perform a tensile test, a sample of the material is prepared in a specific geometry, typically in the form of a standardized dog-bone shape or a cylindrical shape with a reduced section called a "neck." The specimen is then placed in the grips of the tensile testing machine. The machine applies a gradually increasing force, which stretches the specimen until it eventually fractures.

During the test, the tensile testing machine provides several important outputs. These include:

1. Load: The applied force acting on the specimen, measured in Newtons (N) or pounds-force (lbf). The load is typically recorded continuously throughout the test.

2. Displacement: The applied movement or movement acting on sample based on applied force is recorded continuously throughout the test. Generally, expressed in mm (for metals etc.). 

3. Stress: The stress is calculated by dividing the applied force by the original cross-sectional area of the specimen. Stress is usually measured in units of Pascals (Pa) or pounds per square inch (psi).

   Stress (σ) = Force (F) / Cross-sectional area (A)

4. Strain: The strain is a measure of the deformation experienced by the specimen and is calculated by dividing the change in length by the original length. Strain is a dimensionless quantity, but it is often expressed as a percentage.

   Strain (ε) = Change in length (ΔL) / Original length (L)

By using these quantities, several standard curves can be generated to understand material's behavior under monotonic tensile tests; 

1. Load vs. displacement curve: This curve plots the applied load against the displacement of the grips, indicating the elongation of the specimen. It provides a visual representation of the mechanical behavior of the material under tension.

2. Stress vs. strain curve: This curve represents the relationship between the applied stress and the resulting strain. It is one of the most important outputs of a tensile test as it reveals crucial material properties.

Drawing curves from tensile test data involves plotting stress on the y-axis and strain on the x-axis. The resulting stress-strain curve typically exhibits distinct regions:

1. Elastic region: Initially, the stress-strain curve is linear, indicating that the material behaves elastically, meaning it returns to its original shape when the load is removed. The slope of this linear portion is known as the elastic modulus or Young's modulus, and it represents the material's stiffness.

2. Yield point: Beyond the elastic region, the stress-strain curve exhibits a yield point where the material starts to deform plastically, experiencing permanent deformation without an increase in stress. The yield point is an important parameter in determining the material's strength and ductility.

3. Plastic deformation: After the yield point, the stress-strain curve becomes nonlinear, indicating significant plastic deformation. The material undergoes necking, reducing its cross-sectional area and increasing strain until it reaches the ultimate tensile strength (UTS). The UTS represents the maximum stress the material can withstand before failure.

4. Fracture: The stress-strain curve ends with the fracture point, where the material ruptures. The fracture point indicates the material's failure strength.

Tensile testing has a variety of uses, including:

* Selecting materials for an application
* Predicting how a material will perform under different forces
* Determining whether the requirements of a specification, contract or standard are met
* Demonstrating proof of concept for a new product
* Proving characteristics for a proposed patent
* Providing standard quality assurance data for scientific and engineering functions
* Comparing technical data for different material options
* Material testing to provide evidence for use in legal proceedings

## Machines available for this course

For this course, a custom made tensile testing machines will be available. These machines are equipped with

* Custom made grips to hold sample
* A voltage regulator to control the piston
* A piston to provide displacement on the sample based on the given voltage
* A load cell to measure the response while the displacement is applied
* A mitigation controller (based on arduino) to control tensile testing machine with a serial interface

To control the machine and get the responses from the load cell, dedicated graphical user interface is created which is located under 'control_machine' folder. The controlling program is written under Python language to facilitate it's usage and easy modifications.

However, controlling of the piston movement is performed using a voltage regulator and **displacement values are not recorded**. For this purpose, a video recorder is required to survey the entire test. **For instance, you can use your phones to record the entire survey.** To get displacement values or calculating the strain values, you will require another script which is located under 'point_tracking' folder. This program is also written under Python programming language to facilitate it's usage.
