import pickle
from collections import OrderedDict
from FileHelper import FileHelper


class ListFormatter():

    SECTION_ORDERING = ["Früchte & Gemüse", "Fleisch & Fisch", "Milch & Käse", "Brot & Gebäck", "Zutaten & Gewürze", "Getreideprodukte", "Snacks & Süsswaren",
                        "Getränke & Tabak", "Haushalt & Gesundheit", "Pflege & Gesundheit", "Fertig- & Tiefkühlprodukte", "Tierbedarf", "Baumarkt & Garten", "Eigene Artikel"]

    def __init__(self, all_articles=None, catalog=None):
        self.all_articles = all_articles
        self.catalog = catalog

        if self.all_articles is None:
            self.all_articles = FileHelper.load_file("articles")
        if self.catalog is None:
            self.catalog = FileHelper.load_file("catalog")

    def section_for_article_from_catalog(self, article):
        sections = self.catalog["sections"]
        section = next((x for x in sections if article in x['items']), None)
        return section['key'] if section is not None else None

    def section_for_article_from_list_details(self, article, details):
        detail = next(
            (x for x in details if article == x['itemId']), None)
        return detail['userSectionId'] if detail is not None else None

    def section_for_article(self, article, details):
        from_details = self.section_for_article_from_list_details(
            article, details)
        if from_details is not None:
            return from_details
        return self.section_for_article_from_catalog(article)

    def group_articles(self, purchase_list, list_details):
        groups = OrderedDict.fromkeys(ListFormatter.SECTION_ORDERING)
        for item in purchase_list:
            section = self.section_for_article(item['name'], list_details)
            if section is None:
                section = "Eigene Artikel"
            if groups[section] is not None:
                groups[section].append(item)
            else:
                groups[section] = [item]
        return groups

    def item_to_string(self, item):
        if item['name'] in self.all_articles:
            realName = self.all_articles[item['name']]
        else:
            realName = item['name']

        if item['specification'] != "":
            return f"{realName} ({item['specification']})"
        else:
            return realName

    def printable_items(self, purchase_list, list_details):
        out = list()
        groups = self.group_articles(purchase_list, list_details)
        for key, items in groups.items():
            if items is None or len(items) == 0:
                continue
            out.append(('g', key))
            for item in items:
                out.append(('i', self.item_to_string(item)))
        return out
