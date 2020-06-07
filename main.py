import argparse

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
from scipy import stats

# set params here
x_range = (0, 20)
scale = 1.0
loc = 0.0

titledict = {
    "rayleigh": "Rayleigh",
    "norm": "Gaussian/Normal",
    "exp": "Exponential",
}

def func(dist):
    return dist.pdf(x_arr)


def update(_):
    scale = s_scale.val
    loc = s_loc.val
    dist_new = _dist(scale=scale, loc=loc)
    l.set_ydata(func(dist_new))
    fig.canvas.draw_idle()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simple visualization of scipy.stats distributions."
    )
    parser.add_argument(
        "-d",
        "--dist",
        type=str,
        default="exp",
        choices=["exp", "norm", "rayleigh"],
        help='The Distribution to visualize. Can be any of the following: "exp", "norm", "rayleigh"',
    )
    args = parser.parse_args()
    # TODO: add more distributions
    if args.dist == "exp":
        _dist = stats.expon
    elif args.dist == "norm":
        _dist = stats.norm
    elif args.dist == "rayleigh":
        _dist = stats.rayleigh
    else:
        print(f"{args.dist} is not a valid value for --dist, defaulting to exponential")
        _dist = stats.expon

    fig, ax = plt.subplots()

    ax.set_ylim(0, 1)
    ax.set_xlabel(r"$X$")
    ax.set_ylabel("Probability Density")
    ax.set_title(f"{titledict[args.dist]} Distribution Visualized")

    plt.subplots_adjust(left=0.25, bottom=0.25)
    x_arr = np.arange(*x_range, 0.001)

    dist = _dist(scale=scale, loc=loc)

    (l,) = plt.plot(x_arr, func(dist), lw=2)

    ax.margins(x=0)

    axcolor = "lightgoldenrodyellow"
    axscale = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    axloc = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

    s_scale = Slider(axscale, "Scale", 0.01, 10, valinit=scale)
    s_loc = Slider(axloc, "Loc", 0.01, 10, valinit=loc)

    s_scale.on_changed(update)
    s_loc.on_changed(update)

    resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
    button = Button(resetax, "Reset", color=axcolor, hovercolor="0.975")

    def reset(_):
        s_scale.reset()
        s_loc.reset()

    button.on_clicked(reset)

    plt.show()
