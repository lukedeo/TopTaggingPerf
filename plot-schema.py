import yaml
from .ROC import *
import client as apy
from rootpy.io import root_open
import root_numpy as rn
import numpy as np
import os
import hashlib

def _tree_to_array(schema, to_npy = False):
	print 'Loading File...'
	f = root_open(schema['sample']['file'])
	T = f[schema['sample']['tree']]

	if schema['sample'].has_key('selection') == False:
		this_sel = None
	else:
		this_sel = schema['sample']['selection']

	if schema['sample'].has_key('step'):
		this_step = schema['sample']['step']
	else:
		this_step = None

	print 'Pulling Tree...'
	arr = rn.tree2array(T, selection = this_sel, step = this_step)

	if to_npy is True:
		print 'Writing to *.npy file...'
		varlist = "".join(this_sel.split()).replace('(', '').replace(')', '').split('&&')
		varlist.sort()
		hash_name = os.path.basename(schema['sample']['file']) + schema['sample']['tree'] + ''.join(varlist) + str(this_step)
		m = hashlib.sha1()
		m.update(hash_name)
		np.save(m.hexdigest() + '.npy', arr)
	print 'Done.'
	return arr

def _get_data_hash(schema):
	if schema['sample'].has_key('selection') == False:
		this_sel = None
	else:
		this_sel = schema['sample']['selection']
	if schema['sample'].has_key('step'):
		this_step = schema['sample']['step']
	else:
		this_step = None
	varlist = "".join(this_sel.split()).replace('(', '').replace(')', '').split('&&')
	varlist.sort()
	hash_name = os.path.basename(schema['sample']['file']) + schema['sample']['tree'] + ''.join(varlist) + str(this_step)
	m = hashlib.sha1()
	m.update(hash_name)
	return m.hexdigest()

def _get_data(schema):
	if os.path.isfile(_get_data_hash(schema) + '.npy'):
		print 'Matching Schema hash found! Loading from backup.'
		return np.load(_get_data_hash(schema) + '.npy')
	else:
		print 'No matching Schema hash found. Loading from ROOT file.'
		return _tree_to_array(schema, True)

def generate_taggers(schema):
	data = _get_data(schema)

	taggers = {}

	for taggerfile, specifications in schema['taggers']:
		net = apy.NeuralNet()


















	




	
