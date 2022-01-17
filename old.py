from inspect import isframe
import seaborn as sns


def create_hist(df):
    custom_params = {
        "axes.spines.left": False,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.grid": False,
    }
    with sns.axes_style("whitegrid", rc=custom_params):
        # loop over the numeric columns
        for col in df.dtypes[df.dtypes != "object"].index.tolist():
            g = sns.histplot(x=df[col])
            fig = g.get_figure()
            fig.savefig(f"./img/hist_{col}.png")


def main():
    df = sns.load_dataset("penguins")
    create_hist(df)


if __name__ == "__main__":
    main()
