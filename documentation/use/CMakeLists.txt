foreach(name IN ITEMS
        generator.png
        generator.rst
        get_started.rst
        import_export.rst
        index.rst
        plot.rst
    )
    configure_file(${name} ${name} COPYONLY)
endforeach()
