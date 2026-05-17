"""Generated from Jupyter notebook: Bakken production data - decline curve for MCK

Magics and shell lines are commented out. Run with a normal Python interpreter."""

import pandas as pd


def main():
    df = pd.read_csv("data/bakken/combinedfile.csv")
    d = df[df["County"] == "MCK"]
    d.shape
    df.shape
    d.to_csv("data/bakken/MCK.csv")
    d = df.copy()
    d.index("ReportDate", inplace=True)
    df_pivot = pd.pivot_table(
        df, index=df.index.month, columns=df.index.year, values="Data"
    )
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    index = pd.date_range(start="01-Jan-2012", end="01-01-2019", freq="M")
    data = np.random.randn(len(index))
    df = pd.DataFrame(data, index, columns=["Data"])
    df_pivot = pd.pivot_table(
        df, index=df.index.month, columns=df.index.year, values="Data"
    )
    ax = df_pivot.plot(title="Data by Year", figsize=(6, 4))
    ax.get_lines()[-1].set_linewidth(5)
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    ax.figure.tight_layout()
    plt.show()
    df_pivot.head()
    d_pivot = pd.pivot_table(
        d, index=d["ReportDate"], columns=d["WellName"], values=d["Oil"]
    )
    d.head()


def main() -> None:
    main()


if __name__ == "__main__":
    main()
