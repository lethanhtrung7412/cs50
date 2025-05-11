from django.shortcuts import render, redirect
import markdown2 as markdown
from . import util


def index(request):
    entries = util.list_entries()
    query_name = request.GET.get('q')
    if query_name is None:
        return render(request, "encyclopedia/index.html", {
        "entries": entries
    })
    result = [s for s in entries if query_name in s]
    return render(request, "encyclopedia/index.html", {
        "entries": result
    })

def get_entry_page(request, title):
    entry_content = util.get_entry(title)

    # check if content is exist
    if entry_content is None:
        return render(request, "encyclopedia/404.html")
    
    # convert string to markdown content
    convert_entry_content = markdown.markdown(entry_content)
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": convert_entry_content
    },content_type="text/html")

def new_entry(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect('index')
    return render(request, "encyclopedia/new_entry.html")

def edit_entry(request, title):
    old_content = util.get_entry(title)
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect('index')
    
    return render(request, "encyclopedia/edit_entry.html", {
        "title": title,
        "content": old_content
    })