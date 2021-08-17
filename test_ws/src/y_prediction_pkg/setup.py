from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['y_prediction_pkg'],
    package_dir={'': 'src'}
)

setup(**d)