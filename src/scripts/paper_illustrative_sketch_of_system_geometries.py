"""
UTF-8, Python 3

------------------
Flaring SPI
------------------

Ekaterina Ilin, 2023, MIT License


Simplified magnetic star-planet interaction geometries. Panel a: Fully aligned 
system along the line of sight. Magnetic, rotational, and orbital axis are 
aligned. The interaction footpoint moves along the black line, and is visible 
on the red line, i.e. during 50% of the planet's orbit. Flares induced along 
this line will result in excess flares when the planet is in front of the star. 
Panel b: Orbital misalignment. The rotational and magnetic axis are aligned, 
but the planet is highly misaligned. The footpoint of interaction moves between 
the two horizontal black lines, and is still visible 50% of the time, resulting 
in modulated flaring with orbital phase. However, the footpoint passes different 
latitudes on the star, which correspond to different dipole field strengths, 
which may influence the power of interaction. Panel c: Inclined fully aligned 
system. The red interaction footpoint line is visible 100% of the time. No 
modulation due to SPI can observed, even if flares are triggered by the planet. 
The sketch only shows the interaction footpoint region on the Northern 
hemisphere of the star, but they may appear on both. 
"""

import numpy as np
import matplotlib.pyplot as plt
import paths


if __name__ == "__main__":

    # init two figure panels next to each other
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    # Central star
    for ax in [ax1, ax2, ax3]:
        ax.add_patch(plt.Circle((0, 0), 1.0, color='w', fill=True))
        ax.add_patch(plt.Circle((0, 0), 1.03, color='k', fill=False))
        ax.add_patch(plt.Circle((0, 0), 1, color='grey', fill=True, alpha=0.5))


    # -----------------------------------------------------------------------------
    # PANEL 1

    req = 2 # field apex
    aplanet = 2 # semi-major axis

    # plot a dipole field line from the big circle
    theta = np.linspace(-np.pi/2, np.pi/2, 100)
    r = req * np.sin(theta)**2
    # convert to cartesian coordinates
    y = r * np.cos(theta)
    x = r * np.sin(theta)

    # where is r=1
    theta_1 = np.arcsin(np.sqrt(1 / req))
    x1 = np.sin(theta_1)
    y1 = np.cos(theta_1)

    # plot the dipole 
    ax1.plot(x, y, color='olive', zorder=-10, linestyle='--')
    ax1.plot(x, -y, color='olive', zorder=-10, linestyle='--')

    # plot a vertical arrow through the middle of the big circle, that is slightly longer than the big circle
    ax1.arrow(0, -1.2, 0, 2.4, head_width=0.15, head_length=0.3, fc='k', ec='k')

    # plot a small circle in the apex of the dipole field line
    ax1.add_patch(plt.Circle((aplanet, 0), 0.15, color='k', fill=True))
    ax1.add_patch(plt.Circle((aplanet, 0), 0.1, color='teal', fill=True))

    # plot a horizontal line between the centers of the two circles
    ax1.plot([-aplanet, aplanet], [0, 0], color='k', linewidth=0.5)

    # plot a horizontal line at the latitude where the dipole field touches the big circle
    ax1.plot([-x1, x1], [y1, y1], color='k')

    # plot a horizontal line at the latitude where the dipole field touches the big circle
    # but now only on the side of the circle where the small circle is
    ax1.plot([0, x1], [y1, y1], color='r')


    # -----------------------------------------------------------------------------
    # PANEL 2

    inc = -1 # inclination angle of orbital plane in radians

    # add vertical axis
    ax2.arrow(0, -1.2, 0, 2.4, head_width=0.15, head_length=0.3, fc='k', ec='k')

    # calculate r for theta=inc for the dipole
    req_new = aplanet / np.sin(np.pi/2 - inc)**2

    # convert to cartesian coordinates
    xnew = req_new * np.cos(inc)
    ynew = req_new * np.sin(inc)

    rnew = req_new * np.sin(theta)**2
    ydipnew = rnew * np.cos(theta)
    xdipnew = rnew * np.sin(theta)

    # plot new dipole
    ax2.plot(xdipnew, ydipnew, color='olive', zorder=-10, linestyle='--')
    ax2.plot(xdipnew, -ydipnew, color='olive', zorder=-10, linestyle='--')

    # plot old dipole
    ax2.plot(x, y, color='olive',  zorder=-10, linestyle='--')
    ax2.plot(x, -y, color='olive', zorder=-10, linestyle='--')

    # plot the small circle at new position
    ax2.add_patch(plt.Circle((aplanet * np.cos(inc), aplanet * np.sin(inc)),
                            0.15, color='k', fill=True))
    ax2.add_patch(plt.Circle((aplanet * np.cos(inc), aplanet * np.sin(inc)),
                            0.1, color='teal', fill=True))

    # define line through zero at inclination angle
    x2 = np.linspace(-aplanet * np.cos(inc), aplanet * np.cos(inc), 100)
    y2 = np.tan(inc) * x2

    # plot line
    ax2.plot(x2, y2, color='k', linewidth=0.5)

    # define perpendicular arrow through zero
    def y3(x): return -1/np.tan(inc) * x

    # rotated arrow
    extent = 1
    ax2.arrow(-extent, y3(-extent), 2 * extent, np.abs(2 * y3(-extent)),
            head_width=0.15, head_length=0.3, fc='k', ec='k')


    # where is r=1
    theta_2 = np.arcsin(np.sqrt(1 / req_new))
    xup = np.sin(theta_1)
    yup = np.cos(theta_1)

    # fill black area between x1, xup, y1, yup
    for y_ in np.linspace(np.cos(theta_1),np.cos(theta_2),10):
        t_ = np.arccos(y_)
        x_ = np.sin(t_)
        
        ax2.plot([-x_, x_], [y_, y_], color='k', alpha=1)
        ax2.plot([0, x_], [y_, y_], color='r', alpha=1)


    # ----------------------------------------------------------------------------
    # PANEL 3

    inc = -1 # same as panel 1 but the entire system is inclined
    req = 3 # dipole apex
    aplanet = 3 # semi major axis

    # rotation matrix
    def rot_x(x, y, angle=inc): return x * np.cos(angle) - y * np.sin(angle)
    def rot_y(x, y, angle=inc): return x * np.sin(angle) + y * np.cos(angle)

    # plot a dipole field line from the big circle
    theta = np.linspace(-np.pi/2, np.pi/2, 100)
    r = req * np.sin(theta)**2

    # convert to cartesian coordinates
    y = r * np.cos(theta)
    x = r * np.sin(theta)

    # where is r=1
    theta_1 = np.arcsin(np.sqrt(1 / req))
    x1 = np.sin(theta_1)
    y1 = np.cos(theta_1)

    # plot the rotated dipole
    xrot, yrot = rot_x(x, y), rot_y(x, y)
    ax3.plot(xrot, yrot, color='olive', zorder=-10, linestyle='--')

    # plot the southern hemisphere too
    ax3.plot(rot_x(xrot, yrot, angle=np.pi), rot_y(xrot, yrot, angle=np.pi),
            color='olive', zorder=-10, linestyle='--')

    # plot a small circle in the apex of the dipole field line
    ax3.add_patch(plt.Circle((rot_x(aplanet, 0), rot_y(aplanet, 0)),
                            0.15, color='k', fill=True))
    ax3.add_patch(plt.Circle((rot_x(aplanet, 0), rot_y(aplanet, 0)),
                            0.1, color='teal', fill=True))

    # plot a horizontal line between the centers of the two circles
    ax3.plot([rot_x(-aplanet, 0), rot_x(aplanet, 0)],
            [rot_y(-aplanet, 0), rot_y(aplanet, 0)], color='k', linewidth=0.5)

    # plot a horizontal line at the latitude where the dipole field touches the big circle
    ax3.plot([rot_x(-x1, y1), rot_x(x1, y1)],
            [rot_y(-x1, y1), rot_y(x1, y1)], color='r')

    # plot rotated arrow to indicate the rotational/magnetic/orbital axis
    x0 = rot_x(0, -1.1)
    y0 = rot_y(0, -1.1)
    ax3.arrow(x0, y0, -2 * x0, -2*y0,
            head_width=0.15, head_length=0.3, fc='k', ec='k')

    # -----------------------------------------------------------------------------
    # LAYOUT

    axes = [ax1, ax2, ax3]
    for ax in axes:
        # right to the small circle draw a small arrow to the right
        arr = ax.arrow(2, 3, 0.7, 0, head_width=0.3,
                    head_length=0.1, fc='k', ec='k')

        # annotate the arrow with LOS
        ax.annotate('LOS', xy=(2, 3), xytext=(2, 3.4))

        # set axis extent correctly
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)

        # remove axes
        ax.set_axis_off()

    # label each panel with letter in upper left corner
    for label, ax in zip(list("abc"), axes):
        ax.text(0., 0.97, label + ".", transform=ax.transAxes,
                fontsize=18, fontweight='bold', va='top', ha='right')
        
    plt.tight_layout()

    # --------------------------------------------------------------------------
    # SAVE

    plt.savefig(paths.figures / "system_geometries.png", dpi=300)
