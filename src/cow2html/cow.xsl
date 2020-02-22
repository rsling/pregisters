<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:template match="doc/token" />
  
  <xsl:template match="doc">
    <div id="outer">
      <div class='header'>
        <h1>COW document<br />ID <xsl:value-of select="@id"/></h1>
        <h2><a href="{@url}" target="_blank" class="faint"><xsl:value-of select="@url"/></a></h2>
        <h2><a href="index.html" class="faint">Back to pregister...</a></h2>
      </div>
      <xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="div">
    <div id="div{@idx}" class="paragraph bpc-{@bpc}">
      <span class="div-idx"><xsl:value-of select="@idx"/></span><xsl:apply-templates />
    </div>
  </xsl:template>

  <xsl:template match="dup">
    <div id="div{@idx}" class="paragraph dup">
      <span class="div-idx"><xsl:value-of select="@idx"/> is a duplicate of <xsl:value-of select="@of"/></span>
    </div>
  </xsl:template>

  <xsl:template match="title" />

  <xsl:template match="annotations" />

  <xsl:template match="word">
    <span class="word">
      <xsl:apply-templates />
    </span>
  </xsl:template>

  <xsl:template match="s">
    <span class="sentence">
      <xsl:apply-templates />
    </span>
  </xsl:template>

  <xsl:template match="dm|psimpx|rsimpx|simpx|adjx|advx|dp|fx|nx|px|vxfin|vxinf|lv|c|fkoord|koord|lk|mf|mfe|nf|parord|vc|vce|vf|fkonj">
    <span class="{name()}">
      <xsl:apply-templates />
    </span>
  </xsl:template>


  <xsl:template match="/">
    <html>
      <head>
      </head>
      <body>
        <xsl:apply-templates />
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
