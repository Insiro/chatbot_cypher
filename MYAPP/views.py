    })
 
@csrf_exempt
def answer(request):
 
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    datacontent = received_json_data['content']
 
    if datacontent == '오늘':
        today = "오늘 급식"
 
        return JsonResponse({
                'message': {
                    'text': today
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['오늘','내일']
                }
 
            })
 
    elif datacontent == '내일':
        tomorrow = "내일 급식"
 
        return JsonResponse({
                'message': {
                    'text': tomorrow
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['오늘','내일']
                }
 
            })
