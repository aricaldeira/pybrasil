from distutils.core import setup

setup(
    name='pybrasil',
    version='0.0.0.1',
    packages=['',
        'pybrasil',
        'pybrasil.ncm',
        'pybrasil.base',
        'pybrasil.data',
        'pybrasil.ibge',
        'pybrasil.valor',
        'pybrasil.feriado',
        'pybrasil.produto',
        'pybrasil.telefone',
        'pybrasil.inscricao',
        'pybrasil.python_pt_BR',
    ],
    url='git@github.com:aricaldeira/pybrasil.git',
    license='',
    author='Aristides Caldeira',
    author_email='aristides.caldeira@tauga.com.br',
    description='',
    requires=[
        'python-dateutil(>=2.6.0)',
        'pytz(>=2016.10)',
        'pyparsing(>=2.1.10)',
    ],
    package_data = {
        '': ['*.txt'],
    },
)