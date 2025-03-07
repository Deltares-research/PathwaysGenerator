set(AP_TITLE "Adaptation pathways documentation")
set(AP_BOOK_BASENAME "adaptation_pathways-${CMAKE_PROJECT_VERSION}")

# apidoc2 requires the path to packages to be relative
file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/package)
file(CREATE_LINK
    ${PROJECT_SOURCE_DIR}/source/package/adaptation_pathways
    ${CMAKE_CURRENT_BINARY_DIR}/package/adaptation_pathways
    SYMBOLIC
)

configure_file(
    _config.yml.in
    _config.yml
    @ONLY
)

foreach(name IN ITEMS
    changelog.md
    genindex.md
    glossary.md
    index.md
    use/get_started.md
    use/import_export.md
    use/plot.md
    develop/environment.md
    develop/git.md
    develop/release.md
    _toc.yml
)
    configure_file(${name} ${name} COPYONLY)
endforeach()

add_custom_target(documentation
    VERBATIM
    COMMAND
        # https://jupyterbook.org/en/stable/reference/cli.html
        ${CMAKE_COMMAND}
            -E env "PYTHONPATH=${PROJECT_SOURCE_DIR}/source/package:$ENV{PYTHONPATH}"
                ${JupyterBook_EXECUTABLE} build
                    --builder html --all
                    ${CMAKE_CURRENT_BINARY_DIR}
)

set_property(
    DIRECTORY
        ${CMAKE_CURRENT_SOURCE_DIR}
    PROPERTY
        ADDITIONAL_CLEAN_FILES
            _build  # jupyter-book
            _config.yml
)

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

# TODO
# set_property(
#     DIRECTORY
#         ${CMAKE_CURRENT_SOURCE_DIR}
#     PROPERTY
#         ADDITIONAL_CLEAN_FILES
#             api  # apidoc
#             _downloads  # sphinx-gallery
#             _images  # sphinx-gallery
#             _sources  # sphinx-gallery
#             _static  # sphinx-build
#             develop/example  # sphinx-gallery
#             use/example  # sphinx-gallery
#             html  # sphinx-build
# )
