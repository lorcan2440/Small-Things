import webbrowser

original_url = input('What is the link of the cribs which is not working?\n')

url_string = original_url.split('PDFURL=')[-1].split('&title=')[0]
url_string = url_string.replace('%3A', ':')
url_string = url_string.replace('%2F', '/')

webbrowser.open(url_string)

print(url_string)
