import numpy
import matplotlib.pyplot as pyplot
import seaborn


colors = ["blue", "green", "orange", "magenta", "gray"]
cat_cols = ["TaskName", "Category"]
num_cols = ["TimeSpentMins", "DifficultyRate", "NecessityRate", "FunRate"]
style = "whitegrid"
shapes = ["+", "o", "s", "x", "^"]


class Chart:
    def __init__(self, tasks, col, ylabel="number of tasks", title1="number tasks by ", title2="", coly="", bins=6, sizex=6,
                 sizey=6, colshape="", colsize="", colcolor="", alpha=1.0, hist=False):
        self.tasks = tasks
        self.col = col
        self.bins = bins
        self.fig = pyplot.figure(figsize=(sizex, sizey))
        self.axis = self.fig.gca()
        self.counts = 0
        self.title = title1 + coly + title2 + col
        self.ylabel = ylabel
        self.hist = hist
        self.alpha = alpha
        self.colshape = colshape
        self.colsize = colsize
        self.colcolor = colcolor
        self.coly = coly
        if (self.col in num_cols) or (self.col in cat_cols):
            self.counts = tasks[self.col].value_counts()

    def get_header(self):
        # tasks.drop(["TaskNum"], axis=1, inplace=True)  # dropping this field because it is not a feature
        a = [self.tasks.shape, self.tasks.head()]
        return a

    def get_freq(self):
        if self.col == "nums":
            return self.tasks.describe()
        else:
            return self.counts

    def class_imbalance(self):
        cat_counts = self.tasks[["Category"]].groupby("Category").count()
        print(cat_counts)

    def bar(self):
        self.counts.plot.bar(ax=self.axis, color=colors[0])
        return

    def kde(self):
        seaborn.set_style(style)
        seaborn.distplot(self.tasks[self.col], bins=self.bins, rug=True, hist=self.hist)
        return

    def scatter(self):
        seaborn.set_style(style)
        unique_cats = self.tasks[self.colshape].unique()
        unique_colors = self.tasks[self.colcolor].unique()

        for i, cat in enumerate(unique_cats):
            for j, color in enumerate(unique_colors):
                temp = self.tasks[(self.tasks[self.colshape] == cat) & (self.tasks[self.colcolor] == color)]
                seaborn.regplot(self.col, self.coly, data=temp, marker=shapes[i],
                                scatter_kws={"alpha": self.alpha, "s": 0.000025*temp[self.colsize]**2},
                                label=[cat, " and ", color], fit_reg=False, color=colors[j])

        self.tasks.plot.scatter(x=self.col, y=self.coly, ax=self.axis, alpha=self.alpha)
        return

    def contour(self):
        seaborn.set_style(style)
        seaborn.jointplot(self.col, self.coly, data=self.tasks, kind="kde")
        return

    def box(self):
        seaborn.set_style(style)
        seaborn.boxplot(self.col, self.coly, data=self.tasks)
        return

    def violin_basic(self):
        seaborn.set_style(style)
        seaborn.violinplot(self.col, self.coly, data=self.tasks)
        return

    def violin_advanced(self):
        seaborn.set_style(style)
        seaborn.violinplot(self.col, self.coly, data=self.tasks, hue_col=self.colcolor, split=True)
        return

    def pairplot(self):
        seaborn.pairplot(self.tasks[num_cols], hue=self.col, palette="Set2", diag_kind="kde",
                         size=2).map_upper(seaborn.kdeplot, cmap="Blues_d")
        return

    def facetplot_grid(self):
        grid = seaborn.FacetGrid(self.tasks, col=self.coly)
        grid.map(pyplot.hist, self.col, alpha=.7)
        return self.coly

    def facetplot_row(self):
        grid = seaborn.FacetGrid(self.tasks, row=self.coly, hue=self.colcolor, palette="Set2", margin_titles=True)
        grid.map(seaborn.regplot, self.col, "", fit_reg=False)
        return self.coly

    def barsubplot(self):
        self.tasks["dummy"] = numpy.ones(shape=self.tasks.shape[0])
        self.counts = self.tasks[["dummy", self.coly, self.col]].groupby([self.coly, self.col], as_index=False).count()
        temp = self.counts[self.counts[self.coly] == 0][[self.col, "dummy"]]
        pyplot.subplot(1, 2, 1)
        temp = self.counts[self.counts[self.coly] == 0][[self.col, "dummy"]]
        pyplot.bar(temp[self.col], temp.dummy)
        pyplot.xticks(rotation=90)
        pyplot.title("Counts for " + self.col + "\n" + self.coly)
        pyplot.ylabel("count")
        pyplot.subplot(1, 2, 2)
        temp = self.counts[self.counts[self.coly] == 1][[self.col, "dummy"]]
        pyplot.bar(temp[self.col], temp.dummy)
        pyplot.xticks(rotation=90)
        pyplot.title("Counts for " + self.col + "\n" + self.colshape)
        pyplot.ylabel("count")
        pyplot.show()

    def show_chart_axis(self):
        self.axis.set_title(self.title + self.col)
        self.axis.set_xlabel(self.col)
        self.axis.set_ylabel(self.ylabel)

        # legend is probably not needed here
        pyplot.legend()
        pyplot.show()
        return

    def show_chart_pyplot(self):
        pyplot.title(self.title + self.col)
        pyplot.xlabel(self.col)
        pyplot.ylabel(self.ylabel)

        # legend may only be needed when shapes[] is used
        pyplot.legend()
        pyplot.show()


def main_menu(item, tasks):
    if item == 0:
        cat = cat_menu("all")
        c = Chart(tasks, cat)
        print(c.get_header(), "\n")
    elif item == 1:
        print("Look for class imbalance, especially on category columns.")
        print("Class imbalance is unequal numbers of cases.")
        cat = cat_menu("all")
        c = Chart(tasks, cat)
        print(c.get_freq(), "\n")
    elif item == 2:
        # the column can be any individual column
        cat = cat_menu("both")
        c = Chart(tasks, cat)
        c.bar()
        c.show_chart_axis()
    elif item == 3:
        cat = cat_menu("num")
        c = Chart(tasks, cat, title1="Histogram of ")
        c.kde()
        c.show_chart_pyplot()
    elif item == 4:
        cat = cat_menu("num")
        c = Chart(tasks, cat, title1="Histogram of ", bins=20, hist=True, alpha=0.2)
        c.kde()
        c.show_chart_pyplot()
    elif item == 5:
        # get alpha from user
        # scatter plot needs work
        cat = cat_menu("num")
        coly = cat_menu("num")
        shape = cat_menu("num")
        size = cat_menu("num")
        color = cat_menu("num")
        alpha = 0.2
        c = Chart(tasks, cat, ylabel=coly, alpha=alpha, title1="Scater plot of ", coly=coly, title2=" vs. ", sizex=7,
                  colshape=shape, colsize=size, colcolor=color)
        c.scatter()
        c.show_chart_axis()
    elif item == 6:
        # can try cat and coly as "both" when text categories get converted to numeric values
        # 2 windows open but 1 of them is empty
        cat = cat_menu("num")
        coly = cat_menu("num")
        c = Chart(tasks, cat, ylabel=coly, coly=coly)
        c.contour()
        c.show_chart_pyplot()
    elif item == 7:
        print("Is there sufficient differences in the quartiles for the feature to be useful in separation of the"
              " label classes? Look also at the violin plot for the answer to this question.")
        # x = category column, y = numeric column
        cat = cat_menu("cat")
        coly = cat_menu("num")
        c = Chart(tasks, cat, ylabel=coly, coly=coly)
        c.box()
        c.show_chart_pyplot()
    elif item == 8:
        print("Is there sufficient differences in the quartiles for the feature to be useful in separation of the"
              " label classes? Look also at the box plot for the answer to this question.")
        # get colcolor from user to use for hue_col (should be cat_col) on c.violin_advanced()
        # x = category column, y = numeric column
        cat = cat_menu("cat")
        coly = cat_menu("num")
        c = Chart(tasks, cat, ylabel=coly, coly=coly)
        c.violin_basic()
        c.show_chart_pyplot()
    elif item == 9:
        # gets an error
        cat = cat_menu("cat")
        c = Chart(tasks, cat)
        c.pairplot()
    elif item == 10:
        # needs work
        cat = cat_menu("num")
        coly = cat_menu("num")
        c = Chart(tasks, cat, coly=coly)
        c.facetplot_grid()
    elif item == 11:
        # needs work
        cat = cat_menu("num")
        c = Chart(tasks, cat)
        c.facetplot_row()
    elif item == 12:
        # gets an error
        # need coly
        # this might need coly to be a column with exactly 2 values (to compare)
        cat = cat_menu("cat")
        coly = cat_menu("cat")
        c = Chart(tasks, cat, sizex=10, sizey=4, coly=coly)
        c.barsubplot()
        c.show_chart_pyplot()
    elif item == 13:
        cat = cat_menu("all")
        c = Chart(tasks, cat)
        c.class_imbalance()

    return


def cat_menu(group):
    col = ""
    if group != "num":  # group == "cat" || group == "both" || group == "all"
        print("0 - TaskName\n",
              "1 - Category")
    if group != "cat":  # group == "num" || group == "both" || group == "all"
        print("2 - TimeSpentMins\n",
              "3 - DifficultyRate\n",
              "4 - NecessityRate\n",
              "5 - FunRate")
    if group == "all":
        print("6 - all nums")

    item = int(input("select option: "))

    if item == 0:
        col = "TaskName"
    elif item == 1:
        col = "Category"
    elif item == 2:
        col = "TimeSpentMins"
    elif item == 3:
        col = "DifficultyRate"
    elif item == 4:
        col = "NecessityRate"
    elif item == 5:
        col = "FunRate"
    elif item == 6:
        col = "nums"

    return col
