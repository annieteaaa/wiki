from django.shortcuts import render
from . import util
from django import forms
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError
import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def getentry(request, title):
    content = util.get_entry(title)
    if content == None:
        raise Http404
    else:
        for name in util.list_entries():
            if name.upper() == title.upper():
                title = name
                break
        return render(request, "wiki/getentry.html", {
            "title": title,
            "content": markdown2.markdown(content)
        })

def search(request):
    if request.method == "POST":
        entry = request.POST['q']
        for name in util.list_entries():
            if name.upper() == entry.upper():
                return HttpResponseRedirect(reverse("encyclopedia:getentry", args=(name,)))
        return HttpResponseRedirect(reverse("encyclopedia:results", args=(entry,)))
    else:
        return HttpResponseRedirect(reverse("encyclopedia:index"))

def results(request, entry):
    entries = []
    for name in util.list_entries():
        if entry.upper() in name.upper():
            entries.append(name)
    return render(request, "encyclopedia/results.html", {
        "entries": entries,
        "entry": entry
    })

def valid_title(title):
    for name in util.list_entries():
        if title.upper() == name.upper():
            raise ValidationError("Page already exists")

class NewPageForm(forms.Form):
    title = forms.CharField(label="", validators=[valid_title])
    mdcontent = forms.CharField(label="", widget=forms.Textarea(attrs={"rows": 10, "cols": 200, "placeholder": "Content"}))

class EditForm(forms.Form):
    mdcontent = forms.CharField(label="", widget=forms.Textarea(attrs={"rows": 10, "cols": 200, "placeholder": "Content"}))

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            mdcontent = form.cleaned_data["mdcontent"]
        else:
            return render(request, "new/newpage.html", {
                "form": form
            })
        util.save_entry(title, mdcontent)
        return HttpResponseRedirect(reverse("encyclopedia:getentry", args=(title,)))
    return render(request, "new/newpage.html", {
        "form": NewPageForm()
    })

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["mdcontent"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:getentry", args=(title,)))
    content = util.get_entry(title)
    pop = {'mdcontent': content}
    form = EditForm(initial=pop)
    return render(request, f"edit/edit.html", {
        "form": form,
        "title": title
    })

def randomPage(request):
    entries = util.list_entries()
    n = random.randint(0, len(entries)-1)
    return getentry(request, entries[n])