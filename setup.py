from distutils.core import setup

setup(
  name = 'Pyppetheater',
  packages = ['pyppetheater'],
  version = '0.2.19',
  license='MIT',
  description = 'Functional testing using python and puppeteer',
  author = 'Gregoire Penverne',
  author_email = 'gpenverne@gmail.com',
  url = 'https://github.com/gpenverne/pyppettheater',
  download_url = 'https://github.com/gpenverne/pyppettheater/archive/master.zip',
  keywords = ['puppeteer', 'gherkin', 'test'],
  install_requires=[
      'pyppeteer',
      'asyncio',
      'gherkin-parser',
      'pyyaml',
      'coloredlogs',
      'pymysql',
      'requests',
      'faker'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Testing',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
  scripts=['pyppetheater/pyppet_theater']
)
