import numpy as np
import matplotlib.pyplot as plt

x = [10, 20, 40, 80, 160]
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(16, 16))

# MRPS
ax = axs[0][0]

# 1X
y1X = [27.8, 71.6, 203.2, 697.6, 3046.4]
y1X_err = [5.33, 14.47, 34.35, 218.82, 844.8]
# UX
yUX = [17.4, 31.4, 56.4, 97.6, 150.4]
yUX_err = [3.23, 4.98, 7.03, 16.32, 17.82]

ax.errorbar(x, y1X, yerr=y1X_err, uplims=True, lolims=True, label='1X')
ax.errorbar(x, yUX, yerr=yUX_err, uplims=True, lolims=True, label='UX')
# ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Problem size')
ax.set_ylabel('MRPS')
ax.set_title('MRPS of OneMax')
ax.legend()

# Evaluations
ax = axs[0][1]

# 1X
y1X = [4189.6, 17188.48, 69707.84, 362999.2, 2385399.2]
y1X_err = [2052.12, 9205.26, 35901.83, 243689.93, 919680.75]
# UX
yUX = [1453.12, 4881.92, 16089.12, 43767.84, 89239.84]
yUX_err = [1016.19, 3562.37, 9839.59, 20718.33, 41267.62]

ax.errorbar(x, y1X, yerr=y1X_err, uplims=True, lolims=True, label='1X')
ax.errorbar(x, yUX, yerr=yUX_err, uplims=True, lolims=True, label='UX')
# ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Problem size')
ax.set_ylabel('MRPS')
ax.set_title('Evaluation of OneMax')
ax.legend()

### Trap5

# MRPS
ax = axs[1][0]

# 1X
y1X = [124.8, 265.6, 857.6, 2918.4, 8192.0]
y1X_err = [43.85, 51.2, 210.71, 501.66, 0.0]
# UX
yUX = [400.0, 3251.2]
yUX_err = [104.43, 998.4]

ax.errorbar(x, y1X, yerr=y1X_err, uplims=True, lolims=True, label='1X')
ax.errorbar([10, 20], yUX, yerr=yUX_err, uplims=True, lolims=True, label='UX')
# ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Problem size')
ax.set_ylabel('MRPS')
ax.set_title('MRPS of Trap5')
ax.legend()

# Evaluations
ax = axs[1][1]

# 1X
y1X = [23405.92, 70874.24, 440847.36, 1579909.44, 2859996.0]
y1X_err = [12491.25, 38262.7, 264417.82, 382582.37, 72778.4]
# UX
yUX = [91791.36, 1445796.96]
yUX_err = [64980.83, 899714.33]

ax.errorbar(x, y1X, yerr=y1X_err, uplims=True, lolims=True, label='1X')
ax.errorbar([10, 20], yUX, yerr=yUX_err, uplims=True, lolims=True, label='UX')
# ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Problem size')
ax.set_ylabel('MRPS')
ax.set_title('Evaluation of Trap5')
ax.legend()

plt.show()
