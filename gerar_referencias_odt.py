#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para gerar arquivo ODT com referências bibliográficas formatadas em ABNT
"""

try:
    from odf.opendocument import OpenDocumentText
    from odf.text import P, H
    from odf.style import Style, TextProperties, ParagraphProperties
    ODF_AVAILABLE = True
except ImportError:
    ODF_AVAILABLE = False
    print("Biblioteca odfpy não disponível. Criando arquivo ODT manualmente...")

def criar_odt_manual():
    """Cria arquivo ODT manualmente usando estrutura XML"""
    import zipfile
    import xml.etree.ElementTree as ET
    from datetime import datetime
    
    # Conteúdo do arquivo content.xml
    content_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" 
                         xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" 
                         xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" 
                         xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" 
                         xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" 
                         xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" 
                         xmlns:xlink="http://www.w3.org/1999/xlink" 
                         xmlns:dc="http://purl.org/dc/elements/1.1/" 
                         xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" 
                         xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" 
                         xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" 
                         xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" 
                         xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" 
                         xmlns:math="http://www.w3.org/1998/Math/MathML" 
                         xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" 
                         xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" 
                         xmlns:ooo="http://openoffice.org/2004/office" 
                         xmlns:ooow="http://openoffice.org/2004/writer" 
                         xmlns:oooc="http://openoffice.org/2004/calc" 
                         xmlns:dom="http://www.w3.org/2001/xml-events" 
                         xmlns:xforms="http://www.w3.org/2002/xforms" 
                         xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                         office:version="1.2">
  <office:scripts/>
  <office:font-face-decls>
    <style:font-face style:name="Times New Roman" svg:font-family="'Times New Roman'" style:font-family-generic="roman" style:font-pitch="variable"/>
    <style:font-face style:name="Arial" svg:font-family="Arial" style:font-family-generic="swiss" style:font-pitch="variable"/>
  </office:font-face-decls>
  <office:automatic-styles>
    <style:style style:name="P1" style:family="paragraph" style:parent-style-name="Standard">
      <style:paragraph-properties fo:text-align="center" style:justify-single-word="false"/>
      <style:text-properties fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold" fo:font-size="14pt" style:font-size-asian="14pt" style:font-size-complex="14pt"/>
    </style:style>
    <style:style style:name="P2" style:family="paragraph" style:parent-style-name="Standard">
      <style:paragraph-properties fo:text-align="justify" style:justify-single-word="false" fo:margin-left="0cm" fo:margin-right="0cm" fo:text-indent="1.25cm" style:auto-text-indent="false"/>
      <style:text-properties fo:font-size="12pt" style:font-size-asian="12pt" style:font-size-complex="12pt"/>
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:text>
      <text:sequence-decls>
        <text:sequence-decl text:display-outline-level="0" text:name="Illustration"/>
        <text:sequence-decl text:display-outline-level="0" text:name="Table"/>
        <text:sequence-decl text:display-outline-level="0" text:name="Text"/>
        <text:sequence-decl text:display-outline-level="0" text:name="Drawing"/>
      </text:sequence-decls>
      <text:p text:style-name="P1">REFERÊNCIAS</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">AGÊNCIA NACIONAL DE ENERGIA ELÉTRICA. Dados abertos. Disponível em: https://dadosabertos.aneel.gov.br/. Acesso em: 30 out. 2024.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">CAMARA DE COMERCIALIZAÇÃO DE ENERGIA ELÉTRICA. Dados abertos. Disponível em: https://dadosabertos.ccee.org.br/. Acesso em: 30 out. 2024.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">CHEN, Tianqi; GUESTRIN, Carlos. XGBoost: a scalable tree boosting system. In: PROCEEDINGS OF THE 22ND ACM SIGKDD INTERNATIONAL CONFERENCE ON KNOWLEDGE DISCOVERY AND DATA MINING, 22., 2016, San Francisco. Anais [...]. New York: ACM, 2016. p. 785-794.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">FACEBOOK. Prophet: forecasting at scale. Disponível em: https://facebook.github.io/prophet/. Acesso em: 30 out. 2024.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">INSTITUTO NACIONAL DE METEOROLOGIA. Portal INMET. Disponível em: https://portal.inmet.gov.br/. Acesso em: 30 out. 2024.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">JOINT RESEARCH CENTRE. Photovoltaic Geographical Information System (PVGIS). Disponível em: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/. Acesso em: 30 out. 2024.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">MCKINNEY, Wes. Data structures for statistical computing in Python. In: PROCEEDINGS OF THE 9TH PYTHON IN SCIENCE CONFERENCE, 9., 2010, Austin. Anais [...]. Austin: SciPy, 2010. p. 56-61.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">OPERADOR NACIONAL DO SISTEMA ELÉTRICO. Dados abertos. Disponível em: https://dados.ons.org.br/. Acesso em: 30 out. 2024.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">PEDREGOSA, Fabian et al. Scikit-learn: machine learning in Python. Journal of Machine Learning Research, Cambridge, v. 12, p. 2825-2830, 2011.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">TAYLOR, Sean J.; LETHAM, Benjamin. Forecasting at scale. The American Statistician, Alexandria, v. 72, n. 1, p. 37-45, 2018.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">VAN DER WALT, Stefan; COLBERT, S. Chris; VAROQUAUX, Gaël. The NumPy array: a structure for efficient numerical computation. Computing in Science &amp; Engineering, Piscataway, v. 13, n. 2, p. 22-30, 2011.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">WASKOM, Michael L. seaborn: statistical data visualization. Journal of Open Source Software, [s.l.], v. 6, n. 60, p. 3021, 2021.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">HUNTER, John D. Matplotlib: a 2D graphics environment. Computing in Science &amp; Engineering, Piscataway, v. 9, n. 3, p. 90-95, 2007.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">REBACK, Jeff et al. pandas-dev/pandas: Pandas 1.3.0. Zenodo, [s.l.], 2021. Disponível em: https://doi.org/10.5281/zenodo.3509134. Acesso em: 30 out. 2024.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">VAN ROSSUM, Guido; DRAKE, Fred L. Python 3 reference manual. Scotts Valley: CreateSpace, 2009.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">OLIPHANT, Travis E. A guide to NumPy. USA: Trelgol Publishing, 2006. v. 1.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">BRASIL. Lei n. 14.300, de 6 de janeiro de 2022. Estabelece o marco legal da microgeração e minigeração distribuída. Diário Oficial da União, Brasília, DF, 7 jan. 2022. Seção 1, p. 1.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">ANEEL. Resolução Normativa n. 482, de 17 de abril de 2012. Estabelece as condições gerais para o acesso de microgeração e minigeração distribuída aos sistemas de distribuição de energia elétrica. Diário Oficial da União, Brasília, DF, 18 abr. 2012. Seção 1, p. 1.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">CCEE. Preço de Liquidação das Diferenças (PLD). Disponível em: https://www.ccee.org.br/web/guest/preco-de-liquidacao-das-diferencas. Acesso em: 30 out. 2024.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">HASTIE, Trevor; TIBSHIRANI, Robert; FRIEDMAN, Jerome. The elements of statistical learning: data mining, inference, and prediction. 2. ed. New York: Springer, 2009.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">JAMES, Gareth et al. An introduction to statistical learning: with applications in R. New York: Springer, 2013.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">BOX, George E. P.; JENKINS, Gwilym M.; REINSEL, Gregory C. Time series analysis: forecasting and control. 4. ed. Hoboken: John Wiley &amp; Sons, 2008.</text:p>
      <text:p text:style-name="P2"/>
      <text:p text:style-name="P2">HYNDMAN, Rob J.; ATHANASOPOULOS, George. Forecasting: principles and practice. 3. ed. Melbourne: OTexts, 2021. Disponível em: https://otexts.com/fpp3/. Acesso em: 30 out. 2024.</text:p>
    </office:text>
  </office:body>
</office:document-content>'''
    
    # Meta.xml
    meta_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" 
                      xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" 
                      xmlns:dc="http://purl.org/dc/elements/1.1/" 
                      xmlns:xlink="http://www.w3.org/1999/xlink" 
                      office:version="1.2">
  <office:meta>
    <meta:generator>Python ODT Generator</meta:generator>
    <dc:title>Referências Bibliográficas - TCC</dc:title>
    <dc:description>Referências bibliográficas formatadas em ABNT</dc:description>
    <meta:creation-date>{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}</meta:creation-date>
  </office:meta>
</office:document-meta>'''
    
    # Mime type
    mime_type = 'application/vnd.oasis.opendocument.text'
    
    # styles.xml básico
    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" 
                        xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" 
                        xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" 
                        xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" 
                        xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" 
                        xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" 
                        xmlns:xlink="http://www.w3.org/1999/xlink" 
                        xmlns:dc="http://purl.org/dc/elements/1.1/" 
                        xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" 
                        xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" 
                        xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" 
                        xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" 
                        xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" 
                        xmlns:math="http://www.w3.org/1998/Math/MathML" 
                        xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" 
                        xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" 
                        xmlns:ooo="http://openoffice.org/2004/office" 
                        xmlns:ooow="http://openoffice.org/2004/writer" 
                        xmlns:oooc="http://openoffice.org/2004/calc" 
                        xmlns:dom="http://www.w3.org/2001/xml-events" 
                        xmlns:xforms="http://www.w3.org/2002/xforms" 
                        xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                        office:version="1.2">
  <office:font-face-decls>
    <style:font-face style:name="Times New Roman" svg:font-family="'Times New Roman'" style:font-family-generic="roman" style:font-pitch="variable"/>
    <style:font-face style:name="Arial" svg:font-family="Arial" style:font-family-generic="swiss" style:font-pitch="variable"/>
  </office:font-face-decls>
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties fo:hyphenation-ladder-count="no-limit" style:text-autospace="ideograph-alpha" style:punctuation-wrap="hanging" style:line-break="strict" style:tab-stop-distance="1.25cm" style:writing-mode="page"/>
      <style:text-properties style:font-name="Times New Roman" fo:font-size="12pt" fo:language="pt" fo:country="BR" style:font-name-asian="Times New Roman" style:font-size-asian="12pt" style:language-asian="pt" style:country-asian="BR" style:font-name-complex="Times New Roman" style:font-size-complex="12pt" style:language-complex="pt" style:country-complex="BR"/>
    </style:default-style>
    <style:style style:name="Standard" style:family="paragraph" style:class="text"/>
  </office:styles>
</office:document-styles>'''
    
    # Criar arquivo ODT (é um ZIP)
    with zipfile.ZipFile('REFERENCIAS_ABNT.odt', 'w', zipfile.ZIP_DEFLATED) as odt:
        odt.writestr('mimetype', mime_type, compress_type=zipfile.ZIP_STORED)
        odt.writestr('content.xml', content_xml.encode('utf-8'))
        odt.writestr('meta.xml', meta_xml.encode('utf-8'))
        odt.writestr('styles.xml', styles_xml.encode('utf-8'))
        odt.writestr('META-INF/manifest.xml', '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
  <manifest:file-entry manifest:full-path="/" manifest:version="1.2" manifest:media-type="application/vnd.oasis.opendocument.text"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
</manifest:manifest>'''.encode('utf-8'))
    
    print("Arquivo REFERENCIAS_ABNT.odt criado com sucesso!")

if __name__ == "__main__":
    if ODF_AVAILABLE:
        # Usar odfpy se disponível
        doc = OpenDocumentText()
        
        # Título
        h = H(outlinelevel=1, stylename="Heading 1")
        h.addText("REFERÊNCIAS")
        doc.text.addElement(h)
        
        # Referências
        referencias = [
            "AGÊNCIA NACIONAL DE ENERGIA ELÉTRICA. Dados abertos. Disponível em: https://dadosabertos.aneel.gov.br/. Acesso em: 30 out. 2024.",
            "CAMARA DE COMERCIALIZAÇÃO DE ENERGIA ELÉTRICA. Dados abertos. Disponível em: https://dadosabertos.ccee.org.br/. Acesso em: 30 out. 2024.",
            "CHEN, Tianqi; GUESTRIN, Carlos. XGBoost: a scalable tree boosting system. In: PROCEEDINGS OF THE 22ND ACM SIGKDD INTERNATIONAL CONFERENCE ON KNOWLEDGE DISCOVERY AND DATA MINING, 22., 2016, San Francisco. Anais [...]. New York: ACM, 2016. p. 785-794.",
            "FACEBOOK. Prophet: forecasting at scale. Disponível em: https://facebook.github.io/prophet/. Acesso em: 30 out. 2024.",
            "INSTITUTO NACIONAL DE METEOROLOGIA. Portal INMET. Disponível em: https://portal.inmet.gov.br/. Acesso em: 30 out. 2024.",
            "JOINT RESEARCH CENTRE. Photovoltaic Geographical Information System (PVGIS). Disponível em: https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/. Acesso em: 30 out. 2024.",
            "MCKINNEY, Wes. Data structures for statistical computing in Python. In: PROCEEDINGS OF THE 9TH PYTHON IN SCIENCE CONFERENCE, 9., 2010, Austin. Anais [...]. Austin: SciPy, 2010. p. 56-61.",
            "OPERADOR NACIONAL DO SISTEMA ELÉTRICO. Dados abertos. Disponível em: https://dados.ons.org.br/. Acesso em: 30 out. 2024.",
            "PEDREGOSA, Fabian et al. Scikit-learn: machine learning in Python. Journal of Machine Learning Research, Cambridge, v. 12, p. 2825-2830, 2011.",
            "TAYLOR, Sean J.; LETHAM, Benjamin. Forecasting at scale. The American Statistician, Alexandria, v. 72, n. 1, p. 37-45, 2018.",
            "VAN DER WALT, Stefan; COLBERT, S. Chris; VAROQUAUX, Gaël. The NumPy array: a structure for efficient numerical computation. Computing in Science & Engineering, Piscataway, v. 13, n. 2, p. 22-30, 2011.",
            "WASKOM, Michael L. seaborn: statistical data visualization. Journal of Open Source Software, [s.l.], v. 6, n. 60, p. 3021, 2021.",
            "HUNTER, John D. Matplotlib: a 2D graphics environment. Computing in Science & Engineering, Piscataway, v. 9, n. 3, p. 90-95, 2007.",
            "REBACK, Jeff et al. pandas-dev/pandas: Pandas 1.3.0. Zenodo, [s.l.], 2021. Disponível em: https://doi.org/10.5281/zenodo.3509134. Acesso em: 30 out. 2024.",
            "VAN ROSSUM, Guido; DRAKE, Fred L. Python 3 reference manual. Scotts Valley: CreateSpace, 2009.",
            "OLIPHANT, Travis E. A guide to NumPy. USA: Trelgol Publishing, 2006. v. 1.",
            "BRASIL. Lei n. 14.300, de 6 de janeiro de 2022. Estabelece o marco legal da microgeração e minigeração distribuída. Diário Oficial da União, Brasília, DF, 7 jan. 2022. Seção 1, p. 1.",
            "ANEEL. Resolução Normativa n. 482, de 17 de abril de 2012. Estabelece as condições gerais para o acesso de microgeração e minigeração distribuída aos sistemas de distribuição de energia elétrica. Diário Oficial da União, Brasília, DF, 18 abr. 2012. Seção 1, p. 1.",
            "CCEE. Preço de Liquidação das Diferenças (PLD). Disponível em: https://www.ccee.org.br/web/guest/preco-de-liquidacao-das-diferencas. Acesso em: 30 out. 2024.",
            "HASTIE, Trevor; TIBSHIRANI, Robert; FRIEDMAN, Jerome. The elements of statistical learning: data mining, inference, and prediction. 2. ed. New York: Springer, 2009.",
            "JAMES, Gareth et al. An introduction to statistical learning: with applications in R. New York: Springer, 2013.",
            "BOX, George E. P.; JENKINS, Gwilym M.; REINSEL, Gregory C. Time series analysis: forecasting and control. 4. ed. Hoboken: John Wiley & Sons, 2008.",
            "HYNDMAN, Rob J.; ATHANASOPOULOS, George. Forecasting: principles and practice. 3. ed. Melbourne: OTexts, 2021. Disponível em: https://otexts.com/fpp3/. Acesso em: 30 out. 2024."
        ]
        
        for ref in referencias:
            p = P()
            p.addText(ref)
            doc.text.addElement(p)
            # Espaço entre referências
            p_space = P()
            doc.text.addElement(p_space)
        
        doc.save("REFERENCIAS_ABNT.odt")
        print("Arquivo REFERENCIAS_ABNT.odt criado com sucesso usando odfpy!")
    else:
        criar_odt_manual()

