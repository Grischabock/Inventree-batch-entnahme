from plugin import InvenTreePlugin
from plugin.mixins import UrlsMixin
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render
from stock.models import StockItem
from stock.api import StockItemSerializer

class BatchEntnahmePlugin(InvenTreePlugin, UrlsMixin):
    """
    Plugin für InvenTree: Ermöglicht Batch-Scannen und Sammel-Entnahme von Teilen aus dem Lager.
    """

    NAME = "Batch Entnahme"
    SLUG = "batch_entnahme"
    TITLE = "Batch Entnahme"
    DESCRIPTION = "Scanne mehrere Barcodes und buche alle auf einen Schlag aus."

    def setup_urls(self):
        return [
            path('batch-remove/', self.batch_page, name='batch_remove_page'),
            path('batch-remove/api/scan/', self.scan_barcode, name='batch_scan_api'),
            path('batch-remove/api/remove/', self.remove_stock, name='batch_remove_api'),
        ]

    def batch_page(self, request):
        return render(request, 'batch_entnahme.html', {})

    def scan_barcode(self, request):
        barcode = request.GET.get('barcode', None)
        if not barcode:
            return JsonResponse({'error': 'Kein Barcode übergeben'}, status=400)

        try:
            item = StockItem.objects.get(pk=int(barcode.replace('SI-', '')))
        except Exception:
            return JsonResponse({'error': 'Teil nicht gefunden'}, status=404)

        data = StockItemSerializer(item).data
        return JsonResponse({'success': True, 'item': data})

    def remove_stock(self, request):
        import json
        try:
            payload = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Ungültiges JSON'}, status=400)

        results = []
        for entry in payload:
            try:
                item = StockItem.objects.get(pk=entry['id'])
                qty = int(entry['qty'])
                item.take_stock(qty, user=request.user, notes='Batch-Entnahme Plugin')
                results.append({'id': item.pk, 'qty': qty, 'status': 'ok'})
            except Exception as e:
                results.append({'id': entry.get('id'), 'qty': entry.get('qty'), 'status': f'Fehler: {str(e)}'})

        return JsonResponse({'success': True, 'results': results})
