import requests
# GOAL
# to convert html page to PDF preserving the layout without losing the text sharpness, charts, styling, etc.

PDFSHIFT_API_KEY = "sk_619eb4c33e779923d5b92a264aa47f26bd69bc7c"

HTML2PDF_API_KEY = "zOo6X3fkGuiyNZOTvzzNwpUI1CK5fk4r5VTvVpBetvGcghdzH2A9k7zdG3smfMbJ"

output_pdf = "report.pdf"

with open(file="FY25 Highlights.html") as f:
    # print(f.read())
    input_html = f.read()

    # ---------PDF Shift-------
    pdfshift_url = "https://api.pdfshift.io/v3/convert/pdf"
    pdfshift_header = {"X-API-Key": PDFSHIFT_API_KEY}
    pdfshift_payload = {
        "source": input_html,
        "landscape": False,
        "use_print": False,
        "margin": { "top": 0, "bottom": 0, "left": 0, "right": 0, },
    }
    response = requests.post(url=pdfshift_url, headers=pdfshift_header, json=pdfshift_payload)

    # ---------html2pdf-------
    html2pdf_url = "https://api.html2pdf.app/v1/generate"
    html2pdf_params = {
        "html": input_html,
        "apiKey": HTML2PDF_API_KEY,
    }
    # response = requests.get(url=html2pdf_url, params=html2pdf_params)

    # response.raise_for_status()
    print(response.status_code)
    print(response.text)

with open(output_pdf, "wb") as f:
    f.write(response.content)

print("Task execution complete")