from flask import Blueprint, redirect
import flask_restx
from flask_restx import Resource, reqparse
from random import randint
import subprocess
from os import path
import sqlite3
from html.parser import HTMLParser

from sanskrit_parser.base.sanskrit_base import SanskritObject, SLP1
from sanskrit_parser.parser.sandhi_analyzer import LexicalSandhiAnalyzer
from sanskrit_parser.parser.datastructures import VakyaGraph

URL_PREFIX = '/v1'
api_blueprint = Blueprint(
    'sanskrit_parser', __name__,
    template_folder='templates'
)
strict_io = True

api = flask_restx.Api(app=api_blueprint, version='1.0', title='sanskrit_parser API',
                      description='For detailed intro and to report issues: see <a href="https://github.com/kmadathil/sanskrit_parser">here</a>. '
                      'A list of REST and non-REST API routes avalilable on this server: <a href="../sitemap">sitemap</a>.',
                      default_label=api_blueprint.name,
                      prefix=URL_PREFIX, doc='/docs')

dict_ns = api.namespace('dict', description='Dictionaries operations')

LEXICON_DICT_LIST = ["vcp", "skd", "mw", "mwe"]
LEXICON_SAN_DICT_LIST = ["vcp", "skd", "mw"]

analyzer = LexicalSandhiAnalyzer()

vcp_dict_conn = sqlite3.connect('data/vcp.sqlite')
skd_dict_conn = sqlite3.connect('data/skd.sqlite')
mwe_dict_conn = sqlite3.connect('data/mwe.sqlite')
mws_dict_conn = sqlite3.connect('data/mw.sqlite')

DICT_CONN_LIST = {'vcp': vcp_dict_conn, 'skd': skd_dict_conn, 'mwe': mwe_dict_conn, 'mw': mws_dict_conn}


def jedge(pred, node, label):
    return (node.pada.devanagari(strict_io=False),
            jtag(node.getMorphologicalTags()),
            SanskritObject(label, encoding=SLP1).devanagari(strict_io=False),
            pred.pada.devanagari(strict_io=False))


def jnode(node):
    """ Helper to translate parse node into serializable format"""
    return (node.pada.devanagari(strict_io=False),
            jtag(node.getMorphologicalTags()), "", "")


def jtag(tag):
    """ Helper to translate tag to serializable format"""
    return (tag[0].devanagari(strict_io=False), [t.devanagari(strict_io=False) for t in list(tag[1])])


def jtags(tags):
    """ Helper to translate tags to serializable format"""
    return [jtag(x) for x in tags]


@api.route('/tags/<string:p>')
class Tags(Resource):
    def get(self, p):
        """ Get lexical tags for p """
        pobj = SanskritObject(p, strict_io=strict_io)
        tags = analyzer.getMorphologicalTags(pobj)
        if tags is not None:
            ptags = jtags(tags)
        else:
            ptags = []
        r = {"input": p, "devanagari": pobj.devanagari(), "tags": ptags}
        return r


@api.route('/splits/<string:v>')
@api.param('max_paths', default=10)
@api.param('as_devanagari', default=False)
class Splits(Resource):
    def get(self, v):
        parser = reqparse.RequestParser()
        parser.add_argument('max_paths', type=int, default=10)
        parser.add_argument('as_devanagari', type=bool, default=False)
        args = parser.parse_args()
        max_paths = args.get('max_paths', 10)
        as_devanagari = args.get('as_devanagari', False)

        """ Get lexical tags for v """
        vobj = SanskritObject(v, strict_io=strict_io, replace_ending_visarga=None)
        g = analyzer.getSandhiSplits(vobj)
        if g:
            splits = g.find_all_paths(max_paths)
            if as_devanagari == True:
                jsplits = [[ss.devanagari(strict_io=strict_io) for ss in s] for s in splits]
            else:
                jsplits = [[ss.canonical(strict_io=strict_io) for ss in s] for s in splits]
        else:
            jsplits = []
        r = {"input": v, "devanagari": vobj.devanagari(), "splits": jsplits}
        return r


@api.route('/sandhi/<string:v1>/<string:v2>')
@api.param('as_devanagari', default=False)
class Joins(Resource):
    def get(self, v1, v2):
        parser = reqparse.RequestParser()
        parser.add_argument('as_devanagari', type=bool, default=False)
        args = parser.parse_args()
        as_devanagari = args.get('as_devanagari', False)

        """ Get lexical tags for v """
        vobj1 = SanskritObject(v1, strict_io=strict_io, replace_ending_visarga=None)
        vobj2 = SanskritObject(v2, strict_io=strict_io, replace_ending_visarga=None)
        joins = analyzer.sandhi.join(vobj1, vobj2)
        if as_devanagari == True:
            jjoins = [SanskritObject(s, strict_io=strict_io).devanagari() for s in joins]
        else:
            jjoins = [s for s in joins]
        r = {"input": [v1, v2], "devanagari": [vobj1.devanagari(), vobj2.devanagari()], "joins": jjoins}
        return r


@api.route('/analyses/<string:v>')
class Morpho(Resource):
    def get(self, v):
        """ Get morphological tags for v """
        vobj = SanskritObject(v, strict_io=strict_io, replace_ending_visarga=None)
        g = analyzer.getSandhiSplits(vobj, tag=True)
        if g:
            splits = g.find_all_paths(10, score=True)
        else:
            splits = []
        mres = {}
        plotbase = {}
        for sp in splits:
            bn = f"{randint(0,9999):4}"
            vg = VakyaGraph(sp, max_parse_dc=5)
            sl = "_".join([n.devanagari(strict_io=False)
                           for n in sp])
            for (ix, p) in enumerate(vg.parses):
                if sl not in mres:
                    mres[sl] = []
                t = []
                for n in p:
                    preds = list(p.predecessors(n))
                    if preds:
                        pred = preds[0]  # Only one
                        lbl = p.edges[pred, n]['label']
                        t.append(jedge(pred, n, lbl))
                    else:
                        t.append(jnode(n))
                mres[sl].append(t)
            plotbase[sl] = bn
            try:
                vg.write_dot(f"static/{bn}.dot")
            except Exception:
                pass
        r = {"input": v, "devanagari": vobj.devanagari(), "analysis": mres, "plotbase": plotbase}
        return r

    @api.route('/graph/<string:v>')
    class Graph(Resource):
        def get(self, v):
            """ Get graph for v """
            if not path.exists(f"static/{v}.dot.png"):
                subprocess.run(f"dot -Tpng static/{v}.dot -O", shell=True)
            return redirect(f"/static/{v}.dot.png")

# Dictionaries are from https://www.sanskrit-lexicon.uni-koeln.de

# def search_dict_for_text(text,in_dict='vcp',max_hits=10,search_text=False):


@dict_ns.route('/<string:dictionary>/keys/<string:text>')
@dict_ns.param('max_hits', default=10)
@dict_ns.param('search_text', default=False)
@dict_ns.param('in_devanagari', default=False)
class DictKeySearch(Resource):
    def get(self, dictionary, text):
        parser = reqparse.RequestParser()
        parser.add_argument('max_hits', type=int, default=10)
        parser.add_argument('search_text', type=bool, default=False)
        parser.add_argument('in_devanagari', type=bool, default=False)
        args = parser.parse_args()
        max_hits = args.get('max_hits', 10)
        search_text = args.get('search_text', False)
        in_devanagari = args.get('in_devanagari', False)

        """ Get keys matching for text """
        # pobj = SanskritObject(text, strict_io=strict_io)
        if text.find('*') >= 0 or text.find('_') >= 0:
            t = text.replace('*', '%')
            t = (t, t + '%', max_hits) if search_text else (t, max_hits)
        else:
            t = (text + '%', '%' + text + '%', max_hits) if search_text else (text + '%', max_hits)
        keys = []
        keys_devanagari = []

        try:
            if not DICT_CONN_LIST[dictionary]:
                # TODO: deveating from standard dictionary format, special handling required
                return []

            c = DICT_CONN_LIST[dictionary].cursor()
            res = []

            if search_text:
                res = c.execute(f"select distinct key from {dictionary} where key like ? or data like ? limit ? ", t)
            else:
                res = c.execute(f"select distinct key from {dictionary} where key like ? limit ?", t)

            for row in res:
                item = {'key': row[0], 'devanagari': ''}
                if in_devanagari and dictionary in LEXICON_SAN_DICT_LIST:
                    vobj = SanskritObject(row[0], strict_io=strict_io, replace_ending_visarga=None)
                    item['devanagari'] = vobj.devanagari()
                keys.append(item)
        except Exception as e:
            print('exception', e)
            pass
        # finally:
            # vcp_dict_conn.close()

        r = {"input": text,  "keys": keys}
        return r


@dict_ns.route('/<string:dictionary>/meanings')
@dict_ns.param('max_hits', default=10)
@dict_ns.param('in_devanagari', default=False)
class DictMeaningSearch(Resource):
    def post(self, dictionary):
        parser = reqparse.RequestParser()
        parser.add_argument('max_hits', type=int, default=10)
        parser.add_argument('in_devanagari', type=bool, default=False)
        parser.add_argument('keys', type=list, default=[], location="json")
        args = parser.parse_args()
        max_hits = args.get('max_hits', 10)
        in_devanagari = args.get('in_devanagari', False)
        keys = args.get('keys', [])

        res = []

        for key in keys:
            sub_keys = get_meanings_for_key(dictionary, key, in_devanagari, max_hits)
            res.extend(sub_keys)

        r = {"input": keys,  "keys": res}
        return r


@dict_ns.route('/<string:dictionary>/meanings/<string:key>')
@dict_ns.param('max_hits', default=10)
@dict_ns.param('in_devanagari', default=False)
class DictMeaningSearch(Resource):
    def get(self, dictionary, key):
        parser = reqparse.RequestParser()
        parser.add_argument('max_hits', type=int, default=10)
        parser.add_argument('in_devanagari', type=bool, default=False)
        args = parser.parse_args()
        max_hits = args.get('max_hits', 10)
        in_devanagari = args.get('in_devanagari', False)
        keys = get_meanings_for_key(dictionary, key, in_devanagari, max_hits)

        r = {"input": key,  "keys": keys}
        return r


def get_meanings_for_key(dictionary, key, in_devanagari, max_hits):
    """ Get keys matching for key """
    # pobj = SanskritObject(key, strict_io=strict_io)

    t = (key, max_hits)
    keys = []

    try:
        if not DICT_CONN_LIST[dictionary]:
            # TODO: deveating from standard dictionary format, special handling required
            return []

        c = DICT_CONN_LIST[dictionary].cursor()
        res = c.execute(f"select * from {dictionary} where key = ? limit ?", t)
        for row in res:
            res = {
                'key': row[0],
                'lnum': row[1],
                'data': convert_content_to_markdown(dictionary=dictionary, content=row[2], in_devanagari=in_devanagari)
            }
            keys.append(res)
    except Exception as e:
        print('exception', e)
        pass
    # finally:
        # DICT_CONN_LIST[dictionary].close()

    return keys


def convert_content_to_markdown(dictionary, content, in_devanagari):
    if dictionary in LEXICON_DICT_LIST:
        return convert_lexicon_html_to_markdown(dictionary=dictionary, in_devanagari=in_devanagari, content=content)
    return content


def convert_lexicon_html_to_markdown(dictionary, in_devanagari, content):
    parser = LexiconHTMLParser()
    parser.init(dictionary=dictionary, in_devanagari=in_devanagari)
    parser.feed(content)

    return parser.mark_down

# lexicon sample entry
# <H1><h><key1>AGrARa</key1><key2>AGrARa</key2></h><body><s>AGrARa tri0 A + GrA</s>—<s>kta . 1 gfhItaganDe puzpAdO nAsi-</s> <lb/><s>kayA yasya ganDajYAnaM jAtaM tasmin 2 tfpte ca BAve kta .</s> <lb/><s>3 ganGagrahaRe 4 tfptO ca na0 .</s></body><tail><L>6432</L><pc>0624,a</pc></tail></H1>


class LexiconHTMLParser(HTMLParser):
    tag_stack = []
    current_tag = ''
    mark_down = ''
    dictionary = ''
    in_devanagari = False

    def init(self, dictionary='', in_devanagari=False):
        self.dictionary = dictionary
        self.in_devanagari = in_devanagari

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        self.current_tag = tag
        self.tag_stack.append(tag)
        data = ''
        if tag == 'h':
            data = '**'
        elif tag.startswith('key'):
            data = ' _'
        elif tag in ['body', 'lb', 's']:
            data = '  \n'
        else:
            data = ''

        self.mark_down = self.mark_down + data

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        self.current_tag = self.tag_stack.pop()
        data = ''
        if tag == 'h':
            data = '**'
        elif tag.startswith('key'):
            data = '_ '
        else:
            data = ''
        self.mark_down = self.mark_down + data

    def handle_data(self, data):
        # print("Encountered some data  :", self.current_tag, ': ', data)
        final_data = data
        if self.current_tag in ['l', 'pc']:  # as of not not using this info
            return
        if self.current_tag == 's' and self.in_devanagari:  # convert to sanskrit
            vobj = SanskritObject(data, strict_io=strict_io, replace_ending_visarga=None)
            final_data = vobj.devanagari()
        self.mark_down = self.mark_down + final_data
