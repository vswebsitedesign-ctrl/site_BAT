#!/usr/bin/env python3
import json, os, shutil, sys

SERVICE_WORDS = ['house','clearance','rubbish','removal','bereavement','probate','hoarder','loft','garage','shed','office','attic','care','commercial','waste','scrap','black','bag','collection','same','day','we','buy','old','caravan','guest','garden','building','site','man','van','removals','move','clean','motorbike','motorhome','insulation']

H1_PATTERNS = [
    "{service} in {location} - Your Local Husband and Wife Team",
    "Looking for {service} near {location}? Sharna is Based Locally",
    "{location} residents trust Sharna for {service} - Locally Based Since 2009",
    "Get a same day {service} quote in {location} - Local, Licensed and Insured",
    "{service} {location} - We Live and Work Locally - Husband and Wife Business",
    "Stressed about {service} in {location}? Call your local Sharna today",
    "{location} {service} done right - Locally owned, fully insured, eco-friendly",
    "Free {service} quote in {location} - Your local Environment Agency registered team",
]

META_PATTERNS = [
    "Professional {service} in {location}. Locally based, fully licensed, insured and eco-friendly. Free same-day quotes from Sharna at Buildings and Trust.",
    "Looking for trusted {service} near {location}? Sharna and Buildings and Trust are locally based, fully insured and ready to help. Call today for a free quote.",
    "Sharna at Buildings and Trust offers affordable {service} in {location}. Environment Agency registered, locally based and available same day. Get your free quote now.",
    "Need {service} in {location}? Your local husband and wife team cover {location} and surrounding areas. Licensed, insured and eco-friendly. Free quotes available.",
    "Buildings and Trust provide sensitive, professional {service} across {location}. Locally based with 15+ years experience. Call Sharna today for a free same-day quote.",
    "Get a free {service} quote in {location} from Sharna at Buildings and Trust. Locally owned, fully licensed and Environment Agency registered. Discreet and reliable service.",
    "Trusted {service} specialists serving {location} and nearby areas. Husband and wife team, locally based, fully insured. Same-day availability. Call Sharna free today.",
    "{location} {service} from Buildings and Trust. Locally based, eco-friendly and fully licensed waste carriers. Sharna offers free no-obligation quotes - call or WhatsApp today.",
]

TITLE_PATTERNS = [
    "{service} {location} | Free Quotes | Licensed & Insured | Buildings and Trust",
    "{location} {service} | Same Day Available | Husband & Wife Team | Buildings and Trust",
    "{service} in {location} | Locally Based | Environment Agency Registered | Buildings and Trust",
    "{location} {service} Specialists | Free No-Obligation Quote | Buildings and Trust",
    "Affordable {service} {location} | 15+ Years Experience | Fully Insured | Buildings and Trust",
    "{service} near {location} | Licensed Waste Carriers | Same Day | Buildings and Trust",
    "{location} {service} | Eco-Friendly & Fully Licensed | Free Quote | Buildings and Trust",
    "Trusted {service} in {location} | Discreet & Professional | Buildings and Trust",
]


def slug_to_service_location(slug):
    parts = slug.split('-')
    service_parts = [p for p in parts if p in SERVICE_WORDS]
    loc_parts = [p for p in parts if p not in SERVICE_WORDS]
    service = ' '.join(service_parts).title() if service_parts else slug.replace('-', ' ').title()
    location = ' '.join(loc_parts).title() if loc_parts else 'UK'
    return service, location


def make_uk_schema(slug, service, location, canonical):
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://buildingsandtrust.co.uk/"},
            {"@type": "ListItem", "position": 2, "name": service, "item": "https://buildingsandtrust.co.uk/" + slug + "/"},
            {"@type": "ListItem", "position": 3, "name": location, "item": canonical}
        ]
    }
    service_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service + " in " + location,
        "description": "Professional " + service + " in " + location + ". Locally based, fully licensed, insured and Environment Agency registered. Free same-day quotes from Sharna at Buildings and Trust.",
        "areaServed": {"@type": "City", "name": location},
        "provider": {"@id": "https://buildingsandtrust.co.uk"},
        "url": canonical
    }
    return (
        '<script type="application/ld+json">\n' + json.dumps(breadcrumb, indent=2) + '\n</script>\n' +
        '<script type="application/ld+json">\n' + json.dumps(service_schema, indent=2) + '\n</script>\n'
    )


def make_uk_template(slug, service, location):
    idx = hash(slug) % 8
    h1 = H1_PATTERNS[idx].replace('{service}', service).replace('{location}', location)
    return f"""<div class="bat-full-width-hero">
  <div class="bat-overlay"></div>
  <div class="bat-hero-content">
    <h1 class="bat-hero-h1">{h1}</h1>
    <p class="bat-hero-p-22">Professional, affordable and trustworthy {service.lower()} in {location}.</p>
    <div class="bat-flex-j-center bat-gap-20 bat-flex-wrap bat-mb-20">
      <a href="tel:07859730296" class="bat-btn-blue">&#128222; Call Sharna: 07859 730296</a>
      <a href="/contact-us" class="bat-btn-blue">&#128233; Get a Free Quote</a>
    </div>
  </div>
</div>

<div class="bat-badge-container">
  <h2 class="bat-badge-h2">Sharna and Buildings and Trust {location}</h2>
  <div class="bat-badge-flex">
    <span class="bat-badge bat-bg-green-dark">+15 Years Experience</span>
    <span class="bat-badge bat-bg-blue-med">Environment Agency Registered</span>
    <span class="bat-badge bat-bg-orange-dark">Dependable &amp; Discreet</span>
    <span class="bat-badge bat-bg-purple-dark">Fully Insured</span>
    <span class="bat-badge bat-bg-grey-blue">Trusted &amp; Local</span>
  </div>
</div>

<div class="wp-block-gallery columns-3">
  <figure class="gallery-item">
    <h2>Elderly Relatives</h2>
    <img src="/assets/images/Elderly-relative-going-into-care-house-clearance-scaled.webp" alt="Elderly Relative Going into Care {location}">
    <figcaption>Trustworthy and Discreet Care Support</figcaption>
  </figure>
  <figure class="gallery-item">
    <h2>Peace of Mind</h2>
    <img src="/assets/images/House-Moving-Van-13-scaled.webp" alt="{service} in {location}">
    <figcaption>You Can Rely on Sharna and Buildings and Trust</figcaption>
  </figure>
  <figure class="gallery-item">
    <h2>Bereavement Clearances</h2>
    <img src="/assets/images/dad-going-into-care-house-clearance-54.webp" alt="Dad Going into Care in {location}">
    <figcaption>Sensitive Clearances</figcaption>
  </figure>
</div>

<section class="bat-standards">
  <h2 class="bat-standards-h2">{service} Service Standards in {location}</h2>
  <div class="bat-cards-wrap">
    <div class="bat-card bat-card-navy">
      <div class="bat-card-circle"></div>
      <div>
        <h3 class="bat-card-h3 bat-color-gold">Can You?</h3>
        <p class="bat-card-p">Yes: <strong>+15 years experience in {service} in {location}</strong> with Sharna and Buildings and Trust</p>
      </div>
      <div>
        <a href="tel:07859730296" class="bat-card-btn" style="background-color:#FFD700;color:#002D62;">Call Sharna 07859 730296</a>
      </div>
    </div>
    <div class="bat-card bat-card-pink">
      <div class="bat-card-circle bat-card-circle-light"></div>
      <div>
        <h3 class="bat-card-h3">How Much?</h3>
        <p class="bat-card-p">Unbeatable quote given <strong>same day</strong> by Sharna and Buildings and Trust</p>
      </div>
      <div>
        <a href="/contact-us" class="bat-card-btn" style="background-color:#1a1a1a;color:#FFFFFF;">Request a Free Quote</a>
      </div>
    </div>
    <div class="bat-card bat-card-green">
      <div class="bat-card-circle bat-card-circle-light"></div>
      <div>
        <h3 class="bat-card-h3">Are You Licensed?</h3>
        <p class="bat-card-p">Yes: fully licensed, insured and Environment Agency registered waste carrier</p>
      </div>
      <div>
        <a href="/about-us" class="bat-card-btn" style="background-color:#FFD700;color:#002D62;">About Sharna</a>
      </div>
    </div>
  </div>
</section>

<div class="cta-banner">
  <div class="cta-title">&#128222; Free {service} Quote in {location}</div>
  <div class="cta-buttons">
    <a href="tel:07859730296" class="cta-button">Call Sharna: 07859 730296</a>
    <a href="/contact-us" class="cta-button">Send a Message</a>
  </div>
</div>"""


def build():
    pages_path = 'data/pages.json'
    if not os.path.exists(pages_path):
        print("ERROR: pages.json not found")
        sys.exit(1)
    with open(pages_path, 'r') as f:
        pages = json.load(f)
    with open('theme/base.html', 'r') as f:
        template = f.read()
    if os.path.exists('build'):
        shutil.rmtree('build')
    os.makedirs('build')

    for page in pages:
        slug = page['slug']
        service, location = slug_to_service_location(slug)
        canonical = 'https://buildingsandtrust.co.uk/' + slug + '/'
        idx = hash(slug) % 8

        # CONTENT
        content = page.get('body_content', '')
        is_uk_page = not (content or '').strip()
        if is_uk_page:
            content = make_uk_template(slug, service, location)

        # TITLE
        title = page.get('title', '')
        if not title or is_uk_page:
            if location and location != 'UK':
                title = TITLE_PATTERNS[idx].replace('{service}', service).replace('{location}', location)
            else:
                title = service + ' | Free Quotes | Licensed &amp; Insured | Buildings and Trust'

        # META DESCRIPTION
        meta_description = page.get('meta_description', '')
        if not meta_description or is_uk_page:
            meta_description = META_PATTERNS[idx].replace('{service}', service).replace('{location}', location)

        # PAGE SCHEMA - injected into head via token
        if is_uk_page:
            page_schema = make_uk_schema(slug, service, location, canonical)
        else:
            page_schema = ''

        html = template.replace('{{ content }}', content)
        html = html.replace('{{ title }}', title)
        html = html.replace('{{ meta_description }}', meta_description)
        html = html.replace('{{ canonical }}', canonical)
        html = html.replace('{{ page_schema }}', page_schema)

        out_dir = os.path.join('build', slug) if slug else 'build'
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w') as f:
            f.write(html)

    # Generate robots.txt
    with open('build/robots.txt', 'w') as f:
        f.write('User-agent: *\nAllow: /\nSitemap: https://buildingsandtrust.co.uk/sitemap.xml\n')

    # Generate sitemap.xml
    domain = 'https://buildingsandtrust.co.uk'
    urls = []
    for page in pages:
        s = page['slug']
        if s == 'home':
            urls.append(f'{domain}/')
        else:
            urls.append(f'{domain}/{s}/')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        sitemap += f'  <url><loc>{url}</loc></url>\n'
    sitemap += '</urlset>\n'
    with open('build/sitemap.xml', 'w') as f:
        f.write(sitemap)

    # Copy homepage to root index.html
    home_path = os.path.join('build', 'home', 'index.html')
    if os.path.exists(home_path):
        shutil.copy(home_path, os.path.join('build', 'index.html'))
    if os.path.exists('assets'):
        shutil.copytree('assets', 'build/assets', dirs_exist_ok=True)
    print(f"Built {len(pages)} pages")

if __name__ == '__main__':
    build()
