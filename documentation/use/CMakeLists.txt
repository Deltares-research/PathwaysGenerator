foreach(name IN ITEMS index get_started)
    configure_file(
        ${name}.rst
        ${name}.rst
        COPYONLY
    )
endforeach()
