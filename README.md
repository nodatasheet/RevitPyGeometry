# RevitPyGeometry
A collection of utils for Revit geometry written in IronPython.

## Description

Geometry primitives are wrappers around Revit standard geometry to use existing methods and extend them with custom utils.

[SymPy/geometry](https://docs.sympy.org/latest/modules/geometry/index.html) module is used as a base structure also some for wrappers and utils.

## Notes

### Compatibility

- Main purpose is to use it in [pyRevit](https://github.com/eirannejad/pyRevit) until I find a suitable library. So probably it may depend on it in future.

- So far I'm working in IronPython 2.7, but may switch to IronPython 3.x in future.

- On [Pavel Altynnikov's](https://github.com/PavelAltynnikov) recommendation (and with his great help), I made this library independent from the Revit DB itself. We use `Abstract Revit Object` which represents Revit API types.

**I will try to keep it compatible with ipy2/3 and independent from other frameworks as long as possible.**

...but can't promise anything, since I'm still learning ^_^

### WIP

- It is still work in progress. Many things will be changing. So don't rely on it until I get to some sort of stable structure.
