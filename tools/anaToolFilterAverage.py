import numpy

def filter(datalist, indexlist, window_size):
    data = numpy.array(datalist)
    
    # 1. Create uniform weights kernel
    kernel = numpy.ones(window_size) / window_size
    
    # 2. Convolve with mode='same' (keeps original length)
    tmp = numpy.convolve(data, kernel, mode='same')
    ret_list = tmp.tolist()
    
    # 3. Calculate dynamic padding offset
    padding_len = int(window_size / 2)
    
    # FIX: Slice BOTH lists equally so their lengths match perfectly
    sliced_data = ret_list[padding_len:-padding_len]
    sliced_index = indexlist[padding_len:-padding_len]
    
    return sliced_data, sliced_index