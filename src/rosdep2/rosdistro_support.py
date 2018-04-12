try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import yaml


from rosdistro import DistributionFile


def download_rosdistro_as_rosdep_data(rosdistro_name, rosdistro_url):
    """Download a rosdistro distribution.yaml file and generate rosdep data."""
    try:
        response = urlopen(rosdistro_url)
    except:
        print('Unable to download rosdistro.')
        raise
    yaml_text = response.read()
    response.close()

    distribution = DistributionFile(rosdistro_name, yaml.load(yaml_text))
    rosdep_data = {}
    for rospkg in distribution.release_packages.keys():
        packagename = 'ros-{name}-{pkg}'.format(name=rosdistro_name, pkg=rospkg.replace('_', '-'))
        for distro, suites in distribution.release_platforms.items():
            if rospkg not in rosdep_data:
                rosdep_data[rospkg] = {}
            if suites:
                rosdep_data[rospkg][distro] = {}
                for suite in suites:
                    rosdep_data[rospkg][distro][suite] = [packagename]
    return rosdep_data

