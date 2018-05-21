try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import yaml


from rosdistro import get_distribution_file


def get_rosdistro_as_rosdep_data(index, rosdistro_name):
    """Download a rosdistro distribution.yaml file and generate rosdep data."""
    distribution = get_distribution_file(index, rosdistro_name)
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

