import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()
    print(requirements)

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
    install_requires=requirements, 
    include_package_data=True,
    package_data={"": ["assets/*"]},
    python_requires='>=3.7'
)
