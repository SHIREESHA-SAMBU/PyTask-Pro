from pytask_pro.scraper import WebScraper

HTML = """
<article class="product_pod">
  <h3><a title="A Test Book">A Test Book</a></h3>
  <p class="price_color">£10.00</p>
  <p class="star-rating Three">Rating</p>
  <p class="availability"> In stock </p>
</article>
"""

def test_parse_product_card():
    records = WebScraper().parse(HTML, "https://example.com")
    assert len(records) == 1
    assert records[0].title == "A Test Book"
    assert records[0].price == "£10.00"
    assert records[0].source_url == "https://example.com"

def test_parser_handles_empty_page():
    assert WebScraper().parse("<html></html>") == []
