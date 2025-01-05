def audit_mobile_usability(url, soup):
    viewport_not_set = True
    target_size = []
    content_not_sized_correctly = False
    illegible_font_size = []
    unsupported_plugins = []
    mobile_alternate_link = False

    # Check viewport meta tag
    viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
    if viewport_tag:
        content = viewport_tag.get('content', '').lower()
        if 'width=' in content:
            viewport_not_set = False

    # Check tap targets
    tap_targets = soup.find_all(['a', 'button', 'input', 'select', 'textarea'])
    for target in tap_targets:
        width = target.get('width')
        height = target.get('height')
        if not width or not height:
            continue
        width = int(width.replace('px', ''))
        height = int(height.replace('px', ''))
        if width < 48 or height < 48 or (width * height) < (48 * 48 * 0.25):
            target_size.append({
                'element': str(target),
                'width': width,
                'height': height
            })

    # Check if content width matches viewport width
    content_width = soup.find('style',
                              attrs={'media': 'screen and (max-width: 600px)'})
    if content_width:
        content_not_sized_correctly = True

    # Check font sizes
    all_text = soup.find_all(text=True)
    font_sizes = {}
    total_text_length = sum(len(text) for text in all_text)
    for text in all_text:
        style = text.parent.get('style', '').lower()
        if 'font-size:' in style:
            font_size = style.split('font-size:')[1].split(';')[0].strip()
            if font_size.isdigit():
                font_size = int(font_size)
                if font_size < 12 and (font_size * 100 /
                                       total_text_length) > 40:
                    illegible_font_size.append({
                        'text': text.strip(),
                        'font_size': font_size
                    })

    # Check for unsupported plugins
    unsupported_tags = ['object', 'embed']
    for tag in unsupported_tags:
        plugins = soup.find_all(tag)
        for plugin in plugins:
            mime_type = plugin.get('type', '').lower()
            if 'java' in mime_type or 'flash' in mime_type or 'silverlight' in mime_type:
                unsupported_plugins.append(str(plugin))

    # Check for mobile alternate link
    mobile_alternate_link_tag = soup.find(
        'link',
        attrs={
            'rel': 'alternate',
            'media': 'only screen and (max-width: 640px)'
        })
    if mobile_alternate_link_tag:
        mobile_alternate_link = True

    return {
        'URL': url,
        'Viewport Not Set': viewport_not_set,
        'Target Size': target_size,
        'Content Not Sized Correctly': content_not_sized_correctly,
        'Illegible Font Size': illegible_font_size,
        'Unsupported Plugins': unsupported_plugins,
        'Mobile Alternate Link': mobile_alternate_link
    }
