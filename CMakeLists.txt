cmake_minimum_required(
    VERSION 3.26)
project(AdaptationPathways
    LANGUAGES NONE
    VERSION 0.0.9
    DESCRIPTION "Adaptation Pathways TODO"
    HOMEPAGE_URL "https://publicwiki.deltares.nl/display/AP/Adaptation+Pathways"
)

enable_testing()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/environment/cmake)

find_package(CairoSVG REQUIRED)
find_package(PyInstaller REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
find_package(QtTools)
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

add_custom_target(logo
    VERBATIM
    COMMAND
        ${CMAKE_COMMAND} -E env "PYTHONPATH=${AP_PYTHONPATH}"
            # Creates logo.{pdf,svg}
            ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/source/script/ap_create_logo.py logo
)

add_custom_target(icon
    VERBATIM
    COMMAND
        # cairosvg logo.svg -o icon.png
        ${CMAKE_COMMAND} -E env "PYTHONPATH=${AP_PYTHONPATH}"
            ${Python3_EXECUTABLE}
                ${CMAKE_CURRENT_SOURCE_DIR}/environment/script/ap_svg_to_png.py logo.svg icon.png
    COMMAND
        ${Python3_EXECUTABLE} -c "from PIL import Image; img = Image.open('icon.png'); img.save('icon.ico'); img.save('icon.icns')"
    DEPENDS
        logo
)

if(WIN32)
    set(AP_ICON icon.ico)
elseif(APPLE)
    set(AP_ICON icon.icns)
else()
    set(AP_ICON icon.png)
endif()
set(AP_ICON ${CMAKE_CURRENT_SOURCE_DIR}/source/package/adaptation_pathways/desktop/icon/${AP_ICON})

configure_file(
    adaptation_pathways.spec.in
    adaptation_pathways.spec
    @ONLY
)

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

add_custom_target(installer
    VERBATIM
    COMMAND
        ${CMAKE_COMMAND} -E env "PYTHONPATH=${AP_PYTHONPATH}"
            ${PyInstaller_EXECUTABLE}
                --noconfirm
                adaptation_pathways.spec
    DEPENDS
        adaptation_pathways.spec
        # icon
)

add_custom_target(installer_release
    VERBATIM
    COMMAND
        ${CMAKE_COMMAND} -E rm -rf pathway_generator-${CMAKE_PROJECT_VERSION}
    COMMAND
        ${CMAKE_COMMAND} -E copy_directory
            "dist/pathway_generator"
            pathway_generator-${CMAKE_PROJECT_VERSION}
    COMMAND
        ${CMAKE_COMMAND} -E tar "cf"
            "pathway_generator-${AP_HOST_SYSTEM_NAME_LOWER_CASE}-${CMAKE_PROJECT_VERSION}.zip" --format=zip --
            pathway_generator-${CMAKE_PROJECT_VERSION}
)

add_dependencies(installer_release
    installer
)
