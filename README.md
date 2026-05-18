# Decline Curve Analysis for Oil Gas Wells in the Bakken Formation in North Dakota

Published: 2025-02-12
Medium: [https://medium.com/@kyle-t-jones/decline-curve-analysis-for-oil-gas-wells-in-the-bakken-formation-in-north-dakota-ce4cbccb91e8](https://medium.com/@kyle-t-jones/decline-curve-analysis-for-oil-gas-wells-in-the-bakken-formation-in-north-dakota-ce4cbccb91e8)

## Business context

Decline curve analysis is a technique in petroleum engineering used to predict how wells will produce over time. This approach helps operators and investors understand which companies are managing their assets most effectively. Using publicly available production data from the State of North Dakota, we can fit mathematical models to well output and rank operators based on their long-term production potential.

Our analysis began with data from the North Dakota Monthly Production Report Index. This dataset provides well-level production statistics, including oil, gas, and water output, as well as details on well operators. Since our objective was to assess production trends across operators, we first structured the data by extracting relevant fields, converting date formats, and aggregating monthly production figures. Given that our data started in January 2016, we did not have the true initial production rates for many wells. Instead, we worked with available data to fit decline curves based on observed production trends.

To model decline behavior, we chose the hyperbolic decline model which captures gradual slowdowns typical of unconventional wells. This model accounts for a higher initial drop-off followed by a more stable production period than exponential decline, making it well-suited for the Bakken's shale oil formations. The hyperbolic equation relies on three parameters: an estimated initial production rate, an initial decline rate, and a b-factor, which governs how decline slows over time. We fit this model to each well's monthly production data and derived these parameters for each well that has at least five months of production.

## About

Place the code for this article in this repository.
The original article export is saved as `article.md`.

## Files

Add your `.ipynb`, `.py`, `.yaml`, `.js`, `.ts`, or other project files here.

## Disclaimer

Educational/demo code only. Not financial, safety, or engineering advice. Use at your own risk. Verify results independently before any production or operational use.

## License

MIT — see [LICENSE](LICENSE).