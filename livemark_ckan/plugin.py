import yaml
from livemark import Plugin, errors
from frictionless import Package
from frictionless.plugins.ckan import CkanDialect


# NOTE: implement caching


class CkanPlugin(Plugin):
    identity = "ckan"
    priority = 80

    # Process

    def process_snippet(self, snippet):
        if self.document.format == "html":
            if snippet.type == "package/ckan" and snippet.lang == "yaml":
                spec = yaml.safe_load(str(snippet.input).strip())
                path = spec.get("path")
                if not path:
                    raise errors.Error("Ckan dataset path is requried")
                source, dataset = path.rsplit("/dataset/", 1)
                dialect = CkanDialect(dataset=dataset)
                package = Package.from_ckan(source, dialect=dialect)
                package.setdefault("title", dataset)
                snippet.input = package.to_yaml()
                snippet.type = "package"
