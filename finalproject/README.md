# Life as a Trisolarian  
**Adaptive Solving of ODEs for Gravitational N-Body Systems**

**Author:** Sarah Draves  

**TL;DR:** A computational physics project implementing and benchmarking a custom adaptive RK4 integrator for chaotic gravitational N-body systems, with visualization and animation of multi-body dynamics inspired by *The Three-Body Problem*.

## Overview
This project explores numerical solutions to the classical gravitational *N-body problem* through the lens of the fictional planet **Trisolaris** from *The Three-Body Problem* by Liu Cixin. Motivated by the chaotic dynamics experienced by a planet orbiting multiple stars, the project focuses on accurately and efficiently integrating equations of motion using adaptive time-stepping methods.

The core contribution is a custom-built **adaptive Runge–Kutta 4 (RK4)** integrator, developed from scratch and benchmarked against SciPy’s `RK45`. The solver is used to simulate and visualize a variety of multi-body gravitational scenarios in two dimensions, including chaotic and near-periodic configurations.

## Project Goals
- Implement an adaptive ODE solver for Newtonian gravity
- Compare performance and accuracy against SciPy’s `RK45`
- Visualize multi-body gravitational dynamics through static plots and animations
- Provide an interactive interface for users to experiment with initial conditions

## Methods

### Equations of Motion
The system evolves according to the classical Newtonian gravity equations for point masses. Each body obeys a second-order ODE derived from pairwise gravitational forces.

### Adaptive Integration
Three numerical approaches are compared:
- **SciPy `RK45`** (adaptive, reference solver)
- **Custom Adaptive RK4** (this project)
- **Fixed-step RK4**

The adaptive RK4 solver dynamically adjusts the time step based on local truncation error estimates, achieving good agreement with `RK45` for the same error tolerance.

#### Performance Comparison (Example)
| Solver | Tolerance / Step Size | Runtime |
|------|----------------------|--------|
| SciPy RK45 | `1e-12` | ~0.44 s |
| Adaptive RK4 (custom) | `1e-12` | ~4.36 s |
| Fixed-step RK4 | `h = 1e-5` | ~25.4 s |

While slower than `RK45`, the custom adaptive RK4 provides a clear demonstration of adaptive integration principles and significantly outperforms fixed-step methods.

### Animation and Resampling
A challenge with adaptive solvers is that output time points are unevenly spaced, which leads to visually misleading animations. This issue is addressed by:
- Resampling the solution onto a uniform time grid
- Using cubic interpolation via SciPy
- Animating the resampled trajectory

This produces smooth, physically faithful animations while preserving adaptive accuracy.

## Features
- Custom adaptive RK4 integrator
- Static plots and time evolution diagnostics
- 2D animations of gravitational systems
- Interactive mode allowing users to input initial conditions
- Comparison framework for solver accuracy and performance

## Limitations and Future Work
- Simulations are currently restricted to 2D
- The “planet-centric” reference frame analysis was not completed due to time constraints
- Future extensions could include:
  - Full 3D simulations
  - Energy and angular momentum conservation diagnostics
  - Long-term stability analysis
  - Observer-frame transformations from the planet’s perspective


## Sources and References
- Liu Cixin, *The Three-Body Problem*
- *3 Body Problem* (Netflix adaptation)
- Wikipedia: Three-body problem
- R. Reusser, *Periodic Planar Three-Body Orbits*  
  https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
- SciPy documentation

Note: this readme was crafted by ChatGPT after uploading my final project slides, which are in this folder [here](https://github.com/sarahedraves/Draves-GCComputationalAstrophysics/blob/main/finalproject/finalpresentation.pdf).
