from selenium import webdriver
from selenium.webdriver.common.by import By
from inscriptis import get_text
from inscriptis.model.config import ParserConfig


def fetch_html(url: str) -> str:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html


def html_to_annotated_text(html_content: str) -> str:
    # Configure inscriptis to display link targets
    config = ParserConfig(display_links=True)

    # Convert HTML to text using inscriptis
    text = get_text(html_content, config=config)

    # Annotate lines containing URLs with unique IDs
    annotated_text = []
    id_number = 1
    for line in text.split("\n"):
        if "[http" in line:  # Simplified way to identify lines containing URLs
            annotated_text.append(f"{line} [ID: {id_number}]")
            id_number += 1
        else:
            annotated_text.append(line)

    return "\n".join(annotated_text)


def main():
    url = "https://cnn.com"  # Change this to your desired URL
    html_content = fetch_html(url)
    annotated_text = html_to_annotated_text(html_content)
    # save to file
    with open("annotated_text.txt", "w") as f:
        f.write(annotated_text)
    print(annotated_text)


if __name__ == "__main__":
    main()
