#!/usr/bin/env python2.7
# coding: utf-8
"""Tool to filter, organize, compare and display benchmarking results. Usefull
for smaller datasets. It works great with a few dozen runs.
Requires the pandas library to be installed."""
from __future__ import print_function
import argparse
import json
import math
import numbers
import os.path
import pandas as pd
import re
import sys

VERBOSE = True


def _read_lit_json(filename):
    jsondata = json.load(open(filename))
    columns = []
    columnindexes = {}
    names = set()
    info_columns = ['hash']
    # Pass1: Figure out metrics (= the column index)
    if 'tests' not in jsondata:
        sys.stderr.write("%s: Could not find toplevel 'tests' key\n")
        sys.exit(1)
    for test in jsondata['tests']:
        name = test.get("name")
        if name is None:
            sys.stderr.write("Error: Found unnamed test\n" % name)
            sys.exit(1)
        if name in names:
            sys.stderr.write("Error: Multiple tests with name '%s'\n" % name)
            sys.exit(1)
        names.add(name)
        if "metrics" not in test:
            sys.stderr.write("Warning: '%s' has No metrics!\n" % name)
            continue
        for name in test["metrics"].keys():
            if name not in columnindexes:
                columnindexes[name] = len(columns)
                columns.append(name)
        for name in test.keys():
            if name not in columnindexes and name in info_columns:
                columnindexes[name] = len(columns)
                columns.append(name)

    # Pass2 actual data construction
    nan = float('NaN')
    data = []
    testnames = []
    for test in jsondata['tests']:
        name = test['name']
        if 'shortname' in test:
            name = test['shortname']
        testnames.append(name)

        datarow = [nan] * len(columns)
        if "metrics" in test:
            for (metricname, value) in test['metrics'].iteritems():
                datarow[columnindexes[metricname]] = value
        for (name, value) in test.iteritems():
            index = columnindexes.get(name)
            if index is not None:
                datarow[index] = test[name]
        data.append(datarow)
    row_index = pd.Index(testnames, name='Program')
    column_index = pd.Index(columns, name='Metric')
    return pd.DataFrame(data=data, index=row_index, columns=column_index)


def _read_report_simple_csv(filename):
    return pd.read_csv(filename, na_values=['*'], index_col=0, header=0)


def _read(name):
    if name.endswith(".json"):
        return _read_lit_json(name)
    if name.endswith(".csv"):
        return _read_report_simple_csv(name)
    raise Exception("Cannot determine file format")


def _readmulti(filenames):
    # Read datasets
    datasetnames = []
    datasets = []
    prev_index = None
    for filename in filenames:
        data = _read(filename)
        name = os.path.basename(filename)
        # drop .json/.csv suffix; TODO: Should we rather do this in the
        # printing logic?
        for ext in ['.csv', '.json']:
            if name.endswith(ext):
                name = name[:-len(ext)]
        datasets.append(data)
        suffix = ""
        count = 0
        while True:
            if name+suffix not in datasetnames:
                break
            suffix = str(count)
            count += 1

        datasetnames.append(name+suffix)
        # Warn if index names are different
        if prev_index is not None and prev_index.name != data.index.name:
            sys.stderr.write("Warning: Mismatched index names: '%s' vs '%s'\n"
                             % (prev_index.name, data.index.name))
        prev_index = data.index
    # Merge datasets
    row_index_name = datasets[0].index.name
    data = pd.concat(datasets, axis=1, names=['File'], keys=datasetnames,
                     sort=True)
    data.index.name = row_index_name
    return data


def _add_diff_column(data, absolute_diff=False):
    files = data.columns.get_level_values('File').drop_duplicates()
    if len(files) <= 1:
        return data

    metrics = data.columns.get_level_values('Metric').drop_duplicates()
    for metric in metrics:
        if len(files) == 2:
            values0 = data[(files[0], metric)]
            values1 = data[(files[1], metric)]
        else:
            values0 = data.min(axis=1)
            values1 = data.max(axis=1)

        # Quotient or absolute difference?
        column_name = (u"", u"Δ %s" % metric)
        if absolute_diff:
            data[column_name] = values1 - values0
        else:
            data[column_name] = values1 / values0
            data[column_name] -= 1.0
    return data


def _filter_failed(data, key='Exec'):
    return data.loc[data[key] == "pass"]


def _filter_short(data, key='Exec_Time', threshold=0.6):
    return data.loc[data[key] >= threshold]


def _filter_same_hash(data, key='hash'):
    assert key in data.columns
    assert data.index.get_level_values(0).nunique() > 1

    return data.groupby(level=1).filter(lambda x: x[key].nunique() != 1)


def _filter_blacklist(data, blacklist):
    return data.loc[~(data.index.get_level_values(1).isin(blacklist))]


def _print_filter_stats(reason, before, after):
    n_before = len(before.groupby(level=1))
    n_after = len(after.groupby(level=1))
    n_filtered = n_before - n_after
    if VERBOSE and n_filtered != 0:
        print("%s: %s (filtered out)" % (reason, n_filtered))


# Truncate a string to a maximum length by keeping a prefix, a suffix and ...
# in the middle
def _truncate(string, prefix_len, suffix_len):
    return re.sub("^(.{%d}).*(.{%d})$" % (prefix_len, suffix_len),
                  "\g<1>...\g<2>", string)


# Search for common prefixes and suffixes in a list of names and return
# a (prefix,suffix) tuple that specifies how many characters can be dropped
# for the prefix/suffix. The numbers will be small enough that no name will
# become shorter than min_len characters.
def _determine_common_prefix_suffix(names, min_len=8):
    if len(names) <= 1:
        return (0, 0)
    name0 = names[0]
    prefix = name0
    prefix_len = len(name0)
    suffix = name0
    suffix_len = len(name0)
    shortest_name = len(name0)
    for name in names:
        if len(name) < shortest_name:
            shortest_name = len(name)
        while prefix_len > 0 and name[:prefix_len] != prefix:
            prefix_len -= 1
            prefix = name0[:prefix_len]
        while suffix_len > 0 and name[-suffix_len:] != suffix:
            suffix_len -= 1
            suffix = name0[-suffix_len:]

    if suffix[0] != '.' and suffix[0] != '_':
        suffix_len = 0
    suffix_len = max(0, min(shortest_name - prefix_len - min_len, suffix_len))
    prefix_len = max(0, min(shortest_name - suffix_len, prefix_len))
    return (prefix_len, suffix_len)


def _format_diff(value):
    if math.isnan(value):
        return ""
    if not isinstance(value, numbers.Integral):
        return "%4.1f%%" % (value * 100.)
    else:
        return "%-5d" % value


def _sort_data(data, sortkey='diff'):
    # sort (TODO: is there a more elegant way than create+drop a column?)
    data['$sortkey'] = data[sortkey].abs()
    data = data.sort_values("$sortkey", ascending=False)
    del data['$sortkey']
    return data


def _print_result(data, limit_output, shorten_names):
    printdata = data
    if limit_output:
        printdata = printdata.head(limit_output)

    formatters = dict()
    if shorten_names:
        drop_prefix, drop_suffix = \
                _determine_common_prefix_suffix(printdata.index)

        def format_index(name, common_prefix, common_suffix):
            name = name[common_prefix:]
            if common_suffix > 0:
                name = name[:-common_suffix]
            return _truncate(name, 10, 30)

        formatters['__index__'] = lambda name: format_index(name, drop_prefix,
                                                            drop_suffix)
    for n in data.columns:
        if n[1].startswith(u'Δ'):
            formatters[n] = _format_diff

    def float_format(x):
        if math.isnan(x):
            return ""
        return "%6.2f" % x
    out = printdata.to_string(justify='right',
                              float_format=float_format, formatters=formatters)
    print(out)
    print("")
    print(data.describe().to_string(header=False, justify='right',
                                    na_rep=''))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='compare.py')
    parser.add_argument('-a', '--all', action='store_true')
    parser.add_argument('-f', '--full', action='store_true')
    parser.add_argument('-m', '--metric', action='append', dest='metrics',
                        default=[])
    parser.add_argument('--all-metrics', action='store_true')
    parser.add_argument('--nodiff', action='store_false', dest='show_diff',
                        default=None)
    parser.add_argument('--diff', action='store_true', dest='show_diff')
    parser.add_argument('--filter-short', action='store_true',
                        dest='filter_short')
    parser.add_argument('--no-filter-failed', action='store_false',
                        dest='filter_failed', default=True)
    parser.add_argument('--filter-hash', action='store_true',
                        dest='filter_hash', default=False)
    parser.add_argument('--filter-blacklist',
                        dest='filter_blacklist', default=None)
    parser.add_argument('--merge-average', action='store_const',
                        dest='merge_function', const=pd.DataFrame.mean,
                        default=pd.DataFrame.min)
    parser.add_argument('--merge-min', action='store_const',
                        dest='merge_function', const=pd.DataFrame.min)
    parser.add_argument('--merge-max', action='store_const',
                        dest='merge_function', const=pd.DataFrame.max)
    parser.add_argument('--lhs-name', default="lhs",
                        help="Name used to describe left side in 'vs' mode")
    parser.add_argument('--rhs-name', default="rhs",
                        help="Name used to describe right side in 'vs' mode")
    parser.add_argument('--csv', action='store_true')
    parser.add_argument('files', metavar='FILE', nargs='+')
    config = parser.parse_args()

    if config.csv:
        VERBOSE = False

    if config.show_diff is None:
        config.show_diff = len(config.files) > 1

    # Read inputs
    files = config.files
    if "vs" in files:
        split = files.index("vs")
        lhs = files[0:split]
        rhs = files[split+1:]

        # Filter minimum of lhs and rhs
        lhs_d = _readmulti(lhs)
        lhs_merged = config.merge_function(lhs_d, level=1)
        rhs_d = _readmulti(rhs)
        rhs_merged = config.merge_function(rhs_d, level=1)

        # Combine to new dataframe
        data = pd.concat([lhs_merged, rhs_merged], names=['l/r'],
                         keys=[config.lhs_name, config.rhs_name])
    else:
        data = _readmulti(files)

    # Decide which metric to display / what is our "main" metric
    metrics = None
    if not config.all_metrics:
        metrics = config.metrics
        if len(metrics) == 0:
            defaults = ['Exec_Time', 'exec_time', 'Value', 'Runtime']
            for defkey in defaults:
                if defkey in data.columns:
                    metrics = [defkey]
                    break
        if len(metrics) == 0:
            sys.stderr.write("No default metric found and none specified\n")
            sys.stderr.write("Available metrics:\n")
            all_metrics = (data.columns.get_level_values('Metric')
                           .drop_duplicates())
            for column in sorted(all_metrics):
                sys.stderr.write("\t%s\n" % (column,))
            sys.exit(1)
        for metric in metrics:
            problem = False
            if metric not in data.columns.get_level_values('Metric'):
                sys.stderr.write("Unknown metric '%s'\n" % metric)
                problem = True
            if problem:
                sys.exit(1)

    # Filter data
    initial_size = len(data)
    if VERBOSE:
        print("Tests: %s" % (initial_size,))
    if config.filter_failed and hasattr(data, 'Exec'):
        newdata = _filter_failed(data)
        _print_filter_stats("Failed", data, newdata)
        newdata = newdata.drop('Exec', 1)
        data = newdata
    if config.filter_short:
        newdata = _filter_short(data, metric)
        _print_filter_stats("Short Running", data, newdata)
        data = newdata
    if config.filter_hash and 'hash' in data.columns and \
            data.index.get_level_values(0).nunique() > 1:
        newdata = _filter_same_hash(data)
        _print_filter_stats("Same hash", data, newdata)
        data = newdata
    if config.filter_blacklist:
        blacklist = open(config.filter_blacklist).readlines()
        blacklist = [line.strip() for line in blacklist]
        newdata = _filter_blacklist(data, blacklist)
        _print_filter_stats("In Blacklist", data, newdata)
        data = newdata
    final_size = len(data)
    if VERBOSE and final_size != initial_size:
        print("Remaining: %d" % (final_size,))

    # Reduce / add columns
    if metrics:
        if VERBOSE:
            print("Picked Metrics: %s" % (", ".join(metrics),))
        data = data.loc[:, pd.IndexSlice[:, metrics]]

    data = _add_diff_column(data)

    #sortkey = 'diff'
    #if len(config.files) == 1:
    #    sortkey = data.columns[0]
    #data = _sort_data(data, sortkey)

    #if not config.show_diff:
    #    del data['diff']

    if len(data.columns.get_level_values('File').drop_duplicates()) < 2:
        data.columns = data.columns.droplevel('File')

    # Print data
    if config.csv:
        data.to_csv(sys.stdout)
    else:
        if VERBOSE:
            print("")
        shorten_names = not config.full
        limit_output = 15
        if config.all or config.full:
            limit_output = None
        _print_result(data, limit_output, shorten_names)
