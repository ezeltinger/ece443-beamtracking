import numpy as np
import matplotlib.pyplot as plt
from search import search_timing


# Exhaustive search uncertainty region is 2pi/beamcount
# Contiguous beam search uncertainty region is pi/beam_count
# Non-Contiguous beam search uncertainty region is pi/(2^(beam_count-1))
exh_beam_counts = np.arange(5, 21)
exhaustive_u = 2*np.pi/exh_beam_counts
con_beam_counts = np.arange(3, 21)
contiguous_u = np.pi/con_beam_counts
noncon_beam_counts = np.arange(3, 21)
non_contiguous_u = np.pi/(2**(noncon_beam_counts-1))

# The time it takes to send n number of beams where n = 3,4,5,...,20
exh_search_times = 1e6*search_timing(exh_beam_counts, cell_radius=1)
con_search_times = 1e6*search_timing(con_beam_counts, cell_radius=1)
noncon_search_times = 1e6*search_timing(noncon_beam_counts, cell_radius=1)
fig, ax = plt.subplots()
exh_line, = ax.plot(exhaustive_u, exh_search_times, '-o', label='Exhaustive Search')
con_line, = ax.plot(contiguous_u, con_search_times, '-o', label='Contiguous Beam Search')
noncon_line, = ax.plot(non_contiguous_u, noncon_search_times, '-o', label='Non-Contiguous Beam Search')
ax.legend(handles=[exh_line, con_line, noncon_line])

ax2 = ax.twinx()
exh_line, = ax2.plot(exhaustive_u, exh_beam_counts, '-o', label='Exhaustive Search')
con_line, = ax2.plot(contiguous_u, con_beam_counts, '-o', label='Contiguous Beam Search')
noncon_line, = ax2.plot(non_contiguous_u, noncon_beam_counts, '-o', label='Non-Contiguous Beam Search')
ax.legend(handles=[exh_line, con_line, noncon_line])

ax.set_ylabel('Search Time (us)')
ax2.set_ylabel('Beam Count')
ax.set_xticks(np.arange(0, np.pi/2, step=np.pi/16))
xlabels = ['0', r'$\frac{%s}{%s}$'%('\pi',16),
           r'$\frac{%s}{%s}$'%('\pi',8),
           r'$\frac{%s%s}{%s}$'%(3,'\pi',16),
           r'$\frac{%s}{%s}$'%('\pi',4),
           r'$\frac{%s%s}{%s}$'%(5,'\pi',16),
           r'$\frac{%s%s}{%s}$'%(3,'\pi',8),
           r'$\frac{%s%s}{%s}$'%(7,'\pi',16)]
ax.set_xticklabels(xlabels)
ax.set_xlabel('Uncertainty Region (radians)')
plt.title('Minimum Time to Achieve Uncertainty Region')
plt.savefig('../saved_examples/algorithm_comp.png')
plt.show()
