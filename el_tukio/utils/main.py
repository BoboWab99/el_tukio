def print_form_values(form):
    print("\n\n")
    print('Form data:')
    print('------------------------')
    for field in form.visible_fields():
        print(f'{field.name}: {form.cleaned_data[field.name]}')
    print("\n\n")
