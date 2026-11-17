# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "altair==6.3.0",
#     "marimo>=0.25.2",
#     "numpy==2.5.5",
#     "openpyxl==3.1.5",
#     "pandas==3.1.1",
#     "pingouin==0.7.0",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    import numpy as np
    import pingouin as pg

    return alt, mo, np, pd, pg


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Group 3 - What Drives Airbnb prices in Europe?
    **Members who contributed:**
    *Azmi Badjuber,Manavjot Singh,Ruchit Santosh Sanap*
    """)
    return


@app.cell
def _(pd):
    base_url = "https://docs.google.com/spreadsheets/d/"
    doc_id = "1ecopK6oyyb4d_7-QLrCr8YlgFrCetHU7-VQfnYej7JY/"
    format_doc = "export/format=excel"

    url = base_url + doc_id + format_doc

    excel_file = pd.ExcelFile(url)
    return (excel_file,)


@app.cell
def _(excel_file, pd):
    dfs = []

    for sheet in excel_file.sheet_names:
        _df = excel_file.parse(sheet)
        _df["city"] = sheet.split("_")[0]
        _df["type_of_day"] = sheet.split("_")[1]
        dfs.append(_df)

    df = pd.concat(dfs, ignore_index=True)
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Azmi Abubakar Badjuber**
    """)
    return


@app.cell
def _(mo):
    #selecting variable
    variable = mo.ui.dropdown(
            options={
                "room_type", 
                "city", 
                "type_of_day", 
                "cleanliness_rating"},
            value="city",
            label="Select Variable: "
        )
    return (variable,)


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "💡 Variable Selection Rationale (Criteria & Justification)": mo.md(r"""
    We selected four key variables based on the following criteria:

    1. **Room Type (`room_type`)**:
       * *Reason:* Acts as a primary structural driver of price. Entire homes/apartments naturally command a different pricing tier compared to private or shared rooms due to privacy and space.
    2. **City (`city`)**:
       * *Reason:* Captures geographical and macroeconomic variations across European destinations, as tourism demand and cost of living differ significantly between cities.
    3. **Type of Day (`type_of_day`)**:
       * *Reason:* Reflects short-term demand fluctuations between weekdays and weekends, which heavily impact travel pricing strategies.
    4. **Cleanliness Rating (`cleanliness_rating`)**:
       * *Reason:* Represents guest-perceived quality and service standards, which often correlate with property value and pricing premiums.
    """)
    })
    return


@app.cell
def _(df, np):
    #making log_price
    df['log_price'] = np.log(df['realSum'])
    return


@app.cell
def _(alt, df, mo, variable):
    #connecting variable with df by function
    try:
        selected_variable = variable.value
        cols_to_use = ["log_price", selected_variable]
        df_chart = df[cols_to_use].dropna()

    #Assisted by AI
    # samping
        if len(df_chart) > 5000:
            df_chart = df_chart.sample(n=5000, random_state=42)
    # making tittle's dicts
        titles = {
            "room_type": "Room Type",
            "city": "City",
            "type_of_day": "Type of Day",
            "cleanliness_rating": "Cleanliness Rating"
        }
        selected_title = titles.get(selected_variable, "Variable")

        # making altair boxplot
        chart = alt.Chart(df_chart).mark_boxplot().encode(
            x=alt.X(selected_variable, title=selected_title),
            y=alt.Y("log_price:Q", title="Log Price"),
            color=alt.X(f"{selected_variable}:N", legend=None)
        ).properties(
            title=f"Distribution of Log Price by {selected_title}",
            width=600,
            height=400
        )
        output = mo.ui.altair_chart(chart)
    except Exception as e:
        output = mo.callout(f"Error loading chart: {e}", kind="danger")

    output
    return


@app.cell
def _(variable):
    variable
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Ruchit Santosh Sanap**
    """)
    return


@app.cell
def _(df):
    _df = df.columns.tolist()
    return


@app.cell
def _(df):

    # ## Inspect variables for ANOVA 

    print("NUMERICAL VARIABLE SUMMARY")
    print(
        df[[
            "realSum",
            "log_price",
            "dist",
            "metro_dist",
            "cleanliness_rating"
        ]].describe().round(2)
    )

    print("\nCITY DISTRIBUTION")
    print(df["city"].value_counts())

    print("\nROOM TYPE DISTRIBUTION")
    print(df["room_type"].value_counts())

    print("\nMISSING VALUES")
    print(df.isna().sum())

    print("\nVARIABLE DATA TYPES")
    print(df[[
        "realSum",
        "log_price",
        "dist",
        "metro_dist",
        "cleanliness_rating",
        "city",
        "room_type"
    ]].dtypes)
    return


@app.cell
def _(df, np, pd):

    # ## Data Transformation: Distance Categories 

    # Divide distance from city centre into three categories
    dist_q1 = df["dist"].quantile(1/3)
    dist_q2 = df["dist"].quantile(2/3)

    df["dist_category"] = pd.cut(
        df["dist"],
        bins=[-np.inf, dist_q1, dist_q2, np.inf],
        labels=["Near", "Medium", "Far"]
    )

    # Divide distance from metro station into three categories
    metro_q1 = df["metro_dist"].quantile(1/3)
    metro_q2 = df["metro_dist"].quantile(2/3)

    df["metro_category"] = pd.cut(
        df["metro_dist"],
        bins=[-np.inf, metro_q1, metro_q2, np.inf],
        labels=["Near", "Medium", "Far"]
    )

    print("CITY CENTRE DISTANCE CATEGORIES")
    print(f"Near: up to {dist_q1:.2f} km")
    print(f"Medium: {dist_q1:.2f} to {dist_q2:.2f} km")
    print(f"Far: above {dist_q2:.2f} km")
    print(df["dist_category"].value_counts())

    print("\nMETRO DISTANCE CATEGORIES")
    print(f"Near: up to {metro_q1:.2f} km")
    print(f"Medium: {metro_q1:.2f} to {metro_q2:.2f} km")
    print(f"Far: above {metro_q2:.2f} km")
    print(df["metro_category"].value_counts())
    return


@app.cell
def _(df):
    ## Compare Average Prices Across Distance Categories - Ruchit

    print("CITY CENTRE DISTANCE")
    print(
        df.groupby("dist_category", observed=True)["log_price"]
        .agg(["count", "mean", "median"])
        .round(3)
    )

    print("\nMETRO DISTANCE")
    print(
        df.groupby("metro_category", observed=True)["log_price"]
        .agg(["count", "mean", "median"])
        .round(3)
    )
    return


@app.cell
def _(df, pg):
    ### ANOVA Assumption Checks: City - Used AI

    # 1. Check normality within each city
    city_normality = pg.normality(
        data=df,
        dv="log_price",
        group="city",
        method="normaltest"
    )

    print("NORMALITY TEST BY CITY")
    print(city_normality)

    # 2. Check equality of variances across cities
    city_variance = pg.homoscedasticity(
        data=df,
        dv="log_price",
        group="city",
        method="levene"
    )

    print("\nHOMOGENEITY OF VARIANCES")
    print(city_variance)

    # 3. Check sample sizes
    print("\nSAMPLE SIZES")
    print(df.groupby("city", observed=True)["log_price"].count())
    return


@app.cell
def _(df, pg):
    ### One-Way ANOVA: City

    city_anova = pg.anova(
        data=df,
        dv="log_price",
        between="city",
        detailed=True
    )

    print(city_anova)
    return


@app.cell
def _(df, pg):
    ### Welch ANOVA: City 

    city_welch = pg.welch_anova(
        data=df,
        dv="log_price",
        between="city"
    )

    print("WELCH ANOVA RESULTS")
    print(city_welch)
    return


@app.cell
def _(df):
    ### Average Airbnb Prices by City 

    city_prices = (
        df.groupby("city", observed=True)["log_price"]
        .agg(["count", "mean", "median"])
        .sort_values("mean", ascending=False)
    )

    print(city_prices.round(3))
    return


@app.cell
def _(df, pg):
    ### Post-hoc Comparisons: City

    city_posthoc = pg.pairwise_gameshowell(
        data=df,
        dv="log_price",
        between="city"
    )

    print(city_posthoc)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "City ANOVA – Interpretation": mo.md(r"""
    ### City ANOVA – Interpretation

    **Null hypothesis (H0):** The mean log Airbnb price is equal across all ten cities.

    The normality assumption was violated in nine out of ten cities. Levene's test also indicated unequal variances (p < 0.001). Therefore, Welch ANOVA was used as the primary test.

    Welch ANOVA showed a statistically significant difference in average log prices between cities (F = 2356.73, p < 0.001). The effect size was large (np2 = 0.281).

    Amsterdam had the highest average log price (6.191), followed by Paris (5.822) and London (5.639). Athens had the lowest (4.894).

    **Conclusion:** City is an important factor associated with Airbnb price variation.
    """)
    })
    return


@app.cell
def _(df, pg):
    ### ANOVA Assumption Checks: Room Type Used AI

    # Normality test
    room_normality = pg.normality(
        data=df,
        dv="log_price",
        group="room_type",
        method="normaltest"
    )

    print("NORMALITY TEST BY ROOM TYPE")
    print(room_normality)

    # Homogeneity of variances
    room_variance = pg.homoscedasticity(
        data=df,
        dv="log_price",
        group="room_type",
        method="levene"
    )

    print("\nHOMOGENEITY OF VARIANCES")
    print(room_variance)

    # Group sizes
    print("\nSAMPLE SIZES")
    print(df.groupby("room_type", observed=True)["log_price"].count())

    # Average prices
    print("\nAVERAGE PRICES")
    print(
        df.groupby("room_type", observed=True)["log_price"]
        .agg(["count", "mean", "median"])
        .round(3)
    )
    return


@app.cell
def _(df, pg):
    ### One-Way ANOVA: Room Type - Used AI

    room_anova = pg.anova(
        data=df,
        dv="log_price",
        between="room_type",
        detailed=True
    )

    print(room_anova)
    return


@app.cell
def _(df, pg):
    ### Alternative Tests: Room Type

    room_welch = pg.welch_anova(
        data=df,
        dv="log_price",
        between="room_type"
    )

    print("WELCH ANOVA")
    print(room_welch)

    room_kruskal = pg.kruskal(
        data=df,
        dv="log_price",
        between="room_type"
    )

    print("\nKRUSKAL-WALLIS TEST")
    print(room_kruskal)
    return


@app.cell
def _(df, pg):
    ### Games-Howell Post-hoc Test: Room Type

    room_posthoc = pg.pairwise_gameshowell(
        data=df,
        dv="log_price",
        between="room_type"
    )

    print(room_posthoc.round(4))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Room Type ANOVA – Interpretation": mo.md(r"""
    ## Room Type ANOVA – Interpretation

    **Null Hypothesis (H₀):** The mean log prices are equal across entire homes/apartments, private rooms, and shared rooms.

    The normality assumption was violated for all three room types, and Levene's test indicated unequal variances (p < .001). Therefore, Welch ANOVA was used as the primary test, supported by the Kruskal-Wallis test.

    Welch ANOVA showed a statistically significant difference in log prices between room types (F(2, 989.36) = 3635.28, p < .001, np2 = 0.110). The Kruskal-Wallis test confirmed this result (H(2) = 6345.39, p < .001).

    The Games-Howell post-hoc test showed that all three pairs differed significantly (p < .001). Entire homes/apartments had the highest mean log price (5.569), followed by private rooms (5.168) and shared rooms (4.866).

    The effect size (np2 = 0.110) indicates a meaningful association between room type and price. Overall, room type is an important factor associated with Airbnb listing prices.
    """)
    })
    return


@app.cell
def _(df, pg):
    # ## ANOVA Assumption Checks: Distance Category 

    dist_normality = pg.normality(
        data=df,
        dv="log_price",
        group="dist_category",
        method="normaltest"
    )

    print("NORMALITY TEST")
    print(dist_normality)

    dist_variance = pg.homoscedasticity(
        data=df,
        dv="log_price",
        group="dist_category",
        method="levene"
    )

    print("\nHOMOGENEITY OF VARIANCES")
    print(dist_variance)

    print("\nSAMPLE SIZES AND MEAN PRICES")
    print(
        df.groupby("dist_category", observed=True)["log_price"]
        .agg(["count", "mean", "median"])
        .round(3)
    )
    return


@app.cell
def _(df, pg):
    # ## Alternative Tests: Distance Category

    dist_welch = pg.welch_anova(
        data=df,
        dv="log_price",
        between="dist_category"
    )

    print("WELCH ANOVA")
    print(dist_welch)

    dist_kruskal = pg.kruskal(
        data=df,
        dv="log_price",
        between="dist_category"
    )

    print("\nKRUSKAL-WALLIS TEST")
    print(dist_kruskal)
    return


@app.cell
def _(df, pg):
    # ## Games-Howell Post-hoc Test: Distance Category

    dist_posthoc = pg.pairwise_gameshowell(
        data=df,
        dv="log_price",
        between="dist_category"
    )

    print(dist_posthoc.round(4))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({ "Distance Category ANOVA – Interpretation": mo.md(r"""
    ## Distance Category ANOVA – Interpretation

    **Null Hypothesis (H₀):** The mean log prices are equal across Near, Medium, and Far distance categories.

    Normality was violated in all three groups (p < .001), and Levene's test indicated unequal variances (p = .0094). Therefore, Welch ANOVA was used as the primary test, supported by the Kruskal-Wallis test.

    Welch ANOVA showed a statistically significant difference in log prices between distance categories (F(2, 34467.51) = 43.63, p < .001, np2 = 0.00167). The Kruskal-Wallis test supported this result (H(2) = 101.49, p < .001).

    The Games-Howell post-hoc test showed significant differences between all three pairs: Near vs Medium, Near vs Far, and Medium vs Far (all p < .001). Near listings had the highest mean log price (5.449), while Far listings had the lowest (5.389).

    However, the effect size was extremely small (np2 = 0.00167), and all Hedges' g values were small. Therefore, although the differences are statistically significant, distance category has only a very small practical association with Airbnb prices in this dataset.
    """)

    } 
    )
    return


@app.cell
def _(df, pg):
    # ## ANOVA Assumption Checks: Metro Category 
    metro_normality = pg.normality(
        data=df,
        dv="log_price",
        group="metro_category",
        method="normaltest"
    )

    print("NORMALITY TEST")
    print(metro_normality)

    metro_variance = pg.homoscedasticity(
        data=df,
        dv="log_price",
        group="metro_category",
        method="levene"
    )

    print("\nHOMOGENEITY OF VARIANCES")
    print(metro_variance)

    print("\nSAMPLE SIZES AND MEAN PRICES")
    print(
        df.groupby("metro_category", observed=True)["log_price"]
        .agg(["count", "mean", "median"])
        .round(3)
    )
    return


@app.cell
def _(df, pg):
    # ## Alternative Tests: Metro Category 

    metro_welch = pg.welch_anova(
        data=df,
        dv="log_price",
        between="metro_category"
    )

    print("WELCH ANOVA")
    print(metro_welch)

    metro_kruskal = pg.kruskal(
        data=df,
        dv="log_price",
        between="metro_category"
    )

    print("\nKRUSKAL-WALLIS TEST")
    print(metro_kruskal)
    return


@app.cell
def _(df, pg):
    # ## Games-Howell Post-hoc Test: Metro Category 

    metro_posthoc = pg.pairwise_gameshowell(
        data=df,
        dv="log_price",
        between="metro_category"
    )

    print(metro_posthoc.round(4))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "Metro Category ANOVA – Interpretation": mo.md(r"""
    ## Metro Category ANOVA – Interpretation

    **Null Hypothesis (H₀):** The mean log prices are equal across Near, Medium, and Far metro-distance categories.

    Normality was violated in all three groups (p < .001), and Levene's test indicated unequal variances (p < .001). Therefore, Welch ANOVA was used as the primary test, supported by the Kruskal-Wallis test.

    Welch ANOVA showed a statistically significant difference in log prices between metro-distance categories (F(2, 34452.64) = 402.80, p < .001, np2 = 0.01535). The Kruskal-Wallis test supported this result (H(2) = 858.45, p < .001).

    The Games-Howell post-hoc test showed significant differences between all three pairs (p < .001). Near-metro listings had the highest mean log price (5.519), followed by Medium (5.397) and Far (5.343).

    The effect size (np2 = 0.01535) indicates a relatively small association between metro distance and Airbnb prices. The largest pairwise difference was between Near and Far (mean difference = 0.1766, Hedges' g = 0.3001).

    Overall, listings closer to metro stations tend to have higher prices, although the practical effect is relatively small.
    """)
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Manavjot Singh**
    """)
    return


@app.cell
def _(df, pd):
    two_way_data = df[["log_price", "city", "room_type"]].dropna()
    cell_counts = pd.crosstab(two_way_data["city"], two_way_data["room_type"])
    return (two_way_data,)


@app.cell
def _(mo, pg, two_way_data):
    df1 = two_way_data.assign(group=two_way_data["city"] + " | " + two_way_data["room_type"])
    big = df1.groupby("group")["log_price"].transform("size") >= 8
    two_way_levene = pg.homoscedasticity(df1, dv="log_price", group="group", method="levene")
    two_way_normal = pg.normality(df1[big], dv="log_price", group="group", method="normaltest")
    mo.accordion({"Assumption checks: Levene and normality tests": mo.vstack([two_way_levene, two_way_normal])})
    return


@app.cell
def _(mo):
    mo.accordion({
      "Two-way ANOVA (city and room type): assumptions"  : mo.md(r"""
    ### Two-way ANOVA (city and room type): assumptions

    **Normality:** 25 of the 30 city and room type groups fail the normality test.

    **Equal variances:** Levene's test is significant (W = 51.70, p < .001).

    **Group sizes:** Entire homes have between 542 and 5,561 listings per city, but shared rooms only 10–16 in six cities. This makes the ANOVA more sensitive to unequal variances, so results about shared rooms within a single city are less reliable.
    """)
    })
    return


@app.cell
def _(mo, pg, two_way_data):
    # two way anova
    two_way = pg.anova(
        data=two_way_data, dv="log_price",
        between=["city", "room_type"], detailed=True,
    ).round(4)

    #rank based check
    two_way_rank = pg.anova(
        data=two_way_data.assign(rank_price=two_way_data["log_price"].rank()),
        dv="rank_price", between=["city", "room_type"], detailed=True,
    ).round(4)

    mo.vstack([mo.md("**Two-way ANOVA (log price)**"), two_way,
                mo.accordion({"Robustness check (ranked price)": two_way_rank}),])
    return two_way, two_way_rank


@app.cell
def _(alt, two_way_data):
    m = two_way_data.groupby(["city", "room_type"], as_index=False)["log_price"].mean()
    alt.Chart(m).mark_line(point=True).encode(
        x="city:N",
        y=alt.Y("log_price:Q", title="Mean log price", scale=alt.Scale(zero=False)),
        color="room_type:N",
    ).properties(height=350, width=600, title="Mean log price by city and room type")
    return


@app.cell
def _(two_way, two_way_rank):
    np2 = two_way.set_index("Source")["np2"]
    np2r = two_way_rank.set_index("Source")["np2"]
    return np2, np2r


@app.cell
def _(mo, np2, np2r):
    mo.accordion({
       "Two way ANOVA (city and room type): hypotheses and interpretation" : mo.md(f"""
    ### Two way ANOVA (city and room type): hypotheses and interpretation

    **Null hypotheses (H0):**
    1. **City:** the mean log price is the same in all ten cities.
    2. **Room type:** the mean log price is the same for entire homes, private rooms and shared rooms.
    3. **Interaction:** the effect of room type on price does not depend on the city.

    **Result:** all three H0 are rejected (p < .001). The ranked-price check gives the same picture
    (np2: city {np2r["city"]:.2f}, room type {np2r["room_type"]:.2f}, interaction {np2r["city * room_type"]:.2f}).

    The city a listing is in matters most for its price (np2 = {np2["city"]:.2f}), and the type of room matters a lot too (np2 = {np2["room_type"]:.2f}): entire homes are the most expensive, private rooms cost less, and shared rooms are the cheapest in almost every city. How much cheaper a room is than a whole home depends a little on the city (np2 = {np2["city * room_type"]:.2f}).

    """)
    })
    return


@app.cell
def _(mo):
    opts = ["city", "room_type", "type_of_day", "dist_category", "metro_category"]
    factor_a = mo.ui.dropdown(opts, value="city", label="Factor A: ")
    factor_b = mo.ui.dropdown(opts, value="type_of_day", label="Factor B: ")
    mo.hstack([factor_a, factor_b], justify="start")
    return factor_a, factor_b


@app.cell
def _(alt, df, factor_a, factor_b, mo, pg):
    ## AI assisted
    def _order(v):
        return ["Near", "Medium", "Far"] if v.endswith("_category") else "ascending"

    if factor_a.value == factor_b.value:
        custom_out = mo.callout("Please choose two different factors.", kind="warn")
    else:
        _a, _b = factor_a.value, factor_b.value
        _d = df[["log_price", _a, _b]].dropna().astype({_a: str, _b: str})
        if _d.empty:
            custom_out = mo.callout("No data for this combination.", kind="warn")
        else:
            _t = pg.anova(data=_d, dv="log_price", between=[_a, _b], detailed=True).round(4)
            _np = _t.set_index("Source")["np2"]
            _g = _d[_a] + " | " + _d[_b]
            _p = pg.homoscedasticity(_d.assign(g=_g), dv="log_price", group="g", method="levene")["pval"].iloc[0]
            _n = _g.value_counts()
            _inter = f"{_a} * {_b}"

            _m = _d.groupby([_a, _b], as_index=False)["log_price"].mean()
            _chart = alt.Chart(_m).mark_line(point=True).encode(
                x=alt.X(f"{_a}:N", title=_a, sort=_order(_a)),
                y=alt.Y("log_price:Q", title="Mean log price", scale=alt.Scale(zero=False)),
                color=alt.Color(f"{_b}:N", title=_b, sort=_order(_b)),
                tooltip=[_a, _b, alt.Tooltip("log_price:Q", format=".2f", title="Mean log price")],
            ).properties(height=350, width=550, title=f"Mean log price by {_a} and {_b}")

            custom_out = mo.vstack([
                _t,
                _chart,
                mo.md(f"""
    `{_a}` explains {_np[_a]:.0%} of the price variation left over after both factors, `{_b}` explains {_np[_b]:.0%}, and their interaction {_np[_inter]:.0%} (np2). **{_a if _np[_a] > _np[_b] else _b} matters more.** If the lines in the chart are far from parallel, the effect of `{_b}` depends on `{_a}`.
    """),
                mo.accordion({
                    "Hypotheses and assumptions": mo.md(f"""
    **H0:** (1) mean log price is the same across all `{_a}` groups; (2) the same across all `{_b}` groups; (3) no interaction: the effect of `{_a}` does not depend on `{_b}`.

    **Assumptions:** Levene's test p = {_p:.4f} ({"equal variances violated" if _p < 0.05 else "equal variances OK"}). Group sizes range from {_n.min()} to {_n.max()} listings, so unequal group sizes make the test more sensitive to unequal variances. With this many listings, normality is almost always rejected, so treat the results as a good guide, not exact.
    """)
                }),
            ])

    custom_out
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
