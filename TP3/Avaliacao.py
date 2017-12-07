def CalculatePrecisionRecall(reco, term):
    prec = 0
    for element in reco:
        if element in term:
            prec = prec + 1

    return prec/len(reco), prec/len(term)

def avaliation(reco2):
    termBelo = open('Belo Horizonte.dat', 'r').read().split(',')
    termIrla = open('Irlanda.dat', 'r').read().split(',')
    termSap = open('São Paulo.dat', 'r').read().split(',')
    numAval = [5,10,25,50]
    reco = list(); recall_BH = list(); precis_BH = list(); recall_I = list(); precis_I = list(); recall_SP = list(); precis_SP = list()

    for element in reco2:
        reco.append(str(element))

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

    print ('\nPrecisao "Belo Horizonte:"\n@5 ', precis_BH[0], '\n@10', precis_BH[1], '\n@25', precis_BH[2], '\n@50', precis_BH[3])        
    print ('\nPrecisao "Irlanda:"\n@5 ', precis_I[0], '\n@10', precis_I[1], '\n@25', precis_I[2], '\n@50', precis_I[3])        
    print ('\nPrecisao "Sao Paulo:"\n@5 ', precis_SP[0], '\n@10', precis_SP[1], '\n@25', precis_SP[2], '\n@50', precis_SP[3])        
    print ('\nRevocacao "Belo Horizonte:"\n@5 ', recall_BH[0], '\n@10', recall_BH[1], '\n@25', recall_BH[2], '\n@50', recall_BH[3])        
    print ('\nRevocacao "Irlanda:"\n@5 ', recall_I[0], '\n@10', recall_I[1], '\n@25', recall_I[2], '\n@50', recall_I[3])        
    print ('\nRevocacao "Sao Paulo:"\n@5 ', recall_SP[0], '\n@10', recall_SP[1], '\n@25', recall_SP[2], '\n@50', recall_SP[3])        
    
    return
#testeDocID = [484,1083,18111,19588,29241,35985,38636,40226,43658,47967]
#avaliation(testeDocID)