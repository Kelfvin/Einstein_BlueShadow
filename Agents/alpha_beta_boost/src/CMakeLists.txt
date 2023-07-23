set(MODULE_NAME logic)

# set(CMAKE_BUILD_TYPE "Debug")

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


add_library(${MODULE_NAME} SHARED logic.cpp logic.h)

set_target_properties(
    ${MODULE_NAME}
    PROPERTIES
    PREFIX ""
    SUFFIX ".so"
)


target_link_libraries(${MODULE_NAME} Boost::python Python::Python)

