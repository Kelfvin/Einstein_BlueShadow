#include "extern.h"
#include <boost/python.hpp>
#include <iostream>

Hello::Hello() {}

void Hello::sayHello() { std::cout << "Hello, world!" << std::endl; }


// 导出 Hello 类到 Python 模块
BOOST_PYTHON_MODULE(hello) {
    using namespace boost::python;
    class_<Hello>("Hello")
        .def("sayHello", &Hello::sayHello)
    ;
}