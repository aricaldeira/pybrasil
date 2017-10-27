from distutils.core import setup
setup(
    name='pybrasil',
    version='0.0.0.2',
    packages=[
        'pybrasil',
        'pybrasil.base',
        'pybrasil.data',
        'pybrasil.febraban',
        'pybrasil.feriado',
        'pybrasil.ibge',
        'pybrasil.inscricao',
        'pybrasil.ncm',
        'pybrasil.valor',
        'pybrasil.produto',
        'pybrasil.python_pt_BR',
        'pybrasil.telefone',
        'pybrasil.template',
        'pybrasil.valor',
    ],
    url='git@github.com:aricaldeira/pybrasil.git',
    license='',
    author='Aristides Caldeira',
    author_email='aristides.caldeira@tauga.com.br',
    description='',
    package_data = {
        '': ['*.txt'],
    },
    install_requires=[
        'python-dateutil',
        'pytz',
        'pyparsing',
        'mako',
        'future',
        'py3o.template'
    ],
)

