import requests
import semver

def matrix_join(matrix, separator):
    return separator.join([str(x) for x in matrix if x is not None])

def majorize(version):
    version_info = semver.parse(version)
    return "%d" % (version_info["major"])

def minorize(version):
    version_info = semver.parse(version)
    return "%d.%d" % (version_info["major"], version_info["minor"])

def get_tags(image):
    php_version = semver.parse(image[0])
    php_versions = []

    if php_version["major"] == 5:
        if php_version["minor"] == 6:
            php_versions.append("5")
    else:
        php_versions.append(str(php_version["major"]))

    php_versions.extend([minorize(image[0]), image[0]])

    for tag in php_versions:
        yield matrix_join((tag,) + image[1:], "-")

def delete_builds(repo, token):
    headers = {'Authorization': token}
    builds = [];

    response = requests.get("https://hub.docker.com/v2/repositories/%s/autobuild/tags/" % (repo), headers=headers)

    if response.status_code == 200:
        body = response.json()
        builds.extend(body["results"])

        while not (body["next"] is None):
            response = requests.get(body["next"], headers=headers)

            if response.status_code == 200:
                body = response.json()
                builds.extend(body["results"])
            else:
                raise Exception("Invalid response")
    else:
        raise Exception("Invalid response")

    for build in builds:
        requests.delete("https://hub.docker.com/v2/repositories/%s/autobuild/tags/%s/" % (repo, build["id"]), headers=headers)

def add_builds (repo, token, paths, tags):
    headers = {'Authorization': token}

    for i in range(0, len(paths)):
        for tag in tags[i]:
            build = {"name": tag, "dockerfile_location": paths[i], "source_name": "master", "source_type": "Branch", "isNew": True}
            requests.post("https://hub.docker.com/v2/repositories/%s/autobuild/tags/" % (repo), headers=headers, data=build)
