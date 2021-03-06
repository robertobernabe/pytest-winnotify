__author__ = 'florian.schaeffeler'
from setuptools import setup


if __name__ == "__main__":
    setup(
        name='pytest-winnotify', version='0.4.0',
        description='Windows tray notifications for py.test results.',
        author='Florian Schaeffeler',
        author_email="florian.schaeffeler@gmail.com",
        url="https://github.com/robertobernabe/pytest-winnotify",
        keywords=['pytest', 'pytest-', 'windows', 'notifications', 'py.test'],
        platforms="Microsoft Windows",
        packages=['pytest_winnotify'],
        package_data={'pytest_winnotify': ['pytest.ico']},
        entry_points={'pytest11': ['pytest_winnotify = pytest_winnotify', ]},
        install_requires=['pypiwin32']
    )