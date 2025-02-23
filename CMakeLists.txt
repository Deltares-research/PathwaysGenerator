cmake_minimum_required(
    VERSION 3.26)
project(AdaptationPathways
    LANGUAGES NONE
    VERSION 0.0.10
    DESCRIPTION "Adaptation Pathways TODO"
    HOMEPAGE_URL "https://github.com/Deltares-research/PathwaysGenerator"
)

set(AP_COPYRIGHT "2025 by TODO")
string(JOIN ", " AP_AUTHORS
    # TODO Add everybody, in some order (alphabet?)
    "TODO1"
    "TODO2"
    # "Kor de Jong (Geoneric, NL)"
    # "Marjolijn Haasnoot (Deltares, NL)"
    # "Willem van Deursen (Carthago Consultancy, NL)"
)

enable_testing()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/environment/cmake)

set(AP_BASE_URL "" CACHE STRING
    "Base url for web app. Use empty string (the default) for testing locally."
)

find_package(Flet REQUIRED)
find_package(JupyterBook REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
find_package(Quarto)
find_package(Sphinx REQUIRED)

set(AP_PLOT_GRAPHS
    "${CMAKE_CURRENT_SOURCE_DIR}/source/script/ap_plot_graphs.py"
)
set(AP_PYTHONPATH
    "${PROJECT_SOURCE_DIR}/source/package"
    "$ENV{PYTHONPATH}"
)
cmake_path(CONVERT "${AP_PYTHONPATH}" TO_NATIVE_PATH_LIST AP_PYTHONPATH)
string(TOLOWER ${CMAKE_HOST_SYSTEM_NAME} AP_HOST_SYSTEM_NAME_LOWER_CASE)

add_subdirectory(documentation)

if(Quarto_FOUND)
    add_subdirectory(presentation)
endif()
add_subdirectory(source)

add_custom_target(package
    VERBATIM
    COMMAND
        ${CMAKE_COMMAND} -E env "PYTHONPATH=${AP_PYTHONPATH}"
            ${Python3_EXECUTABLE}
                -m build
                --wheel
                --outdir ${CMAKE_CURRENT_BINARY_DIR}/dist
                ${CMAKE_CURRENT_SOURCE_DIR}
)

add_custom_target(release
    # VERBATIM
    COMMAND
        ${CMAKE_COMMAND} -E rm -rf adaptation_pathways-${CMAKE_PROJECT_VERSION}
    COMMAND
        ${CMAKE_COMMAND} -E make_directory
            adaptation_pathways-${CMAKE_PROJECT_VERSION}/dist
            adaptation_pathways-${CMAKE_PROJECT_VERSION}/documentation/html
    COMMAND
        ${CMAKE_COMMAND} -E copy
            "dist/*-${CMAKE_PROJECT_VERSION}-*.whl"
            adaptation_pathways-${CMAKE_PROJECT_VERSION}/dist
    COMMAND
        ${CMAKE_COMMAND} -E copy_directory
            documentation/html
            adaptation_pathways-${CMAKE_PROJECT_VERSION}/documentation/html
    COMMAND
        ${CMAKE_COMMAND} -E tar "cf"
            "adaptation_pathways-${CMAKE_PROJECT_VERSION}.zip" --format=zip --
            adaptation_pathways-${CMAKE_PROJECT_VERSION}
    COMMAND
        ${CMAKE_COMMAND} -E rm -rf adaptation_pathways-${CMAKE_PROJECT_VERSION}
)

add_dependencies(release
    test
    documentation
    package
)
