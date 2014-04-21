#!/usr/bin/env python
import sys
import yaml
import TopTaggingPerf as tt
import datetime


if __name__ == '__main__':
	filename = str(sys.argv[1])
	f = open(filename, 'r')
	
	schema = yaml.load(f)

	taggers = tt.generate_taggers(schema)

	now = datetime.datetime.now()
	timestamp = now.strftime("%Y-%m-%d_%H:%M")

	tt.plot_roc(taggers, schema, 'ROC_plots_' + timestamp + '.pdf')
