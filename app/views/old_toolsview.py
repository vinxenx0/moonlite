
@app.route("/tools/domains/traceroute", methods=["GET", "POST"])
def _traceroute():
    definition = "Traceroute es una herramienta que rastrea la ruta y mide los retrasos de paquetes de datos desde un host a otro. En SEO, es vital para identificar cuellos de botella y problemas de latencia que pueden afectar la velocidad de un sitio web."
    slogan = "Rastreando la ruta hacia un rendimiento óptimo"
    keywords = "traceroute, traceroute online, herramienta traceroute, traceroute gratis"
    info_popup = "Traceroute es una utilidad de diagnóstico de red que rastrea la ruta que siguen los paquetes de datos para llegar a un destino. Proporciona información sobre cada salto en la ruta, incluyendo tiempos de respuesta y posibles puntos de congestión. En el contexto de SEO, la velocidad de un sitio web es un factor crucial para la clasificación en los motores de búsqueda. Utilizando Traceroute, los profesionales de SEO pueden identificar y resolver problemas de latencia en la red que puedan estar ralentizando el tiempo de carga de un sitio web. Por ejemplo, si Traceroute muestra que hay un retraso significativo en uno de los saltos, se puede trabajar con los proveedores de servicios para optimizar esa ruta."
    start_time = time.time()
    breadcrumbs = [
        {
            "url": "/tools",
            "text": "Tools"
        },
        {
            "url": "/tools/domains/",
            "text": "Dominios"
        },
        {
            "url": "/tools/domains/traceroute",
            "text": "Traceroute"
        },
    ]
    form = DomainToolsForm()
    results = None
    is_results_valid = False
    if form.validate_on_submit():
        domain = form.domain.data
        results = {'traceroute_lookup': traceroute_lookup(domain)}

        print(f"traceroute_lookup result: {results['traceroute_lookup']}")
        print(f"type: {type(results['traceroute_lookup'])}")

        # traceroute_lookup result: {'stdout': '', 'stderr': 'google.domain: Nombre o servicio desconocido\nCannot handle "host" cmdline arg `google.domain\' on position 1 (argc 3)\n'}
        # type: <class 'dict'>

        #if isinstance(results["traceroute_lookup"], dict):
        if results['traceroute_lookup']['stderr'] is not None:
            is_results_valid = False
        else:
            is_results_valid = True

    end_time = time.time()
    duration = end_time - start_time
    return render_template(
        "tools/domains/traceroute.html",
        title="Traceroute",
        is_results_valid=is_results_valid,
        duration=duration,
        form=form,
        results=results,
        breadcrumbs=breadcrumbs,
        definition=definition,
        slogan=slogan,
        info_popup=info_popup,
        keywords=keywords,
    )


@app.route("/tools/domains/aaaa", methods=["GET", "POST"])
def _aaaa_domain():
    definition = "AAAA Lookup se utiliza para resolver direcciones IPv6 de un dominio. Es relevante en SEO para asegurar que un sitio web esté accesible en la moderna infraestructura de internet, mejorando la cobertura y accesibilidad global."
    slogan = "Preparando tu sitio para la próxima generación de Internet"
    keywords = "entrada aaaa,resolver ip6, dominio ip6, resolucion ip6 aaaa"
    info_popup = "El registro AAAA (Quad-A) en DNS se utiliza para mapear un nombre de dominio a una dirección IPv6, la versión más reciente del protocolo de Internet. AAAA Lookup permite obtener estas direcciones IPv6, lo cual es cada vez más importante debido al crecimiento del uso de dispositivos conectados y la expansión de la infraestructura de internet. En términos de SEO, asegurar que un sitio web esté accesible a través de IPv6 puede mejorar la accesibilidad y rendimiento del sitio, especialmente en regiones donde IPv6 es más prevalente. Además, tener soporte para IPv6 puede ser un factor diferenciador frente a la competencia, mostrando un compromiso con la modernización y la futura prueba de la infraestructura web."
    start_time = time.time()
    breadcrumbs = [
        {
            "url": "/tools",
            "text": "Tools"
        },
        {
            "url": "/tools/domains/",
            "text": "Dominios"
        },
        {
            "url": "/tools/domains/aaaa",
            "text": "AAAA lookup"
        },
    ]
    form = DomainToolsForm()
    results = None
    is_results_valid = False
    if form.validate_on_submit():
        domain = form.domain.data
        results = {'aaaa_lookup': aaaa_lookup(domain)}

        print(f"aaaa_lookup result: {results['aaaa_lookup']}")
        print(f"type: {type(results['aaaa_lookup'])}")

        # aaaa_lookup result: The DNS response does not contain an answer to the question: 4glsp.com. IN AAAA
        # type: <class 'str'>

        if results and results is not None:
            is_results_valid = True
        else:
            is_results_valid = False

        # Check if results['whois_lookup'] is a dictionary before accessing its keys
        #if isinstance(results["reverse_lookup"], list):
        #    is_results_valid = results["reverse_lookup"].get("domain_name") is not None
        #else:
        # Handle the case where whois_lookup did not return a dictionary
        #      is_results_valid = False

    end_time = time.time()
    duration = end_time - start_time
    return render_template(
        "tools/domains/aaaa.html",
        title="AAAA lookup",
        is_results_valid=is_results_valid,
        duration=duration,
        form=form,
        results=results,
        breadcrumbs=breadcrumbs,
        definition=definition,
        slogan=slogan,
        info_popup=info_popup,
        keywords=keywords,
    )


@app.route("/tools/domains/ip", methods=["GET", "POST"])
def _ip_domain():
    definition = "IP Lookup permite obtener información detallada sobre una dirección IP, incluyendo su ubicación geográfica y el ISP. En SEO, es esencial para analizar la distribución de tráfico y diagnosticar problemas de rendimiento de red."
    slogan = "Descubre todo sobre cualquier IP"
    keywords = "ip domain,resolver ip, dominio ip, resolucion ip dominio"
    info_popup = "IP Lookup es una herramienta que proporciona información detallada sobre una dirección IP específica, como su ubicación geográfica, el proveedor de servicios de Internet (ISP) y el nombre de host asociado. Esta información es útil en SEO para diversas tareas, como analizar la procedencia del tráfico web, identificar patrones sospechosos o fraudulentos, y diagnosticar problemas de red que puedan afectar la velocidad de carga de un sitio web. Por ejemplo, si una gran cantidad de tráfico proviene de una región inesperada, esto puede indicar la necesidad de ajustar la estrategia de marketing regional o investigar posibles ataques de spam."
    start_time = time.time()
    breadcrumbs = [
        {
            "url": "/tools",
            "text": "Tools"
        },
        {
            "url": "/tools/domains/",
            "text": "Dominios"
        },
        {
            "url": "/tools/domains/ip",
            "text": "IP lookup"
        },
    ]
    form = DomainToolsForm()
    results = None
    is_results_valid = False
    if form.validate_on_submit():
        domain = form.domain.data
        results = {'ip_lookup': ip_lookup(domain)}

        print(f"ip_lookup result: {results['ip_lookup']}")
        print(f"type: {type(results['ip_lookup'])}")

        # ip_lookup result: [Errno -2] Name or service not known
        # type: <class 'str'>

        if results and results is not None:
            is_results_valid = True
        else:
            is_results_valid = False

        # Check if results['whois_lookup'] is a dictionary before accessing its keys
        #if isinstance(results["reverse_lookup"], list):
        #    is_results_valid = results["reverse_lookup"].get("domain_name") is not None
        #else:
        # Handle the case where whois_lookup did not return a dictionary
        #      is_results_valid = False

    end_time = time.time()
    duration = end_time - start_time
    return render_template(
        "tools/domains/ip.html",
        title="IP lookup",
        is_results_valid=is_results_valid,
        duration=duration,
        form=form,
        results=results,
        breadcrumbs=breadcrumbs,
        definition=definition,
        slogan=slogan,
        info_popup=info_popup,
        keywords=keywords,
    )


@app.route("/tools/domains/cname", methods=["GET", "POST"])
def _cname_domain():
    definition = "CNAME (Canonical Name) es un tipo de registro DNS que permite mapear un dominio a otro. En SEO, es crucial para gestionar dominios y subdominios, facilitando la redirección y la gestión de URLs canónicas."
    slogan = "Alias perfectos para una gestión de dominios impecable"
    keywords = "reverse domain, dominio inverso, reverse lookup, resolución inversa"
    info_popup = "El registro CNAME se utiliza en el sistema de nombres de dominio (DNS) para alias de un dominio a otro, conocido como el dominio canónico. Esto es útil para redireccionar tráfico de una URL a otra sin alterar la URL visible en el navegador del usuario. Por ejemplo, puedes tener 'www.ejemplo.com' apuntando a 'ejemplo.com'. En términos de SEO, los CNAMEs son útiles para gestionar subdominios, redirecciones y evitar problemas de contenido duplicado. Además, facilitan la implementación de servicios externos como plataformas de marketing o análisis que requieren redirección de subdominios."
    start_time = time.time()
    breadcrumbs = [
        {
            "url": "/tools",
            "text": "Tools"
        },
        {
            "url": "/tools/domains/",
            "text": "Dominios"
        },
        {
            "url": "/tools/domains/cname",
            "text": "CNAME"
        },
    ]
    form = DomainToolsForm()
    results = None
    is_results_valid = False
    if form.validate_on_submit():
        domain = form.domain.data
        results = {'cname_lookup': cname_lookup(domain)}

        print(f"cname_lookup result: {results['cname_lookup']}")
        print(f"type: {type(results['cname_lookup'])}")

        # The DNS response does not contain an answer to the question: migasolinera.app. IN CNAME
        # type: <class 'list'>

        if results and results is not None:
            is_results_valid = True
        else:
            is_results_valid = False

        # Check if results['whois_lookup'] is a dictionary before accessing its keys
        #if isinstance(results["reverse_lookup"], list):
        #    is_results_valid = results["reverse_lookup"].get("domain_name") is not None
        #else:
        # Handle the case where whois_lookup did not return a dictionary
        #      is_results_valid = False

    end_time = time.time()
    duration = end_time - start_time
    return render_template(
        "tools/domains/cname.html",
        title="CName",
        is_results_valid=is_results_valid,
        duration=duration,
        form=form,
        results=results,
        breadcrumbs=breadcrumbs,
        definition=definition,
        slogan=slogan,
        info_popup=info_popup,
        keywords=keywords,
    )


@app.route("/tools/domains/reverse", methods=["GET", "POST"])
def _reverse_domain():
    definition = "El Reverse Domain es una técnica que permite identificar todos los dominios asociados a una dirección IP específica. Es útil en SEO para descubrir redes de sitios web, entender la estructura de enlaces y evaluar posibles riesgos de spam."
    slogan = "Descubre el entramado de sitios web en una IP"
    keywords = "reverse domain, dominio inverso, reverse lookup, resolución inversa"
    info_popup = "El Reverse Domain Lookup, o búsqueda inversa de dominio, permite obtener una lista de todos los dominios que comparten una misma dirección IP. Esta técnica es útil para analizar la red de sitios web de un competidor o cliente. Por ejemplo, si varios sitios comparten una misma IP, podrían estar vinculados de alguna manera, lo que puede afectar sus estrategias de SEO debido a la posible percepción de prácticas de black hat SEO. Además, esta herramienta puede ayudar a identificar si un servidor está sobrecargado con demasiados sitios, lo cual podría afectar el rendimiento y, por ende, la clasificación en los motores de búsqueda."
    start_time = time.time()
    breadcrumbs = [
        {
            "url": "/tools",
            "text": "Tools"
        },
        {
            "url": "/tools/domains/",
            "text": "Dominios"
        },
        {
            "url": "/tools/domains/reverse",
            "text": "Reverse"
        },
    ]
    form = DomainToolsForm()
    results = None
    is_results_valid = False
    if form.validate_on_submit():
        domain = form.domain.data
        results = {'reverse_lookup': reverse_lookup(domain)}

        print(f"reserve_lookup result: {results['reverse_lookup']}")
        print(f"type: {type(results['reverse_lookup'])}")

        # reserve_lookup result: Text input is malformed.
        # type: <class 'str'>

        if results and results is not None:
            is_results_valid = True
        else:
            is_results_valid = False

        # Check if results['whois_lookup'] is a dictionary before accessing its keys
        #if isinstance(results["reverse_lookup"], list):
        #    is_results_valid = results["reverse_lookup"].get("domain_name") is not None
        #else:
        # Handle the case where whois_lookup did not return a dictionary
        #      is_results_valid = False

    end_time = time.time()
    duration = end_time - start_time
    return render_template(
        "tools/domains/reverse.html",
        title="Reverse",
        is_results_valid=is_results_valid,
        duration=duration,
        form=form,
        results=results,
        breadcrumbs=breadcrumbs,
        definition=definition,
        slogan=slogan,
        info_popup=info_popup,
        keywords=keywords,
    )


@app.route("/tools/domains/whois", methods=["GET", "POST"])
def _whois_domain():
    definition = "WHOIS es una herramienta esencial en SEO para obtener información sobre el propietario de un dominio, la fecha de registro y otros datos cruciales. Esta información ayuda a los profesionales de marketing digital a analizar la legitimidad y antigüedad de un dominio, factores que influyen en la estrategia SEO."
    slogan = "Descubre quién está detrás del dominio"
    keywords = "whois, whois lookup, resolver dominio"
    info_popup = "WHOIS es un protocolo que se utiliza para consultar bases de datos que almacenan la información de registro de nombres de dominio en internet. Esta herramienta revela detalles importantes como el registrante, la fecha de creación y vencimiento del dominio, y los servidores DNS asociados. Por ejemplo, conocer la antigüedad de un dominio puede indicar su autoridad y confiabilidad, factores importantes en la evaluación de un sitio web para SEO. Además, WHOIS permite identificar cambios recientes en la propiedad de un dominio, lo cual puede ser relevante para entender fluctuaciones en su rendimiento SEO."
    start_time = time.time()
    breadcrumbs = [
        {
            "url": "/tools",
            "text": "Tools"
        },
        {
            "url": "/tools/domains/",
            "text": "Dominios"
        },
        {
            "url": "/tools/domains/whois",
            "text": "WHOIS"
        },
    ]
    form = DomainToolsForm()
    results = None
    is_results_valid = False
    if form.validate_on_submit():
        domain = form.domain.data
        results = {"whois_lookup": whois_lookup(domain)}

        # Debugging: Print the type and content of results['whois_lookup']
        print(f"whois_lookup result: {results['whois_lookup']}")
        print(f"type: {type(results['whois_lookup'])}")

        # Check if results['whois_lookup'] is a dictionary before accessing its keys
        if isinstance(results["whois_lookup"], dict):
            is_results_valid = results["whois_lookup"].get(
                "domain_name") is not None
        else:
            # Handle the case where whois_lookup did not return a dictionary
            is_results_valid = False

    end_time = time.time()
    duration = end_time - start_time
    return render_template(
        "tools/domains/whois.html",
        title="WHOIS",
        is_results_valid=is_results_valid,
        duration=duration,
        form=form,
        results=results,
        breadcrumbs=breadcrumbs,
        definition=definition,
        slogan=slogan,
        info_popup=info_popup,
        keywords=keywords,
    )
