add_subdirectory(develop)
add_subdirectory(use)

configure_file(
    conf.py.in
    conf.py
    @ONLY
)

foreach(name IN ITEMS changelog glossary index)
    configure_file(
        ${name}.rst
        ${name}.rst
        COPYONLY
    )
endforeach()

set(AP_SPHINX_SOURCE_DIR ${CMAKE_CURRENT_BINARY_DIR})
set(AP_SPHINX_BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR}/html)

# https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html
add_custom_target(apidoc
    VERBATIM
    COMMAND
        ${CMAKE_COMMAND}
            -E env "SPHINX_APIDOC_OPTIONS=members,undoc-members,show-inheritance,inherited-members"
                ${Sphinx_APIDOC_EXECUTABLE}
                    --force
                    --separate
                    --module-first
                    -d 1
                    -o ${CMAKE_CURRENT_BINARY_DIR}/api
                    ${PROJECT_SOURCE_DIR}/source/package/adaptation_pathways
)

# https://www.sphinx-doc.org/en/master/man/sphinx-build.html
add_custom_target(documentation
    VERBATIM
    COMMAND
        ${CMAKE_COMMAND} -E env "PYTHONPATH=${AP_PYTHONPATH}"
            ${Sphinx_BUILD_EXECUTABLE}
                -b html
                -c ${CMAKE_CURRENT_BINARY_DIR}
                ${CMAKE_CURRENT_BINARY_DIR} ${AP_SPHINX_BUILD_DIR}
)

add_dependencies(documentation apidoc)

add_custom_target(documentation.zip
    VERBATIM
    WORKING_DIRECTORY
        ${CMAKE_BINARY_DIR}
    COMMAND
        ${CMAKE_COMMAND} -E tar "cf"
            "adaptation_pathways-${CMAKE_PROJECT_VERSION}-documentation.zip" --format=zip --
            documentation/html
)

add_dependencies(documentation.zip documentation)

set_property(
    DIRECTORY
        ${CMAKE_CURRENT_SOURCE_DIR}
    PROPERTY
        ADDITIONAL_CLEAN_FILES
            api  # apidoc
            _downloads  # sphinx-gallery
            _images  # sphinx-gallery
            _sources  # sphinx-gallery
            _static  # sphinx-build
            develop/example  # sphinx-gallery
            use/example  # sphinx-gallery
            html  # sphinx-build
)
