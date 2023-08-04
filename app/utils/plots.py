import numpy as np
import os
import pandas as pd

from matplotlib.figure import Figure


class BasePlot:

    def __init__(self, path):

        self.path = path
        self.fig = Figure()
        self.ax = self.fig.subplots()
        self.xticks_positions = []
        self.bar_width = 0
        self.bar_coordinates = []

    def _set_graph_layout(self, number_of_bar_labels, number_of_x_labels):

        self.xticks_positions = np.arange(number_of_x_labels)
        self.bar_width = 0.85/ number_of_bar_labels
        shift = (number_of_bar_labels - 1) / 2

        for n in range(number_of_bar_labels):

            coordinates = self.xticks_positions + self.bar_width * (n - shift) 
            self.bar_coordinates.append(coordinates)

    def _savefigure(self, suffix):

        filename = os.path.splitext(self.path)[0] + suffix
        self.fig.savefig(filename, bbox_inches="tight")
        # path_no_extension = os.path.splitext(self.path)[0]
        # self.fig.savefig(path_no_extension + suffix, bbox_inches="tight")


class TablePlot(BasePlot):
    
    # Table output from KAT:

    #     Sample   kmer_size Reference hits percentage
    #     Sample1    20        Ref1      5     0.05
    #     Sample2    20        Ref1      2     0.001
    #     Sample1    20        Ref2     100    0.1
    #     Sample2    20        Ref2      0     0.0

    def __init__(self, path):

        super().__init__(path)
        self.df = pd.read_csv(path, delimiter = ',')
        self.sample_col_ix = 0
        self.reference_col_ix = 2
        self.sample_labels = []
        self.reference_lables = []
        self.columns = []

    def plot(self, column=""):

        self.sample_labels = self._get_labels(self.sample_col_ix)
        self.reference_labels = self._get_labels(self.reference_col_ix)
        self._set_graph_layout(len(self.sample_labels), len(self.reference_labels))
        self._plot_data(column)
        self._add_legend(column)

    def save(self, suffix=""):

        self._savefigure(suffix)

    def _get_labels(self, index):

        column_label = self.df.columns[index]

        return self.df[column_label].unique().tolist()

    def _plot_data(self, column):

        self.ax.clear()

        for n in range(len(self.sample_labels)):

            sample = self.sample_labels[n]
            column_label = self.df.columns[self.sample_col_ix]
            data = self.df.loc[self.df[column_label] == sample, column].tolist()
            self.ax.bar(self.bar_coordinates[n], data, self.bar_width, label=sample)
            # self._plot_sample(data, n, sample)

    # def _plot_sample(self, data, n, sample_name):

    #     self.ax.bar(self.bar_coordinates[n], data, self.bar_width, label=sample_name)

    def _add_legend(self, column):
        
        self.ax.set_ylabel(column)
        self.ax.set_xticks(self.xticks_positions)
        self.ax.set_xticklabels(self.reference_labels, rotation=45)
        self.ax.legend()
        
    