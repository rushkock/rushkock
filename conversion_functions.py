from markdownify import markdownify
  
def html_to_markdown(html):
    markdown = markdownify(html, heading_style="ATX") 
    return markdown

def save_markdown(save_path,markdown):
    with open(f"{save_path}/my_cv.md", "w") as f:
        f.write(markdown)