from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from datetime import datetime
import json
from hypernews.settings import NEWS_JSON_PATH
import itertools


class MainView(View):
    def get(self, request, *args, **kwargs):
        return redirect("news/")


class NewsView(View):
    def get(self, request, *args, **kwargs):
        index = kwargs["n_chapter"]
        with open(NEWS_JSON_PATH, "r") as js:
            news = json.load(js)
        inf = None
        for elem in news:
            if elem["link"] == int(index):
                inf = elem
                break
        return render(request, "news/news.html", context=inf)


class NewsList(View):
    def get(self, request, *args, **kwargs):
        with open(NEWS_JSON_PATH, "r") as js:
            news = json.load(js)
        search = ""
        if request.GET.get("q"):
            search = request.GET.get("q")
            with open("log.txt", "w") as f:
                f.write("AAAa: "+search)
        news = list(filter(lambda x: search in x["title"], news))
        sorted_news = sorted(news, key=lambda i: i['created'], reverse=True)
        groupped_news = itertools.groupby(sorted_news, lambda i: i['created'][:10])
        res = []
        for key, item in groupped_news:
            res.append([key, list(item)])
        return render(request, "news/newslist.html", context={"news": res})


class CreateView(View):
    def get(self, requets, *args, **kwargs):
        return render(requets, "news/create.html", context={})

    def post(self, request, *args, **kwargs):
        with open(NEWS_JSON_PATH, "r+") as js:
            news = json.load(js)
            new = {"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   "text": request.POST.get("text"),
                   "title": request.POST.get("title"),
                   "link": len(news) + 1}
            news.append(new)
            js.seek(0)
            json.dump(news, js)
        return redirect("/news/")
