from setuptools import setup


setup(
    name="geofeather",
    version="0.3.0",
    packages=["geofeather"],
    url="https://github.com/brendan-ward/geofeather",
    license="MIT",
    author="Brendan C. Ward",
    author_email="bcward@astutespruce.com",
    description="Fast file-based format for geometries with Geopandas",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    install_requires=["feather-format", "geopandas"],
    tests_require=["pygeos", "pytest", "pytest-cov", "pytest-benchmark"],
    include_package_data=True,
)
