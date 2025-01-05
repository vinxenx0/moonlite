import requests


def get_image_info(soup):
    image_issues = {
        'Over 100kb': [],
        'Missing Alt Text': [],
        'Missing Alt Attribute': [],
        'Alt Text Over 100 Characters': [],
        'Background Images': [],
        'Missing Size Attributes': [],
        'Incorrectly Sized Images': []
    }

    # Function to get image size from URL
    def get_image_size(url):
        try:
            response = requests.get(url)
            return len(response.content) / 1024  # Convert bytes to kilobytes
        except Exception as e:
            return 0

    # Function to check if image has alt attribute
    def has_alt_attribute(img):
        return 'alt' in img.attrs

    # Function to check if image has alt text
    def has_alt_text(img):
        return img.get('alt', '').strip() != ''

    # Function to check if alt text is over 100 characters
    def alt_text_over_100_chars(img):
        return len(img.get('alt', '').strip()) > 100

    # Function to check if image has size attributes
    def has_size_attributes(img):
        return 'width' in img.attrs and 'height' in img.attrs

    # Function to get image dimensions
    def get_image_dimensions(img):
        width = int(img.get('width', 0))
        height = int(img.get('height', 0))
        return width, height

    # Find all img tags
    images = soup.find_all('img')

    for img in images:
        # Check image size
        image_url = img.get('src', '')
        image_size = get_image_size(image_url)
        if image_size > 100:
            image_issues['Over 100kb'].append(image_url)

        # Check alt text
        if not has_alt_attribute(img):
            image_issues['Missing Alt Attribute'].append(image_url)
        elif not has_alt_text(img):
            image_issues['Missing Alt Text'].append(image_url)
        elif alt_text_over_100_chars(img):
            image_issues['Alt Text Over 100 Characters'].append(image_url)

        # Check size attributes
        if not has_size_attributes(img):
            image_issues['Missing Size Attributes'].append(image_url)
        else:
            # Check if image dimensions match display dimensions
            width, height = get_image_dimensions(img)
            if width == 0 or height == 0:
                continue
            estimated_size = (width * height *
                              3) / 1024  # Assuming 3 bytes per pixel
            actual_size = image_size
            if abs(estimated_size - actual_size) >= 4:  # 4kb difference
                image_issues['Incorrectly Sized Images'].append(image_url)

    return image_issues
