
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='shapeGMMTorch Tutorials',
    version='0.0.0',
    author='Martin McCullagh',
    author_email='martin.mccullagh@okstate.edu',
    description='Tutorials for using shapeGMMTorch',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mccullaghlab/shapeGMMTorch_Tutorials',
    project_urls = {
        "Bug Tracker": "https://github.com/mccullaghlab/shapeGMMTorch/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    license='MIT',
    #install_requires=['numpy','torch==1.11','torch_batch_svd'],
    install_requires=['numpy','torch>=1.11', 'matplotlib', 'nglview', 'shapeGMMTorch', 'MDAnalysis', 'pickle'],
)
