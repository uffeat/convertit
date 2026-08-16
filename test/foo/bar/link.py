"""
test/foo/bar/link.py
"""


def main(use, log=None, **kwargs):

    link = use('use/foo/bar.css')
    
    log("link:\n", link, native=True)

    element = use.document.createElement("h1")
    element.setAttribute("bar", '')
    element.textContent = 'Tester'
    use.document.body.append(element)



   

    
    
