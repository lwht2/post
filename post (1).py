# Before running this script, run
#
# source /usr/local/software/turbostream/ts3610_a100/bashrc_module_ts3610_a100
#
# Then edit `fname` below and run
#
# python post.py

from ts import ts_tstream_reader, ts_tstream_cut, ts_tstream_patch_kind
import numpy as np
import matplotlib.pyplot as plt

Pref = 1e5
Tref = 300.0
fname = "runs/fan_vort/output.hdf5"

# Read the mesh
tsr = ts_tstream_reader.TstreamReader()
g = tsr.read(fname)

# Get numbers of points in i/j/k directions
b = g.get_block(0)
ni = b.ni
nj = b.nj
nk = b.nk

# Cut the inlet
C1 = ts_tstream_cut.TstreamStructuredCut()
C1.read_from_grid(
    g,  # Grid object
    Pref,  # Reference pressure for s=0
    Tref,  # Reference temperature for s=0
    0,  # Block id
    0,  # Starting i index
    1,  # Ending i index
    0,  # Starting j index
    nj,  # Ending j index
    0,  # Starting k index
    nk,  # Ending k index
)

# Cut the outlet
C2 = ts_tstream_cut.TstreamStructuredCut()
C2.read_from_grid(
    g,  # Grid object
    Pref,  # Reference pressure for s=0
    Tref,  # Reference temperature for s=0
    0,  # Block id
    ni - 1,  # Starting i index
    ni,  # Ending i index
    0,  # Starting j index
    nj,  # Ending j index
    0,  # Starting k index
    nk,  # Ending k index
)

# Print properties at inlet and exit
mdot1, Po1 = C1.mass_avg_1d("pstag")
A1, P1 = C1.area_avg_1d("pstat")
mdot2, Po2 = C2.mass_avg_1d("pstag")
print("Mass flow:", mdot1, mdot2)
print("Po", Po1, Po2)

# Cut at mid-span
jmid = nj // 2
Cbld = ts_tstream_cut.TstreamStructuredCut()
Cbld.read_from_grid(
    g,  # Grid object
    Pref,  # Reference pressure for s=0
    Tref,  # Reference temperature for s=0
    0,  # Block id
    0,  # Starting i index
    ni,  # Ending i index
    jmid,  # Starting j index
    jmid + 1,  # Ending j index
    0,  # Starting k index
    nk,  # Ending k index
)

# Plot contours of velocity
fig, ax = plt.subplots()
ax.contourf(Cbld.x, Cbld.rt, Cbld.vabs)
plt.savefig("vabs.pdf")

# Plot static pressure around blade
fig, ax = plt.subplots()
ax.plot(Cbld.x[0, :], Cbld.pstat[(0, -1), :].T)
plt.savefig("pstat.pdf")

# Print available flow field variables
print(dir(Cbld))
