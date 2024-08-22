from distutils.core import setup

setup(
    name='minesweeper',
    version='1.0.0',
    packages=['minesweeper',],
    url='https://gitee.com/wututua/mine-sweeping-in-python',
    license='GPLv3',
    author='wututu',
    author_email='wututua@qq.com',
    description='minesweeper.',
    data_files=[
        (
            'minesweeper/resource',
            [
                'minesweeper/resource/project.txt',
                'minesweeper/resource/images/mine.ico'
            ]
        )
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Games/Entertainment :: Board Games',
    ]
)
