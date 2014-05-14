import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.mlab import griddata
from matplotlib import rc
import numpy.ma as ma

def data_load(filename):
    data = np.genfromtxt(filename, delimiter = ',', names = True)
    return data

def pt_plot(data, pt_label = 'fjet_pt_flat', weighted = None, log = False, bins = 100, logcount = False):
	fig = plt.figure(figsize=(11.69, 8.27), dpi=100) 
	ax = plt.subplot(1,1,1)
	if log:
		ax.set_xscale('log')
	pt = (data[pt_label]) / 1000
	bins = np.linspace(np.min(pt), np.max(pt), bins)
	if log:
		plt.xlabel(r"$\log(p_T)$ in GeV", fontsize=20)
	else:
		plt.xlabel(r"$p_T$ in GeV", fontsize=20)
	plt.ylabel(r"Count", fontsize=20)
	plt.title(r"Distribution of Jet $p_T$")
	plt.xlim(np.min(pt), np.max(pt))
	if weighted is None:
		plt.hist(pt[data['top'] == 1], histtype='step', log = logcount, bins = bins, color = 'red', label = r"$Z'$ jets, $m_{Z'} = 1.75 \mathrm{TeV}$")
		plt.hist(pt[data['top'] == 0], histtype='step', log = logcount, bins = bins, color = 'blue', label = "JZ4W Jets")
	else:
		plt.hist(pt[data['top'] == 1], histtype='step', log = logcount, bins = bins, color = 'red', label = r"$Z'$ jets, $m_{Z'} = \mathsf{1.75 TeV}$", weights=weighted[data['top'] == 1])
		plt.hist(pt[data['top'] == 0], histtype='step', log = logcount, bins = bins, color = 'blue', label = "JZ4W Jets", weights=weighted[data['top'] == 0])
	
	plt.legend(loc = 1)
	plt.show()
	return fig


def sb_plot(data, label = 'fjet_pt_flat', disc = None, weighted = None, log = False, bins = 100, logcount = False):
	fig = plt.figure(figsize=(11.69, 8.27), dpi=100) 
	ax = plt.subplot(1,1,1)
	if disc is None:
		pt = data[label]
	else:
		pt = disc
	if log:
		ax.set_xscale('log')
	bins = np.linspace(np.min(pt), np.max(pt), bins)
	if log:
		plt.xlabel(r"$\log(p_T)$ in GeV", fontsize=20)
	else:
		plt.xlabel(r"" + str(label), fontsize=20)

	plt.ylabel(r"Count", fontsize=20)
	plt.title(r"Distribution of Jet " + label)
	
	plt.xlim(np.min(pt), np.max(pt))
	if weighted is None:
		plt.hist(pt[data['top'] == 1], histtype='step', log = logcount, bins = bins, color = 'red', label = r"$Z'$ jets, $m_{Z'} = 1.75 \mathrm{TeV}$")
		plt.hist(pt[data['top'] == 0], histtype='step', log = logcount, bins = bins, color = 'blue', label = "JZ4W Jets")
	else:
		plt.hist(pt[data['top'] == 1], histtype='step', log = logcount, bins = bins, color = 'red', label = r"$Z'$ jets, $m_{Z'} = \mathsf{1.75 TeV}$", weights=weighted[data['top'] == 1])
		plt.hist(pt[data['top'] == 0], histtype='step', log = logcount, bins = bins, color = 'blue', label = "JZ4W Jets", weights=weighted[data['top'] == 0])
	
	plt.legend(loc = 1)
	plt.show()
	return fig


def pre_process(data):
	data = data[data['fjet_pt_flat']/1000 < 1100]
	data = data[data['fjet_pt_flat']/1000 > 550]
	data = data[np.abs(data['fjet_eta_flat']) < 1.2 ]
	data = data[data['fjet_Tau2_flat'] > -10]
	data = data[data['fjet_Tau3_flat'] > -10]
	return data

def general_roc(data, discriminant, bins = 2000):
	top = data[:]['top']

	qcd_total = np.sum(top == 0)
	top_total = np.sum(top == 1)

	bincount = bins

	top_ind = data[:]['top'] == 1
	qcd_ind = data[:]['top'] == 0

	discriminant_bins = np.linspace(np.min(discriminant), np.max(discriminant), bins)

	sig, b1 = np.histogram(discriminant[top_ind], discriminant_bins)
	bkd, b1 = np.histogram(discriminant[qcd_ind], discriminant_bins)

	t_efficiency = np.add.accumulate(sig[::-1]) / float(top_total)
	qcd_rejection = 1 / (np.add.accumulate(bkd[::-1]) / float(qcd_total))

	return t_efficiency, qcd_rejection


def general_roc_weighted(data, discriminant, weights, bins = 2000):
	top = data[:]['top']

	# qcd_total = np.sum(top == 0)
	# top_total = np.sum(top == 1)
	bincount = bins

	top_ind = data[:]['top'] == 1
	qcd_ind = data[:]['top'] == 0
	qcd_total = np.sum(weights[qcd_ind])
	top_total = np.sum(weights[top_ind])
	discriminant_bins = np.linspace(np.min(discriminant), np.max(discriminant), bins)

	sig, b1 = np.histogram(discriminant[top_ind], discriminant_bins, weights = weights[top_ind])
	bkd, b1 = np.histogram(discriminant[qcd_ind], discriminant_bins, weights = weights[qcd_ind])

	t_efficiency = np.add.accumulate(sig[::-1]) / float(top_total)
	qcd_rejection = 1 / (np.add.accumulate(bkd[::-1]) / float(qcd_total))

	return t_efficiency, qcd_rejection


def tagger_VI_roc(data, bins = 2000):
	top = data[:]['top']

	qcd_total = np.sum(top == 0)
	top_total = np.sum(top == 1)

	discriminant = data['fjet_Tau3_flat'] / data['fjet_Tau2_flat']

	bincount = bins

	top_ind = data[:]['top'] == 1
	qcd_ind = data[:]['top'] == 0

	d12_cut = ((data['fjet_SPLIT12_flat'] > 40000))
	t21_cut = (data['fjet_Tau2_flat'] / data['fjet_Tau1_flat'] > 0.4) & (data['fjet_Tau2_flat'] / data['fjet_Tau1_flat'] < 0.9)
	discriminant_bins = np.linspace(np.min(discriminant[d12_cut & t21_cut]), np.max(discriminant[d12_cut & t21_cut]), bins)

	sig, b1 = np.histogram(discriminant[top_ind & d12_cut & t21_cut], discriminant_bins)
	bkd, b1 = np.histogram(discriminant[qcd_ind & d12_cut & t21_cut], discriminant_bins)

	t_efficiency = np.add.accumulate(sig) / float(top_total)
	qcd_rejection = 1 / (np.add.accumulate(bkd) / float(qcd_total))

	return t_efficiency, qcd_rejection

def tagger_VI_roc_weighted(data, weights, bins = 2000):
	top = data[:]['top']

	# qcd_total = np.sum(top == 0)
	# top_total = np.sum(top == 1)

	discriminant = data['fjet_Tau3_flat'] / data['fjet_Tau2_flat']

	bincount = bins

	top_ind = data[:]['top'] == 1
	qcd_ind = data[:]['top'] == 0

	qcd_total = np.sum(weights[qcd_ind])
	top_total = np.sum(weights[top_ind])

	d12_cut = ((data['fjet_SPLIT12_flat'] > 40000))
	t21_cut = (data['fjet_Tau2_flat'] / data['fjet_Tau1_flat'] > 0.4) & (data['fjet_Tau2_flat'] / data['fjet_Tau1_flat'] < 0.9)
	discriminant_bins = np.linspace(np.min(discriminant[d12_cut & t21_cut]), np.max(discriminant[d12_cut & t21_cut]), bins)

	sig, b1 = np.histogram(discriminant[top_ind & d12_cut & t21_cut], discriminant_bins, weights = weights[top_ind & d12_cut & t21_cut])
	bkd, b1 = np.histogram(discriminant[qcd_ind & d12_cut & t21_cut], discriminant_bins, weights = weights[qcd_ind & d12_cut & t21_cut])

	t_efficiency = np.add.accumulate(sig) / float(top_total)
	qcd_rejection = 1 / (np.add.accumulate(bkd) / float(qcd_total))

	return t_efficiency, qcd_rejection




def ROC_plotter(taggerdict, min_eff = 0, max_eff = 1, linewidth = 1.4, pp = False, signal = "$Z', m_{Z'} = 1.75$ TeV", background = "JZ4W", title = "Top Tagging Efficiency vs. Rejection, $\vert\eta\vert < 1.2, m_{Z'} = 1.75$ TeV ", logscale = True, save_arr = False):
	fig = plt.figure(figsize=(11.69, 8.27), dpi=100)
	ax = fig.add_subplot(111)
	plt.xlim(min_eff,max_eff)
	plt.grid(b = True, which = 'minor')
	plt.grid(b = True, which = 'major')
	max_ = 0
	for tagger, data in taggerdict.iteritems():
		sel = (data['efficiency'] >= min_eff) & (data['efficiency'] <= max_eff)
		if np.max(data['rejection'][sel]) > max_:
			max_ = np.max(data['rejection'][sel])
		if save_arr:
			data.tofile(tagger+'_save.csv', sep=",")
		plt.plot(data['efficiency'][sel], data['rejection'][sel], '-', label = r''+tagger, color = data['color'], linewidth=linewidth)

	ax = plt.subplot(1,1,1)
	for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
		item.set_fontsize(20)
	
	if logscale == True:	
		plt.ylim(1,10 ** 3)
		ax.set_yscale('log')
	ax.set_xlabel(r'$\epsilon_{t}$, Top efficiency (' + signal + ')')
	ax.set_ylabel(r"QCD ("+ background + ") rejection")

	plt.legend()
	plt.title(r''+title)
	if pp:
		pp.savefig(fig)
	else:
		plt.show()
		return fig


def add_tagger(name, color, tagger_pair, dictref):
	dictref.update({name : {'efficiency' : tagger_pair[0], 'rejection' : tagger_pair[1], 'color' : color}})








