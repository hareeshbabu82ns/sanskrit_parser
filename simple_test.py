from sanskrit_parser import Parser
from sanskrit_parser.parser.sandhi import Sandhi
from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, DEVANAGARI, SLP1, SanskritObject
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer

lexan = LexicalSandhiAnalyzer()

# sandhi joins
obj1 = SanskritImmutableString('kon', encoding=SLP1)
obj2 = SanskritImmutableString('vasmin', encoding=SLP1)
joins = lexan.sandhi.join(first_in=obj1, second_in=obj2)
print('joins: ', joins)
splits = lexan.sandhi.split_all(SanskritImmutableString(list(joins)[0]), stop=5)
print('splits: ', [[SanskritImmutableString(s).devanagari() for s in split] for split in splits])

# sandhi splits
obj = SanskritObject('astyuttarasyAMdiSi', encoding=SLP1)
graph = lexan.getSandhiSplits(obj)
splits = graph.find_all_paths(3)
print('\nlexical: splits: ')
for split in splits:
    for i, parse in enumerate(split):
        print(f'Parse {i}: {parse.devanagari()}')

# lexical tags
obj = SanskritImmutableString("kuru", encoding=SLP1)
ts = lexan.getMorphologicalTags(obj)
print('\nlexical: tags: ', ts)

obj = SanskritObject('मूढ जहीहि धनागमतृष्णां कुरु सद्बुद्धिं मनसि वितृष्णाम्', encoding=DEVANAGARI)
graph = lexan.getSandhiSplits(obj)
splits = graph.find_all_paths(10)
print('\nlexical: splits: Devanagari ')
for split in splits:
    print(split)

sentence = SanskritObject("mAmakAH pANDavAshchaiva kimakurvata sa~njaya")  # "astyuttarasyAMdishidevatAtmA"
splits = lexan.getSandhiSplits(sentence).find_all_paths(10)
print('\nlexical: splits: SLP1 ')
for split in splits:
    print(split)
