#!/usr/bin/env python3


import subprocess
import tempfile

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

spect = 1/1.618
resolution = 72.27
textwidth = 307.28987/resolution
textheight = 261.14662/resolution
textiny, texsmall, texnormal = 5.5, 6.5, 8.
offblack = '#262626'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['CMU Sans Serif'],
    'mathtext.fontset': 'custom',
    'mathtext.default': 'it',
    'mathtext.rm': 'sans',
    'mathtext.it': 'sans:italic',
    'mathtext.cal': 'sans',
    'font.size': texsmall,
    'legend.fontsize': texsmall,
    'axes.labelsize': texsmall,
    'axes.titlesize': texsmall,
    'xtick.labelsize': textiny,
    'ytick.labelsize': textiny,
    'lines.linewidth': .8,
    'lines.markeredgewidth': .1,
    'patch.linewidth': .8,
    'axes.linewidth': .4,
    'xtick.major.width': .4,
    'ytick.major.width': .4,
    'xtick.minor.width': .4,
    'ytick.minor.width': .4,
    'xtick.major.size': 1.4,
    'ytick.major.size': 1.4,
    'xtick.minor.size': 0.9,
    'ytick.minor.size': 0.9,
    'xtick.major.pad': 1.5,
    'ytick.major.pad': 1.5,
    'text.color': offblack,
    'axes.edgecolor': offblack,
    'axes.labelcolor': offblack,
    'xtick.color': offblack,
    'ytick.color': offblack,
    'legend.numpoints': 1,
    'legend.scatterpoints': 1,
    'legend.frameon': False,
    'pdf.fonttype': 42
})

grid_max = 2
nucleon_width = 0.6

def main():
    with PdfPages('slideshow.pdf') as pdf:
        for p in np.linspace(-1, 1, 11):
            with tempfile.TemporaryDirectory() as tmpdir:
                print(p)
                subprocess.check_call(
                    'trento p p 1 -q --random-seed 24319 --grid-max {} --grid-step 0.05 '
                    '--b-min {} --b-max {} -w {} -d {} -k 1e12 -p {} -o {}'
                    .format(grid_max, 2*nucleon_width, 2*nucleon_width,
                            nucleon_width, nucleon_width, p, tmpdir).split()
                )
                plt.figure(figsize=(6, 5))

                theta = np.linspace(0, 2*np.pi, 1000)
                for offset in -1, 1:
                    plt.plot(
                        2*nucleon_width*np.cos(theta) + offset*nucleon_width,
                        2*nucleon_width*np.sin(theta), lw=.3,
                        color='.2', alpha=.5)

                plt.imshow(
                    np.loadtxt('{}/0.dat'.format(tmpdir)),
                    aspect='equal',
                    interpolation='none',
                    cmap=plt.cm.Blues,
                    extent=[-grid_max, grid_max,
                            -grid_max, grid_max]
                )

                plt.annotate('$p = {:+.1f}$'.format(p), (.5, .05),
                             fontsize=20,
                             xycoords='axes fraction',
                             ha='center', va='bottom')
                plt.xlabel('$x$ [fm]', fontsize=20)
                plt.ylabel('$y$ [fm]', fontsize=20)
                plt.xticks(np.arange(-grid_max, grid_max + 1), fontsize=18)
                plt.yticks(np.arange(-grid_max, grid_max + 1), fontsize=18)
                plt.xlim(-grid_max, grid_max)
                plt.ylim(-.8*grid_max, .8*grid_max)

                plt.tight_layout(pad=.2)
                pdf.savefig()
                plt.close()


if __name__ == "__main__":
    main()
