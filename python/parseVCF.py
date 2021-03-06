import vcf
from rdflib import Namespace, Graph, URIRef, BNode, Literal
from rdflib.namespace import DCTERMS, RDFS, RDF, DC
import urllib
import sys

chrom = dict()
chrom["X"]= "NC_000023.11"
chrom["Y"] = "NC_000024.10"
chrom["14"] = "NC_000014.9"
chrom["17"] = "NC_000017.11"
chrom["1"] = "NC_000001.11"
chrom["19"] = "NC_000019.10"
chrom["6"] = "NC_000006.12"
chrom["8"] = "NC_000008.11"
chrom["2"] = "NC_000002.12"
chrom["7"] = "NC_000007.14"
chrom["20"] = "NC_000020.11"
chrom["3"] = "NC_000003.12"
chrom["16"] = "NC_000016.10"
chrom["21"] = "NC_000021.9"
chrom["22"] = "NC_000022.11"
chrom["15"] = "NC_000015.10"
chrom["18"] = "NC_000018.10"
chrom["4"] = "NC_000004.12"
chrom["9"] = "NC_000009.12"
chrom["13"] = "NC_000013.11"
chrom["10"] = "NC_000010.11"
chrom["5"] = "NC_000005.10"
chrom["11"] = "NC_000011.10"
chrom["12"] = "NC_000012.12"
chrom["MT"] = "NC_012920.1"

vcfGraph = Graph()
vcfGraph.bind("dcterms", DCTERMS)
vcfGraph.bind("wikidata_prop", URIRef("http://www.wikidata.org/prop/direct/"))
wikidataprop = Namespace("http://www.wikidata.org/prop/direct/")

vcf_reader = vcf.Reader(open('/Users/andra/Downloads/CGC_flagship.missense_variants_snpEff_snpSift_GoNLv5.vcf', 'r'))
for record in vcf_reader:
   #print(record)
   #print(record.CHROM)
   #print(record.POS)
   # print(record.INFO['ANN'])
   for field in record.INFO['ANN'][0].split("|"):
      print(field)

   chrom_nr = chrom[record.CHROM]


   print("hgvs: "+chrom_nr+":g."+str(record.POS)+str(record.REF)+">"+str(record.ALT[0]))
   variant_uri = URIRef("http://umc.nl/genetics/FAIR/"+urllib.parse.quote_plus(chrom_nr+":g."+str(record.POS)+str(record.REF)+">"+str(record.ALT[0])))
   vcfGraph.add((variant_uri, RDF.type, URIRef("http://purl.obolibrary.org/obo/SO_0001060")))
   vcfGraph.add((variant_uri, DCTERMS.identifier, Literal(chrom_nr+":g."+str(record.POS)+str(record.REF)+">"+str(record.ALT[0]))))
   vcfGraph.add((variant_uri, URIRef("http://www.wikidata.org/prop/direct/P3331"), Literal(chrom_nr+":g."+str(record.POS)+str(record.REF)+">"+str(record.ALT[0]))))
   chromosomeIRI = URIRef("http://umc.nl/genetics/FAIR/chromosome/"+chrom_nr)
   vcfGraph.add((chromosomeIRI, RDF.type, URIRef("https://www.wikidata.org/wiki/Q37748")))
   vcfGraph.add((chromosomeIRI, DCTERMS.identifier, Literal(chrom_nr)))
   vcfGraph.add((variant_uri, DCTERMS.isPartOf, chromosomeIRI))

   # Genomic START
   vcfGraph.add((variant_uri, wikidataprop.P644, Literal(record.POS)))
   vcfGraph.add((variant_uri, wikidataprop.P645, Literal(record.POS)))
   #print(record.)
   vcfInfo = record.INFO['ANN'][0].split("|")
   gene_uri = URIRef("http://umc.nl/genetics/FAIR/gene/"+vcfInfo[3])
   print(record.INFO['ANN'][0])

   vcfGraph.add((gene_uri, DCTERMS.identifier, Literal(vcfInfo[4])))
   vcfGraph.add((variant_uri, URIRef("http://www.wikidata.org/prop/direct/P3433"), gene_uri))
   transcript_uri = URIRef("http://umc.nl/genetics/FAIR/variant/"+vcfInfo[6])

   vcfGraph.add((transcript_uri, DCTERMS.identifier, Literal(vcfInfo[6])))
   vcfGraph.add((gene_uri, URIRef("http://umc.nl/genetics/FAIR/properties/has_transcript"), transcript_uri))
   # sys.exit()

vcfGraph.serialize(destination='/tmp/UMC_gene.nt', format='n3')