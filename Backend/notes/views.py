from django.shortcuts import redirect, render

from shared.decorators import require_http_methods

from .forms import AddNoteForm


@require_http_methods('GET')
def note_list(request):
    pass


@require_http_methods('POST')
def add_note(request):
    if (form := AddNoteForm(request.POST)).is_valid():
        form.save()
        return redirect('post-list')
    form = AddNoteForm()
    return render(request, 'posts/post/add.html', {'form': form})
