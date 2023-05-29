# TP-Traction-2023
This repo contains necessary scripts to assist you through your practical course. The main purpose of this course is to get familiar and analyze characteristics of tensile test. 

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

## Scripts available for this course

Before starting, to control the machine and performe video operations, requires specific Python libraries to be installed on your computer. There are several ways to install Python and it's libraries on your system. In this project, we would like to use **conda** for generalization for everybody and easy maintance. 

Conda is an open-source package management and environment management system for Python and other programming languages. It was developed by Anaconda, a Python distribution focused on scientific computing and data science. Conda provides a powerful and flexible way to create, manage, and share software environments and packages. Here are some key features and concepts associated with 

1. **Package Management**: Conda allows you to easily install, update, and uninstall packages from a wide range of software libraries and frameworks. It includes a vast collection of pre-built packages from the Anaconda distribution and other package repositories.

2. **Environment Management**: With Conda, you can create isolated Python environments, also known as Conda environments. Each environment has its own Python interpreter and set of installed packages, enabling you to have multiple environments with different configurations. This isolation helps in avoiding package conflicts and allows for reproducible environments.

3. **Cross-Platform**: Conda works on different operating systems, including Windows, macOS, and Linux. It ensures that packages and environments are compatible across platforms, making it easier to work on projects across different systems.

4. **Dependency Resolution**: Conda handles complex dependency relationships between packages. It automatically resolves dependencies and ensures that all required packages are installed with compatible versions. This feature simplifies the management of complex software stacks and helps avoid dependency conflicts.

5. **Channels**: Conda uses channels to organize and distribute packages. Channels are repositories that store packages, and you can specify different channels to search for packages during installation. The Anaconda distribution provides a default channel, and there are other community channels available as well.

6. **Conda Forge**: Conda Forge is a popular community-led channel that offers additional packages not available in the default Anaconda distribution. It provides a wide variety of software packages and allows users to contribute and maintain packages.

Conda is widely used in the scientific computing and data science communities due to its extensive package availability, environment management capabilities, and robust dependency resolution. It simplifies the process of setting up and managing software environments, making it easier to work on Python projects with different dependencies and configurations.

Anaconda contains huge pack of default libraries which we don't require at the moment. Therefore, we will install **miniconda** instead. Miniconda is a lightweight installer for Conda that includes only the essential components needed to run Conda. It provides a smaller footprint compared to the full Anaconda distribution, making it faster to download and install. Miniconda allows you to create and manage Python environments and install packages using the Conda package manager.

With Miniconda, you have the flexibility to set up custom Python environments tailored to your specific project requirements. You can create isolated environments with different versions of Python and install packages using Conda or pip, depending on your preference.

Miniconda provides the core functionality of Conda, including package management, dependency resolution, and environment management. It's a popular choice for those who prefer a lightweight installation and want more control over the packages and dependencies in their Python environments.


**Before going any further, please follow the instructions below to install and configure your environment**

## Installing and Using Miniconda

This guide will walk you through the installation and usage of Miniconda, a minimal version of the Anaconda Python distribution. Miniconda allows you to create isolated Python environments and easily manage packages for your projects. Additionally, we will cover how to use a `traction.yml` file to install project dependencies.

### Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Creating a Conda Environment](#creating-a-conda-environment)
- [Installing Packages](#installing-packages)
- [Using a `requirements.txt` File](#using-a-requirementstxt-file)

### Prerequisites

Before installing Miniconda, ensure that you have the following:

- Operating System: Windows, macOS, or Linux
- An active internet connection

### Installation

Follow the instructions below to install Miniconda:

1. Visit the Miniconda website at [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html).
2. Download the installer appropriate for your operating system.
3. Run the installer and follow the prompts to complete the installation.
4. Open a new terminal window or command prompt to verify the installation.

To confirm that Miniconda is successfully installed, open your favorite terminal or anaconda prompt to run the following command:

`conda --version`

If the installation was successful, you should see the version of Conda installed on your system.

### Installing Packages

To install packages in your Conda environment, use the `conda install` command. Here's an example:

`conda install numpy`

This command will install the `numpy` package into your active environment. You can specify multiple packages separated by spaces.

To install a specific version of a package, use the following format:

`conda install package_name=version`

For example:

`conda install pandas=1.2.3`

### Using a `traction.yml` File

If you have a `traction.yml` file that lists the packages and versions required for your project, you can use it to install all the dependencies at once. This file is given at the root folder this repository.

Follow these steps:

1. Navigate to the directory where your `traction.yml` file is located.
2. Run the following command to install the packages listed in the `traction.yml` file:

`conda env create --file traction.yml.`

Conda will resolve the dependencies and install the necessary packages.

3. Once the installation is complete, you will have all the required packages for your project. 

4. To use the provided scripts for controlling the machine and video operations, activate the environment as below:

`conda activate traction-tp`

5. To run the scripts following syntax will be used:

`python combine_frames.py` -> for controlling the machine
`python Tracking_Video_ZNCC.py` -> for video operations and get displacement values