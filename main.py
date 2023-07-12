import numpy as np
import magpylib as magpy
import matplotlib.pyplot as plt
import pyvista as pv

'''
coil1 = magpy.Collection()
for z in np.linspace(-8, 8, 16):
    winding = magpy.current.Loop(
        current=100,
        diameter=10,
        position=(0,0,z),
    )
    coil1.add(winding)

coil1.show()

ts = np.linspace(-8, 8, 1000)
vertices = np.c_[5*np.cos(ts*2*np.pi), 5*np.sin(ts*2*np.pi), ts]
coil2 = magpy.current.Line(
    current=100,
    vertices=vertices
)

coil2.show()

fig, [ax1,ax2] = plt.subplots(1, 2, figsize=(13,5))

# create grid
ts = np.linspace(-20, 20, 20)
grid = np.array([[(x,0,z) for x in ts] for z in ts])

# compute and plot field of coil1
B = magpy.getB(coil1, grid)
Bamp = np.linalg.norm(B, axis=2)
Bamp /= np.amax(Bamp)

sp = ax1.streamplot(
    grid[:,:,0], grid[:,:,2], B[:,:,0], B[:,:,2],
    density=2,
    color=Bamp,
    linewidth=np.sqrt(Bamp)*3,
    cmap='coolwarm',
)

# compute and plot field of coil2
B = magpy.getB(coil2, grid)
Bamp = np.linalg.norm(B, axis=2)
Bamp /= np.amax(Bamp)

cp = ax2.contourf(
    grid[:,:,0], grid[:,:,2], Bamp,
    levels=100,
    cmap='coolwarm',
)
ax2.streamplot(
    grid[:,:,0], grid[:,:,2], B[:,:,0], B[:,:,2],
    density=2,
    color='black',
)

# figure styling
ax1.set(
    title='Magnetic field of coil1',
    xlabel='x-position [mm]',
    ylabel='z-position [mm]',
    aspect=1,
)
ax2.set(
    title='Magnetic field of coil2',
    xlabel='x-position [mm]',
    ylabel='z-position [mm]',
    aspect=1,
)

plt.colorbar(sp.lines, ax=ax1, label='[mT]')
plt.colorbar(cp, ax=ax2, label='[mT]')

plt.tight_layout()
plt.show()



'''

coil1 = magpy.Collection()
for z in np.linspace(-8, 8, 16):
    winding = magpy.current.Loop(
        current=100,
        diameter=10,
        position=(0,0,z),
    )
    coil1.add(winding)

grid = pv.UniformGrid(
    dimensions=(41, 41, 41),
    spacing=(2, 2, 2),
    origin=(-40, -40, -40),
)

# compute B-field and add as data to grid
grid['B'] = coil1.getB(grid.points)

# compute field lines
seed = pv.Disc(inner=1, outer=5.2, r_res=3, c_res=12)
strl = grid.streamlines_from_source(
    seed,
    vectors='B',
    max_time=180,
    initial_step_length=0.01,
    integration_direction='both',
)

# create plotting scene
pl = pv.Plotter()

# add field lines and legend to scene
legend_args = {
    'title': 'B [mT]',
    'title_font_size': 20,
    'color': 'black',
    'position_y': 0.25,
    'vertical': True,
}

# draw coils
magpy.show(coil1, canvas=pl, backend='pyvista')

# add streamlines
pl.add_mesh(
    strl.tube(radius=.2),
    cmap="bwr",
    scalar_bar_args=legend_args,
)
# display scene
pl.camera.position=(160, 10, -10)
pl.set_background("white")
pl.show()
