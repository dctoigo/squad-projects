from django.http import HttpResponse
from django.template.loader import render_to_string
import json


class HTMXModalMixin:
    """
    Mixin genérico para CreateViews que usam HTMX + Bootstrap modals.
    - Retorna resposta OOB (Out-of-Band) para atualizar um <select>
    - Fecha o modal via evento HTMX (closeModal)
    - Trata automaticamente form_invalid
    """

    def get_lookup_field(self):
        """
        Define o nome do campo relacionado ao select que deve ser atualizado.
        Deve ser sobrescrito na view (ex: 'billing_type').
        """
        return None

    def get_oob_template(self):
        """
        Define o template que será renderizado com hx-swap-oob.
        Deve ser sobrescrito na view (ex: 'manager/partials/option_oob.html').
        """
        return None

    def form_valid(self, form):
        self.object = form.save()

        lookup_field = self.get_lookup_field()
        oob_template = self.get_oob_template()

        # Se ambos estiverem definidos, monta a resposta OOB
        if lookup_field and oob_template:
            html = render_to_string(
                oob_template,
                {
                    'new': self.object,
                    'select_id': f'id_{lookup_field}'
                }
            )
            html = html.strip()
            
            response = HttpResponse(html, status=200)
            response['HX-Trigger'] = json.dumps({'closeModal': None})
            return response

        # Fallback: fecha o modal sem OOB
        return HttpResponse(status=204)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))