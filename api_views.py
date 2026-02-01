"""
REST API views for AS2 Dashboard
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from pyas2.models import Partner, Organization, Message
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
import json
import tempfile
import os

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """Register a new user"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        return JsonResponse({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def user_login(request):
    """Login user"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'token': f'token_{user.id}',  # Simple token for demo
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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
def get_message_detail(request, message_id):
    """Get message details including payload"""
    try:
        message = Message.objects.get(id=message_id)
        
        # Read payload content
        payload_content = ''
        if message.payload:
            try:
                # message.payload is a FileField, need to read the file
                if hasattr(message.payload, 'path') and os.path.exists(message.payload.path):
                    with open(message.payload.path, 'rb') as f:
                        payload_bytes = f.read()
                        payload_content = payload_bytes.decode('utf-8', errors='replace')
                elif hasattr(message.payload, 'read'):
                    try:
                        message.payload.open('rb')
                        payload_bytes = message.payload.read()
                        message.payload.close()
                        payload_content = payload_bytes.decode('utf-8', errors='replace')
                    except:
                        payload_content = '[Unable to read file content]'
                else:
                    payload_content = str(message.payload)
            except Exception as e:
                payload_content = f'[Error reading payload: {str(e)}]'
        else:
            payload_content = '[No payload available]'
        
        data = {
            'id': message.id,
            'message_id': message.message_id,
            'direction': 'Outbound' if message.direction == 'OUT' else 'Inbound',
            'partner': message.partner.as2_name if message.partner else 'Unknown',
            'status': 'Success' if message.status == 'S' else 'Pending' if message.status == 'P' else 'Failed',
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'size': f'{len(payload_content) / 1024:.2f} KB' if payload_content else '0 KB',
            'payload': payload_content,
            'filename': message.filename if hasattr(message, 'filename') and message.filename else 'N/A',
            'content_type': message.content_type if hasattr(message, 'content_type') and message.content_type else 'text/plain',
        }
        
        return JsonResponse(data)
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def retry_message(request, message_id):
    """Retry sending a failed message"""
    try:
        message = Message.objects.get(id=message_id)
        
        # Check if message is failed or pending
        if message.status not in ['E', 'P']:
            return JsonResponse({
                'error': 'Only failed or pending messages can be retried'
            }, status=400)
        
        # Check if it's an outbound message
        if message.direction != 'OUT':
            return JsonResponse({
                'error': 'Only outbound messages can be retried'
            }, status=400)
        
        # Get the payload content
        payload_content = None
        if message.payload:
            try:
                if hasattr(message.payload, 'path') and os.path.exists(message.payload.path):
                    with open(message.payload.path, 'rb') as f:
                        payload_content = f.read()
                elif hasattr(message.payload, 'read'):
                    message.payload.open('rb')
                    payload_content = message.payload.read()
                    message.payload.close()
            except Exception as e:
                return JsonResponse({
                    'error': f'Failed to read message payload: {str(e)}'
                }, status=500)
        
        if not payload_content:
            return JsonResponse({
                'error': 'Message payload not found'
            }, status=404)
        
        # Create a new message for retry
        from pyas2 import as2lib
        
        new_message = Message.objects.create(
            message_id=as2lib.make_mime_message_id(),
            partner=message.partner,
            organization=message.organization,
            direction='OUT',
            status='P',  # Pending
            payload=payload_content,
            filename=message.filename if hasattr(message, 'filename') else None
        )
        
        # Try to send using management command
        try:
            from django.core.management import call_command
            
            # Save payload to temp file
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.dat') as tmp_file:
                tmp_file.write(payload_content)
                tmp_file_path = tmp_file.name
            
            try:
                # Send using management command
                call_command('sendas2message',
                           message.organization.as2_name,
                           message.partner.as2_name,
                           tmp_file_path,
                           delete=True)
                
                new_message.status = 'S'  # Success
                new_message.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Message retried successfully',
                    'new_message_id': new_message.message_id,
                    'original_message_id': message.message_id
                })
            finally:
                # Clean up temp file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    
        except Exception as e:
            new_message.status = 'E'  # Error
            new_message.save()
            return JsonResponse({
                'error': f'Failed to retry message: {str(e)}'
            }, status=500)
            
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)
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

@require_http_methods(["GET"])
def get_chart_data(request):
    """Get chart data for dashboard"""
    try:
        # Get date range for last 12 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        # Monthly message data for bar chart
        monthly_messages = Message.objects.filter(
            timestamp__gte=start_date
        ).annotate(
            month=TruncMonth('timestamp')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        # Format monthly data
        message_data = []
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Create a dict for easy lookup
        monthly_dict = {}
        for item in monthly_messages:
            month_key = item['month'].strftime('%Y-%m')
            monthly_dict[month_key] = item['count']
        
        # Generate data for last 12 months
        for i in range(12):
            date = end_date - timedelta(days=30 * (11 - i))
            month_key = date.strftime('%Y-%m')
            month_name = month_names[date.month - 1]
            count = monthly_dict.get(month_key, 0)
            message_data.append({
                'month': month_name,
                'messages': count
            })
        
        # Status data for pie chart
        total_messages = Message.objects.count()
        success_count = Message.objects.filter(status='S').count()
        pending_count = Message.objects.filter(status='P').count()
        failed_count = Message.objects.filter(status='E').count()
        
        status_data = []
        if total_messages > 0:
            success_pct = round((success_count / total_messages) * 100, 1)
            pending_pct = round((pending_count / total_messages) * 100, 1)
            failed_pct = round((failed_count / total_messages) * 100, 1)
            
            # Ensure percentages add up to 100
            total_pct = success_pct + pending_pct + failed_pct
            if total_pct != 100:
                success_pct = round(100 - pending_pct - failed_pct, 1)
            
            status_data = [
                {
                    'name': 'Success',
                    'value': success_pct,
                    'count': success_count,
                    'color': '#10B981'
                },
                {
                    'name': 'Pending',
                    'value': pending_pct,
                    'count': pending_count,
                    'color': '#F59E0B'
                },
                {
                    'name': 'Failed',
                    'value': failed_pct,
                    'count': failed_count,
                    'color': '#EF4444'
                }
            ]
        else:
            # Show 0% for all when no messages
            status_data = [
                {'name': 'Success', 'value': 0, 'count': 0, 'color': '#10B981'},
                {'name': 'Pending', 'value': 0, 'count': 0, 'color': '#F59E0B'},
                {'name': 'Failed', 'value': 0, 'count': 0, 'color': '#EF4444'}
            ]
        
        # Trend data for line chart (sent, received, failed by month)
        trend_data = []
        for i in range(12):
            date = end_date - timedelta(days=30 * (11 - i))
            month_start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if i < 11:
                next_month = end_date - timedelta(days=30 * (10 - i))
                month_end = next_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                month_end = end_date
            
            month_name = month_names[date.month - 1]
            
            # Count sent messages (outbound)
            sent_count = Message.objects.filter(
                timestamp__gte=month_start,
                timestamp__lt=month_end,
                direction='OUT'
            ).count()
            
            # Count received messages (inbound)
            received_count = Message.objects.filter(
                timestamp__gte=month_start,
                timestamp__lt=month_end,
                direction='IN'
            ).count()
            
            # Count failed messages
            failed_count = Message.objects.filter(
                timestamp__gte=month_start,
                timestamp__lt=month_end,
                status='E'
            ).count()
            
            trend_data.append({
                'month': month_name,
                'sent': sent_count,
                'received': received_count,
                'failed': failed_count
            })
        
        return JsonResponse({
            'messageData': message_data,
            'statusData': status_data,
            'trendData': trend_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_heatmap_data(request):
    """Get heatmap data for message success/failure visualization"""
    try:
        from datetime import datetime, timedelta
        import calendar
        
        granularity = request.GET.get('granularity', 'weekly')
        
        # Get date range
        end_date = datetime.now()
        
        if granularity == 'hourly':
            # Last 7 days, hourly
            start_date = end_date - timedelta(days=7)
            heatmap_data = []
            
            for day_offset in range(7):
                date = start_date + timedelta(days=day_offset)
                day_name = date.strftime('%a %d')
                
                for hour in range(24):
                    hour_start = date.replace(hour=hour, minute=0, second=0, microsecond=0)
                    hour_end = hour_start + timedelta(hours=1)
                    
                    total = Message.objects.filter(
                        timestamp__gte=hour_start,
                        timestamp__lt=hour_end
                    ).count()
                    
                    success = Message.objects.filter(
                        timestamp__gte=hour_start,
                        timestamp__lt=hour_end,
                        status='S'
                    ).count()
                    
                    failed = Message.objects.filter(
                        timestamp__gte=hour_start,
                        timestamp__lt=hour_end,
                        status='E'
                    ).count()
                    
                    heatmap_data.append({
                        'day': day_name,
                        'hour': hour,
                        'total': total,
                        'success': success,
                        'failed': failed
                    })
        
        elif granularity == 'daily':
            # Last 12 months, daily
            start_date = end_date - timedelta(days=365)
            heatmap_data = []
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            for i in range(12):
                date = end_date - timedelta(days=30 * (11 - i))
                month_name = month_names[date.month - 1]
                year = date.year
                month = date.month
                _, num_days = calendar.monthrange(year, month)
                
                for day in range(1, num_days + 1):
                    try:
                        day_start = datetime(year, month, day)
                        day_end = day_start + timedelta(days=1)
                        
                        total = Message.objects.filter(
                            timestamp__gte=day_start,
                            timestamp__lt=day_end
                        ).count()
                        
                        success = Message.objects.filter(
                            timestamp__gte=day_start,
                            timestamp__lt=day_end,
                            status='S'
                        ).count()
                        
                        failed = Message.objects.filter(
                            timestamp__gte=day_start,
                            timestamp__lt=day_end,
                            status='E'
                        ).count()
                        
                        heatmap_data.append({
                            'month': month_name,
                            'day': day,
                            'total': total,
                            'success': success,
                            'failed': failed
                        })
                    except ValueError:
                        continue
        
        elif granularity == 'weekly':
            # Last 12 months, weekly
            start_date = end_date - timedelta(days=365)
            heatmap_data = []
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            for i in range(12):
                date = end_date - timedelta(days=30 * (11 - i))
                month_name = month_names[date.month - 1]
                year = date.year
                month = date.month
                
                # Get first day of month
                month_start = datetime(year, month, 1)
                
                # Get last day of month
                if month == 12:
                    month_end = datetime(year + 1, 1, 1) - timedelta(days=1)
                else:
                    month_end = datetime(year, month + 1, 1) - timedelta(days=1)
                
                # Calculate actual number of weeks in this month
                # A week starts on Monday (0) and ends on Sunday (6)
                first_weekday = month_start.weekday()  # 0=Monday, 6=Sunday
                num_days = month_end.day
                
                # Calculate number of weeks: if month starts mid-week, we need an extra week
                num_weeks = (num_days + first_weekday) // 7
                if (num_days + first_weekday) % 7 > 0:
                    num_weeks += 1
                
                # Ensure we have at least 4 weeks and at most 5 weeks
                num_weeks = max(4, min(5, num_weeks))
                
                for week in range(1, num_weeks + 1):
                    # Calculate week start and end dates
                    week_start_day = (week - 1) * 7 + 1
                    week_end_day = min(week * 7, num_days)
                    
                    try:
                        week_start = datetime(year, month, week_start_day)
                        week_end = datetime(year, month, week_end_day, 23, 59, 59)
                        
                        total = Message.objects.filter(
                            timestamp__gte=week_start,
                            timestamp__lte=week_end
                        ).count()
                        
                        success = Message.objects.filter(
                            timestamp__gte=week_start,
                            timestamp__lte=week_end,
                            status='S'
                        ).count()
                        
                        failed = Message.objects.filter(
                            timestamp__gte=week_start,
                            timestamp__lte=week_end,
                            status='E'
                        ).count()
                        
                        heatmap_data.append({
                            'month': month_name,
                            'week': week,
                            'total': total,
                            'success': success,
                            'failed': failed
                        })
                    except ValueError:
                        continue
        
        elif granularity == 'monthly':
            # Last 5 years, monthly
            heatmap_data = []
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            for year_offset in range(5):
                year = end_date.year - (4 - year_offset)
                
                for month in range(1, 13):
                    try:
                        month_start = datetime(year, month, 1)
                        if month == 12:
                            month_end = datetime(year + 1, 1, 1)
                        else:
                            month_end = datetime(year, month + 1, 1)
                        
                        total = Message.objects.filter(
                            timestamp__gte=month_start,
                            timestamp__lt=month_end
                        ).count()
                        
                        success = Message.objects.filter(
                            timestamp__gte=month_start,
                            timestamp__lt=month_end,
                            status='S'
                        ).count()
                        
                        failed = Message.objects.filter(
                            timestamp__gte=month_start,
                            timestamp__lt=month_end,
                            status='E'
                        ).count()
                        
                        heatmap_data.append({
                            'year': str(year),
                            'month': month_names[month - 1],
                            'total': total,
                            'success': success,
                            'failed': failed
                        })
                    except ValueError:
                        continue
        
        elif granularity == 'yearly':
            # Last 10 years, yearly
            heatmap_data = []
            
            for year_offset in range(10):
                year = end_date.year - (9 - year_offset)
                
                year_start = datetime(year, 1, 1)
                year_end = datetime(year + 1, 1, 1)
                
                total = Message.objects.filter(
                    timestamp__gte=year_start,
                    timestamp__lt=year_end
                ).count()
                
                success = Message.objects.filter(
                    timestamp__gte=year_start,
                    timestamp__lt=year_end,
                    status='S'
                ).count()
                
                failed = Message.objects.filter(
                    timestamp__gte=year_start,
                    timestamp__lt=year_end,
                    status='E'
                ).count()
                
                heatmap_data.append({
                    'year': str(year),
                    'total': total,
                    'success': success,
                    'failed': failed
                })
        
        return JsonResponse({'heatmapData': heatmap_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def send_as2_message(request):
    """Send an AS2 message via API"""
    try:
        # Get partner from request
        partner_name = request.POST.get('partner')
        if not partner_name:
            return JsonResponse({'error': 'Partner name is required'}, status=400)
        
        # Get partner
        try:
            partner = Partner.objects.get(as2_name=partner_name)
        except Partner.DoesNotExist:
            return JsonResponse({'error': f'Partner {partner_name} not found'}, status=404)
        
        # Get file from request
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'File is required'}, status=400)
        
        uploaded_file = request.FILES['file']
        
        # Get organization (use first one)
        org = Organization.objects.first()
        if not org:
            return JsonResponse({'error': 'No organization configured'}, status=500)
        
        # Create message
        from pyas2.models import Message
        from pyas2 import as2lib
        
        # Read file content
        file_content = uploaded_file.read()
        
        # Create message
        message = Message.objects.create(
            message_id=as2lib.make_mime_message_id(),
            partner=partner,
            organization=org,
            direction='OUT',
            status='P',  # Pending
            payload=file_content
        )
        
        # Try to send the message
        try:
            from django.core.management import call_command
            
            # Save file temporarily
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.dat') as tmp_file:
                tmp_file.write(file_content)
                tmp_file_path = tmp_file.name
            
            try:
                # Send using management command
                call_command('sendas2message', 
                            '--partner', partner.as2_name,
                            '--file', tmp_file_path,
                            '--delete')
                
                message.status = 'S'  # Success
                message.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Message sent successfully',
                    'message_id': message.message_id,
                    'partner': partner.as2_name
                })
            finally:
                # Clean up temp file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    
        except Exception as e:
            message.status = 'E'  # Error
            message.save()
            return JsonResponse({
                'error': f'Failed to send message: {str(e)}'
            }, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
