#! /usr/bin/python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------------------
#+ Autor:	Ran#
#+ Creado:	06/07/2021 15:11:00
#+ Editado:	06/07/2021 16:58:51
# -------------------------------------------------------------------------------------------------------------

from setuptools import setup

setup(
        name='conexions',
        version='1.1',
        description='Módulo para conexións en python3',
        url='https://github.com/Ran-n/conexions',
        author='Ran#',
        author_email='ran-n@tutanota.com',
        license='GPL-3.0',
        packages=['conexions'],
        install_requires=[
            'stem==1.8.0',
            'fake_useragent==0.1.11',
            'requests==2.22.0',
            'beautifulsoup4==4.9.3',
            'secrets==1.0.2',
           ],

        classifiers=[
            'Development Status :: Rolling Release',
            'Intended Audience :: General Public',
            'License :: GPL-3.0',
            'Operating System :: Lignux & Windows',
            'Programming Language :: Python :: 3.8.5',
            ],
        )

# -------------------------------------------------------------------------------------------------------------
