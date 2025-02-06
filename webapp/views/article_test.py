from django.http import JsonResponse

def article_test(request, pk):
    return JsonResponse({"message": f"Тестовая статья {pk}"})
