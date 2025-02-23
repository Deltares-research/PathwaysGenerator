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
    index.md
    develop/index.md
    use/get_started.md
    use/import_export.md
    use/index.md
    use/plot.md
    # use/example/README.rst
    # use/example/README.rst
    # use/example/ex_10_pathway_map/README.rst
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














# add_subdirectory(develop)
# add_subdirectory(use)
#
# configure_file(
#     conf.py.in
#     conf.py
#     @ONLY
# )
#
# foreach(name IN ITEMS changelog glossary index)
#     configure_file(
#         ${name}.rst
#         ${name}.rst
#         COPYONLY
#     )
# endforeach()
#
# set(AP_SPHINX_SOURCE_DIR ${CMAKE_CURRENT_BINARY_DIR})
# set(AP_SPHINX_BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR}/html)
#
# # https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html
# add_custom_target(apidoc
#     VERBATIM
#     COMMAND
#         ${CMAKE_COMMAND}
#             -E env "SPHINX_APIDOC_OPTIONS=members,undoc-members,show-inheritance,inherited-members"
#                 ${Sphinx_APIDOC_EXECUTABLE}
#                     --force
#                     --separate
#                     --module-first
#                     -d 1
#                     -o ${CMAKE_CURRENT_BINARY_DIR}/api
#                     ${PROJECT_SOURCE_DIR}/source/package
# )
#
# # https://www.sphinx-doc.org/en/master/man/sphinx-build.html
# add_custom_target(documentation
#     VERBATIM
#     COMMAND
#         ${CMAKE_COMMAND} -E env "PYTHONPATH=${AP_PYTHONPATH}"
#             ${Sphinx_BUILD_EXECUTABLE}
#                 -b html
#                 -c ${CMAKE_CURRENT_BINARY_DIR}
#                 ${CMAKE_CURRENT_BINARY_DIR} ${AP_SPHINX_BUILD_DIR}
# )
#
# add_dependencies(documentation apidoc)
#
# add_custom_target(documentation.zip
#     VERBATIM
#     WORKING_DIRECTORY
#         ${CMAKE_BINARY_DIR}
#     COMMAND
#         ${CMAKE_COMMAND} -E tar "cf"
#             "adaptation_pathways-${CMAKE_PROJECT_VERSION}-documentation.zip" --format=zip --
#             documentation/html
# )
#
# add_dependencies(documentation.zip documentation)
#
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
