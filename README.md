TopTaggingPerf
==============

<em>Python Scripts for Top Tagging Performance plotting</em>

Clone this repository with 

```
git clone git@github.com:lukedeo/TopTaggingPerf.git
```

Usage is simple, and can be run interactively. First, put `export PYTHONPATH+=:/path/to/TopTaggingPerf` in your `~/.bashrc`. 

We assume you have an record array called `data` pulled from a tree using `rootpy/root_numpy` interface.

```python
>>> from TopTaggingPerf.ROC import *
>>> taggers = {}
>>> add_tagger(r'$\sqrt{d_{23}}$', 'blue', general_roc_weighted(data, data['fjet_SPLIT23_flat'], data['mcevt_weight_flat'], 200000), taggers)
>>>
>>> import agilepy.client as agilepy
>>>
>>> net = agilepy.NeuralNet()
>>> net.load('NetworkFile.yaml')
>>> predictions = net.predict(data)['top_predicted']
>>>
>>> add_tagger(r'AGILETopTagger $\ell_1$ Regularized, Denoising', 'red', general_roc_weighted(data, predictions, data['mcevt_weight_flat'], 10000), taggers)
>>>
>>> roc = ROC_plotter(taggers)
>>> roc.savefig('myROCfile.pdf')
```
