"""Generated from Jupyter notebook: Bakken production data - decline curve for MCK

Magics and shell lines are commented out. Run with a normal Python interpreter."""


# --- code cell ---

import pandas as pd


def main():
    df = pd.read_csv("/Users/jnesnky/Desktop/untitled folder/Bakken/combinedfile.csv")


    # --- code cell ---

    d = df[df["County"] == "MCK"]


    # --- code cell ---

    d.shape


    # --- code cell ---

    df.shape


    # --- code cell ---

    d.to_csv("/Users/jnesnky/Desktop/untitled folder/Bakken/MCK.csv")


    # --- code cell ---

    d = df.copy()
    d.index("ReportDate", inplace=True)


    # --- code cell ---

    df_pivot = pd.pivot_table(
        df, index=df.index.month, columns=df.index.year, values="Data"
    )


    # --- code cell ---

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    # create fake time series dataframe
    index = pd.date_range(start="01-Jan-2012", end="01-01-2019", freq="M")
    data = np.random.randn(len(index))
    df = pd.DataFrame(data, index, columns=["Data"])

    # pivot to get by month in rows, then year in columns
    df_pivot = pd.pivot_table(
        df, index=df.index.month, columns=df.index.year, values="Data"
    )

    # plot
    ax = df_pivot.plot(title="Data by Year", figsize=(6, 4))
    ax.get_lines()[-1].set_linewidth(5)
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    ax.figure.tight_layout()
    plt.show()


    # --- code cell ---

    df_pivot.head()


    # --- code cell ---

    d_pivot = pd.pivot_table(
        d, index=d["ReportDate"], columns=d["WellName"], values=d["Oil"]
    )


    # --- code cell ---

    d.head()


if __name__ == "__main__":
    main()
