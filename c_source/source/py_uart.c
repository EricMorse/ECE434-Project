/*
Copyright (c) 2013 Adafruit
Author: Justin Cooper

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include "Python.h"
#include "constants.h"
#include "common.h"
#include "c_uart.h"
#include "c_pinmux.h"

const char *valid_uarts[4] = {"UART1", "UART2", "UART4", "UART5"};

// python function cleanup()
static PyObject *py_cleanup(__attribute__ ((unused)) PyObject *self, __attribute__ ((unused)) PyObject *args)
{
    // unexport the UART
    uart_cleanup();

    Py_RETURN_NONE;
}

// python function setup()
static PyObject *py_setup_uart(__attribute__ ((unused)) PyObject *self, PyObject *args)
{
    char dt[FILENAME_BUFFER_SIZE];
    char *channel;
    BBIO_err err;

    if (!PyArg_ParseTuple(args, "s", &channel)) {
        PyErr_SetString(PyExc_ValueError, "Invalid UART channel.");
        return NULL;
    }

    err = get_uart_device_tree_name(channel, dt);
    if (err != BBIO_OK) {
        PyErr_SetString(PyExc_ValueError, "Invalid UART channel.");
        return NULL;
    }

    err = uart_setup(dt);
    if (err != BBIO_OK) {
        PyErr_SetString(PyExc_RuntimeError, "Unable to export UART channel.");
        return NULL;        
    }

#ifdef BBBVERSION41
    uart_t *p;
    for (p = uart_table; p->name != NULL; ++p) {
        if (strcmp(p->name, channel) == 0) {
            err = set_pin_mode(p->rx, "uart");
            //Check if set_pin_mode() returned no error
            if (err != BBIO_OK) {
                fprintf(stderr, "py_setup_uart(%s): set_pin_mode() failed for pin=%s", channel, p->rx);
                PyErr_SetString(PyExc_ValueError, "Set pin mode failed for uart channel.");
                return NULL;
            }

            err = set_pin_mode(p->tx, "uart");
            //Check if set_pin_mode() returned no error
            if (err != BBIO_OK) {
                fprintf(stderr, "py_setup_uart(%s): set_pin_mode() failed for pin=%s", channel, p->tx);
                PyErr_SetString(PyExc_ValueError, "Set pin mode failed for uart channel.");
                return NULL;
            }
        }
    }
#endif

    Py_RETURN_NONE;
}

static const char moduledocstring[] = "UART functionality of a BeagleBone using Python";

PyMethodDef uart_methods[] = {
    {"setup", py_setup_uart, METH_VARARGS, "Set up and start the UART channel."},
    {"cleanup", py_cleanup, METH_VARARGS, "Clean up UART."},
    //{"setwarnings", py_setwarnings, METH_VARARGS, "Enable or disable warning messages"},
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION > 2
static struct PyModuleDef bbuartmodule = {
    PyModuleDef_HEAD_INIT,
    "UART",       // name of module
    moduledocstring,  // module documentation, may be NULL
    -1,               // size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
    uart_methods
};
#endif

#if PY_MAJOR_VERSION > 2
PyMODINIT_FUNC PyInit_UART(void)
#else
PyMODINIT_FUNC initUART(void)
#endif
{
    PyObject *module = NULL;

#if PY_MAJOR_VERSION > 2
    if ((module = PyModule_Create(&bbuartmodule)) == NULL)
       return NULL;
#else
    if ((module = Py_InitModule3("UART", uart_methods, moduledocstring)) == NULL)
       return;
#endif

   define_constants(module);


#if PY_MAJOR_VERSION > 2
    return module;
#else
    return;
#endif
}
