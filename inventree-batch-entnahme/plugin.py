from plugin import InvenTreePlugin
from plugin.mixins import UrlsMixin, NavigationMixin
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render
from stock.models import StockItem
from stock.api import StockItemSerializer
import logging
logger = logging.getLogger("inventree")

logger.info("BatchEntnahmePlugin wird geladen")

class BatchEntnahmePlugin(InvenTreePlugin, UrlsMixin, NavigationMixin):
    """
    Plugin für InvenTree: Ermöglicht Batch-Scannen und Sammel-Entnahme von Teilen aus dem Lager.
    
    Nutzung:
    - Unter Menüpunkt „Batch Entnahme“ können mehrere Barcodes nacheinander gescannt werden.
    - Alle gescannten Artikel werden gesammelt angezeigt.
    - Mit einem Klick auf „Alle entnehmen“ wird der gesamte Bestand ausgebucht.
    """

    NAME = "Batch Entnahme"
    SLUG = "batch_entnahme"
    TITLE = "Batch Entnahme"
    DESCRIPTION = "Scanne mehrere Barcodes und buche alle auf einen Schlag aus."
    PLUGIN_URL = "batch-remove/"

    NAVIGATION = [
        {
            "name": "Batch Entnahme",
            "link": "plugin:batch_entnahme:batch_remove_page",
            "icon": "fas fa-barcode"
        }
    ]

    VERSION = "1.0.2"
    AUTHOR = "GrischaMedia"
    MIN_VERSION = "0.12"
    MAX_VERSION = None

    SETTINGS = {
        'BATCH_MODE': {
            'name': 'Batch Modus',
            'description': 'Aktiviert den Batch-Modus für das Scannen',
            'default': True,
            'validator': bool
        }
    }

    def setup_urls(self):
        return [
            path('batch-remove/', self.batch_page, name='batch_remove_page'),
            path('batch-remove/api/scan/', self.scan_barcode, name='batch_scan_api'),
            path('batch-remove/api/remove/', self.remove_stock, name='batch_remove_api'),
        ]

    def batch_page(self, request):
        return render(request, 'inventree_batch_entnahme/batch_entnahme.html', {})

    def scan_barcode(self, request):
        barcode = request.GET.get('barcode', None)
        if not barcode:
            return JsonResponse({'error': 'Kein Barcode übergeben'}, status=400)

        try:
            pk = int(barcode.replace('SI-', ''))
            item = StockItem.objects.get(pk=pk)
        except (ValueError, StockItem.DoesNotExist):
            return JsonResponse({'error': 'Ungültiger Barcode oder Teil nicht gefunden'}, status=404)

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
