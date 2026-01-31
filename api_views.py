"""
REST API views for AS2 Dashboard
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pyas2.models import Partner, Organization, Message
import json

@require_http_methods(["GET"])
def get_partners(request):
    """Get all partners"""
    try:
        partners = Partner.objects.all()
        data = []
        for partner in partners:
            data.append({
                'id': partner.id,
                'as2_name': partner.as2_name,
                'name': partner.name,
                'target_url': partner.target_url,
                'encryption': partner.encryption,
                'signature': partner.signature,
                'status': 'active' if partner.active else 'inactive',
            })
        return JsonResponse({'partners': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_keys(request):
    """Get all certificates and keys"""
    try:
        # Mock data for now since certificate models vary
        data = [
            {
                'id': 'p1_priv',
                'name': 'P1 Private Key',
                'type': 'Private',
                'algorithm': 'RSA 2048',
                'organization': 'P1 Organization',
                'expires': '2027-01-20',
                'status': 'active',
                'fingerprint': 'A1:B2:C3:D4:E5:F6',
            },
            {
                'id': 'p1_pub',
                'name': 'P1 Public Certificate',
                'type': 'Public',
                'algorithm': 'RSA 2048',
                'organization': 'P1 Organization',
                'expires': '2027-01-20',
                'status': 'active',
                'fingerprint': 'A1:B2:C3:D4:E5:F6',
            },
            {
                'id': 'p2_priv',
                'name': 'P2 Private Key',
                'type': 'Private',
                'algorithm': 'RSA 2048',
                'organization': 'P2 Organization',
                'expires': '2027-01-20',
                'status': 'active',
                'fingerprint': 'B2:C3:D4:E5:F6:A1',
            },
            {
                'id': 'p2_pub',
                'name': 'P2 Public Certificate',
                'type': 'Public',
                'algorithm': 'RSA 2048',
                'organization': 'P2 Organization',
                'expires': '2027-01-20',
                'status': 'active',
                'fingerprint': 'B2:C3:D4:E5:F6:A1',
            },
        ]
        
        return JsonResponse({'keys': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_messages(request):
    """Get all messages"""
    try:
        messages = Message.objects.all().order_by('-timestamp')[:100]
        data = []
        for msg in messages:
            data.append({
                'id': msg.id,
                'message_id': msg.message_id,
                'direction': msg.direction,
                'partner': msg.partner.as2_name if msg.partner else 'Unknown',
                'status': 'success' if msg.status == 'S' else 'pending' if msg.status == 'P' else 'failed',
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'size': f'{len(str(msg.payload)) / 1024:.2f} KB' if msg.payload else '0 KB',
            })
        return JsonResponse({'messages': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_stats(request):
    """Get dashboard statistics"""
    try:
        partners_count = Partner.objects.count()
        keys_count = 4  # Mock count
        messages_count = Message.objects.count()
        success_count = Message.objects.filter(status='S').count()
        success_rate = (success_count / messages_count * 100) if messages_count > 0 else 0
        
        return JsonResponse({
            'partners': partners_count,
            'keys': keys_count,
            'messages': messages_count,
            'successRate': round(success_rate, 1),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
