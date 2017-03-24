#!/usr/bin/env python2.7
"""Tool to filter, organize, compare and display benchmarking results. Usefull
for smaller datasets. It works great with a few dozen runs it is not designed to
deal with hundreds.
Requires the pandas library to be installed."""
import pandas as pd
import sys
import os.path
import re
import numbers
import argparse

def read_lit_json(filename):
    import json
    jsondata = json.load(open(filename))
    testnames = []
    columns = []
    columnindexes = {}
    info_columns = ['hash']
    if 'tests' not in jsondata:
        print "%s: Could not find toplevel 'tests' key"
        sys.exit(1)
    for test in jsondata['tests']:
        if "name" not in test:
            print "Skipping unnamed test!"
            continue
        if "metrics" not in test:
            print "Warning: '%s' has No metrics!" % test['name']
            continue
        for name in test["metrics"].keys():
            if name not in columnindexes:
                columnindexes[name] = len(columns)
                columns.append(name)
        for name in test.keys():
            if name not in columnindexes and name in info_columns:
                columnindexes[name] = len(columns)
                columns.append(name)

    nan = float('NaN')
    data = []
    for test in jsondata['tests']:
        if "name" not in test:
            print "Skipping unnamed test!"
            continue
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
    index = pd.Index(testnames, name='Test')
    column_index = pd.Index(columns, name='metric')
    return pd.DataFrame(data=data, index=index, columns=column_index)

def read_report_simple_csv(filename):
    result = pd.read_csv(filename, na_values=['*'], index_col=0, header=0)
    result.columns.name='metric'
    return result

def read(name):
    if name.endswith(".json"):
        return read_lit_json(name)
    if name.endswith(".csv"):
        return read_report_simple_csv(name)
    raise Exception("Cannot determine file format");

def readmulti(filenames):
    # Read datasets
    datasetnames = []
    datasets = []
    prev_index = None
    for filename in filenames:
        data = read(filename)
        name = os.path.basename(filename)
        # drop .json/.csv suffix; TODO: Should we rather do this in the printing
        # logic?
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
            count +=1

        datasetnames.append(name+suffix)
        # Warn if index names are different
        if prev_index is not None and prev_index.name != data.index.name:
            sys.stderr.write("Warning: Mismatched index names: '%s' vs '%s'\n"
                             % (prev_index.name, data.index.name))
        prev_index = data.index
    # Merge datasets
    d = pd.concat(datasets, axis=0, names=['run'], keys=datasetnames)
    return d

def add_diff_columns(d, add_diff, add_delta):
    values = d.unstack(level=0)

    # Pick new column names after unstack() to avoid the multiindex there
    if len(d.index.levels[0]) > 1:
        values.columns = d.index.levels[0].copy()
    else:
        values.columns = d.columns.copy()

    if not add_diff and not add_delta:
        return values

    # It's a mixed set of things with diff/delta so remove the name
    values.columns.name = ''

    has_two_runs = d.index.get_level_values(0).nunique() == 2
    if has_two_runs:
        values0 = values.iloc[:,0]
        values1 = values.iloc[:,1]
    else:
        values0 = values.min(axis=1)
        values1 = values.max(axis=1)

    # Quotient or absolute difference?
    if add_delta:
        values['delta'] = values1 - values0
    if add_diff:
        values['diff'] = values1 / values0
        values['diff'] -= 1.0
    return values

def filter_failed(data, key='Exec'):
    return data.loc[data[key] == "pass"]

def filter_short(data, key='Exec_Time', threshold=0.6):
    return data.loc[data[key] >= threshold]

def filter_same_hash(data, key='hash'):
    assert key in data.columns
    assert data.index.get_level_values(0).nunique() > 1

    return data.groupby(level=1).filter(lambda x: x[key].nunique() != 1)

def filter_blacklist(data, blacklist):
    return data.loc[~(data.index.get_level_values(1).isin(blacklist))]

def print_filter_stats(reason, before, after):
    n_before = len(before.groupby(level=1))
    n_after = len(after.groupby(level=1))
    n_filtered = n_before - n_after
    if n_filtered != 0:
        print "%s: %s (filtered out)" % (reason, n_filtered)

# Truncate a string to a maximum length by keeping a prefix, a suffix and ...
# in the middle
def truncate(string, prefix_len, suffix_len):
    return re.sub("^(.{%d}).*(.{%d})$" % (prefix_len, suffix_len),
                  "\g<1>...\g<2>", string)

# Search for common prefixes and suffixes in a list of names and return
# a (prefix,suffix) tuple that specifies how many characters can be dropped
# for the prefix/suffix. The numbers will be small enough that no name will
# become shorter than min_len characters.
def determine_common_prefix_suffix(names, min_len=8):
    if len(names) <= 1:
        return (0,0)
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

    # Only drop suffixes starting with '.' or '_'
    if len(suffix) > 0 and suffix[0] not in ['.', '_']:
        suffix_len = 0
    # Only drop prefixes ending in '/' or whitespace
    if len(prefix) > 0 and prefix[-1] not in [' ', ':', '/', '\t']:
        prefix_len = 0
    return (prefix_len, suffix_len)

def describe_1d(data):
    stats = [
        ('count', data.count()),
        ('sum', data.sum()),
        ('mean', data.mean()),
        ('std', data.std()),
        ('min', data.min()),
        ('25%', data.quantile(0.25)),
        ('50%', data.quantile(0.5)),
        ('75%', data.quantile(0.75)),
        ('max', data.max()),
    ]
    indices = [name for name,d in stats]
    summarydata = [d for name, d in stats]
    return pd.Series(summarydata, index=indices, name=data.name)

def describe(data):
    '''This is a custom version of pandas Series.describe(), so we can customize
    which aggregations are actually displayed.'''
    ldesc = [describe_1d(s) for _, s in data.iteritems()]
    names = []
    ldesc_indexes = sorted([x.index for x in ldesc], key=len)
    for idxnames in ldesc_indexes:
        for name in idxnames:
            if name not in names:
                names.append(name)
    result = pd.concat(ldesc, join_axes=pd.Index([names]), axis=1)
    result.columns = data.columns.copy()
    return result

def print_result(d, limit_output, shorten_names):
    dataout = d.copy()
    if limit_output:
        # Take 15 topmost elements
        dataout = dataout.head(15)

    # Turn index into a column so we can format it...
    index_name = dataout.index.name
    dataout.insert(0, index_name, dataout.index)

    float_format = lambda x: "{:6.2f}".format(x)
    formatters = dict()
    formatters['diff']  = lambda x: "{:6.1%}".format(x)
    formatters['delta'] = lambda x: "{:7d}".format(x)
    if shorten_names:
        drop_prefix, drop_suffix = determine_common_prefix_suffix(dataout[index_name])
        def format_name(name, common_prefix, common_suffix):
            name = name[common_prefix:]
            if common_suffix > 0:
                name = name[:-common_suffix]
            return "%-45s" % truncate(name, 10, 30)

        formatters[index_name] = lambda name: format_name(name, drop_prefix, drop_suffix)
    pd.set_option("display.max_colwidth", 0)
    out = dataout.to_string(index=False, justify='left',
                            float_format=float_format, formatters=formatters)
    print out
    print ""
    described = describe(d)
    float_format = lambda x: "{: 12.2f}".format(x)
    print described.to_string(float_format=float_format)


def sort_data(data):
    if 'diff' in data.columns:
        sortkey = 'diff'
    elif 'delta' in data.columns:
        sortkey = 'delta'
    else:
        sortkey = data.columns[0]

    data['$sortkey'] = data[sortkey].abs()
    data.sort_values("$sortkey", ascending=False, inplace=True)
    del data['$sortkey']


def print_available_metrics(data):
    sys.stderr.write("Available metrics:\n")
    for column in data.columns:
        sys.stderr.write("\t%s\n" % column)
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='compare.py')
    parser.add_argument('-a', '--all', action='store_true')
    parser.add_argument('-f', '--full', action='store_true')
    parser.add_argument('-m', '--metric', action='append', dest='metrics',
                        default=[])
    parser.add_argument('--no-diff', action='store_false', dest='show_diff',
                        default=None)
    parser.add_argument('--diff', action='store_true', dest='show_diff')
    parser.add_argument('--delta', action='store_true', dest='show_delta')
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
    parser.add_argument('files', metavar='FILE', nargs='+')
    config = parser.parse_args()

    if config.show_diff is None:
        config.show_diff = len(config.files) > 1

    # Read inputs
    files = config.files
    if "vs" in files:
        split = files.index("vs")
        lhs = files[0:split]
        rhs = files[split+1:]

        # Filter minimum of lhs and rhs
        lhs_d = readmulti(lhs)
        lhs_merged = config.merge_function(lhs_d, level=1)
        rhs_d = readmulti(rhs)
        rhs_merged = config.merge_function(rhs_d, level=1)

        # Combine to new dataframe
        data = pd.concat([lhs_merged, rhs_merged], names=['l/r'], keys=['lhs', 'rhs'])
    else:
        data = readmulti(files)

    # Filter data
    proggroup = data.groupby(level=1)
    initial_size = len(proggroup.indices)
    print "Tests: %s" % (initial_size,)
    if config.filter_failed and hasattr(data, 'Exec'):
        newdata = filter_failed(data)
        print_filter_stats("Failed", data, newdata)
        newdata = newdata.drop('Exec', 1)
        data = newdata
    if config.filter_short:
        newdata = filter_short(data, metric)
        print_filter_stats("Short Running", data, newdata)
        data = newdata
    if config.filter_hash and 'hash' in data.columns and \
       data.index.get_level_values(0).nunique() > 1:
        newdata = filter_same_hash(data)
        print_filter_stats("Same hash", data, newdata)
        data = newdata
    if config.filter_blacklist:
        blacklist = open(config.filter_blacklist).readlines()
        blacklist = [line.strip() for line in blacklist]
        newdata = filter_blacklist(data, blacklist)
        print_filter_stats("In Blacklist", data, newdata)
        data = newdata
    final_size = len(data.groupby(level=1))
    if final_size != initial_size:
        print "Remaining: %d" % (final_size,)

    # Reduce: Decide which metric to display / what is our "main" metric
    metrics = config.metrics
    if len(config.files) >= 2:
        # We need a metric for comparisons try to pick one
        if len(metrics) == 0:
            defaults = [ 'Exec_Time', 'exec_time', 'Value', 'Runtime' ]
            for defkey in defaults:
                if defkey in data.columns:
                    metrics = [defkey]
                    break
        if len(metrics) == 0:
            sys.stderr.write("No default metric found and none specified\n")
            print_available_metrics(data)
    for metric in metrics:
        if metric not in data.columns:
            sys.stderr.write("Unknown metric '%s'\n" % metric)
            print_available_metrics(data)

        print "Metric: %s" % (",".join(metrics),)
        if len(metrics) > 0:
            data = data[metrics]

    # Analyse: Add diff column
    data = add_diff_columns(data, add_diff=config.show_diff,
                            add_delta=config.show_delta)

    # Sort
    sort_data(data)

    # Print data
    print ""
    shorten_names = not config.full
    limit_output = (not config.all) and (not config.full)
    print_result(data, limit_output, shorten_names)
