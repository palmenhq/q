from distutils.core import setup

setup(name='q',
      version='1.0',
      description='Life hacks',
      author='Johan Palmfjord',
      author_email='johan.palmfjord@gmail.com',
      install_requires=['pyyaml', 'spotipy', 'termcolor', 'requests'],
      dependency_links=['git+ssh://git@github.com:plamere/spotipy.git#egg=spotipy-2.4.4'],
      entry_points='''
    [console_scripts]
    q=q:main
''',

      )
