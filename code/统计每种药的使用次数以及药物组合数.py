import pandas as pd

df=pd.read_csv(r'C:\Users\pinkpigma\pinkpigma的同步盘\KDD研二上\可解释性框架-工作\数据\patient_diagnoses2000_ndc300_with_history_delete1.csv', encoding='utf-8')

# print(df)

drugs = ['00338001702', '00338004904', '00338004903', '00409672924', '00517570425', '51079025520', '00338004902', '00338070341', '00338355248', '00338004938', '00338011704', '00456066270', '63323026201', '55390007310', '00088222033', '00008084199', '58177020211', '00517260225', '58177000111', '00074610204', '00904224461', '00182844789', '00517391025', '00338055318', '00409176230', '00641040025', '00002831501', '00002821501', '00409665305', '61553008348', '00008092355', '00338055002', '00409490234', '00904516561', '00409792337', '51079000220', '00517571025', '00338001704', '00781305714', '00574705050', '00409198530', '00338008504', '00121054410', '00904404073', '51079080120', '49502069724', '00338001731', '00409729501', '10019016312', '10019003867', '00517090125', '64253033335', '63739008901', '00487980125', '00056017275', '00074198530', '00338001703', '00056016975', '63323026965', '00338004304', '00409128331', '54569523500', '55390000401', '00409610204', '00054848616', '08290036005', '00406055262', '00713016550', '00904526161', '00002735501', '00074407532', '00406051262', '63323031110', '00245004101', '58177000104', '00409131230', '63653117103', '00338004931', '00310030011', '10019003783', '17314931102', '00074665305', '00045025501', '00264751020', '00338067104', '60258000601', '00143987310', '51079041720', '00409662502', '00074148402', '00409125830', '00409779362', '00056017075', '62584078833', '63323026920', '63739002401', '00054839224', '00703450204', '00121065721', '00409433201', '10019002710', '00487950125', '00074779362', '63323061603', '00338002304', '17714001110', '00045050130', '00165002241', '00641037625', '51079012620', '63739027201', '00703115303', '00054829725', '66553000401', '00536338101', '00074233411', '51079038620', '51079001920', '10019051002', '60505068104', '00904399061', '00074177825', '00338519741', '00517293025', '00121043130', '00904777261', '66689036430', '51079055271', '67467064301', '00338070948', '55390034810', '10019017644', '00002751001', '00056017675', '55390005710', '00006494300', '00469061711', '50242004413', '00054001820', '00409665106', '00074176230', '00781345295', '00904770418', '00206886202', '00045152510', '51079096620', '00677178110', '51079090620', '00409781124', '00008081401', '17714002001', '00074781124', '00409148402', '00006473900', '10019002803', '67618030011', '00597001314', '00597008717', '00904053061', '00172375810', '00206885216', '00002445385', '00006353750', '00008092303', '00054829925', '00409739172', '', '00093521193', '00071015540', '00045152010', '00338500241', '00074662502', '00310027539', '00024540134', '00088120806', '00338069104', '00045006801', '00310032520', '00406717162', '51079045420', '51079000522', '00074125901', '00003045051', '63323001302', '00182050789', '00009090020', '10432017002', '00944049101', '55390013020', '00904150061', '55390014710', '51079045620', '00172531210', '00300304613', '00074302401', '00548301200', '63323061401', '63323047401', '00173024256', '17270072101', '51079028520', '00074180001', '52959067430', '00173044202', '00054465025', '00074792201', '00054872425', '00472500360', '00034120081', '00054872625', '00008418806', '00085036207', '49502069703', '00074176201', '51079004120', '00074144304', '00409180001', '00409117830', '10019001303', '49502068524', '10019002804', '51079045120', '00409477702', '63323038810', '51079087101', '63323018410', '00074729501', '63323022110', '00517760425', '00054001720', '00338105102', '63323016101', '00074241612', '00074158411', '00517460525', '00182845389', '68094020462', '00264310311', '11098003002', '00338008904', '00071015823', '60505260400', '63323016501', '00338001710', '00074115170', '00182116189', '10019001617', '00338070541', '51079090520', '00338268975', '00517570225', '00172376010', '51079033530', '00904198861', '66591018442', '00409915801', '00409606211', '00087057007', '33332001001', '51991045757', '00904504561', '51079007220', '00469065773', '60977045101', '00409127332', '00206885516', '00182138167', '00045006701', '58177032304', '33332001101', '00071015640', '00904272561', '00074131230', '43825010201', '00406051201', '00182117089', '51079074520', '00409163802', '00548590000', '54868277600', '00074915801', '00182853489', '00310030050', '61553011841', '00069153041', '00172438210', '00338001738', '00002871501', '55390046001', '17478093401', '00064065001', '60505251903', '00009338901', '51079075920', '00338001701', '51079000620', '00310013039', '00007313705', '00172439018', '63481062375']

first_header = []
second_header = []
history_header = []

for i in drugs:
    first_header.append(i+'_first')
    second_header.append(i + '_second')
    history_header.append(i + '_history')

for i in second_header:
    drug_list = list(df[i].values)
    # print(drug_list)
    print(i, drug_list.count(1))