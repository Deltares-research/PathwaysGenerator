foreach(name IN ITEMS environment git index release)
    configure_file(
        ${name}.rst
        ${name}.rst
        COPYONLY
    )
endforeach()
