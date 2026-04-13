# particle_lab

Physics-based particle simulation framework currently in the prototyping stage.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-prototype-orange)



The long-term goal of this project is to develop a high-performance research-oriented physics simulation engine 
with a C++/CUDA backend, while Python is used for prototyping and experimentation.

## Current Release
 **v0.0.1 - Prototype** \
 The current version focuses on validating architecture and core simulation
 components before transitioning to a high-performance backend.
 
 ## Features
  - Modular structure
  - Multiple numerical integrators 
    - Euler
    - Verlet
    - Velocity Verlet
  - Basic visualization using Matplotlib
  - AoS based particle model supporting:
    - mass
    - gravity
    - drag 
  - Modular constraint system
  - Position-Based Dynamics (PBD) Rod constraints with:
    - adjustable length
    - stiffness
  - Force-Based Dynamics (FBD) Spring constraints with:
    - custom length
    - spring constant
    - damping 

## User Guide 
### Installation

Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/fenn-core/particle-lab.git
cd particle-lab
pip install -e .
```

Verify installation:
```python
import particle_lab
```


### Quick Example
- Following example produces a simple pendulum simulation   

```python
import particle_lab as sim

world = sim.World(
    integrator=sim.VelocityVerletIntegrator(),
    dt=0.001,
    sim_time=10,
)

p1 = sim.Particle(position=[0, 8], mass=0)
p2 = sim.Particle(position=[3, 4], mass=40)

rod = sim.Rod(5, p1, p2)

world.add_particle(p1)
world.add_particle(p2)
world.add_constraint(rod)

renderer = sim.MatPlotLibRenderer(xlim=[-5,5],ylim=[2,9])
world.sim_loop(renderer)
```




 ### Supported Functions 
  #### Creating World
  ```python
    world = particle_lab.World(
        integrator=particle_lab.VelocityVerletIntegrator(),
        dt=0.001,
        sim_time=100,
        FPS=60,
        world_gravity=True,
        particle_gravity=True,
        G=6.67430e-11,
        eps=1e-5,
        constraint_iterations=10,
    )
  ```
   - The user provides a numerical integrator object as the integrator parameter, as there is no default for this value
   - dt is the simulation timestep value in seconds, default value is 0.001
   - sim_time parameter is the total requested simulation time in seconds, default value is 100
   - FPS is the frames per second of the rendered output, default value is 60
   - world_gravity enables Earth gravity for all particles, True as default 
   - particle_gravity enables pairwise gravity for all particles, currently with no exclusion, True as default
   - G is the Gravitation Constant value, its defaulted to the real life value although, its recommended for simulations to run at \
    higher values with modified masses for numerical stability
   - eps parameter is used to prevent division by 0, using lower values might lead to numerical instability
   - constraint_iterations parameter determines the amount of iterations of each constraint per frame, using lower values might lead to Rod constraints appearing floppy 
  #### Defining Particles 
   ```python
     particle = particle_lab.Particle(position=[1,2], mass=10)
   ```
   - Position argument is provided as a list [x, y], the default value is [0.0, 0.0]
   - Mass argument is a float value representing the particles mass in kilograms, the default value is 1.0 
   - In order for a particle to be simulated, it must be added to world via:
   ```python
      world.add_particle(particle)
   ```

  #### Defining Constraints
  - Rod Constraints
    ```python
      rod = particle_lab.Rod(5.0, particle1, particle2)
    ```
   - First argument is the rod length in meters, the user must provide a float value as there is no default
   - Second and third arguments are Particle objects that the Rod anchors on
  - Spring Constraints 
    ```python
      spring = particle_lab.Spring(7.0, particle1, particle2, 1000, damping_constant=2)
    ```
     - First argument is the spring length in meters, the user must provide a float value as there is no default
     - Second and third arguments are Particle objects that the Spring anchors on
     - Fourth argument is the spring constant in N/m   
     - damping_constant argument is the velocity proportional damping coefficient

  - For constraints to be simulated, they have to be included in World via:
    ```python
      world.add_constraint(constraint)
    ```

 ### Rendering
  - Matplotlib Renderer
    ```python 
     renderer = particle_lab.MatPlotLibRenderer(xlim=(-12,6), ylim=(0,7))
    ```
   - Renderer object takes xlim and ylim tuples as window size arguments the default value for both is (-10, 10)
   ```python 
      world.sim_loop(renderer)
   ```
  - For rendering, the renderer object is passed on to World's sim_loop method


## Architecture

The engine is organized into modular subsystems:

- core – simulation world and loop
- physics – integrators, forces, constraints
- rendering – visualization backends
- tools – logging and utilities
- utils – mathematical helpers


## Roadmap 
  ### Short Term Goals
  - Support both:
    - Real-time simulation with live rendering
    - Offline simulation followed by playback

  - Refactor simulation state to SoA layout
  - Implement an extensive data logging and replay system with CSV exports 

  ### Mid Term Goals 
  - Implement Collisions system
  - Introduce additional integrators; RK, symplectic, adaptive etc
  - Implement Advanced Mach number-aware drag system 
  - Implement Rigid Body system 
  - Introduce advanced diagnostics and debugging tools
  - Implement better renderers; Pygame, OpenGL
  - Introduce a offline frame exporting system 

  ### Long Term Goals 
  - Implement advanced plotting and visualisation tools for research uses 
  - Begin development of the  C++ backend
  - Implement CUDA acceleration for massive simulations

## Contributing

Contributions, suggestions, and discussions are welcome.

Please open an issue to discuss potential changes before submitting
large pull requests.


## License 
MIT License
