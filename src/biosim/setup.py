from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import build_ext

ext_modules = [
    Extension(
        "compute_fit",
        ["compute_fit.pyx"],
        libraries=["m"],
        extra_compile_args=["-ffast-math"],
    )
]

setup(
    name="compute_fit",
    cmdclass={"build_ext": build_ext},
    ext_modules=ext_modules,
)
