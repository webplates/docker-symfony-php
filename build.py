import itertools
from jinja2 import Environment, FileSystemLoader
import os
import shutil
from helper import *

DIST = "dist"
REPO = "webplates/symfony-php"

VERSIONS = ["5.5.38", "5.6.24", "7.0.9"]
VARIANTS = ["fpm"]
DISTROS = ["alpine"]

MATRIX = set(itertools.chain(
    itertools.product(VERSIONS, [None], [None]),
    itertools.product(VERSIONS, VARIANTS, [None]),
    itertools.product(VERSIONS, [None], DISTROS),
    itertools.product(VERSIONS, VARIANTS, DISTROS)
))

# Prepare Jinja
env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))))

# Clear the dist folder
if os.path.isdir(DIST):
    shutil.rmtree(DIST, ignore_errors=True)
os.mkdir(DIST)

# Initialize state variables
paths = []
tags = []

# Initialize template
template = env.get_template('Dockerfile.template')

for image in MATRIX:
    path = DIST + "/" + matrix_join((minorize(image[0]),) + image[1:], "/")
    os.makedirs(path, exist_ok=True)
    dockerfile = path + "/Dockerfile"
    template.stream(parent=matrix_join(image, "-"), distro=image[2]).dump(dockerfile)
    paths.append(path)
    tags.append(set(get_tags(image)))

with open(".auth", "r") as f:
    token = f.readline().rstrip()

delete_builds(REPO, token)
add_builds(REPO, token, paths, tags)

FORMAT = "%-35s %s"
print (FORMAT % ("PATH", "TAG"))

for c1, c2 in zip(paths, tags):
    for tag in c2:
        print ("%-35s %s" % (c1, tag))
