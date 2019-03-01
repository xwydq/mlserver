import pandas as pd


class ParseMdlDat:
    '解析模型所需数据'

    # def __init__(self):
    #     # self.data = data

    def getyVar(data):
        data.columns = map(str.lower, data.columns)
        data = data.select_dtypes(include=['float', 'int', 'float64', 'int64'])
        ydat = data.filter(regex='^y$', axis=1)
        if ydat.shape[1]:
            return ydat.values
        return None

    def getxVars(data):
        data.columns = map(str.lower, data.columns)
        data = data.select_dtypes(include=['float', 'int', 'float64', 'int64'])
        xdat = data.filter(regex='^(?!^y$)', axis=1)
        if xdat.shape[1]:
            features = list(xdat.columns)
            xdats = {
                "xdat": xdat.values,
                "features": features
            }
            return xdats
        return None



# def getyVar(mdat):
#     mdat.columns = map(str.lower, mdat.columns)
#     mdat = mdat.select_dtypes(include=['float', 'int', 'float64', 'int64'])
#     mdat = mdat.filter(regex='^y$', axis=1)
#     if mdat.shape[1]:
#         return mdat.values
#     return None
#
# def getxVars(mdat):
#     mdat.columns = map(str.lower, mdat.columns)
#     mdat = mdat.select_dtypes(include=['float', 'int', 'float64', 'int64'])
#     mdat = mdat.filter(regex='^(?!^y$)', axis=1)
#     if mdat.shape[1]:
#         return mdat.values
#     return None

