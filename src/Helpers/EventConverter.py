from src.Mappings import EventParamType


def ConvertParamInt(paramInt, *paramTypes):
    eventParams = [0 for each in range(len(paramTypes))]

    for index, paramType in enumerate(paramTypes):
        if paramType[0] == EventParamType.Bool:
            eventParams[index] = paramInt % 2
            paramInt = paramInt >> 1
            break
        elif paramType[0] == EventParamType.UInt:
            eventParams[index] = paramInt % (1 << paramType[1])
            paramInt = paramInt >> paramType[1]
        elif paramType[0] == EventParamType.Int:
            val = paramInt % (1 << paramType[1] - 1)

            # Complement of two, with variable bit length
            highestBitValue = 1 << (paramType[1] - 1)

            if val >= highestBitValue:
                val = -highestBitValue + (val - highestBitValue)

            eventParams[index] = val
            paramInt = paramInt >> paramType[1]
        else:
            raise ValueError("Invalid paramType! (" + str(paramType[0]) + ")")

    return eventParams
