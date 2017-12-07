def CalculatePrecisionRecall(reco, term):
    prec = 0
    for element in reco:
        if element in term:
            prec = prec + 1

    return prec/len(reco), prec/len(term)

def avaliation(reco):
    termBelo = open('Belo Horizonte.dat', 'r').read().split(',')
    termIrla = open('Irlanda.dat', 'r').read().split(',')
    termSap = open('São Paulo.dat', 'r').read().split(',')
    numAval = [5,10,25,50]
    recall_BH = list()
    precis_BH = list()
    recall_I = list()
    precis_I = list()
    recall_SP = list()
    precis_SP = list()

    for index in numAval:
        prec, rec = CalculatePrecisionRecall(reco[0:index], termBelo)
        recall_BH.append(rec)
        precis_BH.append(prec)        
        
        prec, rec = CalculatePrecisionRecall(reco[0:index], termIrla)
        recall_I.append(rec)
        precis_I.append(prec)        
        
        prec, rec = CalculatePrecisionRecall(reco[0:index], termSap)
        recall_SP.append(rec)
        precis_SP.append(prec)        

    print (recall_SP)        
    return
reco = [484,1083,18111,19588,29241,35985,38636,40226,43658,47967,49186,49772,69168,80198,91593,91853,23467,78,345,234,1,3,23467,78,345,234,1,3,23467,78,345,234,1,3,23467,78,345,234,1,3,23467,78,345,234,1,3,23467,78,345,234,1,3]
avaliation(reco)
