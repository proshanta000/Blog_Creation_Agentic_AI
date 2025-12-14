import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description= f.read()

__version__ = "0.0.0"

REPO_NAME = "Blog_Creation_Agentic_AI"
AUTHOR_USER_NAME = "proshanta000"
SRC_REPO = "Blog_Post_AI_Agent"
AUTHOR_EMAIL = "proshanta.mithu5@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package for Blog Post app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=F"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    }
),