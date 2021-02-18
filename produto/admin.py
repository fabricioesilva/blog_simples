from django.contrib import admin, messages
from .models import Produto, Variacao, Banner
from django.utils.translation import ngettext
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


class VariacaoInline(admin.StackedInline):
    model = Variacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    model = Produto
    list_filter = ['marca']
    inlines = [
            VariacaoInline,
    ]
    

class BannerAdmin(admin.ModelAdmin):
    list_display = ['diferencial', 'tipo_link']


class VariacaoAdmin(admin.ModelAdmin):
    model = Variacao
    list_display = ['id', 'nome', 'produto', 'desconto_var']
    list_display_links = ['nome']
    list_filter = ['produto']

    def aplica_desconto(self, request, queryset):
        updated = queryset.update(desconto_var=7.5)
        self.message_user(request, ngettext(
            '%d desconto atualizado com sucesso.',
            '%d descontos atualizados com sucesso.',
            updated,
        ) % updated, messages.SUCCESS)
    
    def export_selected_objects(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect('/export/?ct=%s&ids=%s' % (
            ct.pk,
            ','.join(str(pk) for pk in selected),
        ))
    
    actions = ['aplica_desconto', 'export_selected_objects']
    aplica_desconto.short_description = "Aplicar desconto"
    export_selected_objects.short_description = 'Exportar seleção.'
    

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Variacao, VariacaoAdmin)
