# -*- coding: utf-8 -*-
from sanskrit_parser import enable_console_logger, enable_file_logger
from sanskrit_parser.base.sanskrit_base import SLP1, DEVANAGARI
import sanskrit_parser.generator.sutra as sutra
from sanskrit_parser.generator.paninian_object import PaninianObject
from sanskrit_parser.generator.prakriya import Prakriya, PrakriyaVakya
from sanskrit_parser.generator.pratyaya import *
from sanskrit_parser.generator.dhatu import *
from sanskrit_parser.generator.pratipadika import *
from conftest import run_test, check_vibhakti, generate_vibhakti, test_prakriya

test_list_slp1 = [
    ("kArt*", "tikaH", ["kArtikaH", "kArttikaH"]),
    ("gaRa", "upadeSaH", "gaRopadeSaH"),
    ("rAma", "eti", "rAmEti"),
    ("rAma", "iti", "rAmeti"),
    ("tyaktvA", "uttizWa", "tyaktvottizWa"),
    ("tava", "ozTaH", "tavOzTaH"),
    ("deva", "fzi", "devarzi"),
    ("gavi", "asmAkam", "gavyasmAkam"),
    ("kavI", "etau", "kavyetau"),
    ("camU", "ASraya", "camvASraya"),
    ("gavi", "iha", "gavIha"),
    ("kavI", "iha", "kavIha"),
    ("kavO", "asmAkam", "kavAvasmAkam"),
    ("AgacCa", "atra", "AgacCAtra"),
    ("yAne", "eti", "yAnaeti"),
    ("yAne", "atra", "yAnetra"),
    ("yAne", "AgacCati", "yAnaAgacCati"),
    ("vizRo", "ava", "vizRova"),
    ("haras", "Sete", ['haraHSete', 'haraSSete']),
    ("Bavat", "caraRam", "BavaccaraRam"),
    # Non pada
    ("praS*", "nas", "praSnas"),
    ("rAmas", "zazQa", ["rAmazzazQa", 'rAmaHzazQa']),
    ("rAmas", "wIkate", "rAmazwIkate"),
    ("sarpiz", "tamam", "sarpizwamam"),
    ("marut", "wIkate", "maruwwIkate"),
    ("SuBam", "karoti", ["SuBaNkaroti", "SuBaMkaroti"]),
    ("vAk", "arTO", "vAgarTO"),
    ("goDuk", "awati", "goDugawati"),
    ("goDuk", "girati", "goDuggirati"),
    ("virAw", "vadati", "virAqvadati"),
    ("kavis", "asti", "kavirasti"),
    ("havis", "vartate", ["havirvartate", "havirvvartate"]),
    ("brah*", "mA", ["brahmA", "brahmmA"]),
    ((mud, Ric), Sap, tip, "modayati"),
    (BU, Sap, tip, "Bavati"),
    (ava, (AN, "ihi"), "avehi"), # 6.1.95
    ("SivAya", "om", "SivAyom"), # 6.1.95
    (kavi, O, "kavI"),
    ("catur", "nAm", ['caturRAm', 'catur~RAm', 'caturRRAm']), #8.4.1
    ("BavAn", "liKati", "BavAl~liKati"), #8.4.60 .1
   ]

test_list_devanagari = [
    ("मरुत्", "टीकते", "मरुट्टीकते"),
    ("मधुलिट्", "तरति", "मधुलिट्तरति"),
    ("मरुत्", "षष्ठः", "मरुत्षष्ठः"),
    ("सन्", "षष्ठः", "सन्षष्ठः"),
    ("षण्", "नाम्", "षण्णाम्"),
    ("वाग्", "मुखम्", ["वाङ्मुखम्", "वाग् मुखम्"]),
     ("षड्", "मुखम्", ["षण्मुखम्", "षड्मुखम्"]),
     ("एतद्", "मुरारि", ["एतद् मुरारि", "एतन्मुरारि"]),
     ("त्रिष्टुब्", "नमति", ["त्रिष्टुम्नमति", "त्रिष्टुब् नमति"]),
     ("वाग्", "चलति", "वाक्चलति"),
     ("त्रिष्टुब्", "छन्दः", "त्रिष्टुप्छन्दः"),
     ("अस्", "ति", "अस्ति"),
     ("तत्", "लीनः", "तल्लीनः"),
     ("प्रत्यङ्", "आत्मा", "प्रत्यङ्ङात्मा"),
     ("सुगण्", "ईशः", "सुगण्णीशः"),
     ("अस्मिन्", "एव", "अस्मिन्नेव"),
     ("वाग्", "हरि", ["वाग्घरि", "वाग् हरि"]),
#     ("अज्*", "हलौ", ["अज्झलौ", "अज् हलौ"]),
     ("मधुलिड्", "हसति", ["मधुलिड्ढसति", "मधुलिड्हसति"]),
     ("तद्", "हितम्", ["तद्धितम्", "तद्हितम्"]),
     ("त्रिष्टुब्", "हि", ["त्रिष्टुब्हि", "त्रिष्टुब्भि"]),
     ("तद्", "शेते", ["तच्शेते", "तच्छेते"]),
     ("मधुलिड्", "शेते", ['मधुलिट्शेते', "मधुलिट्छेते"]),
     ("त्रिष्टुब्", "शेते", ["त्रिष्टुप्शेते", "त्रिष्टुप्छेते"]),
     ("तद्", "श्लोकेन", ["तच्श्लोकेन", "तच्छ्लोकेन"]),
     ("तत्", "जयते", "तज्जयते"),
     ("रामः", "तरति", "रामस्तरति"),
     ("बालः", "थूकरोति", "बालस्थूकरोति"),
     ("हरिः", "चलति", "हरिश्चलति"),
     ("पयः", "क्षीरम्", "पयःक्षीरम्"),
     ("कः", "त्सरुः", "कःत्सरुः"),
     ("हरिस्", "शेते", ["हरिश्शेते", "हरिःशेते"]),
     ("रामस्", "कः", "रामःकः"),
     ("रामस्", "खनति", "रामःखनति"),
     ("रामस्", "पातुः", "रामःपातुः"),
     ("वृक्षस्", "फलतु", "वृक्षःफलतु"),
     ("रामस्", "अस्ति", "रामोस्ति"),
    (("राम", su), (as_dhatu, tip), "रामोस्ति"),
    ("रामस्", "गच्छति", "रामोगच्छति"),
    ('भोस्',  'देवाः', "भोदेवाः"),
    ('भगोस्',  'मनुष्याः', "भगोमनुष्याः"),
    ('अघोस्',  'राक्षसाः', "अघोराक्षसाः"),
    ('देवास्',  'गच्छन्ति', "देवागच्छन्ति"),
    ("रामस्", "आसीत्", "राम आसीत्"),
    ("रामस्", "ईशः", "रामईशः"),
    ("भवान्", "चरति", "भवांश्चरति"),
    ("सन्", "शम्भुः", ["सञ्च्छम्भुः", 'सञ्शम्भुः', 'सञ्च्शम्भुः']),
    ("स्व", "छाया", "स्वच्छाया"),
    (AN, "छाया", "आच्छाया"),
    (AN, ((Cad, Ric), Sap, tip), "आच्छादयति"),
#    (AN, "छादयति", "आच्छादयति"),
    (mAN, "छिदत्", "माच्छिदत्"),
    ("सा", "छाया", ["साच्छाया", "साछाया"]),
    ("कार्*", "यम्", ["कार्य्यम्", "कार्यम्"]),
    ("आदित्य्", "य", ["आदित्य", "आदित्य्य"]),
    ("गो*", yat_t, "गव्य"),  
    ("नौ*", yat_t, "नाव्य"),  
    ("भू*", GaY, "भाव"),
    ("कृ*", Ric, "कारि"),
    ("औपगु*", aR_t, "औपगव"),
    ("बभ्रु*", yaY_t, "बाभ्रव्य"),
    ("नी*", tfc, "नेतृ"),
    ("भू*", Sap, "भव"),
    ("दोघ्*", "धुम्", "दोग्धुम्"),
    ("विद्वान्स्", "अपठत्", "विद्वानपठत्"),
    ("अपठन्त्", "बालकाः", "अपठन्बालकाः"), 
    (lUY, Ryat, "लाव्य"),
    (kzI, yat, ["क्षेय", "क्षय्य"]),
    (ji, yat, ["जेय", "जय्य"]),
    (wukrIY, yat, ["क्रेय", "क्रय्य"]),
     # FIXME - can't test this now
    # आ + वेञ् + यक् + त = ओयते
    ("आ", (veY_smp, yak), "ओय"),
    ("प्र", (eDa, Sap, "te"), "प्रैधते"),
    ("उप", (iR,  tip), "उपैति"),
    (pra, (fcCa, Sap, tip), "प्रार्च्छति"),
    ("ब्रह्म", "ऋषि", "ब्रह्मर्षि"),
    (AN, ((Cad, Ric), Sap, tip), "आच्छादयति"),
    (("राम", su), "आसीत्", "राम आसीत्"),
    (gfj, Sap, tip, "गर्जति"),
    (vid, tip, "वेत्ति"),
    (("राम", su), (as_dhatu, tip), "रामोस्ति"),
    (("राम", su), avasAna, "रामः ।"),
    ("वाच्", ByAm, "वाग्भ्याम्"),
    ("त्यज्", ktvA, "त्यक्त्वा"),
    (("वाच्", su), avasAna, ["वाग् ।", "वाक् ।"]),
    (("वाच्", su), (as_dhatu, tip), "वागस्ति"),
    ("मधुलिह्", ByAm, "मधुलिड्भ्याम्"),
    (("लिह्", su) , avasAna, ["लिट् ।", "लिड् ।"]),
    (qulaBaz, kta, "लब्ध"),
    (guhU, kta, "गूढ"),
    ("पुनर्", "रमते", "पुना रमते"),
    (("अग्नि", su), "रोचते", "अग्नी रोचते"),
    # FIXME: correct when we can do uttizTati, move to utTAna
    (ud, (sTA, tip), ["उत्थाति", "उत्थ्थाति"]),
    ("पुष्*", "ना", "ति", "पुष्णाति"), # 8.4.1
    ("तृंह्*", "अनीय", "तृंहणीय"), # 8.4.2
     ]

viBakti = {}
prAtipadika = {}

prAtipadika["rAma"] = rAma
viBakti["rAma"] = [
    ["रामः", "रामौ", "रामाः"],
    ["रामम्", "रामौ", "रामान्"],
    ["रामेण", "रामाभ्याम्", "रामैः"],
    ["रामाय", "रामाभ्याम्", "रामेभ्यः"],
    [["रामात्", "रामाद्"], "रामाभ्याम्", "रामेभ्यः"],
    ["रामस्य", "रामयोः", "रामाणाम्"],
    ["रामे", "रामयोः", "रामेषु"],
    ["राम", "रामौ", "रामाः"],
]

prAtipadika["sarva"] = sarva
viBakti["sarva"] = [
    ["सर्वः", "सर्वौ", "सर्वे"],
    ["सर्वम्", "सर्वौ", "सर्वान्"],
    ["सर्वेण", "सर्वाभ्याम्", "सर्वैः"],
    ["सर्वस्मै", "सर्वाभ्याम्", "सर्वेभ्यः"],
    [["सर्वस्मात्", "सर्वस्माद्"], "सर्वाभ्याम्", "सर्वेभ्यः"],
    ["सर्वस्य", "सर्वयोः", "सर्वेषाम्"], 
    ["सर्वस्मिन्", "सर्वयोः", "सर्वेषु "],
]

prAtipadika["pAda"] = pAda
viBakti["pAda"] = [
    ["पादः", "पादौ", "पादाः"],
    ["पादम्", "पादौ", ["पादान्", "पदः"]],
    [["पादेन", "पदा"], ["पादाभ्याम्", "पद्भ्याम्"], ["पादैः", "पद्भिः"]],
    [["पादाय", "पदे"], ["पादाभ्याम्", "पद्भ्याम्"], ["पादेभ्यः", "पद्भ्यः"]],
    [["पादात्", "पादाद्", "पदः"], ["पादाभ्याम्", "पद्भ्याम्"], ["पादेभ्यः", "पद्भ्यः"]],
    [["पादस्य", "पदः"], ["पादयोः", "पदोः"], ["पादानाम्", "पदाम्"]],
    [["पादे", "पदि"], ["पादयोः", "पदोः"], ["पादेषु", "पत्सु"]],
    ["पाद", "पादौ", "पादाः"],
]

prAtipadika["yUza"] = yUza
viBakti["yUza"] = [
    ["यूषः", "यूषौ", "यूषाः"],
    ["यूषम्", "यूषौ", ["यूषान्", "यूष्णः"]],
    [["यूषेण", "यूष्णा"], ["यूषाभ्याम्", "यूषभ्याम्"], ["यूषैः", "यूषभिः"]],
    [["यूषाय", "यूष्णे"], ["यूषाभ्याम्", "यूषभ्याम्"], ["यूषेभ्यः", "यूषभ्यः"]],
    [["यूषात्", "यूषाद्", "यूष्णः"], ["यूषाभ्याम्", "यूषभ्याम्"], ["यूषेभ्यः", "यूषभ्यः"]],
    [["यूषस्य", "यूष्णः"], ["यूषयोः", "यूष्णोः"], ["यूषाणाम्", "यूष्णाम्"]],
    [["यूषे", "यूषणि", "यूष्णि"], ["यूषयोः", "यूष्णोः"], ["यूषेषु", "यूषसु"]],
    ["यूष", "यूषौ", "यूषाः"],
]
prAtipadika["viSvapA"] = viSvapA
viBakti["viSvapA"] = [
    ["विश्वपाः", "विश्वपौ", "विश्वपाः"],
    ["विश्वपाम्", "विश्वपौ", "विश्वपः"],
    ["विश्वपा", "विश्वपाभ्याम्", "विश्वपाभिः"],
    ["विश्वपे", "विश्वपाभ्याम्", "विश्वपाभ्यः"],
    ["विश्वपः", "विश्वपाभ्याम्", "विश्वपाभ्यः"],
    ["विश्वपः", "विश्वपोः", "विश्वपाम्"],
    ["विश्वपि", "विश्वपोः", "विश्वपासु"],
    ["विश्वपाः", "विश्वपौ", "विश्वपाः"],
]
prAtipadika["hAhA"] = hAhA
viBakti["hAhA"] = [
    ["हाहाः", "हाहौ", "हाहाः"],
    ["हाहाम्", "हाहौ", "हाहान्"],
    ["हाहा", "हाहाभ्याम्", "हाहाभिः"],
    ["हाहै", "हाहाभ्याम्", "हाहाभ्यः"],
    ["हाहाः", "हाहाभ्याम्", "हाहाभ्यः"],
    ["हाहाः", "हाहौः", "हाहाम्"],
    ["हाहे", "हाहौः", "हाहासु"],
    ["हाहाः", "हाहौ", "हाहाः"],
]
		 
prAtipadika["hari"] = hari
viBakti["hari"] = [
    ["हरिः", "हरी", "हरयः"],
    ["हरिम्", "हरी", "हरीन्"],
    ["हरिणा", "हरिभ्याम्", "हरिभिः"],
    ["हरये", "हरिभ्याम्", "हरिभ्यः"],
    ["हरेः", "हरिभ्याम्", "हरिभ्यः"],
    ["हरेः", "हर्योः", "हरीणाम्"],
    ["हरौ", "हर्योः", "हरिषु"],
    ["हरे", "हरी", "हरयः"],
]

prAtipadika["saKi"] = saKi
viBakti["saKi"] = [
    ["सखा", "सखायौ", "सखायः"],
    ["सखायम्", "सखायौ", "सखीन्"],
    ["सख्या", "सखिभ्याम्", "सखिभिः"],
    ["सख्ये", "सखिभ्याम्", "सखिभ्यः"],
    ["सख्युः", "सखिभ्याम्", "सखिभ्यः"],
    ["सख्युः", "सख्योः", "सखीनाम्"],
    ["सख्यौ", "सख्योः", "सखिषु"],
    ["सखे", "सखायौ", "सखायः"],
]
prAtipadika["tri"] = tri
viBakti["tri"] = [
    [None, None, "त्रयः"],
    [None, None, "त्रीन्"],
    [None, None, "त्रिभिः"],
    [None, None, "त्रिभ्यः"],
    [None, None, "त्रिभ्यः"],
    [None, None, "त्रयाणाम्"],
    [None, None, "त्रिषु"],
    [None, None, "त्रयः"],
]

prAtipadika["kati"] = kati
viBakti["kati"] = [
    [None, None, "कति"],
    [None, None, "कति"],
    [None, None, "कतिभिः"],
    [None, None, "कतिभ्यः"],
    [None, None, "कतिभ्यः"],
    [None, None, "कतीनाम्"],
    [None, None, "कतिषु"],
    [None, None, "कति"],
]

prAtipadika["dvi"] = dvi
viBakti["dvi"] = [
    [None,  "द्वौ", None],
    [None,  "द्वौ", None],
    [None,  "द्वाभ्याम्", None],
    [None,  "द्वाभ्याम्", None],
    [None,  "द्वाभ्याम्", None],
    [None,  "द्वयोः", None],
    [None,  "द्वयोः", None],
    [None,  "द्वौ", None],
]
prAtipadika["pitf"] = pitf
viBakti["pitf"] = [
     ["पिता", "पितरौ", "पितरः"],
     ["पितरम्", "पितरौ", "पितॄन्"],
     ["पित्रा", "पितृभ्याम्", "पितृभिः"],
     ["पित्रे", "पितृभ्याम्", "पितृभ्यः"],
     ["पितुः", "पितृभ्याम्", "पितृभ्यः"],
     ["पितुः", "पित्रोः", "पितॄणाम्"],
     ["पितरि", "पित्रोः", "पितृषु"],
     ["पितः", "पितरौ", "पितरः"],
]

prAtipadika["tvazwf"] = tvazwf
viBakti["tvazwf"] = [
     ["त्वष्टा", "त्वष्टारौ", "त्वष्टारः"],
     ["त्वष्टारम्", "त्वष्टारौ", "त्वष्टॄन्"],
     ["त्वष्ट्रा", "त्वष्टृभ्याम्", "त्वष्टृभिः"],
     ["त्वष्ट्रे", "त्वष्टृभ्याम्", "त्वष्टृभ्यः"],
     ["त्वष्टुः", "त्वष्टृभ्याम्", "त्वष्टृभ्यः"],
     ["त्वष्टुः", "त्वष्ट्रोः", "त्वष्टॄणाम्"],
     ["त्वष्टरि", "त्वष्ट्रोः", "त्वष्टृषु"],
     ["त्वष्टः", "त्वष्टारौ", "त्वष्टारः"],
]
		
prAtipadika["mAtf"] = mAtf
viBakti["mAtf"] = [
     ["माता", "मातरौ", "मातरः"],
     ["मातरम्", "मातरौ", "मातॄः"],
     ["मात्रा", "मातृभ्याम्", "मातृभिः"],
     ["मात्रे", "मातृभ्याम्", "मातृभ्यः"],
     ["मातुः", "मातृभ्याम्", "मातृभ्यः"],
     ["मातुः", "मात्रोः", "मातॄणाम्"],
     ["मातरि", "मात्रोः", "मातृषु"],
     ["मातः", "मातरौ", "मातरः"],
]
prAtipadika["krozwu"] = krozwu
viBakti["krozwu"] = [
     ["क्रोष्टा", "क्रोष्टारौ", "क्रोष्टारः"],
     ["क्रोष्टारम्", "क्रोष्टारौ", "क्रोष्टून्"],
     [["क्रोष्ट्रा","क्रोष्टुना"], "क्रोष्टुभ्याम्", "क्रोष्टुभिः"],
     [["क्रोष्ट्रे","क्रोष्टवे"], "क्रोष्टुभ्याम्", "क्रोष्टुभ्यः"],
     [["क्रोष्टुः","क्रोष्टोः"], "क्रोष्टुभ्याम्", "क्रोष्टुभ्यः"],
     [["क्रोष्टुः","क्रोष्टोः"], ["क्रोष्ट्वोः","क्रोष्ट्रोः"],  "क्रोष्टूनाम्"],
     [["क्रोष्टरि","क्रोष्टौ"], ["क्रोष्ट्वोः","क्रोष्ट्रोः"], "क्रोष्टुषु"],
     ["क्रोष्टो", "क्रोष्टारौ", "क्रोष्टारः"],
]


if __name__ == "__main__":
    import logging
    #logging.basicConfig(level=logging.INFO)
    enable_console_logger()
    enable_file_logger(level=logging.DEBUG)
    from sutras_yaml import sutra_list

    test_prakriya(sutra_list, test_list_slp1, test_list_devanagari)
    for v in viBakti:
        check_vibhakti(generate_vibhakti(prAtipadika[v], viBakti[v]),
                       sutra_list)


