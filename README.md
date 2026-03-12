# particle_lab

Physics-based particle simulation framework currently in the prototyping stage.

The long-term goal of this project is to develop a high-performance physics
simulation engine with a C++/CUDA backend,\
while Python is used forprototyping and experimentation.

## Current Release
 **v0.0.1 - Prototype** \
 The current version focuses on validating architecture and core simulation
 components before transitioning to a high-performance backend.
 
 ## FEATURES
  - Modular structure
  - Multiple numerical integrators 
    - Euler
    - Verlet
    - Velocity Verlet
  - Elementary rendering with MatPlotLib
  - AoS based physical particle implementation simulating:
    - mass
    - gravity
    - drag 
  - Modular constraint system
  - PBD Rod constraints with:
    - adjustable length
    - stiffness
  - FBD Spring constraints with:
    - custom length
    - spring constant
    - damping 

# Users Guide 
## Installation

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


## Quick Example

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




 ## Supported Functions 
  ### Creating World
  ```python
    world = particle_lab.World(
        integrator=particle_lab.VelocityVerletIntegrator()
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
   - dt is the phyics simulation timestep value in seconds, default value is 0.001
   - sim_time parameter is the total requested simulation time in seconds, default value is 100
   - FPS is the frames per second of the rendered output, default value is 60
   - world_gravity enables Earth gravity for all particles, True as default 
   - particle_gravity enables pairwise gravity for all particles, currently with no exclusion, True as default
   - G is the Gravitation Constant value, its defaulted to the real life value although, its recommended for simulations to run at \
    higher values with modified masses for numerical stablity
   - eps parameter is used for numerical stability, to prevent division by 0, using lower vales might lead to numerical instability
   - constraint_iterations parameter determines the amount of iterations of each constraint per frame, using lower values might lead to Rod constraints acting floppy 
  ### Defining Particles 
   ```python
     particle = particle_lab.Particle(position=[1,2], mass=10)
   ```
   - Position argument is provided as an ordered list of [x, y], the default value is [0.0, 0.0]
   - Mass argument is a float value representing the particles mass in kilograms, the default value is 1.0 
   - In order for a particle to be simulated, it should be added to word via:
   ```python
      world.add_particle(particle)
   ```

 ### Defining Constraints
  - Rod Constraints
    ```python
      constraint = particle_lab.Rod(5, particle1, particle2)
    ```
   - First argument is the rod length in meters, the user must provide a float value as there is no default
   - Second and third arguments are particle objects that the constraint anchors to
   - For constraints to be simulated, they have to be included in World via:
     ```python
        world.add_constraint(constraint)
     ```

## Roadmap 




## Contributing

Contributions, suggestions, and discussions are welcome.

Please open an issue to discuss potential changes before submitting
large pull requests.


## License 
MIT License
