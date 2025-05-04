from markdownify import markdownify
  
def html_to_markdown(html):
    """ Convert HTML to markdown"""
    markdown = markdownify(html, heading_style="ATX") 
    return markdown

def save_file(save_path,data):
    """ Save file """
    with open(f"{save_path}", "w") as f:
        f.write(data)