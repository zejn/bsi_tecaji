# coding: utf-8
from django.db import models, transaction
import os
import io
import datetime

class Tecaj(models.Model):
    datum = models.DateField()
    oznaka = models.TextField()
    sifra = models.TextField()
    tecaj = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        unique_together = [['datum', 'sifra']]
        index_together = ['datum', 'oznaka', 'sifra', 'tecaj']

URL_TECAJ_DAY = 'http://www.bsi.si/_data/tecajnice/dtecbs.xml'
URL_TECAJ_FULL = 'http://www.bsi.si/_data/tecajnice/dtecbs-l.xml'

def fetch(full=False):
    import requests
    import datetime
    from django.conf import settings


    if full:
        url = URL_TECAJ_FULL
        which = 'full'
    else:
        url = URL_TECAJ_DAY
        which = 'daily'

    fn = os.path.join(settings.DATA_DIR, '%s_%s.xml' % (datetime.datetime.utcnow().strftime('%Y-%m-%d'), which))
    if os.path.exists(fn):
        return open(fn, 'rb').read()
    
    resp = requests.get(url)
    resp.raise_for_status()

    f = open(fn, 'wb')
    f.write(resp.content)
    f.close()
    return resp.content

def parse(xmldata, full=False):
    import lxml.etree

    ns_doc = lxml.etree.fromstring(xmldata)
    doc = no_ns(ns_doc)
    tecajnice = doc.xpath('//tecajnica')
    
    if full:
        assert len(tecajnice) > 1, u'premalo tecajnic v dumpu'
    else:
        assert len(tecajnice) == 1, u'Vec tecajnic v dnevnem dumpu?'

    
    records = []
    for t in tecajnice:
        datum = datetime.datetime.strptime(t.attrib['datum'], '%Y-%m-%d')

        for tecaj in t.xpath('.//tecaj'):
            info = {
                'oznaka': tecaj.attrib['oznaka'],
                'sifra': tecaj.attrib['sifra'],
                'tecaj': tecaj.text,
                'datum': datum,
            }
            records.append(info)
    return records

def load(records):
    with transaction.atomic():
        for info in records:
            tecaj_obj = Tecaj(**info)
            tecaj_obj.save()

def no_ns(dom):
    # http://wiki.tei-c.org/index.php/Remove-Namespaces.xsl
    xslt='''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="no"/>

    <xsl:template match="/|comment()|processing-instruction()">
        <xsl:copy>
        <xsl:apply-templates/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="*">
        <xsl:element name="{local-name()}">
        <xsl:apply-templates select="@*|node()"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="@*">
        <xsl:attribute name="{local-name()}">
        <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>
    </xsl:stylesheet>
    '''
    from lxml import etree

    xslt_doc = etree.parse(io.BytesIO(xslt))
    transform = etree.XSLT(xslt_doc)
    dom = transform(dom)
    return dom
