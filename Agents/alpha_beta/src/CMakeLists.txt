set(MODULE_NAME logic)



find_package(Boost REQUIRED COMPONENTS python)

find_package(Python 3.11 REQUIRED EXACT COMPONENTS Interpreter Development)


# 输出Python包的路径
if(Python_FOUND)
    message(STATUS "Python found: ${Python_EXECUTABLE}")
    message(STATUS "Python include directory: ${Python_INCLUDE_DIRS}")
    message(STATUS "Python libraries: ${Python_LIBRARIES}")
else()
    message(FATAL_ERROR "Python not found.")
endif()

# 找到Qt5
find_package(Qt5 REQUIRED COMPONENTS Core Gui Widgets)
if(Qt5_FOUND)
    message(STATUS "Qt5 found: ${Qt5_DIR}")
    message(STATUS "Qt5Core_INCLUDE_DIRS: ${Qt5Core_INCLUDE_DIRS}")
    message(STATUS "Qt5Widgets_INCLUDE_DIRS: ${Qt5Widgets_INCLUDE_DIRS}")

else()
    message(FATAL_ERROR "Qt@5 not found.")
endif()


include_directories(${Boost_INCLUDE_DIRS} ${Python_INCLUDE_DIRS} ${Qt5Core_INCLUDE_DIRS} ${Qt5Widgets_INCLUDE_DIRS})
link_libraries(${Boost_LIBRARIES} ${Python_LIBRARIES} ${Qt5_LIBRARIES} ${Qt5Core_LIBRARIES} ${Qt5Widgets_LIBRARIES})


add_library(${MODULE_NAME} SHARED logic.cpp logic.h)

set_target_properties(
    ${MODULE_NAME}
    PROPERTIES
    PREFIX ""
)


target_link_libraries(${MODULE_NAME} Boost::python Python::Python Qt5::Core)

