from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page
            return redirect('polls:index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})