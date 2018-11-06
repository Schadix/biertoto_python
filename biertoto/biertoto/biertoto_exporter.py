from scrapy.exporters import CsvItemExporter
from scrapy.utils.python import to_native_str


class CsvBiertotoItemExporter(CsvItemExporter):

    def _build_row(self, values):
        for s in values:
            try:
                yield to_native_str(s, self.encoding)
            except TypeError:
                if isinstance(s, list):
                    for i in s:
                        yield i
                else:
                    yield s

    def export_item(self, item):
        if self._headers_not_written:
            self._headers_not_written = False
            self._write_headers_and_set_fields_to_export(item)

        fields = self._get_serialized_fields(item, default_value='',
                                             include_empty=True)
        values = list(self._build_row(x for _, x in fields))
        self.csv_writer.writerow(values)
