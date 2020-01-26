# im@sparqlからアイドルの呼び名一覧を取得し、jsonとして保存する
import json
import codecs
from SPARQLWrapper import SPARQLWrapper, JSON


class IdolNameList:
    def __init__(self):
        self.idol_name_dict = []

    def get_idol_name_list(self):
        sparql = SPARQLWrapper("https://sparql.crssnky.xyz/spql/imas/query")

        # すべてのアイドルの名前を取得するクエリ
        # TODO: 呼び名が取れるようにクエリを修正する
        sparql.setQuery('''
            PREFIX schema: <http://schema.org/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX imas: <https://sparql.crssnky.xyz/imasrdf/URIs/imas-schema.ttl#>
            SELECT ?name ?family_name ?given_name ?family_name_kana ?given_name_kana
            WHERE {
                ?sub rdf:type imas:Idol;
                     schema:name ?name;
                     schema:familyName ?family_name;
                     schema:givenName ?given_name;
                     imas:nameKana ?name_kana;
                     imas:familyNameKana ?family_name_kana;
                     imas:givenNameKana ?given_name_kana.
                filter(lang(?name) = "ja")
                filter(lang(?family_name) = "ja")
                filter(lang(?given_name) = "ja")
            }
        ''')

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for idol in results['results']['bindings']:
            idic = {
                'name':         idol['name']['value'],
                'family_name':  idol['family_name']['value'],
                'given_name':       idol['given_name']['value'],
                'family_name_kana': idol['family_name_kana']['value'],
                'given_name_kana':  idol['given_name_kana']['value']
            }
            self.idol_name_dict.append(idic)

        print(self.idol_name_dict)

        # jsonに出力する処理
        with codecs.open('idol_name_list.json', 'w', 'utf-8') as f:
            json.dump(self.idol_name_dict, f, ensure_ascii=False)


if __name__ == '__main__':
    inl = IdolNameList()
    inl.get_idol_name_list()
