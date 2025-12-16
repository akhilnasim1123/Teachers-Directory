from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Teacher, Subject
import csv
import os
import re
from django.conf import settings
from django.core.exceptions import ValidationError

def login_view(request):
    if request.user.is_authenticated:
        return redirect('teachers')  

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('teachers')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def teacher_directory(request):
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'directory.html', {
        'teachers': teachers,
        'subjects': subjects
    })
    
    
@login_required(login_url='login')
def filter_teachers(request):
    letter = request.GET.get('letter')
    subject = request.GET.get('subject')

    teachers = Teacher.objects.all()

    if letter:
        teachers = teachers.filter(last_name__istartswith=letter)

    if subject:
        teachers = teachers.filter(subjects__name=subject)

    return render(request, 'partials/teacher_list.html', {
        'teachers': teachers
    })


@login_required(login_url='login')
def import_teachers(request):
    if request.method == "POST":
        if 'cancel' in request.POST:
            if 'import_preview' in request.session:
                del request.session['import_preview']
            return redirect('import_teachers')

        if 'confirm' in request.POST:
            preview_data = request.session.get('import_preview', [])
            if not preview_data:
                messages.error(request, "No data to import")
                return redirect('import_teachers')

            count = 0
            for row in preview_data:
                teacher, created = Teacher.objects.get_or_create(
                    email=row['email'],
                    defaults={
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'phone': row['phone'],
                        'room_number': row['room'],
                    }
                )

                teacher.subjects.clear()
                for name in row['subjects']:
                    if name.strip():
                        subject, _ = Subject.objects.get_or_create(name=name.strip())
                        teacher.subjects.add(subject)

                if row['image_name']:
                    image_path = os.path.join(settings.MEDIA_ROOT, 'teachers', row['image_name'])
                    if os.path.exists(image_path):
                        teacher.profile_image = f"teachers/{row['image_name']}"
                    else:
                         teacher.profile_image = None
                
                teacher.save()
                count += 1
            
            if 'import_preview' in request.session:
                del request.session['import_preview']
                
            messages.success(request, f"{count} teachers imported successfully")
            return redirect('teachers')

        csv_file = request.FILES.get('file')
        
        if not csv_file:
             messages.error(request, "Please upload a CSV file")
             return redirect('import_teachers')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Please upload a CSV file")
            return redirect('import_teachers')

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            data = csv.reader(decoded_file)
            
            rows = list(data)
            if not rows:
                messages.error(request, "File is empty")
                return redirect('import_teachers')

            first_row = [str(cell).lower() for cell in rows[0]]
            if "email" in first_row or "first code" in first_row or "first name" in first_row:
                rows = rows[1:]

            preview_data = []
            for row in rows:
                if len(row) < 7:
                    continue
                
                # Split by | or ,
                # Using regex to split by | or ,
                subjects_str = row[6].strip()
                subjects = [s.strip() for s in re.split(r'[|,]', subjects_str) if s.strip()]

                preview_data.append({
                    'first_name': row[0].strip(),
                    'last_name': row[1].strip(),
                    'image_name': row[2].strip(),
                    'email': row[3].strip(),
                    'phone': row[4].strip(),
                    'room': row[5].strip(),
                    'subjects': subjects,
                    'subjects_display': ", ".join(subjects)
                })
            
            if not preview_data:
                messages.error(request, "No valid data found in file")
                return redirect('import_teachers')

            request.session['import_preview'] = preview_data
            return render(request, 'import_teachers.html', {'preview_data': preview_data})
            
        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
            return redirect('import_teachers')

    # GET request - if preview exists, show it (optional, but sticking to flow)
    # If user refreshes, maybe show preview? 
    # For now, let's just clear preview on GET to reset state or check if persistent
    # Let's check session
    if 'import_preview' in request.session:
        return render(request, 'import_teachers.html', {'preview_data': request.session['import_preview']})

    return render(request, 'import_teachers.html')


@login_required(login_url='login')
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    subjects = Subject.objects.all()
    return render(request, 'teacher_detail.html', {
        'teacher': teacher, 
        'all_subjects': subjects
    })


@login_required(login_url='login')
def teacher_create(request):
    if request.method == "POST":
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            room_number = request.POST.get('room_number')
            subject_ids = request.POST.getlist('subjects')
            new_subjects = request.POST.get('new_subjects')
            profile_image = request.FILES.get('profile_image')

            if not all([first_name, last_name, email]):
                 messages.error(request, "First name, last name and email are required")
                 return redirect('teacher_create')
                 
            if Teacher.objects.filter(email=email).exists():
                 messages.error(request, "Email already exists")
                 return redirect('teacher_create')

            total_subjects = len(subject_ids)
            if new_subjects:
                total_subjects += len([s for s in new_subjects.split(',') if s.strip()])

            if total_subjects > 5:
                messages.error(request, "Max 5 subjects allowed")
                return redirect('teacher_create')

            teacher = Teacher.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                room_number=room_number,
                profile_image=profile_image
            )
            
            for sub_id in subject_ids:
                teacher.subjects.add(sub_id)

            if new_subjects:
                for name in new_subjects.split(','):
                    name = name.strip()
                    if name:
                        subject, _ = Subject.objects.get_or_create(name=name)
                        teacher.subjects.add(subject)
                
            messages.success(request, "Teacher added successfully")
            return redirect('teachers')

        except Exception as e:
            messages.error(request, f"Error creating teacher: {str(e)}")
            
    subjects = Subject.objects.all()
    return render(request, 'teacher_form.html', {'all_subjects': subjects})


@login_required(login_url='login')
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == "POST":
        try:
            teacher.first_name = request.POST.get('first_name')
            teacher.last_name = request.POST.get('last_name')
            
            new_email = request.POST.get('email')
            if new_email != teacher.email and Teacher.objects.filter(email=new_email).exists():
                 messages.error(request, "Email already in use")
                 return redirect('teacher_update', pk=pk)
            teacher.email = new_email
            
            teacher.phone = request.POST.get('phone')
            teacher.room_number = request.POST.get('room_number')
            
            if request.FILES.get('profile_image'):
                teacher.profile_image = request.FILES.get('profile_image')
                
            subject_ids = request.POST.getlist('subjects')
            new_subjects = request.POST.get('new_subjects')

            total_subjects = len(subject_ids)
            if new_subjects:
                total_subjects += len([s for s in new_subjects.split(',') if s.strip()])

            if total_subjects > 5:
                messages.error(request, "Max 5 subjects allowed")
                return redirect('teacher_update', pk=pk)
                
            teacher.subjects.clear()
            for sub_id in subject_ids:
                teacher.subjects.add(sub_id)
            
            if new_subjects:
                for name in new_subjects.split(','):
                    name = name.strip()
                    if name:
                        subject, _ = Subject.objects.get_or_create(name=name)
                        teacher.subjects.add(subject)
                
            teacher.save()
            
            messages.success(request, "Teacher updated successfully")
            return redirect('teacher_detail', pk=pk)

        except Exception as e:
            messages.error(request, f"Error updating teacher: {str(e)}")
            
    subjects = Subject.objects.all()
    return render(request, 'teacher_form.html', {
        'teacher': teacher, 
        'all_subjects': subjects
    })

@login_required(login_url='login')
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == "POST":
        teacher.delete()
        messages.success(request, "Teacher deleted successfully")
        return redirect('teachers')
        
    return render(request, 'teacher_confirm_delete.html', {'teacher': teacher})