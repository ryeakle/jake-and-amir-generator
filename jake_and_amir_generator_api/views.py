from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from generator.MarkovGenerator import Markov


class CharacterViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retreving characters and their text.
    """
    filter_fields = ('length',)

    def list(self, request):
        """
        List all available characters.
        """
        character_list = settings.CHARACTER_WORDS.keys()
        return Response(character_list)

    def retrieve(self, request, pk=None):
        """
        Retrive text for the character specified by pk.

        The url arg 'length' can be used to generate text of a specific length (minimally 2).
        e.g: /api/jake/?length=15 --> returns a 15 word phrase.
        """
        character = pk
        length = int(self.request.QUERY_PARAMS.get('length', 25))
        if length < 2:
            error_string = "If specified, length must be >=2.  Current length is " + str(length) + "."
            return Response({settings.ERROR_KEY: error_string}, status=status.HTTP_400_BAD_REQUEST)
        try:
            character_words = settings.CHARACTER_WORDS[character]
        except:
            error_string = "Invalid character: " + "'" + character + "'"
            return Response({settings.ERROR_KEY: error_string}, status=status.HTTP_400_BAD_REQUEST)

        character_markov = Markov(character_words)
        character_text = character_markov.generate_markov_text(length=length)
        return Response({settings.DATA_KEY: character_text})
