import numpy as np
import matplotlib.pyplot as plt


def sg_to_brix(sg: float) -> float:
    """
    Convert Specific Gravity (SG) to Brix using the given polynomial.
    """
    return -668.962 + 1262.45 * sg - 776.43 * sg**2 + 182.94 * sg**3


def compute_delle_units(brix: float, abv: float) -> float:
    """
    Calculate Delle Units using the formula: Delle Units = Brix + 4.5 * ABV
    """
    return brix + 4.5 * abv


def plot_delle_units_chart(
    abv_min: float = 5.0,
    abv_max: float = 20.0,
    sg_min: float = 1.000,
    sg_max: float = 1.150,
    threshold: float = 73.0,
    output_file: str = "delle_units_chart.png",
):
    """
    Generate and save a filled contour plot of Delle Units.

    :param abv_min: Minimum ABV (%)
    :param abv_max: Maximum ABV (%)
    :param sg_min:  Minimum Specific Gravity
    :param sg_max:  Maximum Specific Gravity
    :param threshold: Delle Units threshold for contour line
    :param output_file: Filename to save the plot
    """
    # Create a grid of ABV and SG values
    abv_vals = np.linspace(abv_min, abv_max, 200)
    sg_vals = np.linspace(sg_min, sg_max, 200)
    ABV, SG = np.meshgrid(abv_vals, sg_vals)

    # Convert SG to Brix
    brix_vals = sg_to_brix(SG)

    # Compute Delle Units
    delle_units = compute_delle_units(brix_vals, ABV)

    # Create the filled contour plot
    plt.figure(figsize=(8, 6))
    contourf = plt.contourf(ABV, SG, delle_units, levels=100, cmap="viridis")
    plt.colorbar(contourf, label="Delle Units")

    # Overlay the threshold contour line in red
    contour_line = plt.contour(
        ABV, SG, delle_units, levels=[threshold], colors="red", linewidths=2
    )
    # Manually place the label if desired (adjust coords to your liking)
    plt.clabel(
        contour_line,
        fmt={threshold: "Line of Stability 73 DU"},
        colors="red",
        inline=True,
        inline_spacing=5,
        fontsize=10,
        manual=[(12.5, 1.07)],
    )

    # Labeling
    plt.xlabel("ABV (%)")
    plt.ylabel("Specific Gravity (Residual Sugar)")
    plt.title(
        "Delle Units across ABV and Specific Gravity\n(Highlighting Line of Stability 73 DU)"
    )

    # Save and show
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.show()


# If you want this script to run directly:
if __name__ == "__main__":
    plot_delle_units_chart()
