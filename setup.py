from setuptools import setup


setup(
    name="geofeather",
    version="0.4.0",
    packages=["geofeather"],
    url="https://github.com/brendan-ward/geofeather",
    license="MIT",
    author="Brendan C. Ward",
    author_email="bcward@astutespruce.com",
    description="Fast file-based format for geometries with Geopandas",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    install_requires=["pyarrow>=0.17", "geopandas>=0.8"],
    tests_require=["pygeos", "pytest", "pytest-cov", "pytest-benchmark"],
    include_package_data=True,
)
