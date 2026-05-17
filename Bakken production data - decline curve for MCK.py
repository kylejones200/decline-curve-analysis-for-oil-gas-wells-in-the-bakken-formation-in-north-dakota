"""Generated from Jupyter notebook: Bakken production data - decline curve for MCK

Magics and shell lines are commented out. Run with a normal Python interpreter."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def notebook_step_001() -> None:
    df = pd.read_csv("data/bakken/combinedfile.csv")


def notebook_step_002() -> None:
    d = df[df["County"] == "MCK"]


def notebook_step_003() -> None:
    d.shape


def notebook_step_004() -> None:
    df.shape


def notebook_step_005() -> None:
    d.to_csv("data/bakken/MCK.csv")


def notebook_step_006() -> None:
    d = df.copy()

    d.index("ReportDate", inplace=True)


def notebook_step_007() -> None:
    df_pivot = pd.pivot_table(
        df, index=df.index.month, columns=df.index.year, values="Data"
    )


def create_fake_time_series_dataframe() -> None:
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


def notebook_step_009() -> None:
    df_pivot.head()


def notebook_step_010() -> None:
    d_pivot = pd.pivot_table(
        d, index=d["ReportDate"], columns=d["WellName"], values=d["Oil"]
    )


def notebook_step_011() -> None:
    d.head()


def main() -> None:
    notebook_step_001()
    notebook_step_002()
    notebook_step_003()
    notebook_step_004()
    notebook_step_005()
    notebook_step_006()
    notebook_step_007()
    create_fake_time_series_dataframe()
    notebook_step_009()
    notebook_step_010()
    notebook_step_011()


if __name__ == "__main__":
    main()
