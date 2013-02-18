REP: XXX
Title: Releasing Third Party, Non catkin Packages
Author: William Woodall
Status: Draft
Type: TDB
Content-Type: text/x-rst
Created: 15-Feb-2013
Post-History: ?-?-2013

.. contents::

Abstract
========
This REP forms the recommendation for how to handle releases of third party, non catkin packages using the ROS community release infrastructure.

Motivation
==========
Historically, third party packages have been *wrapped* in rosbuild packages, using one of the *download_and_build* Make scripts [1]_. This has since been discouraged, as it often lead to failures on the build farm and generally is considered bad form for a package. One of the reasons for the popularity of this method of "wrapping" packages was that it was not easy to work with or release third party packages along side rosbuild. Therefore one of the design goals of catkin was to make integration with third party packages easier, and for build time that is accomplished by reducing custom infrastructure and depending more on conventional tools like CMake. There are still some custom tools for the release system which provide infrastructure for the highly distributed and modular ROS ecosystem, and there should be a recommended process for releasing third party packages with these custom tools such that they integrate into the build farm and deployment infrastructure for ROS.

Design Requirements
===================
During the Groovy release cycle the existing processes were vetted and several different strategies came of that experience, but some general design requirements have been identified. In particular, after a release, a third party library should:

* Have a catkin package.xml
* Install a catkin package.xml
* Have setup.*sh files after installation

Rationale
=========
The rationale for the design requirements are as follows:

Having a catkin package.xml
---------------------------
Having a package.xml allows tools like bloom to extract meta data which other wise must be continuously be asked for or stored in some other way.  The useful meta data in the package.xml that isn't usually shipped with packages in a standard way are things like versioned build, run, and test dependencies, authors, maintainers, license, description, and version. Having this meta information in the package.xml makes it possible for the release tools to generate similar description files for multiple platforms (debian, fedora, Homebrew).

Installing a catkin package.xml
-------------------------------
In addition to having a package.xml through the release process, the third party packages should also install the package.xml so that once deployed end users can use tools which rely on the existence of package.xml. The installation of the package.xml is normally automatic (when using catkin), but in the case of third party the package.xml simply needs to be installed. For CMake this means a custom install(...) rule, and for other systems, like autotools or SCons, the standard method of installing plain files will also work.

Have setup.*sh Files After Installation
---------------------------------------
Often the deployed binaries (debs) have a non-standard installation prefix, this allows developers to have multiple versions of ROS installed side by side, but means that third party packages which rely on pkg-config or CMake's find_package(...) infrastructure to be found by other packages will not be easily found by default as they will not be in the normal system PATH's. The setup.*sh environment files are designed to solve this problem for catkin packages, but third party packages will also need them (in the case that only third party packages are installed from debs into a given prefix).

Solution Alternatives
=====================
There are several ways to satisfy each of the design requirements.

Have a catkin package.xml
-------------------------
This can be solved by putting a package.xml in the upstream of the third party package (if that is an option). This allows bloom to do things like automatically infer the version being released, and automatically fetch the correct tag for release. Previously the only other option (when putting an package.xml upstream is not a valid option) was to add a package.xml to the release repository as a patch. This is a cumbersome solution because it requires the person releasing to update this patch with the new version number each release. It also broke the bloom work flow, resulting in more, custom commands in order to do a release. Starting in bloom 0.3 and higher the work flow includes the ability to inject package.xml's into a repository and then template them on the version being released. This feature should make releasing third party packages from repositories which do not contain package.xml's easier. However, having the package.xml in the upstream repository has the added advantage of being able to be built along side other catkin packages directly from the source repository. If the package.xml is added in the release repository using bloom then the code must be fetched from the release branch of the release repository in order to be built using the catkin tools.

Install a catkin package.xml
----------------------------
Normally the package.xml is installed by default when catkin_package(...) is invoked from CMake. For third party packages which build with CMake, invoking catkin_package(...) from their CMakeLists.txt is a possible solution, but is not recommended. In stead the third party packages should make a custom install rule for the package.xml using the preferred method for their build system. This install rule can be placed in the upstream repository along with a package.xml if that is acceptable for the maintainers. Having the package.xml and an install rule for it in the upstream means now patches or injects in the release repository and makes for the cleanest solution, while also not making a dependency on catkin or ROS.

Have setup.*sh Files After Installation
---------------------------------------
These setup.*sh files are created when catkin_package(...) is invoked in the CMake of a package. When the -DCATKIN_BUILD_BINARY_PACKAGE="1" option is passed to CMake, then no setup.*sh files are generated. This prevents collisions when packaging for debian. When packaging for debian the setup.*sh files are provided by the catkin package. In this case the easiest way to ensure that there are setup.*sh files when installing only a third party package from debian's is for that third party package to run_depend on catkin. This will cause catkin to be installed before the third party package is installed, ensuring the setup.*sh files will be in the install prefix.

Specification
=============
The recommendation of this REP for releasing third party packages in the ROS community deployment infrastructure is as follows:

* Inject a templated package.xml into the upstream using bloom
 * Optionally, put the package.xml in the actual upstream repository
* Add an install rule for the package.xml as patch in the release branch using bloom
 * Optionally, put the install rule for the package.xml into the actual upstream repository
* Have a run_depend on catkin in the package.xml(s)

This provides the least intrusive, but most automated and correct method for releasing non catkin packages through the ROS infrastructure.

Concerns
========
This section is reserved for feedback from the community.


Resources
=========

TODO: Link to the updated bloom tutorials and documentation regarding third party packages.

TODO: Provide example package.xml and install rules

References
==========
.. [1] Download and build Make Scripts
   (https://github.com/ros/ros/tree/groovy-devel/core/mk)

Copyright
=========
This document has been placed in the public domain.
