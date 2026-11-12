from . import anaToolFilterGaussian, anaToolFilterButterworth


def proc(numpyXarray, numpyYarray, debug_level):
    # filter the curve
    filterOutXarray, filterOutYarray = anaToolFilterGaussian.proc(numpyXarray, numpyYarray, debug_level)
    retXarray, retYarray, paddingLen = anaToolFilterButterworth.proc(filterOutXarray, filterOutYarray, debug_level)
    return retXarray, retYarray, paddingLen
