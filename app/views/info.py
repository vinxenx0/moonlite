# Herramientas disponibles en la app
## hay que poner orden con el tools=[] de __init__.py
tools = [
    # Domains & Email
    {"name": "WHOIS", "description": "Check domain ownership details.", "link": "/tools/domains/whois", "icon": "fas fa-info-circle", "category": "Domains & Email", "subcategory": "Domain Information", "most_used": False, "is_new": False},
    {"name": "Reverse Domain", "description": "Explore reverse domain lookups.", "link": "/tools/domains/reverse", "icon": "fas fa-globe", "category": "Domains & Email", "subcategory": "Domain Information", "most_used": False, "is_new": False},
    {"name": "CNAME Lookup", "description": "Check CNAME records.", "link": "/tools/domains/cname", "icon": "fas fa-cog", "category": "Domains & Email", "subcategory": "Domain Information", "most_used": False, "is_new": False},
    {"name": "IP Lookup", "description": "Find the IP address associated with a domain.", "link": "/tools/domains/ip", "icon": "fas fa-search", "category": "Domains & Email", "subcategory": "Domain Information", "most_used": True, "is_new": False},
    {"name": "AAAA Lookup", "description": "Retrieve IPv6 records for a domain.", "link": "/tools/domains/aaaa", "icon": "fas fa-link", "category": "Domains & Email", "subcategory": "Domain Information", "most_used": True, "is_new": False},
    {"name": "Traceroute", "description": "Trace the route packets take to a domain.", "link": "/tools/domains/traceroute", "icon": "fas fa-route", "category": "Domains & Email", "subcategory": "Domain Information", "most_used": True, "is_new": True},
    {"name": "Nmap", "description": "Perform a network map scan.", "link": "/tools/domains/nmap", "icon": "fas fa-network-wired", "category": "Domains & Email", "subcategory": "Domain Information", "most_used": True, "is_new": True},
    {"name": "Blacklist Check", "description": "Check if your domain is blacklisted.", "link": "/tools/domains/blacklist", "icon": "fas fa-ban", "category": "Domains & Email", "subcategory": "Domain Information", "most_used": True, "is_new": True},

    # Mail Server
    {"name": "MX Discover", "description": "Identify mail exchange servers for a domain.", "link": "/tools/domains/mx", "icon": "fas fa-server", "category": "Domains & Email", "subcategory": "Mail Server", "most_used": True, "is_new": False},
    {"name": "DMARC Lookup", "description": "Check DMARC records for a domain.", "link": "/tools/domains/dmarc", "icon": "fas fa-envelope-open", "category": "Domains & Email", "subcategory": "Mail Server", "most_used": True, "is_new": True},
    {"name": "SPF Lookup", "description": "Check SPF records to prevent email spoofing.", "link": "/tools/domains/spf", "icon": "fas fa-shield-alt", "category": "Domains & Email", "subcategory": "Mail Server", "most_used": True, "is_new": False},
    {"name": "DKIM Lookup", "description": "Verify DKIM signatures for email authentication.", "link": "/tools/domains/dkim", "icon": "fas fa-signature", "category": "Domains & Email", "subcategory": "Mail Server", "most_used": True, "is_new": False},
    {"name": "TXT Lookup", "description": "Retrieve TXT records for a domain.", "link": "/tools/domains/txt", "icon": "fas fa-file-alt", "category": "Domains & Email", "subcategory": "Mail Server", "most_used": True, "is_new": False},
    {"name": "DNS Key Lookup", "description": "Check DNSSEC key records.", "link": "/tools/domains/dnskey", "icon": "fas fa-key", "category": "Domains & Email", "subcategory": "Mail Server", "most_used": True, "is_new": True},
    {"name": "LOC Entry", "description": "Retrieve LOC records for a domain.", "link": "/tools/domains/loc", "icon": "fas fa-map-marker-alt", "category": "Domains & Email", "subcategory": "Mail Server", "most_used": False, "is_new": False},
    {"name": "IP Sec Key", "description": "Analyze IPSEC Key records.", "link": "/tools/domains/ipseckey", "icon": "fas fa-shield-alt", "category": "Domains & Email", "subcategory": "Mail Server", "most_used": False, "is_new": False},

    # DNS Lookup
    {"name": "SOA Lookup", "description": "Check SOA DNS records.", "link": "/tools/domains/soa", "icon": "fas fa-info", "category": "Domains & Email", "subcategory": "DNS Lookup", "most_used": True, "is_new": False},
    {"name": "ASN Lookup", "description": "Perform an ASN record lookup.", "link": "/tools/domains/asn", "icon": "fas fa-sitemap", "category": "Domains & Email", "subcategory": "DNS Lookup", "most_used": False, "is_new": False},
    {"name": "ARIN Lookup", "description": "Retrieve ARIN information for a domain.", "link": "/tools/domains/arin", "icon": "fas fa-database", "category": "Domains & Email", "subcategory": "DNS Lookup", "most_used": False, "is_new": True},
    {"name": "RRSIG Lookup", "description": "Retrieve RRSIG DNS records.", "link": "/tools/domains/rrsig", "icon": "fas fa-lock", "category": "Domains & Email", "subcategory": "DNS Lookup", "most_used": False, "is_new": False},
    {"name": "NSEC Lookup", "description": "Perform NSEC DNS lookups.", "link": "/tools/domains/nsec", "icon": "fas fa-lock", "category": "Domains & Email", "subcategory": "DNS Lookup", "most_used": False, "is_new": False},
    {"name": "MTA STS", "description": "Check MTA STS compliance.", "link": "/tools/domains/mtasts", "icon": "fas fa-envelope", "category": "Domains & Email", "subcategory": "DNS Lookup", "most_used": False, "is_new": True},
    {"name": "NSEC3PARAM", "description": "Check NSEC3PARAM DNS records.", "link": "/tools/domains/nsec3param", "icon": "fas fa-key", "category": "Domains & Email", "subcategory": "DNS Lookup", "most_used": False, "is_new": False},
    {"name": "SRV Lookup", "description": "Perform SRV record lookup.", "link": "/tools/domains/srv", "icon": "fas fa-network-wired", "category": "Domains & Email", "subcategory": "DNS Lookup", "most_used": True, "is_new": False},

    # Accessibility 
    {"name": "WCAG-AA/AAA", "description": "Evaluate website accessibility compliance.", "link": "/tools/accesibility/wcag", "icon": "fas fa-universal-access", "category": "Accessibility & Usability", "subcategory": "Accessibility", "most_used": True, "is_new": False},
    {"name": "Spelling Check", "description": "Detect spelling issues on your site.", "link": "/tools/accesibility/ortografia", "icon": "fas fa-spell-check", "category": "Accessibility & Usability", "subcategory": "Accessibility", "most_used": True, "is_new": False},
    {"name": "Velocidad", "description": "Analyze website performance metrics.", "link": "/tools/accesibility/core-web-vitals", "icon": "fas fa-vials", "category": "Accessibility & Usability", "subcategory": "Accessibility", "most_used": True, "is_new": True},
    {"name": "Core Web Vitals", "description": "Analyze website performance metrics.", "link": "/tools/accesibility/core-web-vitals", "icon": "fas fa-vials", "category": "Accessibility & Usability", "subcategory": "Accessibility", "most_used": True, "is_new": False},
    {"name": "Responsive Design", "description": "Check website responsiveness.", "link": "/tools/accesibility/responsive", "icon": "fas fa-mobile-alt", "category": "Accessibility & Usability", "subcategory": "Accessibility", "most_used": True, "is_new": False},
    # Img optimization
    {"name": "Images", "description": "Validate AMP page compliance.", "link": "/tools/accesibility/amp", "icon": "fas fa-mobile-alt", "category": "Accessibility & Usability", "subcategory": "Image Optimization", "most_used": False, "is_new": False},
    {"name": "Lazy Loading", "description": "Optimize image loading for speed.", "link": "/tools/accesibility/lazy-loading", "icon": "fas fa-clock", "category": "Accessibility & Usability", "subcategory": "Image Optimization", "most_used": True, "is_new": False},
    # Mobile optimization
    {"name": "AMP Valid Page", "description": "Validate AMP page compliance.", "link": "/tools/accesibility/amp", "icon": "fas fa-mobile-alt", "category": "Accessibility & Usability", "subcategory": "Mobile Optimization", "most_used": False, "is_new": False},
    {"name": "Mobile Audit", "description": "Perform a mobile optimization audit.", "link": "/tools/accesibility/mobile-audit", "icon": "fas fa-mobile-alt", "category": "Accessibility & Usability", "subcategory": "Mobile Optimization", "most_used": False, "is_new": True},
    # Usability
    {"name": "Favicon Missing", "description": "Validate AMP page compliance.", "link": "/tools/accesibility/amp", "icon": "fas fa-mobile-alt", "category": "Accessibility & Usability", "subcategory": "Usability", "most_used": False, "is_new": False},
    {"name": "Flash Used", "description": "Perform a mobile optimization audit.", "link": "/tools/accesibility/mobile-audit", "icon": "fas fa-mobile-alt", "category": "Accessibility & Usability", "subcategory": "Usability", "most_used": False, "is_new": False},
    {"name": "X Card Tag Missing", "description": "Validate AMP page compliance.", "link": "/tools/accesibility/amp", "icon": "fas fa-mobile-alt", "category": "Accessibility & Usability", "subcategory": "Usability", "most_used": False, "is_new": False},
    {"name": "Google Search Display", "description": "Perform a mobile optimization audit.", "link": "/tools/accesibility/mobile-audit", "icon": "fas fa-mobile-alt", "category": "Accessibility & Usability", "subcategory": "Usability", "most_used": False, "is_new": True},
    {"name": "Content Optimization", "description": "Validate AMP page compliance.", "link": "/tools/accesibility/amp", "icon": "fas fa-mobile-alt", "category": "Accessibility & Usability", "subcategory": "Usability", "most_used": False, "is_new": False},
    {"name": "Redirection Manager", "description": "Perform a mobile optimization audit.", "link": "/tools/accesibility/mobile-audit", "icon": "fas fa-mobile-alt", "category": "Accessibility & Usability", "subcategory": "Usability", "most_used": False, "is_new": True},
    
    # SEO Tools
    {"name": "Titles (H1)", "description": "Analyze title tags for SEO improvements.", "link": "/tools/seo/titles", "icon": "fas fa-heading", "category": "SEO", "subcategory": "On-Page SEO", "most_used": True, "is_new": False},
    {"name": "Meta Descriptions", "description": "Optimize meta descriptions for search engines.", "link": "/tools/seo/meta-description", "icon": "fas fa-clipboard", "category": "SEO", "subcategory": "On-Page SEO", "most_used": True, "is_new": False},
    {"name": "Meta Keywords", "description": "Ensure canonicalization to prevent duplicates.", "link": "/tools/seo/canonicals", "icon": "fas fa-link", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": False},
    {"name": "Encabezados (Headings)", "description": "Analyze title tags for SEO improvements.", "link": "/tools/seo/titles", "icon": "fas fa-heading", "category": "SEO", "subcategory": "On-Page SEO", "most_used": True, "is_new": False},
    {"name": "Imágenes (IMG)", "description": "Ensure canonicalization to prevent duplicates.", "link": "/tools/seo/canonicals", "icon": "fas fa-link", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": True},
    {"name": "Canonical Tags", "description": "Ensure canonicalization to prevent duplicates.", "link": "/tools/seo/canonicals", "icon": "fas fa-link", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": False},
    {"name": "Directives", "description": "Analyze title tags for SEO improvements.", "link": "/tools/seo/titles", "icon": "fas fa-heading", "category": "SEO", "subcategory": "On-Page SEO", "most_used": True, "is_new": False},
    {"name": "Schema.org", "description": "Optimize meta descriptions for search engines.", "link": "/tools/seo/meta-description", "icon": "fas fa-clipboard", "category": "SEO", "subcategory": "On-Page SEO", "most_used": True, "is_new": False},
    {"name": "OpenGraph", "description": "Ensure canonicalization to prevent duplicates.", "link": "/tools/seo/canonicals", "icon": "fas fa-link", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": True},
    {"name": "Hreflang", "description": "Analyze title tags for SEO improvements.", "link": "/tools/seo/titles", "icon": "fas fa-heading", "category": "SEO", "subcategory": "On-Page SEO", "most_used": True, "is_new": False},
    {"name": "URLs", "description": "Optimize meta descriptions for search engines.", "link": "/tools/seo/meta-description", "icon": "fas fa-clipboard", "category": "SEO", "subcategory": "On-Page SEO", "most_used": True, "is_new": False},
    {"name": "Duplicate Content", "description": "Ensure canonicalization to prevent duplicates.", "link": "/tools/seo/canonicals", "icon": "fas fa-link", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": False},
 
    
    {"name": "Robots.txt", "description": "Analyze robots.txt for crawling directives.", "link": "/tools/seo/robots", "icon": "fas fa-robot", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": False},
    {"name": "Sitemap", "description": "Check the XML sitemap for search engines.", "link": "/tools/seo/sitemap", "icon": "fas fa-sitemap", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": False},
    {"name": "Broken Links", "description": "Identify and fix broken links on your website.", "link": "/tools/seo/broken-links", "icon": "fas fa-unlink", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": True},
    {"name": "Backlinks", "description": "Analyze backlinks to your website.", "link": "/tools/seo/backlinks", "icon": "fas fa-link", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": False},
    {"name": "Outlinks", "description": "Analyze backlinks to your website.", "link": "/tools/seo/backlinks", "icon": "fas fa-link", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": False},
    {"name": "External links", "description": "Analyze backlinks to your website.", "link": "/tools/seo/backlinks", "icon": "fas fa-link", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": False},
    {"name": "Internal Links", "description": "Evaluate internal linking structure.", "link": "/tools/seo/internal-links", "icon": "fas fa-link", "category": "SEO", "subcategory": "Crawling & Linking", "most_used": True, "is_new": False},

    {"name": "CSS Issues", "description": "Identify CSS problems affecting performance.", "link": "/tools/seo/css-issues", "icon": "fas fa-code", "category": "SEO", "subcategory": "HTML/CSS Compliance", "most_used": False, "is_new": False},
    {"name": "Deprecated HTML Tags", "description": "Find deprecated HTML tags.", "link": "/tools/seo/deprecated-html", "icon": "fas fa-exclamation-triangle", "category": "SEO", "subcategory": "HTML/CSS Compliance", "most_used": False, "is_new": False},
    {"name": "Gzip Compression", "description": "Check if Gzip compression is enabled.", "link": "/tools/seo/gzip", "icon": "fas fa-compress", "category": "SEO", "subcategory": "HTML/CSS Compliance", "most_used": False, "is_new": True},

    # Website Security
    {"name": "X-Tags", "description": "Verify security tags like X-Frame-Options.", "link": "/tools/security/x-tags", "icon": "fas fa-tags", "category": "Website Security", "subcategory": "Website Security", "most_used": False, "is_new": False},
    {"name": "Header Info", "description": "Analyze response headers for security.", "link": "/tools/security/header-info", "icon": "fas fa-info-circle", "category": "Website Security", "subcategory": "Website Security", "most_used": False, "is_new": False},
    {"name": "HTTPS/SSL", "description": "Verify HTTPS and SSL certificate compliance.", "link": "/tools/security/ssl", "icon": "fas fa-lock", "category": "Website Security", "subcategory": "Website Security", "most_used": True, "is_new": False},
    {"name": "Server Response", "description": "Analyze server response headers.", "link": "/tools/security/server-response", "icon": "fas fa-server", "category": "Website Security", "subcategory": "Website Security", "most_used": True, "is_new": False},
    {"name": "Security Info", "description": "Review website security configurations.", "link": "/tools/security/info", "icon": "fas fa-shield-alt", "category": "Website Security", "subcategory": "Website Security", "most_used": False, "is_new": True},
    {"name": "Canonical HTTPS to HTTP", "description": "Check if HTTP is redirected to HTTPS.", "link": "/tools/security/canonical-http", "icon": "fas fa-exchange-alt", "category": "Website Security", "subcategory": "Website Security", "most_used": False, "is_new": False},
    {"name": "HTTP to HTTPS Redirect", "description": "Ensure proper redirection from HTTP to HTTPS.", "link": "/tools/security/redirect-http-https", "icon": "fas fa-exchange-alt", "category": "Website Security", "subcategory": "Website Security", "most_used": False, "is_new": False},

    # Localization
    {"name": "Invalid hreflang Attribute", "description": "Detect invalid hreflang attributes.", "link": "/tools/localization/invalid-hreflang", "icon": "fas fa-code", "category": "SEO", "subcategory": "Localization", "most_used": False, "is_new": False},
    {"name": "Multiple Language Codes", "description": "Check for multiple language codes in hreflang.", "link": "/tools/localization/multiple-language-codes", "icon": "fas fa-language", "category": "SEO", "subcategory": "Localization", "most_used": False, "is_new": False},
    {"name": "Invalid HTML lang Attribute", "description": "Identify invalid lang attributes in HTML.", "link": "/tools/localization/invalid-html-lang", "icon": "fas fa-code", "category": "SEO", "subcategory": "Localization", "most_used": False, "is_new": False},
    {"name": "Language Duplicate", "description": "Detect duplicate language attributes.", "link": "/tools/localization/language-duplicate", "icon": "fas fa-clone", "category": "SEO", "subcategory": "Localization", "most_used": False, "is_new": False},
    {"name": "HTML Lang Missing", "description": "Identify missing lang attributes in HTML.", "link": "/tools/localization/missing-html-lang", "icon": "fas fa-code", "category": "SEO", "subcategory": "Localization", "most_used": False, "is_new": False},
    {"name": "x-default Attribute Missing", "description": "Ensure x-default is included in hreflang.", "link": "/tools/localization/x-default-missing", "icon": "fas fa-exclamation-triangle", "category": "SEO", "subcategory": "Localization", "most_used": False, "is_new": False},
]


# Texto de la IA para el PRO
tool_info = {
    'nmap': {
        'definition': "Nmap es una herramienta de escaneo de redes que permite detectar hosts y servicios en una red. En SEO, se utiliza para auditar la seguridad del sitio web, identificando vulnerabilidades que podrían ser explotadas y afectar la confianza y ranking del sitio.",
        'slogan': "Explora y asegura tu red para un SEO sólido",
        'keywords': "network, scan, security",
        'info_popup': "Nmap, abreviatura de Network Mapper, es una herramienta de código abierto utilizada para el escaneo de redes y auditoría de seguridad. Permite descubrir dispositivos activos en una red, identificar los servicios que están ejecutando, y detectar posibles vulnerabilidades. En el ámbito del SEO, la seguridad del sitio web es fundamental, ya que las brechas de seguridad pueden llevar a penalizaciones de los motores de búsqueda y a la pérdida de confianza de los usuarios. Por ejemplo, Nmap puede identificar puertos abiertos y servicios vulnerables que podrían ser puntos de entrada para ataques, permitiendo a los administradores de sitios web tomar medidas correctivas para fortalecer la seguridad y, en consecuencia, mantener o mejorar su posicionamiento en los motores de búsqueda."
    ,"most_used": True, "is_new": False},
    'traceroute': {
        'definition': "Traceroute es una herramienta que rastrea la ruta y mide los retrasos de paquetes de datos desde un host a otro. En SEO, es vital para identificar cuellos de botella y problemas de latencia que pueden afectar la velocidad de un sitio web.",
        'slogan': "Trace the route of your packets.",
        'keywords': "Rastreando la ruta hacia un rendimiento óptimo",
        'info_popup': "Traceroute es una utilidad de diagnóstico de red que rastrea la ruta que siguen los paquetes de datos para llegar a un destino. Proporciona información sobre cada salto en la ruta, incluyendo tiempos de respuesta y posibles puntos de congestión. En el contexto de SEO, la velocidad de un sitio web es un factor crucial para la clasificación en los motores de búsqueda. Utilizando Traceroute, los profesionales de SEO pueden identificar y resolver problemas de latencia en la red que puedan estar ralentizando el tiempo de carga de un sitio web. Por ejemplo, si Traceroute muestra que hay un retraso significativo en uno de los saltos, se puede trabajar con los proveedores de servicios para optimizar esa ruta."
    ,"most_used": True, "is_new": False},
    'aaaa': {
        'definition': "AAAA Lookup se utiliza para resolver direcciones IPv6 de un dominio. Es relevante en SEO para asegurar que un sitio web esté accesible en la moderna infraestructura de internet, mejorando la cobertura y accesibilidad global.",
        'slogan': "Preparando tu sitio para la próxima generación de Internet",
        'keywords': "dns, ipv6, lookup",
        'info_popup': "El registro AAAA (Quad-A) en DNS se utiliza para mapear un nombre de dominio a una dirección IPv6, la versión más reciente del protocolo de Internet. AAAA Lookup permite obtener estas direcciones IPv6, lo cual es cada vez más importante debido al crecimiento del uso de dispositivos conectados y la expansión de la infraestructura de internet. En términos de SEO, asegurar que un sitio web esté accesible a través de IPv6 puede mejorar la accesibilidad y rendimiento del sitio, especialmente en regiones donde IPv6 es más prevalente. Además, tener soporte para IPv6 puede ser un factor diferenciador frente a la competencia, mostrando un compromiso con la modernización y la futura prueba de la infraestructura web."
    ,"most_used": True, "is_new": False},
    'ip': {
        'definition': "IP Lookup permite obtener información detallada sobre una dirección IP, incluyendo su ubicación geográfica y el ISP. En SEO, es esencial para analizar la distribución de tráfico y diagnosticar problemas de rendimiento de red.",
        'slogan': "Descubre todo sobre cualquier IP",
        'keywords': "ip, lookup, information",
        'info_popup': "IP Lookup es una herramienta que proporciona información detallada sobre una dirección IP específica, como su ubicación geográfica, el proveedor de servicios de Internet (ISP) y el nombre de host asociado. Esta información es útil en SEO para diversas tareas, como analizar la procedencia del tráfico web, identificar patrones sospechosos o fraudulentos, y diagnosticar problemas de red que puedan afectar la velocidad de carga de un sitio web. Por ejemplo, si una gran cantidad de tráfico proviene de una región inesperada, esto puede indicar la necesidad de ajustar la estrategia de marketing regional o investigar posibles ataques de spam."
    ,"most_used": True, "is_new": False},
    'cname': {
        'definition': "CNAME (Canonical Name) es un tipo de registro DNS que permite mapear un dominio a otro. En SEO, es crucial para gestionar dominios y subdominios, facilitando la redirección y la gestión de URLs canónicas.",
        'slogan': "Alias perfectos para una gestión de dominios impecable",
        'keywords': "dns, cname, lookup",
        'info_popup': "El registro CNAME se utiliza en el sistema de nombres de dominio (DNS) para alias de un dominio a otro, conocido como el dominio canónico. Esto es útil para redireccionar tráfico de una URL a otra sin alterar la URL visible en el navegador del usuario. Por ejemplo, puedes tener www.ejemplo.com apuntando a ejemplo.com. En términos de SEO, los CNAMEs son útiles para gestionar subdominios, redirecciones y evitar problemas de contenido duplicado. Además, facilitan la implementación de servicios externos como plataformas de marketing o análisis que requieren redirección de subdominios."
    ,"most_used": True, "is_new": False},
    'reverse': {
        'definition': "El Reverse Domain es una técnica que permite identificar todos los dominios asociados a una dirección IP específica. Es útil en SEO para descubrir redes de sitios web, entender la estructura de enlaces y evaluar posibles riesgos de spam.",
        'slogan': "Descubre el entramado de sitios web en una IP.",
        'keywords': "dns, reverse, lookup",
        'info_popup': "El Reverse Domain Lookup, o búsqueda inversa de dominio, permite obtener una lista de todos los dominios que comparten una misma dirección IP. Esta técnica es útil para analizar la red de sitios web de un competidor o cliente. Por ejemplo, si varios sitios comparten una misma IP, podrían estar vinculados de alguna manera, lo que puede afectar sus estrategias de SEO debido a la posible percepción de prácticas de black hat SEO. Además, esta herramienta puede ayudar a identificar si un servidor está sobrecargado con demasiados sitios, lo cual podría afectar el rendimiento y, por ende, la clasificación en los motores de búsqueda."
    ,"most_used": True, "is_new": False},
    'whois': {
        'definition': "WHOIS es una herramienta esencial en SEO para obtener información sobre el propietario de un dominio, la fecha de registro y otros datos cruciales. Esta información ayuda a los profesionales de marketing digital a analizar la legitimidad y antigüedad de un dominio, factores que influyen en la estrategia SEO.",
        'slogan': "Descubre quién está detrás del dominio",
        'keywords': "domain, whois, registration",
        'info_popup': "WHOIS es un protocolo que se utiliza para consultar bases de datos que almacenan la información de registro de nombres de dominio en internet. Esta herramienta revela detalles importantes como el registrante, la fecha de creación y vencimiento del dominio, y los servidores DNS asociados. Por ejemplo, conocer la antigüedad de un dominio puede indicar su autoridad y confiabilidad, factores importantes en la evaluación de un sitio web para SEO. Además, WHOIS permite identificar cambios recientes en la propiedad de un dominio, lo cual puede ser relevante para entender fluctuaciones en su rendimiento SEO."
    ,"most_used": True, "is_new": False},
    #
    'nsec3param': {
        'definition': "NSEC3PARAM es un registro DNS que define los parámetros para el hashing en NSEC3, mejorando la seguridad y privacidad en DNSSEC. Es crucial en SEO para proteger contra el zone walking y asegurar la integridad DNS.",
        'slogan': "Mejora la seguridad y privacidad de tu DNS",
        'keywords': "",
        'info_popup': "NSEC3PARAM es un tipo de registro DNS utilizado en DNSSEC que especifica los parámetros de configuración para NSEC3, una extensión de NSEC que utiliza hashing criptográfico para mejorar la seguridad. NSEC3 evita el 'zone walking', un proceso donde un atacante puede enumerar todos los nombres de dominio en una zona. Mediante el uso de NSEC3 y NSEC3PARAM, se asegura que los registros DNS solo muestren información limitada y cifrada, mejorando la privacidad y la seguridad. En términos de SEO, implementar NSEC3 con parámetros adecuados es vital para proteger la integridad de la zona DNS y mantener la confianza del usuario. Por ejemplo, proteger contra el zone walking previene la exposición de todos los subdominios, lo cual es crucial para la seguridad del sitio."
    ,"most_used": True, "is_new": False},
    'mtasts': {
        'definition': "MTA-STS (Mail Transfer Agent Strict Transport Security) es un protocolo que asegura la entrega de correos electrónicos utilizando conexiones cifradas. Es esencial en SEO para proteger la reputación del dominio y asegurar la entrega segura de emails.",
        'slogan': "Entrega de correos segura y cifrada, siempre",
        'keywords': "",
        'info_popup': "MTA-STS es un protocolo que permite a los administradores de correo electrónico forzar el uso de conexiones cifradas (TLS) al enviar correos electrónicos entre servidores. Este protocolo ayuda a prevenir ataques como el downgrade y la interceptación de correos electrónicos. En el contexto del SEO, implementar MTA-STS es vital para proteger la reputación del dominio, ya que los correos electrónicos no cifrados pueden ser fácilmente interceptados y manipulados, afectando negativamente la confianza del usuario. Además, asegurar la entrega de correos electrónicos de manera segura mejora la fiabilidad de las comunicaciones del dominio, lo que puede tener un impacto positivo en la percepción del usuario y, potencialmente, en el ranking de los motores de búsqueda."
    ,"most_used": True, "is_new": False},
    'arin': {
        'definition': "ARIN Lookup proporciona detalles sobre los registros de direcciones IP y ASN administrados por el American Registry for Internet Numbers (ARIN). Es crucial en SEO para verificar la propiedad y localización de direcciones IP.",
        'slogan': "Verifica y localiza tu red en América del Norte",
        'keywords': "",
        'info_popup': "ARIN Lookup es una herramienta que permite consultar la base de datos del American Registry for Internet Numbers (ARIN) para obtener información sobre las direcciones IP y los números de sistemas autónomos (ASN) registrados en América del Norte. Esta información incluye detalles como el propietario del recurso, la organización registrada y los puntos de contacto. En SEO, esta herramienta es útil para verificar la propiedad y autenticidad de las direcciones IP que acceden a tu sitio web, y para entender mejor la distribución geográfica de tu tráfico. Por ejemplo, si identificas un volumen significativo de tráfico procedente de ciertas direcciones IP, puedes utilizar ARIN Lookup para investigar y optimizar tus estrategias de marketing regional."
    ,"most_used": True, "is_new": False},
    'nsec': {
        'definition': "NSEC Lookup es una herramienta utilizada en DNSSEC para verificar la no existencia de un registro DNS en una zona. Es vital en SEO para asegurar la integridad y transparencia de la configuración DNS.",
        'slogan': "Asegura la inexistencia y protege tu DNS",
        'keywords': "",
        'info_popup': "NSEC (Next Secure) es un registro DNS utilizado en DNSSEC (Domain Name System Security Extensions) que proporciona pruebas de no existencia para nombres de dominio y tipos de registros en una zona DNS. NSEC Lookup permite verificar estas pruebas, asegurando que ciertos nombres o registros no existen en una zona específica. Esto es importante para evitar respuestas DNS fraudulentas y para asegurar la integridad de la configuración DNS. En SEO, la transparencia y la seguridad de la configuración DNS son cruciales para mantener la confianza del usuario y proteger el sitio web contra ataques maliciosos. Por ejemplo, NSEC puede prevenir el envenenamiento de caché DNS, mejorando así la fiabilidad del sitio web."
    ,"most_used": True, "is_new": False},
    'rrsig': {
        'definition': "RRSIG Lookup permite verificar las firmas criptográficas de los registros DNSSEC, asegurando la autenticidad e integridad de las respuestas DNS. Es fundamental en SEO para mantener la seguridad y confiabilidad del sitio web.",
        'slogan': "Verifica la autenticidad de tus registros DNS",
        'keywords': "",
        'info_popup': "RRSIG (Resource Record Signature) es un tipo de registro DNS utilizado en DNSSEC (Domain Name System Security Extensions) que contiene la firma digital de un conjunto de registros DNS. RRSIG Lookup permite verificar estas firmas criptográficas, asegurando que los registros DNS no han sido manipulados y provienen de una fuente auténtica. Esto es crucial para la seguridad del sitio web, ya que protege contra ataques como el envenenamiento de caché DNS. En términos de SEO, la seguridad y confiabilidad del sitio web son factores importantes que pueden influir en la clasificación en los motores de búsqueda y en la confianza del usuario. Implementar y verificar RRSIG contribuye a mantener la integridad de la información DNS y a asegurar una experiencia segura para los usuarios."
    ,"most_used": True, "is_new": False},
    'asn': {
        'definition': "ASN Lookup identifica el Sistema Autónomo (ASN) al que pertenece una dirección IP, proporcionando información sobre la red y su propietario. Es útil en SEO para analizar la distribución de red y optimizar la estrategia de geolocalización.",
        'slogan': "Descubre la red detrás de cada IP",
        'keywords': "",
        'info_popup': "ASN Lookup es una herramienta que permite identificar el Sistema Autónomo (AS) al que pertenece una dirección IP. Un ASN (Autonomous System Number) es una colección de redes IP administradas por una o varias entidades que presentan una política de enrutamiento común. Este lookup proporciona información detallada sobre la red, como el nombre del propietario y el rango de IPs administradas. Para estrategias de SEO, entender la distribución de red y la localización de los usuarios puede ser crucial para optimizar la entrega de contenido y mejorar la experiencia del usuario. Por ejemplo, conocer los ASNs que envían la mayor parte del tráfico a tu sitio web puede ayudar a identificar oportunidades para mejorar la infraestructura de red y el rendimiento del sitio."
    ,"most_used": True, "is_new": False},
    'ipseckey': {
        'definition': "IP Sec Key es un registro DNS que almacena claves criptográficas para la implementación de IPsec, una suite de protocolos de seguridad. En SEO, es importante para asegurar comunicaciones seguras y confiables en la red.",
        'slogan': "Seguridad de red sólida para un SEO confiable",
        'keywords': "",
        'info_popup': "IP Sec Key es un registro DNS utilizado para almacenar claves criptográficas necesarias para la configuración de IPsec (Internet Protocol Security), una suite de protocolos que asegura la comunicación en la red mediante cifrado y autenticación. Este registro es crucial para establecer túneles seguros y proteger los datos en tránsito, especialmente en redes sensibles. En el contexto del SEO y la seguridad del sitio web, la implementación de IPsec y el uso de IP Sec Key ayudan a asegurar que las comunicaciones entre servidores sean seguras y confiables, lo cual es esencial para proteger la integridad de los datos y la privacidad de los usuarios. Un sitio web seguro no solo protege contra ataques, sino que también mejora la confianza del usuario y puede influir positivamente en la clasificación de los motores de búsqueda."
    ,"most_used": True, "is_new": False},
    'loc': {
        'definition': "LOC Entry es un tipo de registro DNS que especifica la ubicación geográfica de un dominio. Es útil en SEO para estrategias de marketing local y para mejorar la precisión de la geolocalización del sitio web.",
        'slogan': "",
        'keywords': "Geolocaliza tu dominio para un SEO local preciso",
        'info_popup': "LOC Entry es un registro DNS que permite especificar la ubicación geográfica (latitud, longitud y altitud) asociada a un nombre de dominio. Esta información puede ser utilizada por los motores de búsqueda para mejorar la precisión de la geolocalización y la relevancia de los resultados de búsqueda locales. Por ejemplo, un negocio local puede beneficiarse de un registro LOC preciso al mejorar su visibilidad en las búsquedas de usuarios cercanos. Para estrategias de SEO, utilizar LOC Entries puede ayudar a optimizar la presencia en búsquedas locales y aumentar la relevancia del contenido para usuarios en áreas geográficas específicas."
    ,"most_used": True, "is_new": False},
    'ssl': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    ,"most_used": True, "is_new": False},
    'soa': {
        'definition': "SOA Lookup permite obtener el registro de Start of Authority (SOA) de un dominio, que contiene información clave sobre la zona DNS. Es vital en SEO para gestionar y optimizar la estructura DNS del sitio web.",
        'slogan': "La clave de tu DNS comienza aquí",
        'keywords': "",
        'info_popup': "El registro SOA (Start of Authority) es fundamental en la configuración DNS de un dominio, ya que contiene información crucial como el servidor de nombres principal, la dirección de correo electrónico del administrador, el número de serie de la zona DNS y varios parámetros de temporización. SOA Lookup permite consultar estos detalles, lo cual es esencial para la gestión y optimización de la estructura DNS. Por ejemplo, el número de serie en el SOA se incrementa cada vez que se realizan cambios en la zona DNS, lo cual es importante para asegurar que todos los servidores de nombres secundarios estén actualizados. Para SEO, mantener una configuración DNS precisa y eficiente puede mejorar la velocidad de resolución del dominio, lo que contribuye a una mejor experiencia del usuario y a un potencial mejoramiento en el ranking de búsqueda."
    ,"most_used": True, "is_new": False},
    'txt': {
        'definition': "TXT Lookup se utiliza para consultar los registros TXT de un dominio, que pueden contener diversas informaciones, como configuraciones de SPF, DKIM y DMARC. Es crucial en SEO para verificar y optimizar la autenticación de correos electrónicos.",
        'slogan': "Cada texto cuenta para una autenticación perfecta",
        'keywords': "",
        'info_popup': "Los registros TXT (Text) son un tipo de registro DNS que permite a los administradores de dominios almacenar cualquier texto en el sistema de nombres de dominio. TXT Lookup es una herramienta que permite consultar estos registros, que a menudo incluyen configuraciones críticas como SPF, DKIM y DMARC, fundamentales para la autenticación de correos electrónicos. Por ejemplo, un registro TXT puede contener una política de SPF que indique qué servidores están autorizados a enviar correos en nombre del dominio, o una clave DKIM utilizada para firmar correos electrónicos. Para estrategias de SEO, verificar y optimizar estos registros ayuda a mantener la seguridad y la reputación del dominio, asegurando la correcta entrega de correos y protegiendo contra ataques de phishing y spam."
    ,"most_used": True, "is_new": False},
    'bimi': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    ,"most_used": True, "is_new": False},
    'dns': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    ,"most_used": True, "is_new": False},
    'http': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    ,"most_used": True, "is_new": False},
    'https': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    ,"most_used": True, "is_new": False},
    'dnskey': {
        'definition': "DNS Key es un tipo de registro DNS que se utiliza en la implementación de DNSSEC para asegurar la autenticidad e integridad de las respuestas DNS. En SEO, asegura que el sitio web sea confiable y seguro para los usuarios.",
        'slogan': "Seguridad y autenticidad desde el DNS",
        'keywords': "",
        'info_popup': "DNS Key es un registro utilizado en DNSSEC (Domain Name System Security Extensions) que contiene las claves criptográficas necesarias para firmar y autenticar las respuestas DNS. Esto asegura que las respuestas no hayan sido manipuladas y provienen de una fuente legítima. La implementación de DNSSEC y el uso de DNS Key son esenciales para proteger contra ataques como el envenenamiento de caché DNS. En el contexto del SEO, la seguridad del sitio web es un factor crucial. Un sitio protegido por DNSSEC es más confiable, lo que puede influir positivamente en la percepción del usuario y en la clasificación del sitio en los motores de búsqueda."
    ,"most_used": True, "is_new": False},
    'cert': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    ,"most_used": True, "is_new": False},
    'srv': {
        'definition': "SRV Lookup se utiliza para encontrar los servidores que proporcionan servicios específicos para un dominio, como correo o VoIP. Es importante en SEO para la configuración precisa y eficiente de servicios de red.",
        'slogan': "Encuentra y configura tus servicios de red con precisión",
        'keywords': "",
        'info_popup': "El registro SRV (Service) en DNS permite especificar la ubicación de los servidores que proporcionan servicios específicos para un dominio, tales como correo (SMTP), VoIP (SIP), y otros servicios de red. SRV Lookup es una herramienta que permite consultar estos registros, proporcionando información detallada sobre los servidores y puertos utilizados. En el ámbito del SEO, una configuración precisa y eficiente de los registros SRV es crucial para garantizar la correcta prestación de servicios y mejorar la experiencia del usuario. Por ejemplo, si un sitio web utiliza servicios externos para manejar llamadas VoIP, los registros SRV asegurarán que las conexiones se dirijan al servidor correcto, optimizando así el rendimiento y la fiabilidad del servicio."
    ,"most_used": True, "is_new": False},
    'dkim': {
        'definition': "DKIM Lookup verifica la autenticidad de los correos electrónicos mediante firmas criptográficas. En SEO, es crucial para asegurar que los emails no sean alterados en tránsito, manteniendo la integridad y confianza en las comunicaciones del dominio.",
        'slogan': "Firmeza en cada correo, confianza en cada clic",
        'keywords': "",
        'info_popup': "DKIM (DomainKeys Identified Mail) es un protocolo de autenticación de correos electrónicos que utiliza firmas criptográficas para asegurar que los mensajes no hayan sido alterados en tránsito. DKIM Lookup permite verificar estas firmas y confirmar que los correos provienen realmente del dominio especificado. Esto es esencial para mantener la integridad y la confianza en las comunicaciones de correo electrónico, lo cual es crucial para estrategias de marketing digital y SEO. Por ejemplo, un email firmado con DKIM puede ser validado por el servidor receptor, reduciendo la probabilidad de que sea considerado spam o phishing. Implementar DKIM contribuye a una mejor entrega de correos y a la protección de la reputación del dominio."
    ,"most_used": True, "is_new": False},
    'dns_server': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    ,"most_used": True, "is_new": False},
    'spf': {
        'definition': "SPF Lookup (Sender Policy Framework) verifica qué servidores están autorizados para enviar correos electrónicos en nombre de un dominio. Es fundamental en SEO para evitar la falsificación de correos y mantener la credibilidad del dominio.",
        'slogan': "Autentica tus envíos y protege tu marca",
        'keywords': "",
        'info_popup': "SPF Lookup es una herramienta utilizada para consultar los registros SPF de un dominio, los cuales especifican qué servidores de correo están autorizados para enviar emails en nombre de ese dominio. Este mecanismo ayuda a prevenir el spoofing de correos electrónicos, asegurando que los emails no sean falsificados. Por ejemplo, si un dominio tiene un registro SPF bien configurado, los servidores de correo receptor pueden verificar la autenticidad del correo, reduciendo la probabilidad de que los correos legítimos sean marcados como spam. Para las estrategias de SEO, mantener una buena reputación del dominio es crucial, ya que la entrega efectiva y segura de correos electrónicos puede influir en la percepción del usuario y la interacción con el sitio web."
    ,"most_used": True, "is_new": False},
    'dmarc': {
        'definition': "DMARC (Domain-based Message Authentication, Reporting & Conformance) es un protocolo de autenticación de email que ayuda a proteger contra el spoofing y phishing. En SEO, es importante para mantener la reputación del dominio y asegurar la confianza del usuario.",
        'slogan': "Protege tu dominio, fortalece tu reputación",
        'keywords': "",
        'info_popup': "DMARC es un protocolo de autenticación de correos electrónicos que permite a los propietarios de dominios especificar qué mecanismos (SPF y/o DKIM) se utilizan para autenticar sus correos electrónicos y cómo deben manejarse los correos electrónicos que no pasen la autenticación. Este protocolo no solo ayuda a prevenir ataques de suplantación de identidad (spoofing) y phishing, sino que también proporciona informes detallados sobre los intentos de envío no autorizados. Para las estrategias de SEO, implementar DMARC es crucial para mantener la reputación del dominio, ya que los correos electrónicos fraudulentos pueden afectar negativamente la percepción del usuario y, en consecuencia, la confianza y el tráfico hacia el sitio web."
    ,"most_used": True, "is_new": False},
    'mx': {
        'definition': "MX Discover es una herramienta crucial en SEO para identificar los servidores de correo responsables de recibir emails para un dominio. Esta información es vital para configurar y optimizar las estrategias de email marketing y asegurar una correcta entrega de correos electrónicos.",
        'slogan': "Conecta tus correos con precisión y seguridad",
        'keywords': "",
        'info_popup': "MX Discover permite obtener los registros de intercambio de correo (MX) de un dominio, que especifican los servidores encargados de recibir los correos electrónicos dirigidos a ese dominio. Esta información es esencial para la configuración y optimización de campañas de email marketing, asegurando que los correos electrónicos se entreguen correctamente. Por ejemplo, si un dominio tiene múltiples registros MX, es posible determinar la prioridad y redundancia de los servidores de correo, lo cual puede influir en la fiabilidad y velocidad de entrega de los emails. Además, esta herramienta ayuda a diagnosticar problemas de entrega y a implementar medidas de seguridad como SPF, DKIM y DMARC."
    ,"most_used": True, "is_new": False},
    'titles': {
        'definition': "Los títulos son esenciales para el SEO, ya que indican a los motores de búsqueda y a los usuarios de qué trata una página. Un título optimizado debe ser relevante, incluir palabras clave y atraer clics.",
        'slogan': "Títulos impactantes, clics garantizados",
        'keywords': "",
        'info_popup': "Los títulos (o title tags) son elementos HTML que especifican el título de una página web. Este título aparece en la pestaña del navegador y en los resultados de búsqueda. Un título bien escrito es crucial para el SEO porque proporciona a los motores de búsqueda información sobre el contenido de la página y ayuda a los usuarios a decidir si hacer clic en el enlace. Por ejemplo, un título como 'Guía Completa de SEO para Principiantes' es más efectivo que 'SEO'. El primero es específico, incluye palabras clave relevantes y es más probable que atraiga a usuarios interesados en aprender sobre SEO. Además, los títulos deben ser concisos, preferiblemente de menos de 60 caracteres, para evitar que se corten en los resultados de búsqueda."
    ,"most_used": True, "is_new": False},
    'meta-description': {
        'definition': "Las meta descriptions resumen el contenido de la página en los resultados de búsqueda, influyendo en el CTR y proporcionando una vista previa a los usuarios. Son esenciales en SEO para atraer tráfico relevante.",
        'slogan': "Tu resumen en los resultados de búsqueda",
        'keywords': "",
        'info_popup': "La meta description es una breve descripción del contenido de una página web, que aparece debajo del título en los resultados de búsqueda. Aunque no afecta directamente el ranking, una meta description bien redactada puede mejorar significativamente el CTR (Click-Through Rate), ya que ofrece a los usuarios un resumen conciso y atractivo del contenido de la página. Por ejemplo, una meta description como 'Descubre nuestra guía completa de SEO y aprende técnicas avanzadas para mejorar tu posicionamiento en Google' informa y atrae a los usuarios interesados en SEO. Las mejores prácticas incluyen mantener la longitud entre 150 y 160 caracteres, utilizar palabras clave relevantes y hacerla lo suficientemente persuasiva para incentivar a los usuarios a hacer clic en el enlace."
    ,"most_used": True, "is_new": False},
    'meta-keywords': {
        'definition': "Las meta keywords eran utilizadas para especificar las palabras clave relevantes de una página. Aunque su uso ha disminuido en SEO moderno, entender su historia es importante para el contexto de la evolución de SEO",
        'slogan': "Del pasado del SEO, una lección de evolución",
        'keywords': "",
        'info_popup': "Las meta keywords eran una etiqueta HTML que permitía a los webmasters especificar palabras clave relacionadas con el contenido de una página web. En los primeros días de SEO, los motores de búsqueda utilizaban estas palabras clave para comprender el tema de la página y mejorar el ranking en los resultados de búsqueda. Sin embargo, con el tiempo, esta práctica fue abusada con el uso excesivo de palabras clave irrelevantes (keyword stuffing), lo que llevó a los motores de búsqueda como Google a devaluar su importancia. Hoy en día, la mayoría de los motores de búsqueda no consideran las meta keywords como un factor de ranking significativo. Sin embargo, conocer su historia ayuda a comprender cómo ha evolucionado el SEO y por qué es crucial enfocarse en la calidad del contenido y otras prácticas de optimización."
    ,"most_used": True, "is_new": False},
    'headings': {
        'definition': "Los encabezados (headings) estructuran el contenido y mejoran la legibilidad y la SEO. Utilizados correctamente, facilitan a los motores de búsqueda y a los usuarios comprender el tema de la página.",
        'slogan': "Estructura y claridad para tu contenido",
        'keywords': "",
        'info_popup': "Los encabezados (headings) son etiquetas HTML que se utilizan para definir la estructura jerárquica del contenido de una página web, desde el H1 hasta el H6. El H1 generalmente se usa para el título principal de la página, mientras que H2 a H6 se utilizan para subtítulos y secciones dentro del contenido. Los encabezados no solo mejoran la legibilidad al dividir el texto en secciones manejables, sino que también ayudan a los motores de búsqueda a entender la estructura y el tema del contenido. Por ejemplo, en una guía sobre SEO, un H1 podría ser 'Guía Completa de SEO', mientras que los H2 podrían ser 'Qué es SEO', 'Importancia de las Palabras Clave', y así sucesivamente. La correcta utilización de encabezados con palabras clave relevantes puede mejorar el ranking y la experiencia del usuario."
    ,"most_used": True, "is_new": False},
    'canonicals': {
        'definition': "Las etiquetas canonicals indican la versión preferida de una página duplicada, ayudando a evitar problemas de contenido duplicado. Son esenciales en SEO para consolidar señales de ranking.",
        'slogan': "Consolidando tu contenido para un mejor ranking",
        'keywords': "",
        'info_popup': "La etiqueta canonical es un elemento HTML que se utiliza para informar a los motores de búsqueda sobre la versión preferida de una página web cuando existen múltiples versiones con contenido similar o duplicado. Esto es crucial en SEO para evitar problemas de contenido duplicado que pueden diluir las señales de ranking y confundir a los motores de búsqueda. Por ejemplo, si un sitio tiene varias URLs que muestran el mismo contenido (como 'example.com/page' y 'example.com/page?ref=123'), la etiqueta canonical puede especificar cuál es la versión principal que debe indexarse, consolidando así el valor SEO de las diferentes versiones. Implementar canonicals correctamente ayuda a mantener la coherencia del contenido y a maximizar el potencial de ranking en los resultados de búsqueda."
    ,"most_used": True, "is_new": False},
    'directives': {
        'definition': "Las directivas son instrucciones para los motores de búsqueda sobre cómo indexar y rastrear el contenido del sitio. Son vitales en SEO para controlar la visibilidad y el acceso a las páginas",
        'slogan': "Controla cómo los motores de búsqueda ven tu sitio",
        'keywords': "",
        'info_popup': "Las directivas en SEO son instrucciones específicas que se proporcionan a los motores de búsqueda sobre cómo deben rastrear e indexar el contenido de un sitio web. Estas directivas pueden incluirse en el archivo robots.txt, en las meta etiquetas del HTML, o a través de encabezados HTTP. Por ejemplo, la directiva 'noindex' puede indicarle a un motor de búsqueda que no indexe una página específica, mientras que 'nofollow' puede prevenir que los motores de búsqueda sigan ciertos enlaces. Utilizar directivas de manera adecuada permite a los webmasters controlar qué contenido es visible en los resultados de búsqueda y cómo se rastrea el sitio, optimizando así la gestión de la visibilidad y mejorando la eficiencia del rastreo. Implementar directivas correctas es esencial para evitar problemas de duplicación de contenido y gestionar adecuadamente el SEO del sitio."
    ,"most_used": True, "is_new": False},
    'shema-org': {
        'definition': "Schema.org proporciona vocabularios para estructurar datos en páginas web, mejorando la comprensión de los motores de búsqueda y habilitando rich snippets. Es crucial en SEO para aumentar la visibilidad.",
        'slogan': "Estructura tus datos, destaca en los resultados de búsqueda",
        'keywords': "",
        'info_popup': "Schema.org es una iniciativa colaborativa que proporciona un conjunto de vocabularios para estructurar datos en páginas web, permitiendo a los motores de búsqueda comprender mejor el contenido. Mediante el uso de schema markup, los webmasters pueden definir elementos específicos como productos, eventos, reseñas, y más, que los motores de búsqueda pueden interpretar y mostrar de manera más rica en los resultados de búsqueda (rich snippets). Por ejemplo, una página de producto con schema markup puede mostrar información adicional como el precio, la disponibilidad y las calificaciones directamente en los resultados de búsqueda, lo que mejora el CTR y la visibilidad. Implementar Schema.org en el contenido web es una práctica esencial en SEO moderno para destacar en los resultados de búsqueda y proporcionar una experiencia más informativa a los usuarios."
    ,"most_used": True, "is_new": False},
    'hreflang': {
        'definition': "Las etiquetas Hreflang indican a los motores de búsqueda la versión lingüística y regional correcta de una página, mejorando la experiencia del usuario y el SEO en sitios multilingües.",
        'slogan': "Optimiza tu contenido para una audiencia global",
        'keywords': "",
        'info_popup': "Las etiquetas Hreflang son atributos HTML utilizados para especificar la versión lingüística y regional de una página web, ayudando a los motores de búsqueda a mostrar la versión correcta a los usuarios en función de su idioma y ubicación. Esto es especialmente importante para sitios web multilingües o internacionales. Por ejemplo, un sitio web con versiones en inglés, español y francés puede usar hreflang para indicar a Google que la página example.com/en/ es para usuarios de habla inglesa,example.com/es/ es para usuarios de habla hispana, y example.com/fr/ es para usuarios de habla francesa. Implementar hreflang correctamente asegura que los usuarios sean dirigidos a la versión más relevante de la página, mejorando su experiencia y el SEO del sitio web en diferentes mercados."
    ,"most_used": True, "is_new": False},
    'urls': {
        'definition': "Las URLs optimizadas son esenciales en SEO, ya que afectan la indexación, la visibilidad y la experiencia del usuario. Deben ser claras, concisas y contener palabras clave relevantes.",
        'slogan': "URLs claras, mejor SEO",
        'keywords': "",
        'info_popup': "Las URLs (Uniform Resource Locators) son direcciones web que indican la ubicación de un recurso en Internet. En SEO, las URLs bien estructuradas y optimizadas son cruciales porque afectan la manera en que los motores de búsqueda y los usuarios perciben y acceden al contenido de un sitio web. Una URL optimizada debe ser clara, concisa, fácil de entender y contener palabras clave relevantes. Por ejemplo, example.com/guia-seo-basica es mucho más efectiva y amigable para el SEO que example.com/page123. Las URLs claras y descriptivas no solo mejoran la experiencia del usuario, facilitando la navegación y la comprensión del contenido, sino que también ayudan a los motores de búsqueda a indexar y clasificar mejor las páginas. Implementar buenas prácticas en la creación de URLs es fundamental para el éxito en SEO."
    ,"most_used": True, "is_new": False},
    'gzip': {
        'definition': "La compresión Gzip es una técnica para reducir el tamaño de los archivos transmitidos entre el servidor y el navegador del usuario, mejorando así el rendimiento del sitio web y la velocidad de carga. Es crucial para el SEO, ya que influye en la experiencia del usuario y en el ranking de búsqueda",
        'slogan': "Optimiza tu velocidad, mejora tu SEO con Gzip",
        'keywords': "",
        'info_popup': "Gzip es un método de compresión de datos utilizado para reducir el tamaño de los archivos HTML, CSS, JavaScript y otros recursos web transmitidos entre el servidor y el navegador del usuario. Cuando un servidor web habilita la compresión Gzip, los archivos se comprimen antes de ser enviados y se descomprimen automáticamente por el navegador del usuario, lo que resulta en tiempos de carga más rápidos y una menor cantidad de datos transferidos. Esta técnica no solo mejora significativamente la velocidad de carga de las páginas web, lo cual es un factor de ranking en SEO según Google, sino que también reduce el consumo de ancho de banda del servidor y mejora la experiencia del usuario al hacer que las páginas se carguen más rápido. Por ejemplo, si una página web tiene un archivo HTML de 1 MB y se comprime con Gzip a solo 100 KB, los usuarios experimentarán tiempos de carga mucho más rápidos sin comprometer la calidad del contenido.Implementar la compresión Gzip en un sitio web es relativamente sencillo y puede configurarse en el servidor web mediante la modificación de archivos de configuración como .htaccess en Apache o mediante la configuración de compresión en Nginx. Los beneficios de la compresión Gzip son especialmente notables en sitios web con mucho tráfico y grandes volúmenes de contenido estático, como imágenes y scripts.Para el SEO, la compresión Gzip es crucial porque Google y otros motores de búsqueda valoran la velocidad de carga rápida como un factor de ranking importante. Sitios web optimizados con Gzip no solo tienen mejor posicionamiento en los resultados de búsqueda, sino que también ofrecen una experiencia de usuario mejorada, reduciendo las tasas de rebote y aumentando el tiempo de permanencia en el sitio."
    ,"most_used": True, "is_new": False},
    'css': {
        'definition': "Los problemas de CSS pueden afectar la apariencia y funcionalidad de un sitio web. Resolverlos es esencial para asegurar una buena experiencia de usuario y un rendimiento óptimo en SEO",
        'slogan': "Soluciona tus problemas de estilo, mejora tu SEO",
        'keywords': "",
        'info_popup': "CSS (Cascading Style Sheets) es el lenguaje utilizado para describir la presentación de un documento HTML. Los problemas de CSS, como estilos rotos o mal aplicados, pueden afectar negativamente la apariencia y la funcionalidad de un sitio web. Esto no solo perjudica la experiencia del usuario, sino que también puede impactar negativamente el SEO. Por ejemplo, un diseño desordenado o elementos mal alineados pueden aumentar la tasa de rebote y disminuir el tiempo de permanencia en el sitio. Además, los problemas de CSS pueden afectar la capacidad de los motores de búsqueda para rastrear e indexar el contenido correctamente. Identificar y resolver problemas de CSS, mediante herramientas de validación y pruebas en múltiples dispositivos, es crucial para mantener un sitio web atractivo y optimizado para los motores de búsqueda."
    ,"most_used": True, "is_new": False},
    'deprecated-html': {
        'definition': "Las etiquetas HTML obsoletas pueden afectar la compatibilidad y el rendimiento del sitio web. Reemplazarlas es esencial para mantener estándares actuales y una buena práctica de SEO",
        'slogan': "Actualiza tu código, optimiza tu SEO",
        'keywords': "",
        'info_popup': "Las etiquetas HTML obsoletas (deprecated HTML tags) son aquellas que ya no se recomiendan en las versiones actuales de HTML y pueden ser incompatibles con los navegadores modernos. El uso de estas etiquetas puede llevar a problemas de presentación y funcionalidad en el sitio web. Por ejemplo, etiquetas como `<font>` y `<center>` han sido reemplazadas por CSS para definir estilos y alineaciones. Utilizar etiquetas HTML modernas y seguir los estándares actuales es crucial para asegurar la compatibilidad del sitio web en todos los dispositivos y navegadores. Además, mantener el código HTML actualizado y limpio ayuda a los motores de búsqueda a rastrear e indexar el contenido de manera más eficiente, mejorando así el SEO. Es importante revisar y actualizar el código regularmente para evitar el uso de etiquetas obsoletas."
    }

}