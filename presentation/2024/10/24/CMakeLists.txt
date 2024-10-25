configure_file(presentation.qmd presentation.qmd COPYONLY)

add_custom_target(presentation.2024.10.24
    COMMAND
        ${Quarto_EXECUTABLE}
            render ${CMAKE_CURRENT_BINARY_DIR}/presentation.qmd --to html
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
