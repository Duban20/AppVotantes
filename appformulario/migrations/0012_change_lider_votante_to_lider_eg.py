from django.db import migrations

def change_roles(apps, schema_editor):
    Votante = apps.get_model('appformulario', 'Votante')
    LiderEG = apps.get_model('appformulario', 'LiderEG')

    # Solo líderes que realmente existen como LiderEG
    lideres_ids = LiderEG.objects.values_list('votante_id', flat=True)

    Votante.objects.filter(
        id__in=lideres_ids,
        rol='LIDER_VOTANTE'
    ).update(rol='LIDER_EG')


class Migration(migrations.Migration):

    dependencies = [
        ('appformulario', '0011_migrate_lideres_to_lidereg'),
    ]

    operations = [
        migrations.RunPython(change_roles),
    ]
