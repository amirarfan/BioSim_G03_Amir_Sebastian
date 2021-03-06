from setuptools import setup, dist

# from distutils.core import setup
dist.Distribution().fetch_build_eggs(['Cython>=0.15.1', 'numpy>=1.10'])
from distutils.extension import Extension
from Cython.Distutils import build_ext

# One might have to remove "libraries=["m"]" when building the code on windows

ext_modules = [
    Extension(
        "biosim.compute_fit",
        ["src/biosim/compute_fit.pyx"],
        # libraries=["m"],
        extra_compile_args=["-ffast-math", "-O3"],
    ),
    Extension(
        "biosim.weighted_prob",
        ["src/biosim/weighted_prob.pyx"],
        # libraries=["m"],
        extra_compile_args=["-ffast-math", "-O3"],
    ),
    Extension(
        "biosim.det_kill",
        ["src/biosim/det_kill.pyx"],
        # libraries=["m"],
        extra_compile_args=["-ffast-math", "-O3"],
    ),
]

setup(
    name="biosim",
    description="A population dynamics simulation written in Python",
    author="Amir Arfan & Sebastian Becker",
    author_email="amar@nmbu.no & sebabeck@nmbu.no",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
    include_package_data=True,
    package_dir={"": "src"},
)
