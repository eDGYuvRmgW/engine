import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Don't change the order of `PyOpenGL` and `PyOpenGL-accelerate`!
# https://github.com/pypa/setuptools/issues/196
# https://github.com/pypa/setuptools/issues/498 
install_requires = [
    "freetype-py",
    "glfw",
    "PyGLM",
    "PyOpenAL-accelerate",
    "PyOpenGL",
    "numpy",
    "pillow",
]

setuptools.setup(
    name="framework",
    version="0.1.0",
    author="Balaji Veeramani, Haiwen Dai, Jordi Aviles, Nicholas Spevacek",
    author_email="bveeramani@berkeley.edu",
    description="A lightweight and easy-to-use game development framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eDGYuvRmgW/framework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires, 
    include_package_data=True,
    package_data={"framework": ["assets/fonts/*"]},
    python_requires='>=3.7'
)
