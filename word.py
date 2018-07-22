from wordsegment import load, segment

load()
string = 'TUTORIALSHEET#61.Aconfinedquiferis25mthickand2kmwide.Twoobservationwellslocated2kmapart' \
         'inthedirectionofflowindicatehydraulicheadof45and39.5m.Ifthecoefficientofpermeability' \
         'oftheaquiferis30m/day,calculate(i)totaldailyflowthroughtheaquifer,and(ii)piezometricheadatan' \
         'observationwelllocatedat300mfromtheupstreamwell.'
print(segment(string))