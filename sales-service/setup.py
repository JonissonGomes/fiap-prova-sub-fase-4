from setuptools import setup, find_packages

setup(
    name="sales-service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.68.1",
        "uvicorn==0.15.0",
        "motor==2.5.1",
        "pydantic==1.8.2",
        "python-dotenv==0.19.0",
        "httpx==0.23.0",
    ],
) 