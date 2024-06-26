add_custom_command(
    OUTPUT
        pathways-1-actions_graph.svg
        pathways-1-pathways_graph.svg
        pathways-1-pathways_map.svg
    COMMAND
        ${CMAKE_COMMAND}
            -E env "PYTHONPATH=${PROJECT_SOURCE_DIR}/source/package:$ENV{PYTHONPATH}"
                ${Python3_EXECUTABLE} ${AP_PLOT_GRAPHS}
                    ${CMAKE_CURRENT_SOURCE_DIR}/pathways-1.txt ${CMAKE_CURRENT_BINARY_DIR}
)

configure_file(presentation.qmd presentation.qmd COPYONLY)

add_custom_target(presentation.2023.12.05
    COMMAND
        ${Quarto_EXECUTABLE}
            render ${CMAKE_CURRENT_BINARY_DIR}/presentation.qmd --to html
    DEPENDS
        pathways-1-actions_graph.svg
        pathways-1-pathways_graph.svg
        pathways-1-pathways_map.svg
    BYPRODUCTS
        presentation.html
)

set_property(
    DIRECTORY
        ${CMAKE_CURRENT_SOURCE_DIR}
    PROPERTY
        ADDITIONAL_CLEAN_FILES
            presentation_files
)

configure_file(graph.qmd graph.qmd COPYONLY)

add_custom_target(presentation.2023.12.graph
    COMMAND
        ${Quarto_EXECUTABLE}
            render ${CMAKE_CURRENT_BINARY_DIR}/graph.qmd --to html
    BYPRODUCTS
        graph.html
)

set_property(
    DIRECTORY
        ${CMAKE_CURRENT_SOURCE_DIR}
    PROPERTY
        ADDITIONAL_CLEAN_FILES
            graph_files
)
