from __future__ import unicode_literals
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from api import price_calculator

# Create your views here.

# -*- coding: utf-8 -*-
from django.template import loader

from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from django.views import View
from django import forms
from api import models
from api import serializers
from api import book_parser
from api import emailer


class StyleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.StyleSerializer
    lookup_field = 'uuid'
    queryset = models.Style.objects.all()


class StyleColorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.StyleColorSerializer
    lookup_field = 'slug'
    queryset = models.StyleColor.objects.all()

    def get_queryset(self):
        style_uuid = self.kwargs['style_uuid']
        style = models.Style.objects.get(uuid=style_uuid)
        return style.stylecolor_set.all()


# returns every style but just a single color for display purposes
class StyleImageList(generics.ListAPIView):
    serializer_class = serializers.StyleImageSerializer

    def get_queryset(self):
        queryset = []
        for style in models.Style.objects.all():
            image = models.StyleImage.filter(style=style)[0]
            if image is not None:
                queryset.append(image)

        return queryset


class StyleImageDetail(generics.RetrieveAPIView):
    serializer_class = serializers.StyleImageSerializer
    queryset = models.StyleImage.objects.all()

    # get object based on style and color
    def get_object(self):
        queryset = self.get_queryset()
        style_id = self.kwargs['style_id']
        color_slug = self.kwargs['color']
        style = models.Style.objects.filter(style_id=style_id)
        color = models.StyleColor.objects.filter(slug=color_slug)
        obj = get_object_or_404(queryset, style=style, color=color)
        return obj


class AddonListView(generics.ListAPIView):
    serializer_class = serializers.AddonSerializer
    queryset = models.Addon.objects.all()


class UploadFileForm(forms.Form):
    file = forms.FileField(required=True)
    clear = forms.BooleanField(required=False)


# for uploading excel sheets to populate the database
class UploadBookView(View):
    def get(self, request):
        form = UploadFileForm()
        template = loader.get_template('api/upload_book.html')
        return render(request, 'api/upload_book.html', { 'form': form })

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        uploaded_file = request.FILES.get('file')
        clear = request.POST.get('clear')
        error = False
        error_message = ""
        if(uploaded_file is not None):
            # handle file
            book_parser.parse_workbook(uploaded_file, clear)
        else:
            error = True
            error_message = "There was an error uploading the file, please try again"

        uploaded = form.is_valid()
        return render(
            request,
            'api/upload_book.html',
            {
                'form': form,
                'uploaded': uploaded,
                'error': error,
                'error_message': error_message
            }
        )


class CalculatePriceView(APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request):

        if 'front' not in request.data or 'back' not in request.data:
            response = Response(status=400, data={'error': 'image is missing'})
            return response

        front_image = request.data['front']
        back_image = request.data['back']

        # validate that correct params have come through
        style_id = request.GET.get('style')
        quantity_string = request.GET.get(
            'quantities')  # in order of increasing size as string of comma separated numbers
        ink_colors = request.GET.get('inks')
        addon_string = request.GET.get('addons')  # as string of comma-separated numbers
        comments = request.GET.get('comments')
        email = request.GET.get('email')

        # parse comma separated numbers
        quantities = [int(x) for x in quantity_string.split(',')]
        addons = []
        if addon_string is not None and len(addon_string) > 0:
            addons = [int(x) for x in addon_string.split(',')]

        # validate all fields are present
        if style_id is not None and quantities is not None and ink_colors is not None:
            price = price_calculator.calculate_price(style_id, quantities, ink_colors, addons)

            # send email report
            emailer.send_report(style_id, quantities, ink_colors, addons, email, comments, price, front_image, back_image)

            # return calculated price
            response = Response({'price': price})

            # add cors headers
            return response
        else:
            response = Response(status=400, data={'error': 'fields missing'})
            return response
