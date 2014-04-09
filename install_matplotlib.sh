# Install Mock
wget https://pypi.python.org/packages/source/m/mock/mock-1.0.1.tar.gz#md5=c3971991738caa55ec7c356bbc154ee2 --no-check-certificate
tar -xzvf mock-1.0.1.tar.gz
cd mock-1.0.1
python setup.py install --user
cd ..

#Install PyParsing
wget https://pypi.python.org/packages/source/p/pyparsing/pyparsing-2.0.1.tar.gz#md5=37adec94104b98591507218bc82e7c31 --no-check-certificate
tar -xzvf pyparsing-2.0.1.tar.gz 
cd pyparsing-2.0.1
python setup.py install --user
cd ..

#install six
wget https://pypi.python.org/packages/source/s/six/six-1.6.1.tar.gz#md5=07d606ac08595d795bf926cc9985674f --no-check-certificate
tar -xzvf six-1.6.1.tar.gz
cd six-1.6.1
python setup.py install --user
cd ..

wget https://labix.org/download/python-dateutil/python-dateutil-1.5.tar.gz --no-check-certificate
tar -xzvf python-dateutil-1.5.tar.gz
cd python-dateutil-1.5
python setup.py install --user
cd ..


git clone git@github.com:matplotlib/matplotlib.git
cd matplotlib
python setup.py build
python setup.py install --user
